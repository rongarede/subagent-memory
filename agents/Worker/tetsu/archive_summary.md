---
name: archive_summary
description: 历史任务记忆蒸馏摘要（tetsu）
type: archive
created: 2026-03-15
source_count: 80
---

## 关键经验教训

### Bug 修复模式
- **macOS /tmp symlink 陷阱**：`/tmp → /private/tmp`，路径安全检查需对 home 和 tmp_dir 做 `realpath`，额外允许 `/private/tmp` 前缀
- **CLI 参数优先级**：`--store` 必须优先于 `--agent`；原因是 `--agent` 硬编码 `~/.claude/memory/agents/{name}/` 覆盖了 CLAUDE.md 规定的 `~/mem/mem/agents/{Type}/{name}/` 路径。TDD RED→GREEN 验证。
- **不可变性原则**：`cmd_evolve/cmd_feedback/cmd_add` 的直接 mutation 改为 `dataclasses.replace()`；`feedback_loop.py` 同理用 `dataclasses.replace`
- **decay 测试的二次衰减陷阱**：测试中不要在调用 `cleanup_decayed` 前先手动 `store.update(decayed_*)`，否则二次衰减导致 floor 基准错误
- **sys.path 注入模式**：`decay_engine.py` 顶部需加 `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` 与 `consolidator.py` 保持一致
- **distiller 路径安全**：路径穿越风险用 home+tmp 白名单；ID 碰撞改用 sha256；cluster 最小 50 字符质量门槛；Jaccard >= 0.9 近似重复 pre-filter

### agent-memory 系统开发（6 轮迭代）
- **Phase/Round 模式**：每轮用 TDD（RED→GREEN→REFACTOR）开发，审计（shin）后修复，fumio 同步文档，tetsu commit+push
- **测试增长曲线**：Phase 1 → 125 → Round 2 → 247 → Round 3 → 339 → Round 4 → 428 → Round 5 → 491 → Round 6 → 577
- **consolidator Jaccard 设计**：用 keywords+tags 集合计算 Jaccard（而非全文 BM25 token），高信噪比，相同关键词=1.0，不同主题=0.0
- **decay Ebbinghaus 公式**：`R = e^(-t/S)`，`S = importance * 3`，floor = `max(1, int(base * 0.2))`，优先 `last_accessed` 否则用 `timestamp`
- **feedback_loop 三态健康**：healthy / warning / blocked。`check_escalation`：0 次 none / 1-2 次 downweight / 3-4 次 warning / ≥5 次 block
- **feedback_factor 范围**：0.5（极端负面）到 2.0（极端正面），无反馈时 factor=1.0 向后兼容
- **retriever health 过滤**：blocked 排除检索，warning 降权 0.5，健康状态结果优先
- **health_cache 性能优化**：retrieve() 内用 dict 缓存 `{id: health}`，消除重复 `check_memory_health` 调用
- **R3-A hook 安全机制**：超时保护 3 秒，任何异常均 `exit 0` 不 block 用户
- **R4-B decay hook**：24h cooldown 文件 `~/.last-decay-timestamp`，最多 10 store，1s/store 超时，冷数据优先

### 测试工程经验
- **conftest.py fixtures**：设计 `clean_store/sample_memory/sample_memory_fb/populated_store/memory_factory`（含无 feedback 和含 feedback 两种风格），工厂函数用闭包 `_counter` 实现自增 ID
- **incremental index**：`.index-meta.json` 记录每个 `mem_*.md` 的 mtime，--force 强制全量重建，meta 损坏自动回退
- **损坏文件容错**：`load_all()` 改为捕获异常时写 `.corrupted_memories.log`；repair 子命令支持 --fix（修复缺少结束 `---` 的文件）
- **全工作流测试**：固定 `now` 参数确保 decay 测试确定性；用 `compute_importance_score()` 直接比较重要性比依赖 BM25 检索结果更稳定
- **覆盖率瓶颈**：cli.py（13%）是主要瓶颈，需专门 subprocess 集成测试；core modules 均可达 80%+

## 常见任务模式

### 配置文件编辑（CLAUDE.md / agents.md / trigger-map）
- Read 文件定位精确位置 → Edit 工具精确字符串匹配替换（无副作用）
- 多处修改时逐一 Edit，每次验证成功
- 重要约束：tetsu 不得擅自重命名用户创建的内容，执行前确认范围

### 审计修复（shin/haku 审计后）
- HIGH 必须立即修复，MEDIUM 同批次修复，LOW 可选批量
- 每次修复后全量测试回归，确认零新增失败
- commit+push 在所有修复完成且全量测试通过后执行

### Git commit 模式
- 两个仓库：`~/.claude`（代码）和 Obsidian（设计文档）
- commit 只包含相关文件，不用 `git add -A`
- distiller.py/cli.py/tests 在 `~/.claude` 仓库，设计文档在 Obsidian 仓库

### TDD 流程
1. 先写测试文件（RED 阶段，全 FAIL）
2. 实现代码（GREEN 阶段）
3. 全量回归确认无破坏
4. commit+push

## 重要发现

### 系统架构决策
- **决策链格式**：b1 要求用 MD 而非 JSON，已统一修改 CLAUDE.md 和所有已存在的 workflow run 文件
- **Mission Mode Phase 链路**：Phase 4 由 haku→shin，新增 Phase 5 提交步骤，共 8 步（Phase 0-7）
- **agent 路径约束**：中文类型名是磁盘实际目录名（蚁工/斥候/药师等），英文类型名在 CLAUDE.md 注册表中，两者必须区分
- **trigger-map 软链接**：`~/.claude/docs/trigger-map.md → ~/mem/mem/workflows/trigger-map.md`
- **singleton 角色命名**：Devourer→Raiga, Librarian→Fumio, Matrix→Norna，类型=角色名
- **~/mem 软链接**：将 `~/.claude/memory` 相关目录软链接到 `~/mem` 方便访问

### agent-memory skill
- **distiller 核心**：4 个 frozen dataclass（Knowledge, MemoryCluster, OutputAction, DistillResult），纯算法无 LLM 依赖
- **cross-agent retrieve**：多 store 并行检索，去重（同 ID 取最高分），--cross-agent 自动扫描 `~/mem/mem/agents/`
- **低相关度警告阈值**：`LOW_RELEVANCE_THRESHOLD = 2.4`，score < 2.4 时输出警告

### Obsidian PARA 维护
- 根目录异常文件（`_Home.md.backup`、`Associative_Memory_设计文档.md`、`未命名.base`）需移到正确位置
- up 字段格式：YAML frontmatter 用 `up: "[[Parent_MOC]]"`（单冒号带引号）
- 断链修复：`_inbox_moc → _inbox_index`，`_Tech_Notes_moc → _resources_index`
