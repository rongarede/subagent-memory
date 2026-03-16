---
name: archive_summary
description: 历史任务记忆蒸馏摘要（yume）
type: archive
created: 2026-03-15
source_count: 5
---

## 关键经验教训

### 记忆系统管理原则
- yume 是 ~/mem/mem/ 的唯一管理者，其他 agent 不得直接操作记忆系统
- 根目录散落的 .md 记忆文件必须归入对应 agent 子目录，通过 ~/mem/<agent>/ 统一访问
- 批量修复 frontmatter 时（补全 positive_feedback/negative_feedback/timestamp/related/accessed_by/evolution_history 等字段），可以一次性处理 100+ 文件

### 记忆清理经验
- 常见问题类型：无名文件（.md 孤儿）、旧格式（JSONL 残留）、双扩展名（如 CLAUDE.md.md）、broken symlink
- P1 修复顺序：无名文件重命名 → 双扩展名修复 → 旧格式 frontmatter 补全（共 123 个文件）
- P2 修复顺序：垃圾文件删除 → JSON→MD 转换 → 无前缀文件重命名 → shared/auto-memory 评估
- 检查 shared/ 和 auto-memory/ 后发现已是干净状态（2026-03-14），无需进一步清理

### 记忆统计（历史基线）
- 2026-03-13 首次盘点：11 个 agent 注册，共 30 条 .md 记忆，空 agent 4 个（fumio/haku/mirin/raiga）
- 2026-03-13 盘点时：shin 2 条，yume 3 条，tetsu 最多 9 条
- 清理了 6 个 .jsonl.bak 迁移残留、6 个 MISSING_id（kaze 004-006, shared 009-011）、1 个 broken symlink

## 重要发现

- workflow 模板系统：root 决策链可复用为 research-decide-implement 模板，存入 ~/mem/mem/workflows/templates/
- 记忆系统运行正常（2026-03-13 验证）：retriever 检索有效，新保存的任务记忆格式正确
- total 文件数 204，total 大小 832K（2026-03-14 基线）
