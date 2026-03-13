# Subagent Memory

联想记忆系统：为 Claude Code subagent 提供基于 BM25 + 三维评分的任务记忆检索、创建和关联管理。

## 特性

- **BM25 + 三维评分检索**：relevance（BM25 min-max normalized）+ recency（0.995^hours）+ importance（val/10）
- **扩散激活**：1-hop 遍历 related_ids，自动拉入关联记忆
- **双层记忆**：个人记忆（per-agent）+ 共享记忆（common knowledge），支持被动晋升
- **角色注册系统**：6 类角色（Explore/Worker/Auditor/Operator/Analyst/Inspector），每类预定义名字池
- **邻居演化**：LLM 驱动的 3 步分解（判断→计划→执行），基于 A-MEM 论文改进
- **Obsidian 导出**：记忆导出为 Obsidian 笔记 + MOC + 关联图谱
- **中文支持**：字符级 + bigram 分词，完整中文检索链路

## 架构

```
scripts/
├── memory_store.py    # 数据模型 + JSONL 持久化
├── retriever.py       # BM25 + 三维评分检索
├── associator.py      # 双向关联管理
├── extractor.py       # Claude API 字段提取
├── inject.py          # Prompt 注入 + 被动演化
├── evolver.py         # LLM 驱动邻居演化
├── registry.py        # 角色注册与管理
├── obsidian_export.py # Obsidian 导出
└── cli.py             # CLI 入口

tests/
├── test_retriever.py      # 检索测试
├── test_extractor.py      # 提取测试
├── test_inject.py         # 注入测试
├── test_evolver.py        # 演化测试
├── test_integration.py    # 端到端集成测试
└── test_multi_agent.py    # 多角色测试
```

## 角色系统

| 类型 | 职责 | 名字池 |
|------|------|--------|
| Explore | 代码库探索、信息收集 | Kaze, Mirin, Soren, Vento, Cirro |
| Worker | 文件修改、代码实现 | Tetsu, Aspen, Ember, Riven, Cobalt |
| Auditor | 代码审查、质量审计 | Shin, Onyx, Argon, Quartz, Flint |
| Operator | 通用任务执行 | Sora, Nimba, Prism, Helix, Pulse |
| Analyst | 分析、研究 | Yomi, Lyric, Astra, Cipher, Nexus |
| Inspector | 检查、验证 | Haku, Rune, Velox, Ignis, Terra |

## 使用

### CLI

```bash
# 添加记忆
python scripts/cli.py add "LaTeX 编译失败，fontspec 找不到字体"

# 检索记忆
python scripts/cli.py retrieve "字体编译错误"

# 带角色检索
python scripts/cli.py --agent kaze retrieve "字体编译错误"

# 查看统计
python scripts/cli.py stats

# 导出到 Obsidian
python scripts/cli.py export --output ./obsidian_notes/
```

### 作为 Claude Code Skill

将本项目放置于 `~/.claude/skills/agent-memory/`，Claude Code 会自动识别 SKILL.md 并启用记忆功能。

## 测试

```bash
python -m pytest tests/ -v
```

69 个测试，覆盖单元测试 + 集成测试 + 多角色测试。

## 致谢

邻居演化机制参考了 [A-MEM](https://github.com/WujiangXu/A-mem) 论文的 `update_neighbor` 模式。

## License

MIT
