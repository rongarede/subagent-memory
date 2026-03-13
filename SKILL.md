---
name: agent-memory
description: 联想记忆系统：为 Claude Code subagent 提供基于 BM25 + 三维评分的任务记忆检索、创建和关联管理。
triggers:
  - /memory
  - /recall
  - 记忆检索
  - 联想记忆
  - 记忆管理
---

# Agent Memory — 联想记忆系统

## 概述

为 Claude Code subagent 构建的轻量级联想记忆系统，融合：
- **A-MEM** 的 Zettelkasten 数据模型（keywords/tags/context/links）
- **Generative Agents** 的三维评分检索（recency + importance + relevance）
- **BM25** 全文检索（零外部依赖，无需向量数据库）

## 使用方式

### 1. 检索记忆（最常用）

启动 subagent 前，检索相关历史经验注入 prompt：

```bash
cd ~/.claude/skills/agent-memory
python3 scripts/cli.py retrieve "LaTeX 编译错误"
```

或在主会话中：
```
/memory 检索 LaTeX 编译错误
```

### 2. 添加记忆

手动添加一条记忆（通常由 hook 自动完成）：

```bash
python3 scripts/cli.py add \
  --subject "修复 fontspec 编译错误" \
  --description "XeLaTeX 路径配置问题" \
  --importance 7
```

### 3. 查看统计

```bash
python3 scripts/cli.py stats
```

### 4. 列出最近记忆

```bash
python3 scripts/cli.py list --limit 10
```

### 5. 演化记忆

更新已有记忆的 context 或 tags：

```bash
python3 scripts/cli.py evolve mem_20260312_001 \
  --context "新的语境描述" \
  --tags "updated-tag1,updated-tag2"
```

## 工作流

### 自动记忆提取（Hook 驱动）

```
TaskUpdate → completed
    ↓
memory-extract-hook.py (后台)
    ↓
extractor.py → Claude API 提取 keywords/tags/context/importance
    ↓
associator.link_memory() → BM25 Top-5 自动关联
    ↓
memories.jsonl 写入
```

### 手动记忆检索（Skill 驱动）

```
用户: /memory 检索 <查询>
    ↓
retriever.retrieve() → BM25 + 三维评分
    ↓
扩散激活 → 展开 related_ids（score × 0.5 衰减）
    ↓
format_for_prompt() → 注入 subagent context
```

## 三维评分模型

| 维度 | 公式 | 含义 |
|------|------|------|
| Recency | `0.995 ^ hours_since_last_access` | 近因性衰减 |
| Importance | `importance / 10` | 重要性归一化 |
| Relevance | BM25 min-max 归一化 | 查询相关度 |

**综合分 = recency + importance + relevance**（各维度独立归一化到 [0,1]，最高 3.0 分）

扩散激活（spreading activation）：命中记忆的 `related_ids` 以 `score × 0.5` 权重加入结果集，实现联想链扩展。

## 文件结构

```
~/.claude/skills/agent-memory/
├── SKILL.md              # 本文件
├── CLAUDE.md             # 项目开发规则
├── plan.md               # 执行计划
├── auto-pilot.sh         # 自主执行驱动脚本
├── scripts/
│   ├── memory_store.py   # Memory 数据模型 + JSONL 存储
│   ├── retriever.py      # BM25 + 三维评分 + 扩散激活
│   ├── associator.py     # 双向联想链管理
│   ├── extractor.py      # Claude API 记忆字段提取（Phase 2）
│   └── cli.py            # CLI 入口
└── tests/
    ├── test_retriever.py  # 检索测试（17 tests）
    └── test_extractor.py  # 提取测试
```

默认记忆库路径：`~/.claude/memory/memories.jsonl`

## 记忆数据格式

每条记忆存储为 JSONL 一行：

```json
{
  "id": "mem_20260312_001",
  "content": "任务描述 + 结果",
  "timestamp": "2026-03-12T16:04:00",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "tags": ["分类1", "分类2"],
  "context": "一句话语境摘要",
  "importance": 7,
  "related_ids": ["mem_20260311_003"],
  "access_count": 0,
  "last_accessed": null
}
```

## 依赖

```bash
pip install rank-bm25
```

## Python API（供 subagent 直接调用）

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/agent-memory/scripts"))

from memory_store import Memory, MemoryStore
from retriever import retrieve, format_for_prompt
from associator import link_memory

store = MemoryStore()  # 使用默认路径
results = retrieve("查询文本", store, top_k=3, spread=True)
prompt_text = format_for_prompt(results)
# 将 prompt_text 注入 subagent 的系统提示词
```
