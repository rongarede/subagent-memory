"""
邻居演化引擎

当新记忆创建时，LLM 主动决策是否更新已有邻居记忆的 context/tags/keywords。
采用 3 步分解调用：判断 → 生成指令 → 执行更新。
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

from memory_store import Memory, MemoryStore

MAX_EVOLUTION_HISTORY = 10


def get_client():
    """获取 Anthropic 客户端（与 extractor 共享，便于统一 mock）"""
    import anthropic
    return anthropic.Anthropic()


def _build_should_evolve_prompt(new_memory: Memory, neighbors: list) -> str:
    """构建 Step 1 prompt：判断是否需要演化"""
    neighbor_summaries = []
    for n in neighbors:
        neighbor_summaries.append(
            f"- [{n.id}] {n.context} (keywords: {', '.join(n.keywords[:5])})"
        )

    return f"""你是一个记忆管理系统。判断新记忆是否包含能更新已有邻居记忆的新信息。

新记忆：
- 内容：{new_memory.content}
- 关键词：{', '.join(new_memory.keywords)}
- 上下文：{new_memory.context}

已有邻居记忆：
{chr(10).join(neighbor_summaries)}

判断：新记忆是否包含邻居尚未知道的信息（如解决方案、新发现、修正）？
如果邻居的 context 已经完整，不需要更新。

返回 JSON（不要包含其他文本）：
{{"should_evolve": true/false, "reason": "一句话说明原因"}}"""


def _build_evolution_plan_prompt(new_memory: Memory, neighbors: list) -> str:
    """构建 Step 2 prompt：生成演化指令"""
    neighbor_details = []
    for n in neighbors:
        neighbor_details.append(
            f"ID: {n.id}\n内容: {n.content}\n上下文: {n.context}\n关键词: {', '.join(n.keywords)}\n标签: {', '.join(n.tags)}"
        )

    return f"""你是一个记忆管理系统。根据新记忆的信息，为需要更新的邻居记忆生成更新指令。

新记忆：
内容：{new_memory.content}
关键词：{', '.join(new_memory.keywords)}
上下文：{new_memory.context}

邻居记忆：
{(chr(10) + '---' + chr(10)).join(neighbor_details)}

规则：
1. 只更新真正需要补充信息的邻居
2. new_context 应该在原有 context 基础上补充新信息，不要完全重写
3. add_tags 和 add_keywords 只添加新的，不重复已有的
4. 最多更新 3 个邻居

返回 JSON（不要包含其他文本）：
{{"updates": [{{"neighbor_id": "xxx", "new_context": "更新后的上下文", "add_tags": ["tag1"], "add_keywords": ["kw1"]}}]}}"""


def should_evolve(
    new_memory: Memory,
    neighbors: list,
    client=None,
) -> tuple:
    """
    Step 1: 判断是否需要演化邻居（1 次 Haiku 调用）
    Returns: (should_evolve: bool, reason: str)
    """
    if not neighbors:
        return (False, "no neighbors")

    if client is None:
        client = get_client()

    prompt = _build_should_evolve_prompt(new_memory, neighbors)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        # 从响应中提取 JSON
        if '{' in text:
            text = text[text.index('{'):text.rindex('}') + 1]
        result = json.loads(text)
        return (result.get("should_evolve", False), result.get("reason", ""))
    except Exception as e:
        return (False, f"error: {str(e)}")


def generate_evolution_plan(
    new_memory: Memory,
    neighbors: list,
    client=None,
) -> list:
    """
    Step 2: 生成演化指令（1 次 Haiku 调用）
    Returns: list of update dicts
    """
    if client is None:
        client = get_client()

    prompt = _build_evolution_plan_prompt(new_memory, neighbors)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if '{' in text:
            text = text[text.index('{'):text.rindex('}') + 1]
        result = json.loads(text)
        updates = result.get("updates", [])
        # 最多更新 3 个邻居
        return updates[:3]
    except Exception as e:
        return []


def execute_evolution(
    plan: list,
    store: MemoryStore,
    triggered_by_id: str,
) -> list:
    """
    Step 3: 执行演化更新 + 记录 evolution_history（纯代码）
    Returns: list of updated memory IDs
    """
    updated_ids = []
    now = datetime.now().isoformat()

    for update in plan:
        neighbor_id = update.get("neighbor_id")
        if not neighbor_id:
            continue

        neighbor = store.get(neighbor_id)
        if not neighbor:
            continue

        changes = {}

        # 更新 context
        new_context = update.get("new_context")
        if new_context and new_context != neighbor.context:
            changes["context"] = {"old": neighbor.context, "new": new_context}
            neighbor.context = new_context

        # 新增 tags
        add_tags = update.get("add_tags", [])
        if add_tags:
            new_tags = [t for t in add_tags if t not in neighbor.tags]
            if new_tags:
                changes["tags"] = {"added": new_tags}
                neighbor.tags = list(set(neighbor.tags + new_tags))

        # 新增 keywords
        add_keywords = update.get("add_keywords", [])
        if add_keywords:
            new_kw = [k for k in add_keywords if k not in neighbor.keywords]
            if new_kw:
                changes["keywords"] = {"added": new_kw}
                neighbor.keywords = list(set(neighbor.keywords + new_kw))

        if not changes:
            continue

        # 追加演化历史
        history_entry = {
            "timestamp": now,
            "triggered_by": triggered_by_id,
            "changes": changes,
        }
        neighbor.evolution_history.append(history_entry)

        # 截断历史到 MAX_EVOLUTION_HISTORY
        if len(neighbor.evolution_history) > MAX_EVOLUTION_HISTORY:
            neighbor.evolution_history = neighbor.evolution_history[-MAX_EVOLUTION_HISTORY:]

        store.update(neighbor)
        updated_ids.append(neighbor_id)

    return updated_ids


def evolve_neighbors(
    new_memory: Memory,
    store: MemoryStore,
    agent_type: str = None,
    max_neighbors: int = 3,
) -> list:
    """
    入口函数：完整的邻居演化流程

    1. 找 top-N 同类型邻居
    2. should_evolve() → 不需要则 return []
    3. generate_evolution_plan()
    4. execute_evolution()
    5. return 被更新的 ID 列表
    """
    from associator import find_associations

    # 找邻居（复用 associator 的逻辑）
    try:
        neighbor_ids = find_associations(
            new_memory, store, top_k=max_neighbors,
            threshold=0.2, agent_type=agent_type,
        )
    except Exception:
        neighbor_ids = []

    if not neighbor_ids:
        return []

    # 加载邻居 Memory 对象
    neighbors = []
    for nid in neighbor_ids:
        mem = store.get(nid)
        if mem:
            neighbors.append(mem)

    # 若同类型跨角色场景，在其他存储中查找未找到的邻居
    if not neighbors and agent_type:
        from registry import AgentRegistry
        from pathlib import Path
        registry = AgentRegistry()
        same_type_agents = registry.get_agents_by_type(agent_type)
        base = Path(os.path.expanduser("~/.claude/memory"))
        for agent in same_type_agents:
            agent_path = base / "agents" / agent / "memories.jsonl"
            if agent_path.exists():
                agent_store = MemoryStore(store_path=str(agent_path))
                for nid in neighbor_ids:
                    mem = agent_store.get(nid)
                    if mem:
                        neighbors.append(mem)

    if not neighbors:
        return []

    # Step 1: 是否需要演化？
    try:
        do_evolve, reason = should_evolve(new_memory, neighbors)
    except Exception:
        return []

    if not do_evolve:
        return []

    # Step 2: 生成演化指令
    try:
        plan = generate_evolution_plan(new_memory, neighbors)
    except Exception:
        return []

    if not plan:
        return []

    # Step 3: 执行演化
    updated = execute_evolution(plan, store, new_memory.id)

    # 检查跨角色存储中尚未更新的条目
    if agent_type:
        updated_set = set(updated)
        remaining = [u for u in plan if u.get("neighbor_id") not in updated_set]
        if remaining:
            from registry import AgentRegistry
            from pathlib import Path
            registry = AgentRegistry()
            same_type_agents = registry.get_agents_by_type(agent_type)
            base = Path(os.path.expanduser("~/.claude/memory"))
            for agent in same_type_agents:
                agent_path = base / "agents" / agent / "memories.jsonl"
                if agent_path.exists():
                    agent_store = MemoryStore(store_path=str(agent_path))
                    cross_updated = execute_evolution(remaining, agent_store, new_memory.id)
                    updated.extend(cross_updated)

    return updated
