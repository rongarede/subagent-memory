---
name: archive_summary
description: 历史任务记忆蒸馏摘要（shin）
type: archive
created: 2026-03-15
source_count: 14
---

## 关键经验教训

### 审计流程
- 审计结论必须独立核实，不能依赖 subagent 自报结果；所有测试数必须亲自运行确认
- 发现 CRITICAL/HIGH 问题时立即上报并阻塞 commit；MEDIUM 问题建议修复后再发布；LOW 问题可记录后续跟进
- 审计范围需覆盖：源文件、对应测试文件、CLI 注册完整性、SKILL.md 文档一致性
- 审计报告须包含：问题严重级、具体行号/文件、复现路径

### 代码质量模式
- 常见 LOW 问题：直接 mutation dataclass 字段（应用 `dataclasses.replace()`）、函数超过 50 行
- 常见 MEDIUM 问题：缺少 `sys.path.insert(0, ...)` 导致跨目录运行 ImportError、TOCTOU 竞态（双重读取无锁）、权重变更不持久化
- `_apply_warning` 用 f-string 拼接 YAML frontmatter 时，含冒号的 pattern 名会生成 invalid YAML（安全问题）
- `Path.glob()` 直接接受用户输入 pattern 参数会触发意外文件匹配（安全问题）
- hook 脚本中 `Popen` 调用必须传 `env=os.environ.copy()` 确保子进程继承 API key

### CLAUDE.md 审计经验
- 项目级 CLAUDE.md 首次审计通常在 68-72/100（C 级），修复后可达 76-86/100
- 常见问题：中英文路径混用（中文目录名用英文占位符）、emoji 违反 no-emoji 规则、SSOT 矛盾（post-commit-journal hook 往 Daily 追加 commit 记录，但 SSOT 表禁止写入 Daily）
- 决策链执行记录机制使用率偏低（只有 1 条 workflow run），需加强 enforcement

## 常见任务模式

| 模式 | 频率 | 产出 |
|------|------|------|
| agent-memory 各 Phase 代码审计 | 极高（R2~R6，Phase A~E） | 测试数、问题列表（分级） |
| CLAUDE.md 质量审计 | 中等 | 评分/100、残留问题清单 |
| hook 修复质量验证 | 低 | PASS/FAIL + WARNING 列表 |
| 记忆保存机制验证 | 低 | 多维度检查清单 |

## 重要发现

- agent-memory 整体代码质量良好：234→247→339→491→577 测试递增，均 100% 通过
- distiller.py 评分 82/100（B 级）：collect_candidates or-chain 可能传 None（HIGH）；cluster_memories O(n²·k）（MEDIUM）；execute_output 无路径穿越检查（MEDIUM）
- SKILL.md 覆盖率历史低至 57%，后修复到基本完整（R6-A 审计发现 7 项遗漏）
- feedback_loop.py 全程用 `dataclasses.replace()`，是不可变模式的正确示范
- journal-summarizer 锁机制存在 TOCTOU 理论缺陷（应改用 `fcntl.flock`），已记录但尚未修复
