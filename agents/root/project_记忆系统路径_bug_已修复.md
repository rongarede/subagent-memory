---
id: project_记忆系统路径_bug_已修复
name: 记忆系统路径 bug 已修复
description: --store 参数被 --agent 静默覆盖的 bug，TDD 验证并修复
type: project
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- 记忆系统
- 路径bug
- get_store
- cli.py
- TDD
- 修复
tags:
- task
context: ''
timestamp: '2026-03-14T13:18:15.680038'
related:
- '[[project_yume_记忆反馈改进方案决策]]'
- '[[task_整夜优化完成_—_6_轮_577_测试]]'
- '[[feedback_agent_配置文件修改归属_yume]]'
- '[[task_phase_2_consolidation+decay_决策]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
---

关键 bug：cli.py get_store() 中 --agent 优先级高于 --store，导致所有记忆写入 ~/.claude/memory/agents/{name}/ 而非 CLAUDE.md 规定的 ~/mem/mem/agents/{Type}/{name}/。本次会话 6 次 yume 调度全部受影响。已通过 TDD 三阶段修复（RED 11 FAIL → GREEN 13 PASS）。设计文档：docs/plans/2026-03-14-yume-memory-test-design.md
