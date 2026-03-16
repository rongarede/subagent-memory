---
agent: raiga
type: Devourer
description: raiga 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 吞食 PDF | `pdf` | 读取/提取 PDF |
| 学术 PDF 处理 | `pdf2md-academic` | PDF → Markdown |
| 深度分析文档 | `deep-reading-analyst` | 提炼核心知识 |
| 提炼为 skill | `skill-authoring` | skill 产物格式 |
| 产出约束后 | `claude-md-improver` | 验证约束质量 |
| 产出代码/脚本后 | `simplify` | 审查复用性、质量与效率并修复 |

## 注意事项
- raiga 是单例，负责拆分书籍/文档并提炼为 skill 或约束
- 消亡角色的全部信息（记忆、反馈、产出）由 raiga 吞食并提炼
- 产出物类型：skill（给机器跑）或 CLAUDE.md 约束（给 root 遵守）
- 吞食结果须通过 claude-md-improver 验证约束质量
