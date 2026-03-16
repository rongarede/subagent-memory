#!/usr/bin/env python3
# ============================================================
# post-agent-trigger-stats: PostToolUse / Agent hook
# Agent 完成后更新 trigger-stats.json 统计计数
#
# 触发条件：tool_name == "Agent"
# 超时保护：整体执行 < 4 秒
# 安全：所有异常静默处理（exit 0）
# ============================================================

import fcntl
import json
import os
import re
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

# Fix 7: Recovery Ladder — 每个反射首次失败的预期恢复级别
# 实现反射失败跳过 L1 直接 L2（方案问题非执行问题），其他默认 L1
REFLEX_RECOVERY_RULES = {
    "implement": "L2",  # 跳过 L1，直接 Re-spawn
    # 其他反射默认 L1 Resume
}

# Recovery level → action 名映射
LEVEL_ACTION = {"L1": "resume", "L2": "re-spawn", "L3": "re-assign", "L4": "escalate"}

# recovery_history 最大保留条数
MAX_RECOVERY_HISTORY = 20

# parallel_batches history 最大保留条数
MAX_BATCH_HISTORY = 10

# 批次默认超时（分钟）
DEFAULT_BATCH_TIMEOUT_MINUTES = 10

# Fix 4: 词边界 regex 模式，替代简单 substring 匹配
FAIL_PATTERNS = [
    re.compile(r'\b(failed|failure|exception|traceback)\b', re.IGNORECASE),
    re.compile(r'(失败|报错)'),
]
SKIP_PATTERNS = [
    re.compile(r'\b(skipped?|n/a)\b', re.IGNORECASE),
    re.compile(r'(跳过|不适用)'),
]


# ==================== 超时保护 ====================

# Fix 5: signal.alarm(4) 整体超时保护
def _timeout_handler(signum, frame):
    sys.exit(0)


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


def determine_outcome(tool_result):
    """从 tool_result 判断执行结果：success / failure / skip"""
    if not tool_result:
        return "success"  # 无结果信息，默认成功

    result_str = str(tool_result)

    # Fix 4: 词边界 regex 匹配，避免 "no error"、"error-free" 误判
    for pattern in FAIL_PATTERNS:
        if pattern.search(result_str):
            return "failure"

    for pattern in SKIP_PATTERNS:
        if pattern.search(result_str):
            return "skip"

    return "success"


def maybe_recover_open(entry):
    """Fix 3: OPEN 超 24h 自动转 HALF-OPEN"""
    if entry.get("cb_state") != "OPEN":
        return
    opened_at = entry.get("cb_opened_at")
    if not opened_at:
        return
    try:
        opened_dt = datetime.fromisoformat(opened_at)
        if datetime.now() - opened_dt >= timedelta(hours=24):
            entry["cb_state"] = "HALF-OPEN"
            entry["cb_consecutive_failures"] = 0
            entry["cb_half_open_successes"] = 0
    except (ValueError, TypeError):
        pass


def get_expected_recovery_level(reflex_name):
    """返回该反射首次失败的预期恢复级别"""
    return REFLEX_RECOVERY_RULES.get(reflex_name, "L1")


def ensure_recovery_fields(entry):
    """确保 entry 具有 recovery 相关字段（向后兼容）"""
    if "recovery_history" not in entry:
        entry["recovery_history"] = []
    if "last_recovery_level" not in entry:
        entry["last_recovery_level"] = None
    if "l1_skip_count" not in entry:
        entry["l1_skip_count"] = 0


def record_recovery_on_failure(entry, reflex_name, agent_name):
    """失败时追加一条 pending recovery 记录"""
    expected_level = get_expected_recovery_level(reflex_name)
    recovery_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": expected_level,
        "action": "pending",
        "original_agent": agent_name,
        "replacement_agent": None,
        "reason": f"{reflex_name} 失败，预期恢复级别 {expected_level}"
            + (" （跳过L1，方案问题非执行问题）" if expected_level != "L1" else ""),
        "outcome": "pending"
    }
    entry["recovery_history"].append(recovery_entry)
    entry["last_recovery_level"] = expected_level

    # 如果是跳过 L1 的反射，增加 l1_skip_count
    if expected_level != "L1":
        entry["l1_skip_count"] = entry.get("l1_skip_count", 0) + 1

    # 保持 recovery_history 不超过上限
    if len(entry["recovery_history"]) > MAX_RECOVERY_HISTORY:
        dropped = len(entry["recovery_history"]) - MAX_RECOVERY_HISTORY
        sys.stderr.write(f"[trigger-stats] recovery_history truncated: dropped {dropped} oldest entries for {reflex_name}\n")
        entry["recovery_history"] = entry["recovery_history"][-MAX_RECOVERY_HISTORY:]


def resolve_pending_recovery(entry, outcome):
    """成功/跳过时，将最近的 pending recovery 标记为已解决"""
    for rec in reversed(entry.get("recovery_history", [])):
        if rec.get("outcome") == "pending":
            rec["outcome"] = outcome  # "success" 或 "skip"
            break  # 只解决最近一条 pending


def now_iso():
    """返回当前时间的 ISO 格式字符串"""
    return datetime.now().isoformat()


def ensure_parallel_batches(data):
    """确保 data 具有 parallel_batches 字段（向后兼容）"""
    if "parallel_batches" not in data:
        data["parallel_batches"] = {"active": None, "history": []}
    pb = data["parallel_batches"]
    if "active" not in pb:
        pb["active"] = None
    if "history" not in pb:
        pb["history"] = []


def start_batch(stats, batch_id, reflexes, timeout_minutes=None):
    """开始一个并行批次（由 root 在派发并行 agent 前调用）

    Args:
        stats: trigger-stats.json 的完整数据
        batch_id: 批次标识（如 "phase3-implement-document"）
        reflexes: 反射名列表（如 ["implement", "document"]）
        timeout_minutes: 超时分钟数，默认 DEFAULT_BATCH_TIMEOUT_MINUTES
    """
    ensure_parallel_batches(stats)
    if timeout_minutes is None:
        timeout_minutes = DEFAULT_BATCH_TIMEOUT_MINUTES
    stats["parallel_batches"]["active"] = {
        "id": batch_id,
        "reflexes": {r: "PENDING" for r in reflexes},
        "started_at": now_iso(),
        "timeout_minutes": timeout_minutes,
    }


def update_batch_reflex(stats, reflex_name, result):
    """Agent 完成时自动更新批次状态

    Args:
        stats: trigger-stats.json 的完整数据
        reflex_name: 完成的反射名（如 "implement"）
        result: 执行结果（SUCCESS/FAILURE/SKIP）

    Returns:
        dict or None: 如果批次已全部完成，返回完成的批次记录；否则返回 None
    """
    ensure_parallel_batches(stats)
    batch = stats["parallel_batches"]["active"]
    if not batch:
        return None

    # 仅更新属于此批次的反射
    if reflex_name not in batch["reflexes"]:
        return None

    batch["reflexes"][reflex_name] = result.upper()

    # 检查是否全部完成（无 PENDING）
    all_done = all(v != "PENDING" for v in batch["reflexes"].values())
    if not all_done:
        return None

    # 批次完成：归档到 history
    batch["completed_at"] = now_iso()

    # MISSING 检测（理论上此处不应有 PENDING，但做防御性检查）
    missing = [r for r, v in batch["reflexes"].items() if v == "PENDING"]
    if missing:
        batch["missing_detected"] = missing

    stats["parallel_batches"]["history"].append(batch)
    stats["parallel_batches"]["active"] = None

    # 保持 history 不超过上限
    if len(stats["parallel_batches"]["history"]) > MAX_BATCH_HISTORY:
        stats["parallel_batches"]["history"] = stats["parallel_batches"]["history"][-MAX_BATCH_HISTORY:]

    return batch


def check_batch_timeout(stats):
    """检查活跃批次是否超时，超时则将 PENDING 标记为 MISSING 并归档

    Returns:
        dict or None: 如果发现超时批次，返回该批次记录（含 missing_detected）；否则返回 None
    """
    ensure_parallel_batches(stats)
    batch = stats["parallel_batches"]["active"]
    if not batch:
        return None

    started_at = batch.get("started_at")
    timeout_minutes = batch.get("timeout_minutes", DEFAULT_BATCH_TIMEOUT_MINUTES)
    if not started_at:
        return None

    try:
        started_dt = datetime.fromisoformat(started_at)
    except (ValueError, TypeError):
        return None

    if datetime.now() - started_dt < timedelta(minutes=timeout_minutes):
        return None

    # 超时：将所有 PENDING 标记为 MISSING
    missing = [r for r, v in batch["reflexes"].items() if v == "PENDING"]
    if missing:
        for r in missing:
            batch["reflexes"][r] = "MISSING"
        batch["missing_detected"] = missing

    batch["completed_at"] = now_iso()
    batch["timed_out"] = True

    stats["parallel_batches"]["history"].append(batch)
    stats["parallel_batches"]["active"] = None

    # 保持 history 不超过上限
    if len(stats["parallel_batches"]["history"]) > MAX_BATCH_HISTORY:
        stats["parallel_batches"]["history"] = stats["parallel_batches"]["history"][-MAX_BATCH_HISTORY:]

    return batch


def update_stats(reflection, outcome, agent_name=None):
    """更新 trigger-stats.json"""
    if not STATS_PATH.exists():
        return

    try:
        # Fix 1: fcntl 排他锁防止竞态条件
        with open(STATS_PATH, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.load(f)

                rules = data.get("rules", {})

                if reflection not in rules:
                    # 反射不在统计中，跳过
                    return

                entry = rules[reflection]

                # Fix 7: 确保 recovery 字段存在（向后兼容旧数据）
                ensure_recovery_fields(entry)

                # Fix 3: 检查 OPEN 是否超过 24h，若是则自动转 HALF-OPEN
                maybe_recover_open(entry)

                # 更新计数
                if outcome == "success":
                    entry["success"] = entry.get("success", 0) + 1
                    # CB: 成功时重置连续失败计数
                    entry["cb_consecutive_failures"] = 0
                    if entry.get("cb_state") == "HALF-OPEN":
                        entry["cb_half_open_successes"] = entry.get("cb_half_open_successes", 0) + 1
                        if entry["cb_half_open_successes"] >= 2:
                            entry["cb_state"] = "CLOSED"
                            entry["cb_half_open_successes"] = 0
                            entry["cb_opened_at"] = None
                    # Fix 7: 成功时解决 pending recovery
                    resolve_pending_recovery(entry, "success")
                elif outcome == "failure":
                    entry["failure"] = entry.get("failure", 0) + 1
                    entry["cb_consecutive_failures"] = entry.get("cb_consecutive_failures", 0) + 1
                    # CB: 连续失败 >= 3 触发熔断
                    if entry["cb_consecutive_failures"] >= 3:
                        entry["cb_state"] = "OPEN"
                        entry["cb_opened_at"] = datetime.now().isoformat()
                    elif entry.get("cb_state") == "HALF-OPEN":
                        # Fix 2: HALF-OPEN 下失败 1 次回到 OPEN，重置 cb_half_open_successes
                        entry["cb_state"] = "OPEN"
                        entry["cb_opened_at"] = datetime.now().isoformat()
                        entry["cb_half_open_successes"] = 0
                    # Fix 7: 失败时记录 pending recovery
                    record_recovery_on_failure(entry, reflection, agent_name or "unknown")
                elif outcome == "skip":
                    entry["skip"] = entry.get("skip", 0) + 1
                    # Fix 7: 跳过时也解决 pending recovery（如果有的话）
                    resolve_pending_recovery(entry, "skip")

                entry["last_triggered"] = datetime.now().isoformat()

                # 并行批次追踪：更新批次中对应反射的状态
                batch_result = {"success": "SUCCESS", "failure": "FAILURE", "skip": "SKIP"}.get(outcome, "SUCCESS")
                update_batch_reflex(data, reflection, batch_result)

                # 检查批次超时（每次更新时顺带检查）
                check_batch_timeout(data)

                data["updated_at"] = datetime.now().isoformat()

                # 写回（seek+truncate 原地覆写）
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except (json.JSONDecodeError, IOError):
        pass


# ==================== 主函数 ====================

def main():
    # Fix 5: 设置超时保护
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(4)

    try:
        raw = sys.stdin.read()
        if not raw.strip():
            signal.alarm(0)
            sys.exit(0)
        input_data = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        signal.alarm(0)
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

    tool_result = input_data.get("tool_result", "")

    # 提取 agent 名和任务描述
    description = tool_input.get("description", "") or ""
    agent_name, task_desc = extract_agent_name(description)

    if not agent_name:
        signal.alarm(0)
        sys.exit(0)

    # 确定反射类型
    reflection = resolve_reflection(agent_name, task_desc or "")
    if not reflection:
        signal.alarm(0)
        sys.exit(0)

    # 确定执行结果
    outcome = determine_outcome(tool_result)

    sys.stderr.write(f"[trigger-stats] agent={agent_name} reflection={reflection} outcome={outcome}\n")

    # 更新统计（传入 agent_name 用于 recovery 追踪）
    update_stats(reflection, outcome, agent_name=agent_name)

    # Fix 5: 正常完成时取消超时
    signal.alarm(0)
    sys.exit(0)


def cli_start_batch():
    """CLI: 开始一个并行批次
    用法: python3 post-agent-trigger-stats.py start-batch <batch_id> <reflex1,reflex2,...> [timeout_minutes]
    示例: python3 post-agent-trigger-stats.py start-batch phase3-impl-doc implement,document 10
    """
    if len(sys.argv) < 4:
        print(json.dumps({"error": "用法: start-batch <batch_id> <reflex1,reflex2,...> [timeout_minutes]"}))
        sys.exit(1)

    batch_id = sys.argv[2]
    reflexes = [r.strip() for r in sys.argv[3].split(",") if r.strip()]
    timeout_minutes = int(sys.argv[4]) if len(sys.argv) > 4 else None

    if not STATS_PATH.exists():
        print(json.dumps({"error": f"trigger-stats.json not found at {STATS_PATH}"}))
        sys.exit(1)

    try:
        with open(STATS_PATH, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.load(f)
                start_batch(data, batch_id, reflexes, timeout_minutes)
                data["updated_at"] = datetime.now().isoformat()
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        print(json.dumps({
            "status": "ok",
            "batch_id": batch_id,
            "reflexes": reflexes,
            "timeout_minutes": timeout_minutes or DEFAULT_BATCH_TIMEOUT_MINUTES,
        }))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cli_check_batch():
    """CLI: 检查当前批次状态（含超时检测）
    用法: python3 post-agent-trigger-stats.py check-batch
    """
    if not STATS_PATH.exists():
        print(json.dumps({"error": f"trigger-stats.json not found at {STATS_PATH}"}))
        sys.exit(1)

    try:
        with open(STATS_PATH, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.load(f)
                ensure_parallel_batches(data)

                # 检查超时
                timed_out_batch = check_batch_timeout(data)

                active = data["parallel_batches"]["active"]
                history = data["parallel_batches"]["history"]

                if timed_out_batch:
                    data["updated_at"] = datetime.now().isoformat()
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2, ensure_ascii=False)

            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        result = {"status": "ok"}
        if timed_out_batch:
            result["timed_out"] = timed_out_batch
        if active:
            result["active"] = active
        else:
            result["active"] = None
        result["recent_history"] = history[-3:] if history else []

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cli_record_recovery():
    """CLI: 记录 recovery 操作（root 在 L1-L4 恢复后调用）
    用法: python3 post-agent-trigger-stats.py record-recovery <reflex> <level> <replacement_agent> [reason]
    示例: python3 post-agent-trigger-stats.py record-recovery implement L2 Aspen "方案问题非执行问题"
    """
    if len(sys.argv) < 5:
        print(json.dumps({"error": "用法: record-recovery <reflex> <level> <replacement_agent> [reason]"}))
        sys.exit(1)

    reflex = sys.argv[2]
    level = sys.argv[3].upper()
    replacement_agent = sys.argv[4]
    reason = sys.argv[5] if len(sys.argv) > 5 else None

    if level not in LEVEL_ACTION:
        print(json.dumps({"error": f"无效 level: {level}，可用: {', '.join(LEVEL_ACTION.keys())}"}))
        sys.exit(1)

    action = LEVEL_ACTION[level]

    if not STATS_PATH.exists():
        print(json.dumps({"error": f"trigger-stats.json not found at {STATS_PATH}"}))
        sys.exit(1)

    try:
        with open(STATS_PATH, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.load(f)
                rules = data.get("rules", {})

                if reflex not in rules:
                    print(json.dumps({"error": f"反射 '{reflex}' 不在 trigger-stats.json 的 rules 中"}))
                    sys.exit(1)

                entry = rules[reflex]
                ensure_recovery_fields(entry)

                # 查找最近一条 pending 记录
                updated_existing = False
                for rec in reversed(entry["recovery_history"]):
                    if rec.get("outcome") == "pending":
                        rec["level"] = level
                        rec["action"] = action
                        rec["replacement_agent"] = replacement_agent
                        if reason:
                            rec["reason"] = reason
                        updated_existing = True
                        break

                # 无 pending 记录，创建新的
                if not updated_existing:
                    new_rec = {
                        "timestamp": datetime.now().isoformat(),
                        "level": level,
                        "action": action,
                        "original_agent": None,
                        "replacement_agent": replacement_agent,
                        "reason": reason or f"{reflex} recovery {level}",
                        "outcome": "pending"
                    }
                    entry["recovery_history"].append(new_rec)

                    # 保持 recovery_history 不超过上限
                    if len(entry["recovery_history"]) > MAX_RECOVERY_HISTORY:
                        dropped = len(entry["recovery_history"]) - MAX_RECOVERY_HISTORY
                        sys.stderr.write(f"[trigger-stats] recovery_history truncated: dropped {dropped} oldest entries for {reflex}\n")
                        entry["recovery_history"] = entry["recovery_history"][-MAX_RECOVERY_HISTORY:]

                entry["last_recovery_level"] = level
                data["updated_at"] = datetime.now().isoformat()

                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        print(json.dumps({
            "status": "ok",
            "reflex": reflex,
            "level": level,
            "action": action,
            "replacement_agent": replacement_agent,
            "reason": reason,
            "updated_existing": updated_existing,
        }))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    # CLI 子命令分发
    if len(sys.argv) > 1:
        subcmd = sys.argv[1]
        if subcmd == "start-batch":
            cli_start_batch()
        elif subcmd == "check-batch":
            cli_check_batch()
        elif subcmd == "record-recovery":
            cli_record_recovery()
        else:
            print(json.dumps({"error": f"未知子命令: {subcmd}，可用: start-batch, check-batch, record-recovery"}))
            sys.exit(1)
    else:
        # 默认行为：PostToolUse hook 模式（stdin 读取）
        main()
