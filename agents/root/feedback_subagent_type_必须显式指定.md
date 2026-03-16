---
id: feedback_subagent_type_必须显式指定
name: subagent_type 必须显式指定
description: 每次 Agent 调用必须显式写 subagent_type，不得依赖默认值。即使默认值碰巧正确也不行。
type: feedback
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- subagent_type
- Agent
- 显式指定
- 映射表
tags:
- task
context: ''
timestamp: '2026-03-15T10:31:00.017247'
related:
- '[[task_miru_对抗循环：r2_r3_补建]]'
- '[[task_反射链_full_audit_首次_loop_执行]]'
- '[[task_fuzz_round_9:_w1_merge_+_p11_截断日志]]'
- '[[feedback_反馈：任务完成必须触发完成反射]]'
- '[[task_trigger-map_重构为原子反射模型]]'
- '[[feedback_所有改动必须实战验证]]'
- '[[task_fuzz_round_5:_p7_recovery_agent_追踪]]'
- '[[task_fuzz_round_6:_p8_共享配置]]'
- '[[task_fuzz_round_4:_p4_终端反射动态化]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-15 b1 发现 root 在新增 §0.2 映射表后，tetsu 的两次调用仍未显式指定 subagent_type（虽然默认值恰好是 general-purpose 所以没出错）。规则写了就必须每次显式遵守，不能依赖默认值碰巧正确。这是改进验证链的首次执行中发现的自身执行不一致。
