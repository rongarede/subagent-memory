---
id: feedback_update_project_page
name: 每轮 task 完成后必须更新项目主页
description: TaskUpdate status=completed 后，root 必须检查并更新对应的 Obsidian 项目主页迭代日志
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.727193
related:
- '[[task_task10-个人摘要改写为叙述风格]]'
- '[[feedback_反馈：任务完成必须触发完成反射]]'
- '[[task_round_4_智能自动化完成]]'
- '[[feedback_subagent_需要各自的_trigger-map]]'
- '[[feedback_subagent_type_必须显式指定]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-13：b1 指出 root 在多轮 task 完成后未更新 Associative_Memory_项目主页.md。

规则：
- 每个 Task 标记 completed 后，root 必须确认对应项目主页已更新
- task-sync-hook.py 可能自动触发，但 root 不能依赖 hook，必须独立验证
- 更新内容：迭代日志追加当轮完成的任务摘要、日期、执行角色
- 涉及文件：/Users/bit/Obsidian/100_Projects/Active/Project_Associative_Memory/Associative_Memory_项目主页.md
