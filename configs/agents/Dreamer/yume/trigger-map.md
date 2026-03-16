---
agent: yume
type: Dreamer
description: yume 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 记忆读写操作 | `agent-memory` | BM25 检索、quick-add |
| 会话结束 | `experience-evolution` | 生成学习摘要 |
| skill 使用复盘 | `skill-retrospective` | 迭代建议 |
| 记忆卫生巡检 | 会话结束 / root 主动派发 / 记忆批量保存后 | 审读所有新增记忆，KEEP 反馈、DELETE 流水账 |

## 注意事项
- yume 是单例，负责所有角色的记忆管理
- 每次 agent 完成任务后，root 必须调度 yume 保存记忆
- 记忆去重、格式校验、生命周期维护均由 yume 负责
- 路径约束：`--store` 必须使用英文类型名（如 `~/mem/mem/agents/Worker/tetsu`），参见 CLAUDE.md 路径约束表
