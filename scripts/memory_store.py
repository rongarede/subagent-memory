"""Memory store: JSONL-based storage for associative memories."""

import json
import os
import tempfile
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path
from datetime import datetime


@dataclass
class Memory:
    """A single memory note, inspired by A-MEM's Zettelkasten model."""
    id: str                          # mem_YYYYMMDD_NNN 或 {agent}_{YYYYMMDD}_{NNN}
    content: str                     # task description + outcome
    timestamp: str                   # ISO format
    keywords: list[str]              # >= 3, ordered by importance
    tags: list[str]                  # broad categories
    context: str                     # one-line summary
    importance: int                  # 1-10 (Generative Agents style)
    related_ids: list[str] = field(default_factory=list)  # A-MEM links
    access_count: int = 0
    last_accessed: Optional[str] = None
    # Phase 6b: 多角色记忆层
    owner: str = ""                                       # 角色名，如 "kaze"
    scope: str = "personal"                               # "personal" | "shared"
    accessed_by: list = field(default_factory=list)       # 哪些角色检索过
    # Phase 7: 邻居演化历史
    evolution_history: list = field(default_factory=list) # 该记忆被演化更新的历史记录

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Memory':
        # 只取 dataclass 已知字段，兼容旧 JSONL（不含 owner/scope/accessed_by）
        known = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data.items() if k in known}
        # 为新字段设置默认值，保证旧文件可正常加载
        filtered.setdefault('owner', '')
        filtered.setdefault('scope', 'personal')
        filtered.setdefault('accessed_by', [])
        filtered.setdefault('evolution_history', [])
        return cls(**filtered)


class MemoryStore:
    """JSONL-based memory storage with atomic append.

    三种构造模式：
    1. store_path 指定  → legacy/test 模式，直接使用该路径
    2. agent_name 指定  → personal 模式，路径为 ~/.claude/memory/agents/{name}/memories.jsonl
    3. 两者都不指定     → 默认路径 ~/.claude/memory/memories.jsonl（向后兼容）
    """

    def __init__(self, store_path: str = None, agent_name: str = None, agent_type: str = None):
        self.agent_name = agent_name
        self.agent_type = agent_type

        if store_path is not None:
            # legacy / test 模式：直接使用指定路径
            self.store_path = Path(store_path)
        elif agent_name is not None:
            # personal 模式：按角色名定位
            base = Path(os.path.expanduser("~/.claude/memory"))
            self.store_path = base / "agents" / agent_name / "memories.jsonl"
        else:
            # 默认路径（向后兼容）
            self.store_path = Path(os.path.expanduser("~/.claude/memory/memories.jsonl"))

        self.store_path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, memory: Memory) -> Memory:
        """Append a memory to the store."""
        with open(self.store_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(memory.to_dict(), ensure_ascii=False) + '\n')
        return memory

    def load_all(self) -> list[Memory]:
        """Load all memories from store."""
        if not self.store_path.exists():
            return []
        memories = []
        with open(self.store_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    memories.append(Memory.from_dict(json.loads(line)))
        return memories

    def get(self, memory_id: str) -> Optional[Memory]:
        """Get a specific memory by ID."""
        for m in self.load_all():
            if m.id == memory_id:
                return m
        return None

    def update(self, memory: Memory) -> None:
        """Update a memory in-place (rewrite entire file)."""
        memories = self.load_all()
        with open(self.store_path, 'w', encoding='utf-8') as f:
            for m in memories:
                if m.id == memory.id:
                    f.write(json.dumps(memory.to_dict(), ensure_ascii=False) + '\n')
                else:
                    f.write(json.dumps(m.to_dict(), ensure_ascii=False) + '\n')

    def generate_id(self, id_prefix: str = None) -> str:
        """Generate a unique memory ID.

        若指定 id_prefix，直接使用该前缀；
        否则若 agent_name 已设置，格式为 {agent_name}_{YYYYMMDD}_{NNN}；
        否则使用原格式 mem_{YYYYMMDD}_{NNN}。

        序号基于已存在的同前缀记忆的最大序号递增，而非计数，
        避免因删除或重复写入导致的序号碰撞。
        """
        today = datetime.now().strftime("%Y%m%d")
        if id_prefix is not None:
            prefix = id_prefix
        elif self.agent_name:
            prefix = f"{self.agent_name}_{today}"
        else:
            prefix = f"mem_{today}"

        max_seq = 0
        for m in self.load_all():
            if m.id.startswith(prefix + "_"):
                suffix = m.id[len(prefix) + 1:]
                if suffix.isdigit():
                    max_seq = max(max_seq, int(suffix))
        seq = max_seq + 1
        return f"{prefix}_{seq:03d}"

    def count(self) -> int:
        """Return the number of memories."""
        return len(self.load_all())

    # ==================== Phase 6b: 多角色合并检索 ====================

    def retrieve_merged(self, query: str, top_k: int = 3, spread: bool = True,
                        spread_decay: float = 0.5, now=None) -> list:
        """合并检索：个人记忆 + 同类型其他角色记忆 + shared 记忆。

        扩散激活仅在同类型角色间生效。
        返回 list[tuple[Memory, float]]，与 retriever.retrieve() 格式一致。
        """
        from retriever import retrieve as _retrieve
        from registry import AgentRegistry

        all_memories = []

        # 1. 个人记忆
        personal = self.load_all()
        all_memories.extend(personal)

        # 2. 同类型其他角色的记忆
        if self.agent_name and self.agent_type:
            registry = AgentRegistry()
            same_type_agents = registry.get_agents_by_type(self.agent_type)
            base = Path(os.path.expanduser("~/.claude/memory"))
            for agent in same_type_agents:
                if agent != self.agent_name:
                    other_path = base / "agents" / agent / "memories.jsonl"
                    if other_path.exists():
                        other_store = MemoryStore(store_path=str(other_path))
                        all_memories.extend(other_store.load_all())

        # 3. Shared 记忆
        shared_path = Path(os.path.expanduser("~/.claude/memory/shared/memories.jsonl"))
        if shared_path.exists():
            shared_store = MemoryStore(store_path=str(shared_path))
            all_memories.extend(shared_store.load_all())

        if not all_memories:
            return []

        # 将所有记忆写入临时存储，统一评分
        tmp = tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False)
        tmp.close()
        try:
            merged_store = MemoryStore(store_path=tmp.name)
            for m in all_memories:
                merged_store.add(m)
            results = _retrieve(query, merged_store, top_k=top_k, spread=spread,
                                spread_decay=spread_decay, now=now)

            # 对原始存储中的记忆更新访问追踪
            for mem, score in results:
                self._track_access(mem)

            return results
        finally:
            os.unlink(tmp.name)

    def _track_access(self, memory: Memory) -> None:
        """更新访问追踪，检查晋升条件。"""
        if not self.agent_name:
            return

        # 若记忆属于其他角色，更新对方存储中的 accessed_by
        if memory.owner and memory.owner != self.agent_name:
            base = Path(os.path.expanduser("~/.claude/memory"))
            owner_path = base / "agents" / memory.owner / "memories.jsonl"
            if owner_path.exists():
                owner_store = MemoryStore(store_path=str(owner_path))
                original = owner_store.get(memory.id)
                if original and self.agent_name not in original.accessed_by:
                    original.accessed_by.append(self.agent_name)
                    owner_store.update(original)
                    self.check_promotion(memory.id, owner_store, original)

    def check_promotion(self, memory_id: str, source_store: 'MemoryStore' = None,
                        memory: Memory = None) -> bool:
        """检查记忆是否应晋升到 shared（被 >= 3 个不同角色检索过）。

        晋升条件达成时，将记忆复制到 shared 层并标记原记忆 scope="shared"。
        返回是否发生了晋升。
        """
        store = source_store or self
        mem = memory or store.get(memory_id)
        if not mem or mem.scope == "shared":
            return False

        if len(mem.accessed_by) >= 3:
            # 晋升到 shared 层
            shared_path = Path(os.path.expanduser("~/.claude/memory/shared/memories.jsonl"))
            shared_path.parent.mkdir(parents=True, exist_ok=True)
            shared_store = MemoryStore(store_path=str(shared_path))

            # 生成 shared ID：使用 shared_ 前缀 + 今日日期，序号自动递增
            today = datetime.now().strftime("%Y%m%d")
            shared_id = shared_store.generate_id(id_prefix=f"shared_{today}")

            promoted = Memory(
                id=shared_id,
                content=mem.content,
                timestamp=mem.timestamp,
                keywords=mem.keywords,
                tags=mem.tags,
                context=mem.context,
                importance=mem.importance,
                related_ids=[],          # shared 层不保留个人关联
                access_count=mem.access_count,
                last_accessed=mem.last_accessed,
                owner="shared",
                scope="shared",
                accessed_by=mem.accessed_by[:],
            )
            shared_store.add(promoted)

            # 标记原记忆已晋升
            mem.scope = "shared"
            store.update(mem)
            return True

        return False
