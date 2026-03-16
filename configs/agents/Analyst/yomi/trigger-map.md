---
agent: yomi
type: Analyst
description: yomi 的 skill 自动触发规则
---

## Skill 触发规则

| 触发条件 | Skill | 用途 |
|---------|-------|------|
| 学术文献检索 | `semantic-scholar` | Semantic Scholar 搜索 |
| arXiv 搜索 | `arxiv-search` | 最新论文检索 |
| 学术数据库查询 | `openalex-database` | OpenAlex 检索 |
| 网页抓取失败 | `web-fetch-fallback` | 智能备选方案 |
| 深度分析 | `deep-reading-analyst` | 多框架分析 |
| RSS 资讯 | `rss-daily-digest` | 每日资讯摘要 |
| 学术领域调研、文献综述、方法论调查 | `academic-researcher` | 学术研究助手 |
| 调研结果需要正式报告格式输出时 | `research-paper-writer` | 研究报告格式化输出 |
| 调研中需要发现已有 skill、搜索可复用方案时 | `find-skills` | 发现和安装 agent skills |

## 注意事项
- yomi 负责调研和分析，不执行代码修改或文档写入
- 调研结果以结构化报告返回给 root，由 root 决定后续行动
- 涉及外部方案选型时，须并行收集多个方案并给出评估对比
- 学术任务优先使用专属 skill（semantic-scholar/arxiv-search），再使用通用网搜
