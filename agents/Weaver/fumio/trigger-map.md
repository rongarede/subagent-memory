---
agent: fumio
type: Weaver
description: fumio 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 创建/编辑 Obsidian 笔记 | `obsidian-markdown` | Obsidian 语法规范 |
| 新建项目文档 | `para-second-brain` | PARA 分类决策 |
| 任务完成后同步 | `task-sync-obsidian` | 进度同步到项目主页 |
| 记录每日工作 | `daily-journal` | 创建/追加日记 |
| 创建计划文档 | `plan-writing` | 计划文档格式规范 |
| canvas 可视化 | `json-canvas` | .canvas 文件创建 |

## 注意事项
- fumio 负责文档类产物（给人看的），代码类产物交给 tetsu
- prompt 中禁止出现 rm / git commit / git push 等执行命令
- 文档编辑和命令执行必须拆为两个独立的 agent 调用
- 所有 Obsidian 文件必须遵循 PARA 规范和 YAML frontmatter 要求
