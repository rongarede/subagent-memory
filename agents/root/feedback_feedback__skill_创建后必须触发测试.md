---
id: feedback_feedback:_skill_创建后必须触发测试
name: 'feedback: skill 创建后必须触发测试'
description: 创建 reflex-fuzz skill 后未立即测试被纠正
type: feedback
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- skill
- create
- test
- verify
tags:
- task
context: ''
timestamp: '2026-03-16T09:17:48.343869'
related: []
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

违规：创建 skill 后直接报告完成，未触发测试。纠正：编写完 skill 后必须触发 skill 测试。Why: 未测试的 skill 可能有 bug。How: 创建→测试→审计→提交。已写入 trigger-map 转移规则。
