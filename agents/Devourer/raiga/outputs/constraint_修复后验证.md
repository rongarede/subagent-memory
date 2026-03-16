---
source: feedback_test_after_fix.md, feedback_verify_subagent_output.md
consumed_at: 2026-03-13
target: ~/.claude/CLAUDE.md

id: constraint_修复后验证
importance: 5
access_count: 0
last_accessed: 
keywords: []
tags: []
positive_feedback: 0
negative_feedback: 0
scope: private
context: 
timestamp: 2026-03-14T23:33:44.695765
related: []
accessed_by: []
evolution_history: []
---

## 修复后验证约束（CRITICAL）

Worker（tetsu）完成任何修复任务后，root 必须立即安排 Auditor（shin）审计：
1. tetsu 完成修复 → 标记 Task completed
2. root 立即创建审计 Task → 分配给 shin
3. shin 审计通过 → 才可 commit/push
4. shin 发现问题 → tetsu 二次修复 → shin 再审

禁止：跳过审计直接 commit/push
禁止：忘记安排审计后由用户提醒
