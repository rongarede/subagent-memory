#!/usr/bin/env python3
# ============================================================
# pre-agent-cb-check: PreToolUse / Agent hook
# Agent 调用前检查对应反射的 Circuit Breaker 状态
#
# 触发条件：tool_name == "Agent"
# 超时保护：整体执行 < 4 秒
# 安全：所有异常静默处理（输出 allow）
# ============================================================

import json
import os
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 配置 ====================

STATS_PATH = Path(os.path.expanduser("~/mem/mem/workflows/trigger-stats.json"))
REFLEX_CONFIG_PATH = Path(os.path.expanduser("~/.claude/hooks/reflex-config.json"))

# 内联默认值（reflex-config.json 读取失败时的 fallback）
_DEFAULT_AGENT_REFLECTION_MAP = {
    "kaze":  "explore",
    "yomi":  "research",
    "tetsu": "implement",
    "fumio": "document",
    "shin":  "audit",
    "haku":  "verify",
    "raiga": "devour",
    "norna": "define",
    "yume":  "memory",
}

_DEFAULT_KEYWORD_OVERRIDES = {
    "commit": "commit",
    "提交": "commit",
    "git commit": "commit",
    "日记": "journal",
    "journal": "journal",
    "daily": "journal",
    "日报": "journal",
}


def _load_reflex_config():
    """从 reflex-config.json 加载共享配置，失败时返回内联默认值"""
    try:
        with open(REFLEX_CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        agent_map = {**_DEFAULT_AGENT_REFLECTION_MAP, **cfg.get("agent_reflection_map", {})}
        keyword_overrides = {**_DEFAULT_KEYWORD_OVERRIDES, **cfg.get("keyword_overrides", {})}
        return agent_map, keyword_overrides
    except (json.JSONDecodeError, IOError, TypeError):
        return _DEFAULT_AGENT_REFLECTION_MAP, _DEFAULT_KEYWORD_OVERRIDES


AGENT_REFLECTION_MAP, KEYWORD_OVERRIDES = _load_reflex_config()

# 终端反射：CB OPEN 时自动 SKIP（拦截）
# 从 reflex-config.json 的 terminal_reflections 字段读取
# 读取失败时回退到默认值
DEFAULT_TERMINAL_REFLECTIONS = {"journal", "memory"}


def _load_terminal_reflections():
    """从 reflex-config.json 读取终端反射列表"""
    try:
        with open(REFLEX_CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        terminals = cfg.get("terminal_reflections")
        if isinstance(terminals, list) and len(terminals) > 0:
            return set(terminals)
    except (json.JSONDecodeError, IOError, TypeError):
        sys.stderr.write("[pre-agent-cb-check] WARNING: failed to read terminal_reflections from reflex-config.json, using defaults\n")
    return DEFAULT_TERMINAL_REFLECTIONS


# 关键反射：CB OPEN 时警告但允许执行（建议 L4 Escalate）
# 所有非终端反射都是关键反射


# ==================== 超时保护 ====================

def _timeout_handler(signum, frame):
    # 超时时默认 allow
    output_allow()
    sys.stdout.flush()
    sys.exit(0)


# ==================== 输出函数 ====================

def output_allow(message=None):
    """输出 allow 决策"""
    result = {"decision": "allow"}
    if message:
        result["message"] = message
    print(json.dumps(result))


def output_block(message):
    """输出 block 决策"""
    print(json.dumps({"decision": "block", "message": message}))


# ==================== 辅助函数 ====================

def extract_agent_name(description):
    """从 '角色名 | 任务描述' 格式提取 agent 名"""
    if not description or "|" not in description:
        return None, None
    parts = description.split("|", 1)
    agent = parts[0].strip().lower()
    task_desc = parts[1].strip().lower() if len(parts) > 1 else ""
    return agent, task_desc


def resolve_reflection(agent_name, task_desc):
    """根据 agent 名和任务描述确定反射类型"""
    # 先检查关键词覆盖
    for keyword, reflection in KEYWORD_OVERRIDES.items():
        if keyword in task_desc:
            return reflection

    # 使用默认映射
    return AGENT_REFLECTION_MAP.get(agent_name)


def maybe_recover_open(entry):
    """OPEN 超 24h 自动转 HALF-OPEN（只读检查，不修改文件）"""
    if entry.get("cb_state") != "OPEN":
        return entry.get("cb_state", "CLOSED")
    opened_at = entry.get("cb_opened_at")
    if not opened_at:
        return "OPEN"
    try:
        opened_dt = datetime.fromisoformat(opened_at)
        if datetime.now() - opened_dt >= timedelta(hours=24):
            return "HALF-OPEN"
    except (ValueError, TypeError):
        pass
    return "OPEN"


def check_cb_state(reflection):
    """检查指定反射的 CB 状态，返回 (effective_state, entry_or_none)"""
    if not STATS_PATH.exists():
        return "CLOSED", None

    try:
        with open(STATS_PATH, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return "CLOSED", None

    rules = data.get("rules", {})
    entry = rules.get(reflection)
    if not entry:
        return "CLOSED", None

    # 检查 OPEN 是否已过 24h（只读，不修改文件；写入端 post hook 会处理状态转移）
    effective_state = maybe_recover_open(entry)
    return effective_state, entry


# ==================== 主函数 ====================

def main():
    # 设置超时保护
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(4)

    try:
        raw = sys.stdin.read()
        if not raw.strip():
            signal.alarm(0)
            sys.exit(0)
        input_data = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        # 解析失败，默认 allow
        signal.alarm(0)
        output_allow()
        sys.exit(0)

    # 仅处理 Agent 事件
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Agent":
        signal.alarm(0)
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    if not isinstance(tool_input, dict):
        signal.alarm(0)
        sys.exit(0)

    # 提取 agent 名和任务描述
    description = tool_input.get("description", "") or ""
    agent_name, task_desc = extract_agent_name(description)

    if not agent_name:
        # 无法识别 agent，默认 allow
        signal.alarm(0)
        sys.exit(0)

    # 确定反射类型
    reflection = resolve_reflection(agent_name, task_desc or "")
    if not reflection:
        # 未知反射，默认 allow
        signal.alarm(0)
        sys.exit(0)

    # 检查 CB 状态
    cb_state, entry = check_cb_state(reflection)

    if cb_state == "CLOSED":
        # 正常，无输出
        signal.alarm(0)
        sys.exit(0)

    elif cb_state == "HALF-OPEN":
        # 警告但允许执行
        signal.alarm(0)
        output_allow(
            f"CB HALF-OPEN: 反射 {reflection} 正在恢复中，允许执行（需连续 2 次成功恢复 CLOSED）"
        )
        sys.exit(0)

    elif cb_state == "OPEN":
        if reflection in _load_terminal_reflections():
            # 终端反射：拦截
            signal.alarm(0)
            output_block(
                f"CB OPEN: 终端反射 {reflection} 已熔断，自动 SKIP。"
                f"（连续失败 {entry.get('cb_consecutive_failures', '?')} 次，"
                f"熔断于 {entry.get('cb_opened_at', '未知')}）"
            )
            sys.exit(0)
        else:
            # 关键反射：警告但允许
            signal.alarm(0)
            output_allow(
                f"CB OPEN: 关键反射 {reflection} 已熔断，建议 L4 Escalate 上报 b1。"
                f"（连续失败 {entry.get('cb_consecutive_failures', '?')} 次，"
                f"熔断于 {entry.get('cb_opened_at', '未知')}）"
            )
            sys.exit(0)

    # 未知状态，默认 allow
    signal.alarm(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
