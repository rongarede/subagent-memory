# Memory Index

## User
- [用户称呼偏好](user_name_b1.md) — 用户要求 root 称呼其为 b1

## Feedback
- [错误的 agent 任务分配](.md) — root 将角色定义任务错误分配给 tetsu 而非 norna
- [agent 配置文件修改归属 yume](feedback_agent_配置文件修改归属_yume.md) — ~/mem/mem/agents/ 下的 role.md、trigger-map.md、WhoAmI.md 等 agent 配置文件的增删改归 yume 管辖，不是 tetsu
- [用户建议必须自动记录](feedback_auto_record_suggestions.md) — 用户提出建议或纠正时，root 必须立即记录到 CLAUDE.md 和 feedback
- [root 应自主决策明显修复](feedback_autonomous_decisions.md) — 审计发现的 P2/P3 修复、用户已确认方向的执行，root 不需要再次询问确认
- [b1 鼓励持续执行](feedback_b1_鼓励持续执行.md) — b1 表示期待 root 持续工作，肯定了自主推进模式
- [b1要求记录决策链](feedback_b1要求记录决策链.md) — b1 要求每次任务都记录决策链过程到 workflows/runs/
- [Codex CLI 已移除](feedback_codex_removed.md) — b1 订阅 Max 计划，Codex CLI 已从工作流中移除，所有任务统一用 Agent tool + sonnet
- [严重错误：subagent 从未保存任务记忆](feedback_critical_memory_save.md) — 10+ 次 subagent 调用零条记忆保存，系统性遗漏，b1 指出为严重错误
- [root 需自主分析决策影响程度](feedback_decision_analysis.md) — root 应对每个决策分析重要程度和影响程度，低影响直接决定，高影响才请示 b1
- [feedback: reflex-audit 报告后不要问是否继续](feedback_feedback:_reflex-audit_报告后不要问是否继续.md) — 审计报告输出后应直接推进 Phase 5 修复，不要问要不要继续
- [feedback: research before proposing](feedback_feedback:_research_before_proposing.md) — b1 纠正：讨论方案时不要凭直觉直接给答案，应先做 research 调研已有方法论，再基于调研结果提出建议
- [feedback: skill 创建后必须触发测试](feedback_feedback:_skill_创建后必须触发测试.md) — 创建 reflex-fuzz skill 后未立即测试被纠正
- [feedback: 创建 skill 应使用 /skill-create](feedback_feedback:_创建_skill_应使用__skill-create.md) — b1 指出创建 skill 时应先检查 /skill-create（everything-claude-code:skill-create），而非直接派 raiga 手工创建
- [feedback: 对抗性机制+miru 验证成功](feedback_feedback:_对抗性机制+miru_验证成功.md) — b1 对 miru 对抗循环和反射系统 fuzz 测试表示认可
- [feedback: 建议即执行，不等确认](feedback_feedback:_建议即执行，不等确认.md) — b1 要求：root 一旦有了建议就立即执行，不要问要不要我推进
- [feedback: 新机制需调研外部实现](feedback_feedback:_新机制需调研外部实现.md) — 对抗性机制设计时未主动检索外部 skill 被纠正
- [feedback: 每轮必须走完整反射链](feedback_feedback:_每轮必须走完整反射链.md) — Round 2/3 跳过完整流程被纠正两次
- [feedback: 禁止询问策略确认](feedback_feedback:_禁止询问策略确认.md) — root 在 Round 1 询问'你觉得这个策略OK吗'被纠正
- [feedback: 默认选最快方案](feedback_feedback:_默认选最快方案.md) — cron 参数从 30min→45min→5min 被纠正两次
- [大型项目必须并发探索](feedback_parallel_exploration.md) — 面对大型仓库/项目时，root 必须并发启动多个 kaze/mirin
- [root 必须主动保存记忆](feedback_root_must_save_memory.md) — 每次会话中做出重要决策或收到 b1 反馈后，root 必须保存记忆到 ~/mem/mem/root/
- [root 违规：主会话直接使用 Read/Bash](feedback_root_违规：主会话直接使用_read_bash.md) — root 在主会话直接调用 Read 和 Bash 工具，违反协调器约束
- [subagent_type 必须显式指定](feedback_subagent_type_必须显式指定.md) — 每次 Agent 调用必须显式写 subagent_type，不得依赖默认值。即使默认值碰巧正确也不行。
- [subagent 需要各自的 trigger-map](feedback_subagent_需要各自的_trigger-map.md) — b1 要求每个 subagent 也有 trigger-map，用于触发 skill 工作流
- [修复后必须测试](feedback_test_after_fix.md) — 所有修复执行完成后必须运行一轮测试验证，不能跳过
- [每轮 task 完成后必须更新项目主页](feedback_update_project_page.md) — TaskUpdate status=completed 后，root 必须检查并更新对应的 Obsidian 项目主页迭代日志
- [root 必须验证 subagent 输出质量](feedback_verify_subagent_output.md) — subagent 完成任务后 root 必须检查实际结果（如 git log），不能只看自报摘要
- [错误的 agent 任务分配](feedback_wrong_agent_assignment.md) — root 将角色定义任务错误分配给 tetsu 而非 norna
- [记忆系统归 yume 管理](feedback_yume_owns_memory.md) — 所有 ~/mem/mem 下的记忆操作（目录重构、索引、迁移）应委派 yume，不要交给 kaze 或其他角色
- [决策链用 MD 不用 JSON](feedback_决策链用_md_不用_json.md) — b1 要求决策链记录使用 Markdown 格式而非 JSON
- [反馈-审计结果必须立即修正](feedback_反馈-审计结果必须立即修正.md) — b1 纠正：收到 miru 审计报告后必须立即执行修正行动，口头认领不等于修正
- [反馈：root 知道答案时禁止询问](feedback_反馈：root_知道答案时禁止询问.md) — 用户多次指出 root 在已有明确判断时仍然询问确认，属于回避责任
- [反馈：任务完成必须触发完成反射](feedback_反馈：任务完成必须触发完成反射.md) — root 完成任务后未自动触发日记+记忆的完成反射，被 b1 纠正
- [反馈：执行优先，不怕犯错，错了回滚](feedback_反馈：执行优先，不怕犯错，错了回滚.md) — 用户明确表态：只想看结果，哪怕错了也没关系，可以回滚
- [反馈：更新 CLAUDE.md 必须用 /claude-md-improver](feedback_反馈：更新_claude.md_必须用__claude-md-improver.md) — 用户指示更新 CLAUDE.md 必须通过 claude-md-improver skill，不能直接编辑
- [所有改动必须实战验证](feedback_所有改动必须实战验证.md) — 任何改动（规则、配置、skill注册等）必须经过实战验证（非静态检查）通过后才可声明完成。静态验证（文件存在性检查）不够，必须有实际调用/执行的端到端验证。
- [用户反馈必须由 yume 记录](feedback_用户反馈必须由_yume_记录.md) — b1 要求：每次纠正或鼓励都必须由 yume 记录为 feedback 记忆
- [纠正：不要忽略全局任务面板](feedback_纠正：不要忽略全局任务面板.md) — b1 纠正 root 忽略了全局任务面板，所有进行中和待办工作必须有 Task 条目
- [脑暴是内部思考不是外部提问](feedback_脑暴是内部思考不是外部提问.md) — b1 反馈：自行判断时仍需脑暴，脑暴是内部思考过程不是对话形式
- [记忆系统变更必须同步项目主页](feedback_记忆系统变更必须同步项目主页.md) — b1 要求：每次对记忆系统的更改都要记录到 Obsidian 项目主页，由 fumio 执行
- [鼓励：决策链工作流获得肯定](feedback_鼓励：决策链工作流获得肯定.md) — b1 说'你很棒，这就是我希望看到的你做的决定'——指 root 自主完成调研→决策→实现的全链路

## Task
- [ARIS 项目探索决策](task_aris_项目探索决策.md) — 探索 Auto-claude-code-research-in-sleep (ARIS) 项目后的决策：参考借鉴不直接引入
- [E2E 测试反射系统 — 4个场景全部通过](task_e2e_测试反射系统_—_4个场景全部通过.md) — 反射系统端到端测试：修复路径、探索异常、审计失败循环、纯文档路径全部验证通过
- [Fuzz Round 4: P4 终端反射动态化](task_fuzz_round_4:_p4_终端反射动态化.md) — 终端反射列表从 pre-agent-cb-check.py 硬编码改为 trigger-stats.json metadata 动态读取
- [Fuzz Round 5: P7 recovery agent 追踪](task_fuzz_round_5:_p7_recovery_agent_追踪.md) — 新增 record-recovery CLI 命令，支持 L2 Re-spawn 后记录替代角色
- [Fuzz Round 6: P8 共享配置](task_fuzz_round_6:_p8_共享配置.md) — 提取 AGENT_REFLECTION_MAP + KEYWORD_OVERRIDES 为 reflex-config.json
- [Fuzz Round 7: P5/P9 并行派发文档](task_fuzz_round_7:_p5_p9_并行派发文档.md) — trigger-map 新增并行派发协议章节，shin 审计零问题
- [Fuzz Round 8: P10 终端反射统一](task_fuzz_round_8:_p10_终端反射统一.md) — terminal_reflections 从 trigger-stats metadata 迁移到 reflex-config.json
- [Fuzz Round 9: W1 merge + P11 截断日志](task_fuzz_round_9:_w1_merge_+_p11_截断日志.md) — config merge 防 partial 丢失 + recovery 截断 stderr 警告
- [hook E2E测试通过+6项修复](task_hook_e2e测试通过+6项修复.md) — post-agent-trigger-stats.py E2E测试全部通过，修复6个审计问题（fcntl锁、CB状态重置、24h超时、regex词边界、signal超时、fumio分类）
- [miru 对抗循环：R2/R3 补建](task_miru_对抗循环：r2_r3_补建.md) — miru 审计驱动的递归合规修正：补建违规记录时也要遵守反射链
- [Phase D 完成：5 场景端到端测试](task_phase_d_完成：5_场景端到端测试.md) — 12 个 e2e 测试全部通过，234 tests 全绿
- [reflex-audit首次审计：D级48分](task_reflex-audit首次审计：d级48分.md) — 反射系统首次Full Audit评分48/100(D级)，核心问题是trigger-stats.json未与Agent执行绑定，已通过post-agent-trigger-stats.py hook修复
- [session: 2026-03-16 反射系统强化 + miru 创建](task_session:_2026-03-16_反射系统强化_+_miru_创建.md) — 10 轮 fuzz 修复 14 问题 + 对抗性协议 + miru 监者角色 + subagent-memory 仓库
- [Task10-个人摘要改写为叙述风格](task_task10-个人摘要改写为叙述风格.md) — 将简历个人摘要从 bullet 列表改为流畅段落叙述
- [Task12-精简个人摘要突出三线](task_task12-精简个人摘要突出三线.md) — 将个人摘要从 107 字压缩至 71 字，突出工作/AI/科研三方面
- [Task14-工作经历移至个人摘要前](task_task14-工作经历移至个人摘要前.md) — 调整简历章节顺序：工作经历移到个人摘要之前
- [trigger-map 重构为原子反射模型](task_trigger-map_重构为原子反射模型.md) — 将 trigger-map 从固定链路重构为原子反射+转移规则的响应式模型
- [反射系统失败处理+竞争假设形式化](task_反射系统失败处理+竞争假设形式化.md) — trigger-map.md补全Recovery Ladder(L1-L4)、Circuit Breaker、Accounting Rule和竞争假设协议(L3调研)
- [反射系统补全：失败处理形式化 + 竞争假设](task_反射系统补全：失败处理形式化_+_竞争假设.md) — trigger-map 新增 Recovery Ladder (L1-L4)、Circuit Breaker、Accounting Rule、竞争假设协议 (L3)
- [反射链 Full Audit 2026-03-16: B 级](task_反射链_full_audit_2026-03-16:_b_级.md) — 审计评分 B(77.5/100)，从 D(48) 提升 29.5 分。14 个问题已修复，recovery 数据补录完成
- [反射链 Full Audit 首次 loop 执行](task_反射链_full_audit_首次_loop_执行.md) — 审计评分 D (56/100)，修复 3 项一致性问题，发现 skill 自身缺少完成反射
- [记忆系统现状评估完成](task_记忆系统现状评估完成.md) — 三维度评估：15脚本/577测试/325+记忆文件，8/12改进已实现，4项未完成（跨系统桥接/RL闭环/语义检索/Letta分层）

## Project
- [Agent 生命周期规则](project_agent_lifecycle.md) — b1 创建的原始 agent 不朽，母体创建的 agent 可因反馈过差被消亡，消亡时吞食者吞食其全部信息
- [yume 记忆反馈改进方案决策](project_yume_记忆反馈改进方案决策.md) — 综合 kaze 探索 + yomi 调研，决定 3 阶段改进方案
- [记忆系统路径 bug 已修复](project_记忆系统路径_bug_已修复.md) — --store 参数被 --agent 静默覆盖的 bug，TDD 验证并修复
