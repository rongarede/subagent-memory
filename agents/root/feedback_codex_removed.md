---
id: feedback_codex_removed
name: Codex CLI 已移除
description: b1 订阅 Max 计划，Codex CLI 已从工作流中移除，所有任务统一用 Agent tool + sonnet
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.726441
related:
- '[[feedback_feedback:_新机制需调研外部实现]]'
- '[[task_trigger-map_重构为原子反射模型]]'
- '[[task_phase_b_完成：feedback_retriever+cli_集成]]'
- '[[feedback_feedback:_创建_skill_应使用__skill-create]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-13：b1 确认已订阅 Claude Max 计划，不再需要 Codex CLI 作为外部子代理工具。

变更：
- ~/.claude/CLAUDE.md 移除 3 处 Codex 引用
- ~/.claude/rules/agents.md 移除 4 处（含整个 Codex CLI Integration 章节）
- 适中/大型任务统一路由到 Agent tool (parallel subagents, model: sonnet)
- 不再使用 collaborating-with-codex skill
