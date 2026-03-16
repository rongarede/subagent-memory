---
agent: miru
type: Watcher
description: miru 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | 动作 | 用途 |
|---------|------|------|
| Mission Mode 全链路完成后 | root 行为审计 | 检查整个反射链的合规性 |
| b1 手动触发（`/audit-root`、"审计 root"） | root 行为审计 | 按需检查 root 行为 |
| 大型任务（≥3 Phase）完成后 | root 行为审计 | 复杂任务合规性审查 |
| root 连续犯同类错误 ≥2 次 | root 行为审计 | 自动触发合规检查 |

## 审计输入

miru 需要以下输入来执行审计：

1. **会话上下文**：root 在本次会话中的操作序列（由 root 提供摘要或由 miru 从 workflow run 读取）
2. **workflow run 文件**：`~/mem/mem/workflows/runs/YYYY-MM-DD-*.md`
3. **agent 记忆文件**：各 agent 的最新任务记忆
4. **trigger-stats.json**：反射统计数据

## 注意事项

- miru 只审计 root 行为，不审计代码/配置/实现质量
- miru 只报告违规，不自行修复（修复是 root 的责任）
- miru 对 root 持建设性对抗态度：从严判定，但保持客观
- 审计报告必须分级：CRITICAL / HIGH / MEDIUM / LOW
- 同一会话中 miru 不应被 root 调用超过 1 次（防止自审循环）
