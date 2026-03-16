# Memory Index

## Task
- [Fix7: recovery_level 字段扩展](task_fix7:_recovery_level_字段扩展.md) — 扩展 trigger-stats.json 支持 Recovery Ladder L1-L4 追踪
- [Fuzz F3: 实现失败直接 L2 Re-spawn](task_fuzz_f3:_实现失败直接_l2_re-spawn.md) — 测试实现反射失败后跳过L1直接L2的规则，发现trigger-stats.json缺少recovery_level等字段
- [Fuzz H4 — 吞食反射路径分析](task_fuzz_h4_—_吞食反射路径分析.md) — 分析 devour 反射从未触发的根因：设计缺陷（转移规则中无入站边）
