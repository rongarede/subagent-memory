---
name: agent-memory
description: 联想记忆系统：为 Claude Code subagent 提供基于 BM25 + 三维评分的记忆检索、存储、反馈学习能力
version: 3.0
---

# Agent Memory System

为 Claude Code subagent 提供联想记忆能力。

## 核心能力

| 能力 | 模块 | 说明 |
|------|------|------|
| 存储 | memory_store.py | Markdown 文件存储，YAML frontmatter 元数据 |
| 检索 | retriever.py | BM25 + 扩散激活 + 三维评分（相关性/重要性/新近性） |
| 关联 | associator.py | 共现分析 + 语义相似度 |
| 提取 | extractor.py | 从任务描述自动提取结构化记忆 |
| 注入 | inject.py | 向 agent prompt 注入相关记忆上下文 |
| 演化 | evolver.py | LLM 驱动的记忆邻居演化 |
| 去重 | consolidator.py | Jaccard 相似度合并（阈值 0.85） |
| 衰减 | decay_engine.py | Ebbinghaus 遗忘曲线 R=e^(-t/S) |
| 学习 | feedback_loop.py | 自动推断 + 渐进式升级（降权→告警→阻断，health 过滤） |
| 触发 | trigger_tracker.py | 触发效率追踪：record/efficiency/adjust/stats/reset |
| 导出 | obsidian_export.py | Obsidian 笔记/MOC/Mermaid 图 |
| 注册 | registry.py | Agent 角色注册表 |

## 存储格式

每条记忆为一个 `.md` 文件，YAML frontmatter 包含元数据：

```yaml
---
id: task_example
name: 任务描述
description: 一句话摘要
type: task
owner: tetsu
scope: private
importance: 8
access_count: 3
positive_feedback: 5
negative_feedback: 1
keywords: [TDD, Python]
tags: [implementation]
timestamp: 2026-03-14T22:00:00
---

记忆正文内容...
```

## CLI 用法

```bash
# 基础路径
SCRIPT=~/.claude/skills/agent-memory/scripts/cli.py

# 快速添加记忆
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu \
  quick-add --name "任务名" --description "描述" --type task "正文内容"

# 检索记忆
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu \
  retrieve --query "搜索关键词" --top-k 5

# 反馈（手动）
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu \
  feedback --memory-id "mem_id" --positive

# 反馈（自动推断）
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu \
  feedback --memory-id "mem_id" --auto --event task_success

# 记忆去重合并
python3 $SCRIPT --store ~/mem/mem/agents/蚁工/tetsu \
  consolidate --threshold 0.85 --dry-run

# 统计
python3 $SCRIPT --store ~/mem/mem/agents/蚁工/tetsu stats

# 生成索引
python3 $SCRIPT --store ~/mem/mem/agents/蚁工/tetsu generate-index
```

## 路径约束

| Agent | 正确路径 |
|-------|---------|
| tetsu | ~/mem/mem/agents/蚁工/tetsu |
| shin | ~/mem/mem/agents/Auditor/shin |
| fumio | ~/mem/mem/agents/织者/fumio |
| root | ~/mem/mem/root |

`--store` 参数优先于 `--agent` 推断的路径。

## 测试

```bash
cd ~/.claude/skills/agent-memory
python3 -m pytest  # 234 tests, ~5s
```

## 架构演进

| Phase | 内容 | 状态 |
|-------|------|------|
| Phase 1 | Active Recall + Retrieval Feedback | 已完成 |
| Phase 2 | Memory Consolidation + Decay | 已完成 |
| Phase 3 | Feedback Learning Loop | 已完成 |
| Phase A | feedback_loop.py 审计修复（M1-M4） | 已完成 |
| Phase B | retriever + cli feedback 集成 | 已完成 |
| Phase C | trigger_tracker.py 智能触发追踪 | 已完成 |
| Phase D | 端到端测试（5 场景，12 tests） | 已完成 |
| Phase E | 全量审计 + 文档同步 | 已完成 |

也可在 CLI 中添加 health-check 和 trigger 子命令：

```bash
# 健康检查
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu health-check

# 触发追踪
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu trigger stats
python3 $SCRIPT --agent tetsu --store ~/mem/mem/agents/蚁工/tetsu trigger reset
```
