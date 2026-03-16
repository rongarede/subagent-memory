# Agent Memory Directory

按 subagent_type 分组：

| Type | Agents | 说明 |
|------|--------|------|
| Explore | kaze | 代码库快速搜索 / 深度阅读、PDF 分析 |
| Auditor | shin | 只读审计、质量检查 |
| Worker | tetsu | 文件操作、代码修改 |
| Operator | sora | 运维操作 |
| Analyst | yomi | 外部信息勘探、学术检索 |
| Inspector | haku | 代码审查 |
| Devourer | raiga | 吞食文档，产出 skill 和 CLAUDE.md 约束 |
| Weaver | fumio | 知识库文档管理 |
| Matrix | norna | 创造与销毁 agent |
| Dreamer | yume | 记忆系统管理 |

## 目录结构

```
~/mem/mem/agents/
├── Explore/
│   └── kaze/
├── Auditor/
│   └── shin/
├── Worker/
│   └── tetsu/
├── Operator/
│   └── sora/
├── Analyst/
│   └── yomi/
├── Inspector/
│   └── haku/
├── Devourer/
│   └── raiga/
├── Weaver/
│   └── fumio/
├── Matrix/
│   └── norna/
├── Dreamer/
│   └── yume/
└── README.md
```

## 每个 Agent 目录包含

- `WhoAmI.md` — 身份定义
- `role.md` — 技能分配与工作流
- `feedback_*.md` — 行为反馈
- `{agent}_{date}_{seq}.md` — 任务记忆
