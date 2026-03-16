---
id: feedback_test_after_fix
name: 修复后必须测试
description: 所有修复执行完成后必须运行一轮测试验证，不能跳过
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.723939
related:
- '[[feedback_所有改动必须实战验证]]'
- '[[feedback_feedback:_skill_创建后必须触发测试]]'
- '[[feedback_b1_鼓励持续执行]]'
- '[[feedback_脑暴是内部思考不是外部提问]]'
- '[[task_e2e_测试反射系统_—_4个场景全部通过]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-13：b1 要求所有修复执行后都需要进行一轮测试。

规则：
- 代码修复后 → 运行相关测试套件
- 配置修复后（CLAUDE.md、agents.md 等）→ shin 验证写入正确性
- 目录重构后 → 验证文件数量和路径
- 任何修复都不能跳过验证直接声称完成
- 这是 Definition of Done 的隐含前提
