---
id: feedback_verify_subagent_output
name: root 必须验证 subagent 输出质量
description: subagent 完成任务后 root 必须检查实际结果（如 git log），不能只看自报摘要
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.725064
related:
- '[[task_phase_a_完成：feedback_loop.py_审计修复]]'
- '[[feedback_subagent_type_必须显式指定]]'
- '[[feedback_所有改动必须实战验证]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
---

2026-03-13：tetsu 执行 git commit + push 后产生重复 commit，root 未验证 git log 就声明完成。b1 事后发现。

规则：
- git 操作后：检查 git log 确认 commit 数量和内容
- 文件操作后：抽查关键文件内容
- 测试操作后：确认通过数量与预期一致
- 不要只转述 subagent 自报结果，必须独立验证
