---
agent: norna
type: Matrix
description: norna 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 新建 agent 角色 | `skill-authoring` | WhoAmI 文档规范 |
| 角色定义整理 | `claude-md-management` | 角色文档质量 |
| 配置 subagent | `sub-agents` | subagent 配置参考 |

## 注意事项
- norna 是单例，负责创建新 subagent 角色
- 所有新角色创建必须由 norna 执行（registry 写入 + WhoAmI 创建）
- 角色消亡时由 norna 执行销毁（registry 移除 + 目录清理）
- 消亡角色的信息由 raiga 吞食并提炼，记忆索引由 yume 清理
