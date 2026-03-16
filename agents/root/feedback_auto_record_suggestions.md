---
id: feedback_auto_record_suggestions
name: 用户建议必须自动记录
description: 用户提出建议或纠正时，root 必须立即记录到 CLAUDE.md 和 feedback
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.725343
related:
- '[[feedback_feedback:_建议即执行，不等确认]]'
- '[[feedback_反馈：任务完成必须触发完成反射]]'
- '[[feedback_反馈-审计结果必须立即修正]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

## 反馈

用户指出：root 收到用户行为建议后只口头承认，没有主动记录到 CLAUDE.md 和 feedback 记忆中。

## 规则

用户提出行为建议或纠正时，root 必须立即：
1. 触发 raiga 吞食反馈 → 产出 CLAUDE.md 约束
2. 触发 yume 记录 feedback 到 ~/mem/mem/root/
3. 不等用户二次提醒
