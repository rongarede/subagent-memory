"""Phase 2.2 Memory Decay Engine: Ebbinghaus-inspired exponential decay.

算法规格：
  R = e^(-t/S)，其中 t = 距上次访问天数，S = base_importance * 3（stability 天数）
  decayed_importance = max(base * 0.2, base * R)       floor = base × 20%，至少为 1
  last_accessed 为 None 时，使用 memory.timestamp（创建时间）作为参考点。
  compute_retention(None, ...) → 1.0（保守策略：无记录时不惩罚）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
import dataclasses
from datetime import datetime
from typing import Optional

from memory_store import Memory, MemoryStore


def compute_retention(
    last_accessed: Optional[str],
    base_importance: float,
    now: Optional[datetime] = None,
) -> float:
    """计算记忆保留率 R = e^(-t/S)，S = base_importance * 3（天）。

    Args:
        last_accessed: ISO 格式的上次访问时间字符串，或 None
        base_importance: 原始重要性值（1-10）
        now: 当前时间，用于测试（None 时取 datetime.now()）

    Returns:
        retention ratio，范围 [0.0, 1.0]。
        last_accessed 为 None 时返回 1.0（保守策略）。
    """
    if last_accessed is None:
        return 1.0

    if now is None:
        now = datetime.now()

    try:
        last_dt = datetime.fromisoformat(last_accessed)
    except (ValueError, TypeError):
        return 1.0  # 无法解析时保守处理

    # t = 距上次访问的天数
    t = max(0.0, (now - last_dt).total_seconds() / 86400.0)

    # S = stability 天数（base_importance * 3），防止除零
    stability = max(1e-9, float(base_importance) * 3.0)

    return math.exp(-t / stability)


def apply_decay(memory: Memory, now: Optional[datetime] = None) -> Memory:
    """对记忆施加时间衰减，返回新 Memory 对象（不可变）。

    decayed_importance = max(base * floor_ratio, base * R)
    floor_ratio = 0.2，且 floor 最低为 1（int 取整后）

    若 memory.last_accessed 为 None，则使用 memory.timestamp 作为参考点。

    Args:
        memory: 原始 Memory 对象（不修改）
        now: 当前时间，用于测试（None 时取 datetime.now()）

    Returns:
        新 Memory 对象，importance 已更新为衰减后值。
    """
    base = memory.importance

    # 决定参考时间点：last_accessed 优先，否则用创建时间
    if memory.last_accessed is not None:
        ref_time = memory.last_accessed
    else:
        ref_time = memory.timestamp

    # 计算 retention（ref_time 此时肯定非 None）
    retention = compute_retention(
        last_accessed=ref_time,
        base_importance=base,
        now=now,
    )

    # 计算衰减后 importance
    floor_val = max(1, int(base * 0.2))
    decayed_float = max(base * 0.2, base * retention)
    decayed_int = max(floor_val, int(decayed_float))

    return dataclasses.replace(memory, importance=decayed_int)


def cleanup_decayed(
    store: MemoryStore,
    floor_ratio: float = 0.2,
    now: Optional[datetime] = None,
) -> int:
    """清理 store 中所有已触底的记忆，返回删除数量。

    触底判断：apply_decay 后的 importance == floor（即已不可再降）。
    floor = max(1, int(original_importance * floor_ratio))

    Args:
        store: MemoryStore 实例
        floor_ratio: 触底比例（默认 0.2）
        now: 当前时间，用于测试（None 时取 datetime.now()）

    Returns:
        删除的记忆条数。
    """
    memories = store.load_all()
    deleted_count = 0

    for memory in memories:
        base = memory.importance
        floor_val = max(1, int(base * floor_ratio))

        decayed = apply_decay(memory, now=now)

        # 触底条件：衰减后 importance 等于 floor（已降无可降）
        if decayed.importance <= floor_val:
            store.delete(memory.id)
            deleted_count += 1

    return deleted_count
