---
name: archive_summary
description: 历史任务记忆蒸馏摘要（yomi）
type: archive
created: 2026-03-15
source_count: 2
---

## 关键经验教训

### 调研方法论
- L2 深度调研产出的建议应附优先级（P0-P3）和可行性评估，避免泛泛而谈
- 评估外部项目时需对比与 b1 系统的差异点，明确"可借鉴"vs"无需集成"的结论
- JSONL→.md 重构评估：memory_store.py 是核心（~80行），其他文件主要改 import 和构造方式，总预估 200-300 行；推荐重构顺序：memory_store → retriever → associator → 其他

### 记忆系统反馈机制
- 现有系统的主要缺口（调研时）：无显式反馈标记、无动态权重调整、无自动合并去重、无间隔重复调度
- 已实现的改进顺序：Active Recall+Feedback(P0) → Consolidation+Decay(P1) → feedback_loop+trigger_tracker(Phase A-E) → Round 2-5 深度集成 → distiller.py
- 未实现项：P3 语义检索（向量数据库）、P4 Letta 式 Core/Archival/Recall 分层、injection_log RL 闭环

## 重要发现

- 架构文档推荐组合：ADR + C4 Model + Structurizr DSL + Mermaid，对 AI agent 编排系统适配度最高
  - ADR：轻量决策记录，1-2 页，单个决策即可创建
  - C4：4 层抽象，开发者友好
  - Structurizr DSL：架构即代码，多图输出
  - TOGAF 过重，不适用
- ARIS 项目（auto-claude-code-research-in-sleep）：MVP 级，19 个 skill，覆盖 ML 研究全链路；可借鉴 REVIEW_STATE.json 状态持久化模式和 DSE-loop 迭代优化设计
