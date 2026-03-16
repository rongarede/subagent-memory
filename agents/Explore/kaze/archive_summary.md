---
name: archive_summary
description: 历史任务记忆蒸馏摘要（kaze）
type: archive
created: 2026-03-15
source_count: 14
---

## 关键经验教训

### 探索方法论
- 探索任务优先读 MEMORY.md 和目录结构，再深入单个文件；避免盲目读取全量文件
- agent-memory 项目有 9 个 Python 模块（后扩展到 14 个）：memory_store → retriever → associator → extractor → inject → evolver → registry → obsidian_export → cli，其中 memory_store 是核心数据模型
- 跨 agent 记忆检索用 `python3 cli.py retrieve <query> --cross-agent`，自动扫描所有 store；`--stores` 参数支持指定路径

### 记忆系统架构要点（反复需要的知识）
- Memory dataclass 有 20+ 字段；CLI 有 14+ 子命令
- retrieve() 三维评分：recency(0.995^hours) + importance_score + BM25 relevance，各维 [0,1]
- feedback_loop.py 提供 `check_memory_health()` → 'healthy'|'warning'|'blocked'；filter_by_health 插入点在 retriever.py `store.load_all()` 之后、计算 relevance 之前
- consolidator 用 Jaccard（BM25）相似度合并，阈值 0.85；decay_engine 用 Ebbinghaus R=e^(-t/S)，S=importance*3天，floor=0.2

### Obsidian 库结构
- PARA 顶层目录（000-500）完整；100_Projects 有 Active/On_Hold/Completed 三个子目录，Active 下 5 个项目
- 200_Areas 子目录统一 Area_ 前缀；300_Resources 含 Zettelkasten/Assets/Templates（10 个模板）
- 根目录异常文件：_Home.md.backup（备份）、Associative_Memory_设计文档.md（孤儿）、未命名.base

### ~/mem 可索引性
- auto-memory/*.md 有 frontmatter，可被 Obsidian Base 索引
- ~/mem 不在 vault 内，需创建 symlink 才能在 Obsidian 中访问角色记忆目录

## 常见任务模式

| 模式 | 频率 | 产出 |
|------|------|------|
| agent-memory 模块架构探索 | 极高 | 接口签名、数据流图、测试覆盖统计 |
| Phase N 代码上下文提取 | 高 | 设计文档规格、实现接口摘要 |
| 记忆系统状态探索 | 中等 | 各 agent 记忆数量、格式验证 |
| Obsidian 库目录结构探索 | 低 | PARA 结构报告、异常文件清单 |

## 重要发现

- agent-memory 测试数量演化：125 → 194 → 234 → 247 → 339 → 491 → 577，均 100% 通过
- Phase 1 (active recall + feedback fields) 已完整实现；Phase 2 (consolidator + decay) 已完整实现；Phase 3 (feedback_loop + trigger_tracker) 已完整实现
- distill 输出评估：L1 聚类 related_ids 存在重复 keyword 问题（如 [symlink,symlink,symlink]），多条内容被截断；distilled/ 目录未创建
- 系统架构全貌（2026-03-15）：CLAUDE.md 476行/23章节、8个 rules、7个 docs、11个激活 hook、104个 skills、11个注册 agent、约 320 条记忆文件、13个 workflow 模板
- cross-agent retrieve 当时共 11 个 agent store，16 条记忆文件（系统初期规模）

## 来自 mirin 的历史经验

### Obsidian 库 MOC 与 up 字段审计（mirin 执行，2026-03-15）
- 全库 273 个非系统 MD 文件中 238 个有 up 字段（87%）
- MOC 覆盖：顶层 6 个 PARA 目录均有 index；200_Areas 下 6 个 Area 均有 MOC；区块链子目录（01-10）9 个子目录全无 MOC
- 真实 broken links 11 个：6 个指向不存在的 [[100_Projects/Active/Project_控制论]]，3 个指向不存在的 [[_inbox_moc]]，各 1 个指向 [[_Tech_Notes_moc]] 和 [[_notebooklm_moc]]
- Orphan notes：100_Projects 7 个、200_Areas 4 个、300_Resources 9 个、400_Archives 13 个

### 工作上下文读取（mirin 执行）
- mirin 曾承担日记/changelog/root 记忆的上下文汇总任务（该职责现归 kaze）
