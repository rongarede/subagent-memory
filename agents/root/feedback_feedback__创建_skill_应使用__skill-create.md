---
id: feedback_feedback:_创建_skill_应使用__skill-create
name: 'feedback: 创建 skill 应使用 /skill-create'
description: b1 指出创建 skill 时应先检查 /skill-create（everything-claude-code:skill-create），而非直接派
  raiga 手工创建
type: feedback
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- skill-create
- raiga
- skill
- workflow
tags:
- task
context: ''
timestamp: '2026-03-15T19:18:58.153836'
related:
- '[[feedback_feedback:_skill_创建后必须触发测试]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

b1 反馈：创建新 skill 时，应首先检查是否有专门的 /skill-create skill 可用，而非直接派 raiga 手工编写。/skill-create 是 everything-claude-code 提供的专用 skill 创建工具。Why: 已有现成工具但 root 未触发，浪费了 raiga 的手工编写时间。How to apply: 以后创建 skill 前，先 invoke /skill-create 或 everything-claude-code:skill-create，仅在该工具不适用时才回退到 raiga 手工创建。
