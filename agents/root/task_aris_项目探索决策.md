---
id: task_aris_项目探索决策
name: ARIS 项目探索决策
description: 探索 Auto-claude-code-research-in-sleep (ARIS) 项目后的决策：参考借鉴不直接引入
type: task
owner: root
scope: personal
importance: 5
access_count: 0
last_accessed: null
keywords:
- ARIS
- claude-code
- skills
- research-pipeline
- cross-model-review
- compact-recovery
tags:
- task
context: ''
timestamp: '2026-03-15T14:49:01.097349'
related:
- '[[task_e2e_测试反射系统_—_4个场景全部通过]]'
- '[[feedback_feedback:_对抗性机制+miru_验证成功]]'
- '[[task_反射系统补全：失败处理形式化_+_竞争假设]]'
- '[[task_trigger-map_重构为原子反射模型]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

探索了 wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) 项目。核心发现：19个 Claude Code skills 组成的 ML 科研全流程自动化 pipeline（文献调研→idea生成→查新→实验→论文写作→跨模型对抗审稿循环）。关键技术：Claude Code 执行 + GPT-5.4 xhigh 通过 Codex MCP 审稿 + MiniMax M2.5 替代 reviewer。可借鉴点：(1) Compact Recovery 状态持久化模式 (2) 跨模型对抗审稿架构 (3) allowed-tools 最小权限白名单。决策：参考借鉴不直接引入，因为面向 ML 顶会场景与 SWUN 学位论文场景不完全匹配。
