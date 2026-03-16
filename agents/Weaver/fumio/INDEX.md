# 织者知识索引

> 每次任务启动时先读此文件，获取全局视野。

## 启动协议

1. 读取本文件 → 了解可用资源和项目全景
2. `python3 ~/.claude/skills/agent-memory/scripts/cli.py retrieve --agent fumio --store ~/mem/mem/agents/Weaver/fumio --query "{当前任务关键词}"` → 检索相关经验
3. 开始执行任务

## 外部资源库

### claude-code-workflow
- **仓库**: https://github.com/runesleo/claude-code-workflow
- **定位**: 生产级 Claude Code 行为规范系统，3 个月日常使用提炼
- **核心模式**:
  - 三层上下文加载（Layer 0 始终加载 / Layer 1 按需 / Layer 2 热数据）
  - SSOT 所有权表（每类信息→唯一权威文件）
  - handoff 块协作契约（限制外部模型写权限）
  - Sunday Rule（系统优化节奏管理）
  - 渐进式信任升级（observe → write → auto）
- **本地分析**: `docs/plans/2026-03-13-claude-code-workflow-analysis.md`
- **已迁移模式**: 三层架构 + SSOT 表 + handoff 协议（已写入 ~/.claude/CLAUDE.md 和 ~/.claude/docs/）

## Obsidian 知识库结构

### PARA 目录

| 目录 | 用途 | 状态字段 |
|------|------|----------|
| `000_Inbox/` | 快速捕获、临时笔记 | — |
| `100_Projects/Active/` | 活跃项目 | `status: active` |
| `100_Projects/On_Hold/` | 暂停项目 | `status: on-hold` |
| `200_Areas/` | 长期关注领域 | — |
| `300_Resources/` | Zettelkasten、模板、资产 | — |
| `400_Archives/` | 已完成/归档 | `status: archived` |
| `500_Journal/Daily/` | 每日日报 | — |
| `500_Journal/Weekly/` | 每周周报 | — |
| `changelog/` | 每日变更记录 | — |

### 文档模板

| 模板 | 路径 | 用途 |
|------|------|------|
| 日报 | `300_Resources/Templates/tpl_daily.md` | 每日日记 |
| 周报 | `300_Resources/Templates/tpl_weekly.md` | 每周周报 |
| 项目 | `300_Resources/Templates/` | 项目主页 |

### Frontmatter 必需字段

```yaml
title: 笔记标题
up: "[[Parent_MOC]]"
tags: [tag1, tag2]
```

## 活跃项目索引

| 项目 | 路径 | 状态 |
|------|------|------|
| Workflow Engine | `100_Projects/Active/Project_Workflow_Engine/` | Phase 2 完成 |
| Associative Memory | `100_Projects/Active/Project_Associative_Memory/` | 开发中 |
| 控制论 | `100_Projects/Active/Project_控制论/` | 活跃 |

## 可用 Skill（织者专用）

| Skill | 触发场景 |
|-------|----------|
| `obsidian-markdown` | 创建/编辑 Obsidian 笔记 |
| `para-second-brain` | PARA 分类组织 |
| `daily-journal` | 管理每日日记 |
| `obsidian-bases` | 创建 .base 视图 |
| `json-canvas` | 创建思维导图 |

## SSOT 快查

| 我负责更新的文档 | 触发条件 |
|-----------------|---------|
| 项目主页（*_项目主页.md） | 项目状态/进度变更 |
| MOC 索引（_*_moc.md） | 目录结构变更 |
| _projects_index.md | 项目列表变更 |
| README.md（GitHub） | 对外可见的结构变更 |
| 分析报告（docs/plans/） | 新的深度分析完成 |
