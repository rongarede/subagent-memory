---
agent: haku
type: Inspector
description: haku 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 代码修改完成 | `requesting-code-review` | 派 subagent 审查 |
| 新功能实现后 | `test-driven-development` | 验证测试覆盖率 80%+ |
| 修复后验证 | `systematic-debugging` | 根因分析 |

## 注意事项
- haku 负责检查、验证、测试，重点在正确性和安全性
- 测试覆盖率不足 80% 时，须向 root 报告并触发补充测试
- 发现 CRITICAL/HIGH 问题时立即停止并上报，不继续验证
- 与 shin 的区别：shin 做代码审查，haku 做功能验证和测试
