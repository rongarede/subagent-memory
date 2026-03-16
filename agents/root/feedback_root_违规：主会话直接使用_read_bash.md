---
id: feedback_root_违规：主会话直接使用_read_bash
name: root 违规：主会话直接使用 Read/Bash
description: root 在主会话直接调用 Read 和 Bash 工具，违反协调器约束
type: feedback
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- violation
- coordinator
- Read
- Bash
- subagent-first
tags:
- task
context: ''
timestamp: '2026-03-15T18:34:29.036598'
related:
- '[[feedback_feedback:_禁止询问策略确认]]'
- '[[feedback_feedback:_新机制需调研外部实现]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-15: root 接到用户任务（检索 trigger-map 并搜索 skill），直接在主会话使用 Read 读取 trigger-map.md 和 Bash 执行 npx skills find，违反了 CLAUDE.md 中「主对话禁止直接执行操作」的铁律。即使是简单的文件读取或命令执行，也必须通过 subagent 委托。正确做法：派发 kaze 读取文件 + tetsu/yomi 执行 npx skills find 命令。
