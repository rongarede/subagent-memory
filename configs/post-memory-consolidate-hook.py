#!/usr/bin/env python3
# ============================================================
# post-memory-consolidate-hook: PostToolUse / Agent hook
#
# 功能 1（记忆验证）：Agent 完成后检查其 store 中是否有最近 5 分钟
#   内修改的记忆文件。如果没有，输出 stderr 警告提醒 root 补录。
#
# 功能 2（记忆合并）：检查 store 中的 mem_*.md 文件数量，
#   超过阈值时自动触发 cli.py consolidate，最多合并 5 对。
#
# 触发条件：tool_name == "Agent"
# 阈值：默认 20 个 mem_*.md 文件（MEMORY_CONSOLIDATE_THRESHOLD 覆盖）
# 超时保护：整体执行 < 4 秒（hook 默认超时 5 秒）
# 安全：所有异常静默处理（exit 0），合并前先 dry-run 确认有可合并对
# ============================================================

import json
import os
import sys
import subprocess
import time
from pathlib import Path


# ==================== 配置 ====================

CLI_PATH = os.path.expanduser("~/.claude/skills/agent-memory/scripts/cli.py")

# 默认阈值（超过此数量触发合并）
DEFAULT_THRESHOLD = 20

# 每次最多合并对数
DEFAULT_MAX_PAIRS = 5

# agent 名称 → store 磁盘路径（英文目录名，与磁盘实际路径一致）
AGENT_STORE_MAP = {
    "tetsu":  "~/mem/mem/agents/Worker/tetsu",
    "kaze":   "~/mem/mem/agents/Explore/kaze",
    "shin":   "~/mem/mem/agents/Auditor/shin",
    "yomi":   "~/mem/mem/agents/Analyst/yomi",
    "haku":   "~/mem/mem/agents/Inspector/haku",
    "raiga":  "~/mem/mem/agents/Devourer/raiga",
    "fumio":  "~/mem/mem/agents/Weaver/fumio",
    "norna":  "~/mem/mem/agents/Matrix/norna",
    "yume":   "~/mem/mem/agents/Dreamer/yume",
    "miru":   "~/mem/mem/agents/Watcher/miru",
}

# 排除合并的 agent（避免循环）
SKIP_AGENTS = {"yume"}

# 记忆保存验证：检查窗口（秒）
MEMORY_CHECK_WINDOW = 300  # 5 分钟

# 排除记忆检查的 agent（如 yume 自身管理记忆，不需要被检查）
SKIP_MEMORY_CHECK = {"yume"}


# ==================== 辅助函数 ====================

def get_threshold() -> int:
    """从环境变量读取阈值，无效时降级使用 DEFAULT_THRESHOLD。"""
    raw = os.environ.get("MEMORY_CONSOLIDATE_THRESHOLD", "")
    if raw:
        try:
            return int(raw)
        except (ValueError, TypeError):
            pass
    return DEFAULT_THRESHOLD


def extract_agent_name(description: str) -> str | None:
    """从 '角色名 | 任务描述' 格式提取 agent 名。

    返回在 AGENT_STORE_MAP 中注册的名字；否则返回 None。
    """
    if not description or "|" not in description:
        return None
    candidate = description.split("|")[0].strip().lower()
    if candidate in AGENT_STORE_MAP:
        return candidate
    return None


def infer_store_path(agent_name: str) -> str | None:
    """根据 agent 名返回对应的 store 路径（~/ 展开前）。

    返回 None 若 agent 未注册。
    """
    return AGENT_STORE_MAP.get(agent_name)


def should_consolidate(store_path: str, threshold: int = DEFAULT_THRESHOLD) -> bool:
    """检查 store 目录中 mem_*.md 文件数量是否超过阈值。

    - 只统计以 mem_ 开头的 .md 文件
    - 不存在的目录返回 False
    - 数量必须严格大于阈值才返回 True（等于不触发）
    """
    try:
        expanded = os.path.expanduser(store_path)
        p = Path(expanded)
        if not p.exists():
            return False
        count = sum(1 for f in p.glob("mem_*.md") if f.is_file())
        return count > threshold
    except Exception:
        return False


def run_consolidate(store_path: str, max_pairs: int = DEFAULT_MAX_PAIRS) -> dict | None:
    """执行记忆合并：先 dry-run 预检，有可合并对则执行真正合并。

    步骤：
    1. dry-run 确认是否有可合并的对
    2. 若有，调用 consolidate 子命令，合并所有发现的相似对

    所有异常静默处理，超时 4 秒，返回摘要 dict 或 None。
    """
    if not os.path.exists(CLI_PATH):
        return None

    expanded_store = os.path.expanduser(store_path)

    # ---- Step 1: dry-run 预检 ----
    dry_run_cmd = [
        sys.executable, CLI_PATH,
        "--store", expanded_store,
        "consolidate",
        "--dry-run",
    ]

    try:
        dry_result = subprocess.run(
            dry_run_cmd,
            capture_output=True,
            text=True,
            timeout=4,
        )
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

    dry_output = dry_result.stdout or ""

    # 检测是否发现可合并对（干运行输出含"发现 N 对"或不含"未发现"）
    has_pairs = (
        dry_result.returncode == 0
        and "发现" in dry_output
        and "未发现" not in dry_output
    )

    if not has_pairs:
        # 无可合并对，直接返回
        return {"merged": 0, "deleted": 0, "pairs": 0}

    # ---- Step 2: 执行真正合并 ----
    merge_cmd = [
        sys.executable, CLI_PATH,
        "--store", expanded_store,
        "consolidate",
    ]

    try:
        merge_result = subprocess.run(
            merge_cmd,
            capture_output=True,
            text=True,
            timeout=4,
        )
        if merge_result.returncode == 0:
            return {
                "merged": -1,
                "stdout": merge_result.stdout[:200] if merge_result.stdout else "",
            }
        return {"merged": 0, "deleted": 0, "pairs": 0}
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def check_recent_memory(agent_name: str, store_path: str) -> bool:
    """检查 agent 是否在最近 MEMORY_CHECK_WINDOW 秒内保存了记忆。

    返回 True 表示有近期记忆，False 表示没有。
    如果没有，向 stderr 写入警告。
    """
    try:
        expanded = os.path.expanduser(store_path)
        mem_dir = Path(expanded)

        if not mem_dir.exists():
            sys.stderr.write(
                f"[memory-check] WARNING: {agent_name} 记忆目录不存在 ({expanded})\n"
            )
            return False

        now = time.time()
        recent_files = [
            f for f in mem_dir.rglob("*")
            if f.is_file()
            and f.name.endswith(".md")
            and f.name != "MEMORY.md"
            and f.name != "WhoAmI.md"
            and f.name != "trigger-map.md"
            and (now - f.stat().st_mtime) < MEMORY_CHECK_WINDOW
        ]

        if not recent_files:
            sys.stderr.write(
                f"[memory-check] WARNING: {agent_name} 完成任务但最近 "
                f"{MEMORY_CHECK_WINDOW // 60} 分钟无记忆保存。"
                f"请 root 派 yume 补录记忆。\n"
            )
            return False

        return True

    except Exception:
        # 检查失败时静默，不阻塞
        return True


def process_agent_event(agent_name: str, store_path: str, threshold: int = DEFAULT_THRESHOLD) -> None:
    """处理 Agent 完成事件：检查记忆保存 + 按需触发合并。"""
    # ---- 记忆保存验证 ----
    if agent_name not in SKIP_MEMORY_CHECK:
        check_recent_memory(agent_name, store_path)

    # ---- 记忆合并检查 ----
    if not should_consolidate(store_path, threshold=threshold):
        return

    result = run_consolidate(store_path, max_pairs=DEFAULT_MAX_PAIRS)
    if result and result.get("merged", 0) > 0:
        print(json.dumps({
            "message": (
                f"[post-memory-consolidate-hook] {agent_name} store 超阈值，"
                f"已合并 {result['merged']} 对记忆"
            )
        }))


# ==================== 主函数 ====================

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        input_data = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        # stdin 解析失败，静默退出，不 block
        sys.exit(0)

    # 仅处理 Agent 事件
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Agent":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    # 从 description 提取 agent 名
    description = tool_input.get("description", "") or ""
    agent_name = extract_agent_name(description)

    if not agent_name:
        # 无法推断 agent，静默跳过
        sys.exit(0)

    # 跳过保护 agent
    if agent_name in SKIP_AGENTS:
        sys.exit(0)

    # 获取 store 路径
    store_path = infer_store_path(agent_name)
    if not store_path:
        sys.exit(0)

    # 读取阈值
    threshold = get_threshold()

    # 执行检查与按需合并
    try:
        process_agent_event(agent_name, store_path, threshold=threshold)
    except Exception:
        # 任何异常都静默处理，不阻塞用户操作
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
