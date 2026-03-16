---
id: feedback_critical_memory_save
name: 严重错误：subagent 从未保存任务记忆
description: 10+ 次 subagent 调用零条记忆保存，系统性遗漏，b1 指出为严重错误
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.723198
related:
- '[[task_记忆系统现状评估完成]]'
- '[[feedback_subagent_需要各自的_trigger-map]]'
- '[[feedback_subagent_type_必须显式指定]]'
- '[[task_task10-个人摘要改写为叙述风格]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-13：b1 指出 root 从未让 subagent 保存任务记忆，这是严重的系统性错误。

## 错误描述

本轮会话完成 Task #55-64，调用 subagent 10+ 次，但零条任务记忆被保存到 ~/mem/mem/agents/。
agent-memory 的 quick-add CLI 存在但从未被调用。

## 根因

1. WhoAmI.md 中缺少强制收尾规则
2. root 在 Agent prompt 中从未包含「保存记忆」指令
3. task-complete-hook 不触发记忆保存
4. root 未将「记忆保存」纳入 Definition of Done 检查

## 修复

1. agents.md 追加 0.1 任务记忆保存（CRITICAL）全局约束
2. 11 个 WhoAmI.md 追加「任务完成收尾（MANDATORY）」
3. root 每次 Agent prompt 末尾必须附带记忆保存指令模板

## root 行为变更

从此以后，root 在构造每个 Agent prompt 时，末尾必须包含：
"任务完成后，使用 quick-add 保存记忆到你的目录。"

严重程度：CRITICAL — 直接导致整个记忆系统形同虚设。
