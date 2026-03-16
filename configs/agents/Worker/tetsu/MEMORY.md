# Memory Index

## Feedback
- [授权与越权约束](feedback_authorization.md) — tetsu 不得擅自重命名用户创建的内容，执行前确认范围
- [工作范围边界](feedback_scope.md) — sora 执行运维操作，与 tetsu 分工明确
- [工作范围边界](feedback_scope.md) — sora 执行运维操作，与 tetsu 分工明确

## Task
- [feedback](feedback.md) — 用户反馈：agent 默认后台运行
- [commit 4 bug fixes in agent-memory](task_commit_4_bug_fixes_in_agent-memory.md) — Committed 4 infrastructure bug fixes to agent-memory repo (350501b)
- [Fix1: 创建 CB 拦截 hook](task_fix1:_创建_cb_拦截_hook.md) — 创建 pre-agent-cb-check.py 实现 CB OPEN 时的 agent 拦截
- [fix empty content frontmatter parsing bug](task_fix_empty_content_frontmatter_parsing_bug.md) — Fixed _frontmatter_to_memory() crash on empty content by ensuring trailing newline after strip()
- [Fuzz F1: 审计失败 L1 Resume](task_fuzz_f1:_审计失败_l1_resume.md) — 测试审计反射失败后 Recovery Ladder L1 行为 — 全部通过
- [Fuzz Round 1 提交](task_fuzz_round_1_提交.md) — 提交 Fuzz Round 1 全部修复：日报 + changelog + workflow run 记录
- [Fuzz Round 3](task_fuzz_round_3.md) — 启用 parallel_batches CLI 入口（start-batch / check-batch），修复 P2 问题
- [git commit+push: trigger-map 并行派发协议](task_git_commit+push:_trigger-map_并行派发协议.md) — Staged all 87 pending changes, committed as c5cf8dd, pushed to main
- [git commit+push: 反射链 Full Audit B 级 + recovery 数据补录](task_git_commit+push:_反射链_full_audit_b_级_+_recovery_数据补录.md) — Staged and committed 3 files (daily journal 03-15, 03-16, changelog 03-15), pushed to main as 2b4bee6
- [git commit+push 日报changelog](task_git_commit+push_日报changelog.md) — Staged 2 files (日报+changelog), committed and pushed to main
- [git commit 反射系统失败处理+竞争假设](task_git_commit_反射系统失败处理+竞争假设.md) — 4个目标文件不在任何git仓库中，无法完成git commit
- [hook修复6个审计问题](task_hook修复6个审计问题.md) — 修复post-agent-trigger-stats.py：文件锁、CB状态重置、24h超时、词边界匹配、超时保护、fumio分类
- [Implement retrieval usage feedback loop in agent-memory](task_implement_retrieval_usage_feedback_loop_in_agent-memory.md) — Added retrieval_count, last_retrieved, usefulness_score fields to Memory dataclass; auto-tracking on retrieve; CLI feedback --useful/--not-useful; stale detection; importance score integration
- [IPFlow 改为工作经历并更新时间](task_ipflow_改为工作经历并更新时间.md) — 将 IPFlow 从项目经历移至新的工作经历章节，时间从 2025.11 改为 2025.06
- [P0-2 + P0-3 git commit](task_p0-2_+_p0-3_git_commit.md) — Committed P0-2 记忆分层 and P0-3 检索反馈闭环 to agent-memory repo (96b0654)
- [P7 record-recovery CLI 子命令](task_p7_record-recovery_cli_子命令.md) — 在 post-agent-trigger-stats.py 中添加 record-recovery CLI 子命令，支持 root 在 Recovery Ladder 执行后更新 replacement_agent
- [Register CB intercept hook in settings.json](task_register_cb_intercept_hook_in_settings.json.md) — Added pre-agent-cb-check.py as PreToolUse hook for Agent matcher, updated hooks.md docs
- [Round 2 hook 修复: 冗余清理 + 超时 flush](task_round_2_hook_修复:_冗余清理_+_超时_flush.md) — 修复 post-agent-trigger-stats.py 冗余 ensure_parallel_batches 调用 + pre-agent-cb-check.py 超时 flush
- [优化中文简历 Resume_Web3_Fullstack_ZH](task_优化中文简历_resume_web3_fullstack_zh.md) — 按 Web3 简历最佳实践优化中文简历：重排章节、分层技术栈、增加链上指标、修复截断
- [修复 post-memory-consolidate-hook.py 审计问题](task_修复_post-memory-consolidate-hook.py_审计问题.md) — 修复 miru 审计发现的 3 个代码问题：添加 miru 到 AGENT_STORE_MAP、修正 run_consolidate 返回值、修正 docstring
- [修复记忆系统4个基础设施bug](task_修复记忆系统4个基础设施bug.md) — 修复 YAML frontmatter、hook 路径、index-meta.json、tokenize trigram 四个 bug，全部 613 测试通过
- [创建 reflex-fuzz skill](task_创建_reflex-fuzz_skill.md) — 创建反射系统 Fuzz 测试 skill，包含 skill.md、explore.sh、report.py 三个文件
- [创建 trigger-stats 写入 hook](task_创建_trigger-stats_写入_hook.md) — 创建 post-agent-trigger-stats.py hook，Agent 完成后自动更新反射统计
- [创建入门级 Web3 简历并编译 PDF](task_创建入门级_web3_简历并编译_pdf.md) — 将英文入门级 Web3 开发者简历翻译为中文并保存为 Markdown，使用 pandoc+xelatex 编译为 PDF（41K）
- [创建轻量级 workflow run 模板](task_创建轻量级_workflow_run_模板.md) — 为 overnight/batch 类任务创建兼容 collect.py 的模板
- [合并 IPFlow 三项工作经历](task_合并_ipflow_三项工作经历.md) — 将简历中抽奖协议、DeFi 交易基础设施、链上数据与 NFT 工具链合并为一个 IPFlow 项目
- [同步 rules/trigger-map.md 与 SSOT](task_同步_rules_trigger-map.md_与_ssot.md) — 将 SSOT trigger-map.md 完整同步到 rules/ 自动加载副本
- [实现 4 层记忆架构 L0-L3](task_实现_4_层记忆架构_l0-l3.md) — 在 agent-memory 系统中实现 L0-L3 四层记忆层级
- [实现 parallel_batches 并行批次追踪](task_实现_parallel_batches_并行批次追踪.md) — 在 trigger-stats.json 和 post-agent-trigger-stats.py 中实现并行批次追踪，解决 E3 Fuzz 发现的两个 MEDIUM 问题
- [对抗性协议 git commit+push](task_对抗性协议_git_commit+push.md) — 提交反射系统对抗性协议日报+changelog到远程
- [推送 ~/mem/mem/ 到 GitHub subagent-memory 仓库](task_推送_~_mem_mem__到_github_subagent-memory_仓库.md) — 初始化 git repo、解决 .gitignore 冲突、rebase 后成功推送 308 文件到 GitHub
- [添加记忆保存验证到 post-memory-consolidate-hook](task_添加记忆保存验证到_post-memory-consolidate-hook.md) — 在现有 hook 中新增 check_recent_memory 函数，Agent 完成后检查 5 分钟内是否有记忆文件变更，无则 stderr 警告
- [清理 trigger-stats 旧 test 条目](task_清理_trigger-stats_旧_test_条目.md) — 删除 test-rule/test_rule/fail_rule/skip_rule 4 个旧条目
- [终端反射修复提交检查](task_终端反射修复提交检查.md) — 检查 Obsidian 库是否有终端反射修复相关变更，确认修改在 ~/.claude/ 下不受库 git 管理，跳过提交
- [补全 trigger-stats.json CB 字段](task_补全_trigger-stats.json_cb_字段.md) — 为所有反射条目补全 Circuit Breaker 状态字段
- [补建 workflow run 文件](task_补建_workflow_run_文件.md) — 为简历编辑会话补建 workflow run 记录
- [迁移 trigger-map 到 rules/](task_迁移_trigger-map_到_rules_.md) — 将 trigger-map 从 CLAUDE.md 内联迁移为独立 rules 文件 ~/.claude/rules/trigger-map.md
