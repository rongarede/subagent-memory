---
id: project_agent_lifecycle
name: Agent 生命周期规则
description: b1 创建的原始 agent 不朽，母体创建的 agent 可因反馈过差被消亡，消亡时吞食者吞食其全部信息
type: project
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.721938
related:
- '[[task_adr_+_mermaid_架构文档_mission]]'
- '[[feedback_subagent_需要各自的_trigger-map]]'
- '[[task_trigger-map_重构为原子反射模型]]'
- '[[feedback_root_违规：主会话直接使用_read_bash]]'
- '[[feedback_feedback:_创建_skill_应使用__skill-create]]'
accessed_by: []
evolution_history: []
positive_feedback: 0
negative_feedback: 0
retrieval_count: 0
last_retrieved: ''
usefulness_score: 0.5
layer: L1
---

2026-03-13：b1 定义了 agent 生命周期规则。

## 不朽 Agent（b1 直接创建）

以下 11 个 agent 由 b1 亲自创建，永不消亡：
- kaze、mirin、shin、tetsu、sora、yomi、haku（通用角色）
- 吞食者(raiga)、图书管理员(fumio)、母体(norna)、梦者(yume)（Singleton 中文角色）

## 可消亡 Agent（母体创建）

母体（norna）创建的新 subagent，如果反馈评估过差，触发消亡机制：

### 消亡流程
1. 反馈积累到一定负面程度 → root 或 b1 决定消亡
2. **母体** 执行销毁：从 registry 移除、清理目录结构
3. **吞食者** 吞食该 agent 的所有信息：
   - 记忆文件（~/mem/mem/agents/ 下的全部 .md）
   - 反馈记录
   - 产出物
   - 消化提炼为 skill 或 CLAUDE.md 约束（知识不浪费）
4. 梦者清理记忆索引

### 消亡条件（待 b1 细化）
- 反馈文件中"禁止行为"被多次触犯
- 多轮任务中持续表现不佳
- root 或 b1 明确下达消亡指令
