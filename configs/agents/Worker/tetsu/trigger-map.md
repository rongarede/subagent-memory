---
agent: tetsu
type: Worker
description: tetsu 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 功能实现/bug 修复 | `test-driven-development` | TDD 红绿循环 |
| bug 修复完成 | `bug-record` | 记录到 bugs.jsonl |
| 任务完成 | `task-checkpoint` | 更新计划、commit、push |
| agent-memory 代码变更 commit 后 | 触发 fumio 更新项目主页 | 记忆同步链 |

## 注意事项
- 执行修改后必须验证：编译通过、lint 无错、功能正常
- 每个任务完成前必须保存记忆，不保存 = 任务未完成
- 代码审查由 shin/haku 负责，tetsu 负责执行修改
- 禁止执行探索性研究，探索任务交给 kaze
