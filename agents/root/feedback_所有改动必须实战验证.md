---
id: feedback_所有改动必须实战验证
name: 所有改动必须实战验证
description: 任何改动（规则、配置、skill注册等）必须经过实战验证（非静态检查）通过后才可声明完成。静态验证（文件存在性检查）不够，必须有实际调用/执行的端到端验证。
type: feedback
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- 验证
- 实战
- 端到端
- 改动
- 改进验证链
tags:
- task
context: ''
timestamp: '2026-03-15T10:51:04.935293'
related:
- '[[feedback_root_违规：主会话直接使用_read_bash]]'
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

2026-03-15 b1 明确要求：所有改动都需要最终实战验证通过后才可停止。之前 kaze 对 find-skills 补注册的验证只是静态检查（文件中是否有这行文字），b1 要求必须让 yomi 实际调用 find-skills 做实战验证。此规则应写入改进验证链和 CLAUDE.md。
