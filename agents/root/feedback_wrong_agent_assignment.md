---
id: feedback_wrong_agent_assignment
name: 错误的 agent 任务分配
description: root 将角色定义任务错误分配给 tetsu 而非 norna
type: feedback
owner: ''
scope: private
importance: 5
access_count: 0
last_accessed: null
keywords: []
tags: []
context: ''
timestamp: 2026-03-14 23:33:44.728073
related:
- '[[task_reflex-audit首次审计：d级48分]]'
- '[[task_反射链_full_audit_首次_loop_执行]]'
- '[[feedback_agent_配置文件修改归属_yume]]'
- '[[feedback_feedback:_创建_skill_应使用__skill-create]]'
- '[[feedback_subagent_type_必须显式指定]]'
- '[[task_adr_+_mermaid_架构文档_mission]]'
- '[[feedback_root_违规：主会话直接使用_read_bash]]'
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

## 错误

root 将"为所有 agent 定义角色、分配 skills 和 workflow"任务分配给了 tetsu（Worker），但这是 norna（母体）的职责。

## 原因

- 角色定义和技能分配是管理性/创造性任务，属于母体职责
- tetsu 是 Worker，只负责文件操作，不应做角色决策
- root 未正确匹配任务性质与 agent 职责

## 教训

分配任务前必须分析：
1. 任务性质（执行性 vs 管理性 vs 分析性）
2. 对应的 agent 职责域
3. Worker 不做决策，母体不做搬运

## 再犯记录（2026-03-13）

root 再次将角色重定义任务（yomi Analyst → 斥候）分配给 tetsu（Worker），而非 norna（母体）。

这是同一错误的第二次发生。root 已有此反馈却未内化执行。

### 强化规则

凡涉及以下关键词的任务，**必须**分配给 norna：
- 角色定义 / 重定义
- 类型变更
- WhoAmI 修改
- 技能分配
- 工作流定义
- agent 创建 / 销毁

tetsu 只做机械性文件搬运（mv/cp/rm），不做身份内容决策。

### 2026-03-13 再再犯：文档任务错派 tetsu

**错误**：将"保存设计文档"和"创建 YAML 模板文件"任务分配给 tetsu（蚁工），应该分配给 fumio（图书管理员）。

**规则**：
- 设计文档、YAML 模板、README、MOC 等**文档类产物**的创建和整理 → fumio
- tetsu 只负责**代码实现**（编写代码、修 bug、执行构建命令）
- 判断标准：产物是给人看的文档 → fumio；产物是给机器跑的代码 → tetsu

**触发地图更新建议**：
- 创建/编辑 .yaml 模板 → fumio
- 创建/编辑 设计文档 → fumio
- 创建/编辑 项目主页 → fumio

### 2026-03-13 第四次：fumio 执行了 tetsu 的工作

**错误**：让 fumio（图书管理员）在更新项目主页的同时执行 `rm -f` 清理和 `git commit/push`。应该拆分为两步：fumio 只编辑文档，tetsu 执行清理和提交。

**根因**：为了"效率"把文档编辑和命令执行合并到一个 agent，违反了角色边界。

**强化规则**：
- fumio 的 prompt 中**禁止**出现 `rm`、`git commit`、`git push`、`chmod` 等执行类命令
- 文档编辑和命令执行**必须拆为两个 agent 调用**，即使看起来"顺手"
- 效率不是打破角色边界的理由
