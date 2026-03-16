# 约束产出：文档同步约束

**来源反馈**：用户多次提醒 root 在完成角色定义、目录重构、配置变更后忘记触发 fumio 更新文档。

**吞食时间**：2026-03-13

**写入位置**：`~/.claude/CLAUDE.md` → `## 文档同步约束（CRITICAL）` 节（位于「修复后验证约束」之前）

---

## 产出约束内容

```markdown
## 文档同步约束（CRITICAL）

以下变更发生后，root **必须**立即安排 fumio（织者）更新文档：
- Agent 角色定义变更（WhoAmI/role.md/类型/职责）
- 目录结构变更（迁移/重命名/新增目录）
- 全局配置变更（CLAUDE.md/agents.md 规则变更）
- 项目状态变更（Active ↔ On_Hold ↔ Archived）

**触发流程：**
1. 变更完成 → root 创建 fumio 文档更新 Task
2. fumio 更新 Obsidian 项目文档 + GitHub README
3. 必要时 commit + push

**禁止**：变更后不触发文档同步
**禁止**：等用户提醒才想起更新文档
```

---

## 吞食分析

**根本原因**：root 缺乏"变更 → 文档同步"的强制触发机制，仅依赖人工记忆。

**约束强度**：CRITICAL（与「修复后验证约束」同级，防止被遗忘）

**覆盖场景**：
1. 角色定义更新 → fumio 同步角色文档
2. 目录重构 → fumio 更新目录索引/README
3. CLAUDE.md 规则变更 → fumio 同步变更日志
4. 项目状态切换 → fumio 更新项目主页状态

**预期效果**：root 在完成上述任意变更后，自动触发 fumio Task，无需用户提醒。
