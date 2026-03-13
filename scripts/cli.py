#!/usr/bin/env python3
"""CLI entry point for the agent-memory system.

Usage:
    python3 cli.py retrieve <query> [--top-k N] [--no-spread] [--format prompt|text]
    python3 cli.py add --subject <subject> [--description <desc>] [--keywords k1,k2] [--tags t1,t2] [--importance N]
    python3 cli.py stats
    python3 cli.py list [--limit N]
    python3 cli.py evolve <memory_id> [--context <ctx>] [--tags <tags>]
    python3 cli.py export [--output <dir>]
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scripts dir to path so sibling modules resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_store import Memory, MemoryStore
from retriever import retrieve, format_for_prompt


DEFAULT_STORE = os.path.expanduser("~/.claude/memory/memories")
DEFAULT_EXPORT_DIR = str(Path(os.path.expanduser("~/Obsidian/300_Resources/Agent_Memory")))


# ==================== 工厂函数：根据参数创建 MemoryStore ====================

def get_store(args) -> MemoryStore:
    """根据参数创建合适的 MemoryStore。

    优先级：--agent 参数 > --store 参数 > 默认路径。
    """
    if getattr(args, 'agent', None):
        from registry import AgentRegistry
        registry = AgentRegistry()
        agent_type = registry.get_agent_type(args.agent)
        return MemoryStore(agent_name=args.agent, agent_type=agent_type)
    return MemoryStore(store_path=args.store)


# ==================== 子命令实现 ====================

def cmd_retrieve(args):
    """检索与查询最相关的记忆，按三维评分排序。"""
    store = get_store(args)

    # 当指定 --agent 时使用合并检索（个人 + 同类型 + shared）
    if getattr(args, 'agent', None) and store.agent_name:
        results = store.retrieve_merged(
            query=args.query,
            top_k=args.top_k,
            spread=not args.no_spread,
        )
    else:
        results = retrieve(
            query=args.query,
            store=store,
            top_k=args.top_k,
            spread=not args.no_spread,
        )

    if not results:
        print("未找到相关记忆。")
        return

    if args.format == "prompt":
        print(format_for_prompt(results))
    else:
        for mem, score in results:
            print(f"[{score:.2f}] {mem.id}: {mem.content}")
            print(f"         keywords: {', '.join(mem.keywords)}")
            print(f"         context:  {mem.context}")
            print(f"         importance: {mem.importance}/10 | accessed: {mem.access_count}x")
            if mem.related_ids:
                print(f"         links: {', '.join(mem.related_ids)}")
            print()


def cmd_add(args):
    """手动添加一条记忆。"""
    store = get_store(args)

    # 解析 keywords 和 tags（逗号分隔字符串 → 列表）
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else [args.subject]
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else ["manual"]

    content = f"{args.subject}: {args.description}" if args.description else args.subject

    memory = Memory(
        id=store.generate_id(),
        content=content,
        timestamp=datetime.now().isoformat(),
        keywords=keywords,
        tags=tags,
        context=args.subject,
        importance=args.importance,
    )

    # 当指定 --agent 时，标记记忆所有者
    if getattr(args, 'agent', None):
        memory.owner = args.agent

    store.add(memory)

    print(f"记忆已创建: {memory.id}")
    print(f"  content:    {memory.content}")
    print(f"  keywords:   {', '.join(memory.keywords)}")
    print(f"  tags:       {', '.join(memory.tags)}")
    print(f"  importance: {memory.importance}/10")
    if memory.owner:
        print(f"  owner:      {memory.owner}")


def cmd_stats(args):
    """显示记忆库统计信息。"""
    store = get_store(args)
    memories = store.load_all()

    # 当指定 --agent 时，同时展示 shared 记忆统计
    if getattr(args, 'agent', None):
        shared_path = Path(os.path.expanduser("~/.claude/memory/shared"))
        if shared_path.exists():
            shared_store = MemoryStore(store_path=str(shared_path))
            shared_memories = shared_store.load_all()
        else:
            shared_memories = []

        print(f"=== Agent Memory 统计 [{args.agent}] ===")
        if not memories:
            print(f"个人记忆: 0 条")
        else:
            total = len(memories)
            avg_importance = sum(m.importance for m in memories) / total
            total_links = sum(len(m.related_ids) for m in memories)
            total_accesses = sum(m.access_count for m in memories)

            tag_counts: dict[str, int] = {}
            for m in memories:
                for t in m.tags:
                    tag_counts[t] = tag_counts.get(t, 0) + 1
            top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]

            print(f"个人记忆总数:   {total}")
            print(f"平均重要性:     {avg_importance:.1f}/10")
            print(f"总关联链接:     {total_links}")
            print(f"总访问次数:     {total_accesses}")
            print(f"存储路径:       {store.store_path}")
            print("\nTop Tags (个人):")
            for tag, count in top_tags:
                print(f"  {tag}: {count}")

        print(f"\nShared 记忆总数: {len(shared_memories)}")
        if shared_memories:
            avg_shared = sum(m.importance for m in shared_memories) / len(shared_memories)
            print(f"Shared 平均重要性: {avg_shared:.1f}/10")
        return

    if not memories:
        print("记忆库为空。")
        return

    total = len(memories)
    avg_importance = sum(m.importance for m in memories) / total
    total_links = sum(len(m.related_ids) for m in memories)
    total_accesses = sum(m.access_count for m in memories)

    # Tag 分布统计
    tag_counts: dict[str, int] = {}
    for m in memories:
        for t in m.tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    print("=== Agent Memory 统计 ===")
    print(f"记忆总数:     {total}")
    print(f"平均重要性:   {avg_importance:.1f}/10")
    print(f"总关联链接:   {total_links}")
    print(f"总访问次数:   {total_accesses}")
    print(f"存储路径:     {args.store}")
    print("\nTop Tags:")
    for tag, count in top_tags:
        print(f"  {tag}: {count}")


def cmd_evolve(args):
    """更新已有记忆的 context 或 tags。"""
    store = get_store(args)
    memory = store.get(args.memory_id)

    if not memory:
        print(f"记忆 {args.memory_id} 不存在。")
        sys.exit(1)

    updated = False
    if args.context:
        memory.context = args.context
        updated = True
    if args.tags:
        memory.tags = [t.strip() for t in args.tags.split(",")]
        updated = True

    if not updated:
        print("未提供任何更新字段（--context 或 --tags）。")
        return

    store.update(memory)
    print(f"记忆 {memory.id} 已更新。")
    print(f"  context: {memory.context}")
    print(f"  tags:    {', '.join(memory.tags)}")


def cmd_list(args):
    """列出最近的记忆（按时间戳降序）。"""
    store = get_store(args)
    memories = store.load_all()

    if not memories:
        print("记忆库为空。")
        return

    # 按时间戳降序排列
    memories.sort(key=lambda m: m.timestamp, reverse=True)

    agent_header = f" [{args.agent}]" if getattr(args, 'agent', None) else ""
    print(f"最近 {min(args.limit, len(memories))} 条记忆{agent_header}（共 {len(memories)} 条）：\n")
    for m in memories[: args.limit]:
        links_info = f" [{len(m.related_ids)} links]" if m.related_ids else ""
        owner_info = f" owner:{m.owner}" if m.owner else ""
        preview = m.content[:60] + ("..." if len(m.content) > 60 else "")
        print(f"  {m.id} | imp:{m.importance}/10 | {preview}{links_info}{owner_info}")


def cmd_quick_add(args):
    """直接保存记忆，无需 API 调用"""
    store = get_store(args)

    from memory_store import Memory
    from datetime import datetime

    keywords = [k.strip() for k in args.keywords.split(',')]
    tags = [t.strip() for t in args.tags.split(',')]

    memory = Memory(
        id=store.generate_id(name=args.name, memory_type=args.type),
        content=args.content,
        timestamp=datetime.now().isoformat(),
        name=args.name or '',
        description=args.description or '',
        type=args.type,
        keywords=keywords,
        tags=tags,
        context=args.context or '',
        importance=args.importance,
        owner=getattr(args, 'agent', '') or '',
        scope='personal',
    )

    store.add(memory)

    # 自动关联
    from associator import link_memory
    agent_type = None
    if hasattr(args, 'agent') and args.agent:
        from registry import AgentRegistry
        reg = AgentRegistry()
        agent_type = reg.get_agent_type(args.agent)

    updated = link_memory(memory, store, agent_type=agent_type)
    associations = updated.related_ids

    print(f'已保存: [{memory.id}] {memory.content[:50]}')
    print(f'关键词: {keywords}')
    print(f'标签: {tags}')
    print(f'重要度: {args.importance}')
    if associations:
        print(f'关联: {associations}')

    # 自动刷新索引
    _generate_index(store)


def _generate_index(store: MemoryStore) -> Path:
    """Generate MEMORY.md index grouped by memory type."""
    memories = store.load_all()

    type_order = ["user", "feedback", "task", "knowledge", "project", "reference"]
    grouped: dict[str, list[Memory]] = {t: [] for t in type_order}
    for mem in memories:
        mt = (mem.type or "task").strip().lower() or "task"
        if mt not in grouped:
            grouped[mt] = []
        grouped[mt].append(mem)

    lines: list[str] = ["# Memory Index", ""]
    for mt in type_order:
        items = grouped.get(mt, [])
        if not items:
            continue
        lines.append(f"## {mt.capitalize()}")
        for mem in sorted(items, key=lambda m: m.id):
            title = (mem.name or "").strip() or mem.id
            desc = (mem.description or "").strip() or (mem.context or "").strip() or mem.content.strip()
            desc = desc.replace("\n", " ")
            lines.append(f"- [{title}]({mem.id}.md) — {desc}")
        lines.append("")

    output = store.store_path / "MEMORY.md"
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output


def cmd_generate_index(args):
    """Generate MEMORY.md index in store directory."""
    store = get_store(args)
    output = _generate_index(store)
    print(f"索引已生成: {output}")


def cmd_export(args):
    """Export memories to Obsidian notes + graph."""
    from obsidian_export import export_all
    agent_name = getattr(args, 'agent', None)
    result = export_all(args.store, args.output, agent_name=agent_name)
    if result["status"] == "empty":
        print("No memories to export.")
    else:
        print(f"Exported {result['count']} memories to Obsidian")
        print(f"  MOC: {result['moc']}")
        print(f"  Graph: {result['graph']}")
        for p in result["notes"]:
            print(f"  Note: {p}")


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="Agent Memory CLI — 联想记忆系统命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--store",
        default=DEFAULT_STORE,
        help=f"记忆库目录路径（默认: {DEFAULT_STORE}）",
    )
    parser.add_argument(
        "--agent",
        type=str,
        default=None,
        help="角色名（如 kaze），使用该角色的个人记忆存储",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ---- retrieve ----
    p_retrieve = subparsers.add_parser("retrieve", help="检索记忆")
    p_retrieve.add_argument("query", help="搜索查询文本")
    p_retrieve.add_argument("--top-k", type=int, default=3, help="返回结果数（默认: 3）")
    p_retrieve.add_argument("--no-spread", action="store_true", help="禁用扩散激活")
    p_retrieve.add_argument(
        "--format",
        choices=["text", "prompt"],
        default="text",
        help="输出格式：text（默认）或 prompt（适合注入 subagent）",
    )

    # ---- add ----
    p_add = subparsers.add_parser("add", help="添加新记忆")
    p_add.add_argument("--subject", required=True, help="记忆主题（必填）")
    p_add.add_argument("--description", default="", help="详细描述")
    p_add.add_argument("--keywords", help="关键词，逗号分隔（默认使用 subject）")
    p_add.add_argument("--tags", help="标签，逗号分隔（默认: manual）")
    p_add.add_argument("--importance", type=int, default=5, help="重要性 1-10（默认: 5）")

    # ---- stats ----
    subparsers.add_parser("stats", help="显示统计信息")

    # ---- evolve ----
    p_evolve = subparsers.add_parser("evolve", help="更新记忆字段")
    p_evolve.add_argument("memory_id", help="要更新的记忆 ID")
    p_evolve.add_argument("--context", help="新的语境描述")
    p_evolve.add_argument("--tags", help="新标签，逗号分隔")

    # ---- list ----
    p_list = subparsers.add_parser("list", help="列出最近记忆")
    p_list.add_argument("--limit", type=int, default=20, help="最多显示条数（默认: 20）")

    # ---- export ----
    p_export = subparsers.add_parser("export", help="导出记忆到 Obsidian 笔记和图谱")
    p_export.add_argument(
        "--output",
        default=DEFAULT_EXPORT_DIR,
        help=f"输出目录（默认: {DEFAULT_EXPORT_DIR}）",
    )

    # ---- quick-add ----
    parser_quick_add = subparsers.add_parser("quick-add", help="直接保存记忆（无需 API）")
    parser_quick_add.add_argument("content", help="记忆内容")
    parser_quick_add.add_argument("--keywords", required=True, help="关键词（逗号分隔）")
    parser_quick_add.add_argument("--tags", default="task", help="标签（逗号分隔，默认 task）")
    parser_quick_add.add_argument("--importance", type=int, default=5, help="重要度 1-10（默认 5）")
    parser_quick_add.add_argument("--context", default="", help="上下文说明")
    parser_quick_add.add_argument("--name", default="", help="人类可读短名")
    parser_quick_add.add_argument("--description", default="", help="一句话摘要")
    parser_quick_add.add_argument(
        "--type",
        dest="type",
        choices=["user", "feedback", "task", "knowledge", "project", "reference"],
        default="task",
        help="记忆类型（默认 task）",
    )

    # ---- generate-index ----
    subparsers.add_parser("generate-index", help="按类型生成 MEMORY.md 索引")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "retrieve": cmd_retrieve,
        "add": cmd_add,
        "quick-add": cmd_quick_add,
        "generate-index": cmd_generate_index,
        "stats": cmd_stats,
        "evolve": cmd_evolve,
        "list": cmd_list,
        "export": cmd_export,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
