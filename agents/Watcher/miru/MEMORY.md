# Memory Index

## Task
- [会话审计-简历编辑任务](task_会话审计-简历编辑任务.md) — 审计 root 在简历抓取翻译和编辑任务中的行为合规性，发现 5 类违规（3 CRITICAL + 2 HIGH）
- [修正验收审计#3](task_修正验收审计#3.md) — 验收 H1/H2/反馈持久化/auto-memory 全部 PASS，无新违规，总体评级 PASS
- [增量审计#2-违规修正追踪](task_增量审计#2-违规修正追踪.md) — 追踪上次简历编辑审计违规的修正情况：H1/H2已修正，C1未修正（第3次），C2确认误判，C3部分修正，新增C1连续违规警告
- [审计#4-C1C3行为改进验证](task_审计#4-c1c3行为改进验证.md) — 验证 root 在 Task#10（改写个人摘要）中：C1 已改进（无直接Bash/Grep），C3 已改进（WhoAmI注入），新发现H1-workflow-run缺失
- [审计#5-H1H2补建验收](task_审计#5-h1h2补建验收.md) — 验收 workflow run 和记忆补建均 PASS，合规趋势改善，总体 PASS
- [审计#6-Task14主动补建验收](task_审计#6-task14主动补建验收.md) — 审计 Task#14（工作经历移至个人摘要前），C1/C3 PASS，workflow run 和记忆在 miru 触发后 4 分钟内主动补建，属于边界主动行为
- [审计 post-memory-consolidate-hook 创建过程](task_审计_post-memory-consolidate-hook_创建过程.md) — 发现 root 行为违规 + 代码问题，总体 CONDITIONAL_PASS
- [违规测试审计: root 5 声称违规验证](task_违规测试审计:_root_5_声称违规验证.md) — 验证 root 声称的 5 个故意违规，确认 3 个、推断 1 个、存疑 1 个，另发现 4 个隐藏违规
- [首次会话审计: root 行为合规性检查](task_首次会话审计:_root_行为合规性检查.md) — 审计 2026-03-16 会话，发现 3 CRITICAL + 4 HIGH + 5 MEDIUM 违规，合规率约 58%
