---
id: feedback_parallel_exploration
name: 大型项目必须并发探索
description: 面对大型仓库/项目时，root 必须并发启动多个 kaze/mirin
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.722173
related:
- '[[task_aris_项目探索决策]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
---

## 反馈

用户指出：分析 wshobson/agents（大型仓库 112 agent + 146 skills）时，root 只启动了单个 kaze 串行探索，应该并发多路。

## 规则

- 小型项目（<20 文件）：单个 kaze
- 大型项目（>50 文件或多模块）：并发 2-3 个 kaze/mirin，按方向分工
- 分工方式：按模块、按关注点、按文件类型拆分
