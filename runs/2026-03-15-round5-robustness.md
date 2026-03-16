# Round 5 健壮性强化 — 工作流记录

**日期：** 2026-03-15
**执行者：** tetsu（蚁工）
**文档：** fumio（织者）
**测试验证：** haku（药师）

---

## 目标

在 Round 4（智能自动化）基础上，进一步强化测试基础设施和系统健壮性，解决以下已知痛点：
1. 各测试文件中重复的 setup/teardown 代码
2. 大规模 store 下全量索引重建开销
3. 损坏记忆文件导致整个 store 无法加载的问题
4. 缺乏边界条件和异常路径的端到端覆盖

---

## 执行步骤

### R5-A: conftest fixtures

**目标：** 统一 pytest fixtures，消除重复代码

**实施：**
- 创建 `tests/conftest.py`，定义共用 fixtures：
  - `tmp_store(tmp_path)` — 临时 store 目录（每个测试独立）
  - `sample_memories(tmp_store)` — 预填充 5 条样例记忆
  - `mock_llm_client()` — 模拟 LLM API 客户端（避免真实调用）
- 各测试文件中重复的 `tmpdir` / `mkdtemp` 调用改为引用共用 fixtures

**结果：** 测试文件平均减少 15-20 行 setup 代码，fixture 复用率提升

### R5-B: incremental index

**目标：** `generate-index` 支持增量更新，`--force` 标志触发全量重建

**实施：**
- `cli.py` `generate-index` 子命令新增 `--force` 参数
- 增量逻辑：对比 index 中已有记录与 store 中 `.md` 文件的 mtime，仅处理新增/变更文件
- 全量逻辑（`--force`）：删除现有 index，从头扫描所有文件

**结果：** 1000 条 store 的索引更新从全量 ~2s 降至增量 ~0.1s（无变化时）

### R5-C: corrupted recovery

**目标：** 系统在遇到损坏文件时不崩溃，提供修复工具

**实施：**
- `memory_store.py` `load_all()` 新增异常捕获：YAML 解析失败时跳过文件并记录警告，不抛出异常
- 新增 `repair` CLI 子命令：
  - 扫描 store 中所有 `.md` 文件
  - 对 YAML frontmatter 解析失败的文件，尝试自动修复（补全缺失字段）
  - 无法修复的文件移至 `{store}/_quarantine/` 目录隔离

**结果：** store 中存在坏文件时，系统降级运行（跳过坏文件），而非整体崩溃

### R5-D: full workflow tests

**目标：** 补充边界条件和异常路径的端到端测试

**测试场景：**
1. `test_store_init_with_missing_dir` — store 目录不存在时自动创建
2. `test_concurrent_write_isolation` — 两个并发 `quick-add` 不互相覆盖
3. `test_index_corruption_recovery` — index 文件损坏后 `repair` 能恢复正常检索
4. `test_cross_agent_empty_store` — 跨 agent 检索时某个 store 为空不报错
5. `test_generate_index_force_vs_incremental` — `--force` 和增量模式结果一致性验证

---

## 测试结果

| 阶段 | 测试数 | 状态 |
|------|--------|------|
| Round 4 基线 | 428 | 全部通过 |
| R5-A conftest fixtures | +8 | 全部通过 |
| R5-B incremental index | +18 | 全部通过 |
| R5-C corrupted recovery | +22 | 全部通过 |
| R5-D full workflow tests | +15 | 全部通过 |
| **Round 5 合计** | **491** | **全部通过** |

---

## 关键发现

1. `memory_store.py` 原始实现在 YAML 解析失败时会抛出 `yaml.YAMLError`，导致 `load_all()` 中断——需要显式捕获
2. `generate-index` 的增量逻辑依赖文件 mtime，需注意 NFS/iCloud 同步场景下 mtime 的一致性（已添加注释说明）
3. 并发写入测试中发现 `generate_id()` 在极端情况下可能产生碰撞，已通过加文件锁解决

---

## 产出物

- `tests/conftest.py` — 统一 pytest fixtures
- `tests/test_robustness.py` — R5-C/D 健壮性测试
- CLI 新增子命令：`repair`、`generate-index --force`
- `memory_store.py` 异常捕获增强

---

## 决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| 损坏文件处理策略 | 隔离到 `_quarantine/` | 保留原始文件便于人工检查，不直接删除 |
| 增量索引依据 | 文件 mtime | 简单可靠，无需维护额外哈希数据库 |
| `--force` 行为 | 删除重建 | 语义清晰，避免增量逻辑与全量结果不一致 |
