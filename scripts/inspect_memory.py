#!/usr/bin/env python3
"""
Inspect Local Memory System (OKF Policies & ChromaDB Context)

Provides human-readable inspection, searching, and JSON output of knowledge
captured in both:
1. OKF (Deterministic Rules, Architecture Standards, and Policies)
2. ChromaDB (Semantic Memory, Bug Fixes, Troubleshooting Logs, and Context)
"""

import os
import sys
import re
import json
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Reconfigure stdout/stderr for Unicode support on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def get_memory_paths() -> Tuple[Path, Path, Path, Path]:
    """Resolve standard local memory system directories."""
    mem_root = Path(os.environ.get("MEMORY_SYSTEM_ROOT", Path.home() / "memory_system")).resolve()
    mem_db = Path(os.environ.get("MEMORY_DB", mem_root / "db")).resolve()
    mem_okf = Path(os.environ.get("MEMORY_OKF", mem_root / "knowledge" / "okf")).resolve()
    mem_inbox = Path(os.environ.get("MEMORY_INBOX", mem_root / "inbox")).resolve()
    return mem_root, mem_db, mem_okf, mem_inbox

def parse_memory_document(text: str, filename: str = "", default_type: str = "Unclassified") -> Dict[str, str]:
    """
    Parse title, type, domain, and a clean human-readable summary from markdown content.
    Extracts structured metadata while stripping excessive markdown noise.
    """
    lines = [line.rstrip() for line in (text or "").splitlines()]
    title = ""
    doc_type = default_type
    domain = ""
    summary = ""

    # Check for YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            for line in fm.splitlines():
                if line.startswith("name:"):
                    title = f"Skill: {line.split(':', 1)[1].strip()}"
                    doc_type = "Skill Specification"
                elif line.startswith("description:"):
                    summary = line.split(":", 1)[1].strip()

    # Extract headers and metadata keys
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if not title:
            if s.startswith("# OKF Decision:") or s.startswith("# OKF Decision -"):
                title = s.split(":", 1)[1].strip() if ":" in s else s.split("-", 1)[1].strip()
            elif s.startswith("# Chroma Context:") or s.startswith("# Chroma Context -"):
                title = s.split(":", 1)[1].strip() if ":" in s else s.split("-", 1)[1].strip()
            elif s.startswith("# ") and s not in ("# OKF Decision", "# Chroma Context"):
                title = s[2:].strip()
        if s.lower().startswith("title:") and (not title or title in ("# OKF Decision", "OKF Decision", "Chroma Context")):
            title = s.split(":", 1)[1].strip()
        if s.lower().startswith("type:"):
            doc_type = s.split(":", 1)[1].strip()
        elif s.lower().startswith("domain:"):
            domain = s.split(":", 1)[1].strip()
        elif s.lower().startswith("summary:") and not summary:
            summary = s.split(":", 1)[1].strip()

    if not title:
        title = filename or "Untitled Memory Entry"

    # If title still generic, refine from filename or first sentence
    if title.lower() in ("okf decision", "# okf decision", "chroma context", "# chroma context"):
        clean_stem = Path(filename).stem.replace("_", " ").replace("-", " ").title()
        title = clean_stem if clean_stem else title

    # Extract summary if not explicitly provided
    if not summary:
        in_summary_sec = False
        body_candidates = []
        for line in lines:
            s = line.strip()
            if not s or s.startswith("---"):
                continue
            if s.lower().startswith("## summary") or s.lower().startswith("## overview"):
                in_summary_sec = True
                continue
            if in_summary_sec:
                if s.startswith("#"):
                    break
                body_candidates.append(s)
            elif not s.startswith("#") and not s.lower().startswith((
                "type:", "domain:", "date:", "status:", "component:", "system:",
                "**date:", "**component:", "**document version:", "**status:"
            )):
                body_candidates.append(s)

        if body_candidates:
            summary = " ".join(body_candidates[:2])

    # Strip markdown syntax symbols (*, _, `, #, [[, ]]) for human viewing
    summary = re.sub(r"[\*_`#]", "", summary).strip()
    summary = re.sub(r"\s+", " ", summary)

    return {
        "title": title,
        "type": doc_type,
        "domain": domain,
        "summary": summary,
        "content": text
    }

def load_okf_entries(okf_dir: Path) -> List[Dict[str, Any]]:
    """Load and parse all OKF policy markdown documents."""
    entries = []
    if not okf_dir.exists():
        return entries

    for fpath in sorted(okf_dir.glob("*.md")):
        if not fpath.is_file():
            continue
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
            mtime = fpath.stat().st_mtime
            size = fpath.stat().st_size
            dt_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            parsed = parse_memory_document(content, filename=fpath.name, default_type="Policy")
            entries.append({
                "storage": "OKF",
                "filename": fpath.name,
                "path": str(fpath),
                "size_bytes": size,
                "updated": dt_str,
                **parsed
            })
        except Exception:
            continue
    return entries

def load_chroma_entries(db_dir: Path) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Load ChromaDB records directly from SQLite without relying on third-party python modules.
    Guarantees zero-dependency resilience and instant execution.
    """
    entries = []
    collection_name = "memory_context"
    db_file = db_dir / "chroma.sqlite3"
    if not db_file.exists():
        return collection_name, entries

    try:
        conn = sqlite3.connect(str(db_file))
        c = conn.cursor()

        # Query collection name
        try:
            c.execute("SELECT name FROM collections LIMIT 1")
            col_row = c.fetchone()
            if col_row and col_row[0]:
                collection_name = col_row[0]
        except Exception:
            pass

        # Query records with joined metadata and FTS content
        query = """
        SELECT e.embedding_id, e.created_at, m.string_value AS source, f.c0 AS doc
        FROM embeddings e
        LEFT JOIN embedding_metadata m ON e.id = m.id AND m.key = 'source'
        LEFT JOIN embedding_fulltext_search_content f ON e.id = f.rowid
        ORDER BY e.created_at DESC
        """
        c.execute(query)
        rows = c.fetchall()
        for eid, created, src, doc in rows:
            parsed = parse_memory_document(doc or "", filename=src or eid, default_type="Context / Troubleshooting")
            entries.append({
                "storage": "ChromaDB",
                "id": eid,
                "created": str(created),
                "source": src or "unknown",
                **parsed
            })
        conn.close()
    except Exception:
        pass

    return collection_name, entries

def get_inbox_stats(inbox_dir: Path) -> Dict[str, int]:
    """Get counts of pending, processed, and errored ingestion files."""
    stats = {"pending": 0, "processed": 0, "error": 0}
    if not inbox_dir.exists():
        return stats

    try:
        stats["pending"] = len([f for f in inbox_dir.glob("*.md") if f.is_file()])
        proc_dir = inbox_dir / "processed"
        if proc_dir.exists():
            stats["processed"] = len([f for f in proc_dir.glob("*.md") if f.is_file()])
        err_dir = inbox_dir / "error"
        if err_dir.exists():
            stats["error"] = len([f for f in err_dir.glob("*.md") if f.is_file()])
    except Exception:
        pass
    return stats

def matches_query(entry: Dict[str, Any], query: str) -> bool:
    """Case-insensitive matching across entry fields and full text."""
    q = query.lower()
    fields = [
        entry.get("title", ""),
        entry.get("filename", ""),
        entry.get("id", ""),
        entry.get("source", ""),
        entry.get("type", ""),
        entry.get("domain", ""),
        entry.get("summary", ""),
        entry.get("content", "")
    ]
    return any(q in f.lower() for f in fields)

def format_size(bytes_count: int) -> str:
    """Format bytes into a human-friendly string."""
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    return f"{bytes_count / (1024 * 1024):.1f} MB"

def wrap_text(text: str, width: int = 76, indent: str = "    ") -> str:
    """Simple word-wrap helper for human-readable terminal output."""
    if not text:
        return ""
    words = text.split()
    lines = []
    cur_line = []
    cur_len = 0
    max_len = width - len(indent)

    for word in words:
        if cur_len + len(word) + (1 if cur_line else 0) <= max_len:
            cur_line.append(word)
            cur_len += len(word) + (1 if len(cur_line) > 1 else 0)
        else:
            if cur_line:
                lines.append(indent + " ".join(cur_line))
            cur_line = [word]
            cur_len = len(word)

    if cur_line:
        lines.append(indent + " ".join(cur_line))
    return "\n".join(lines)

def display_memory(
    search_query: Optional[str] = None,
    show_details: bool = False,
    okf_only: bool = False,
    chroma_only: bool = False,
    json_output: bool = False
) -> None:
    """
    Main presentation routine. Renders human-readable memory contents or machine-readable JSON.
    """
    mem_root, mem_db, mem_okf, mem_inbox = get_memory_paths()

    okf_entries = load_okf_entries(mem_okf)
    col_name, chroma_entries = load_chroma_entries(mem_db)
    inbox_stats = get_inbox_stats(mem_inbox)

    # Apply search filtering if specified
    if search_query:
        okf_entries = [e for e in okf_entries if matches_query(e, search_query)]
        chroma_entries = [e for e in chroma_entries if matches_query(e, search_query)]

    # Machine-readable output for agent harnesses or pipelines
    if json_output:
        result = {
            "root_dir": str(mem_root),
            "status": {
                "root_exists": mem_root.exists(),
                "okf_exists": mem_okf.exists(),
                "chroma_exists": (mem_db / "chroma.sqlite3").exists(),
                "inbox_exists": mem_inbox.exists()
            },
            "inbox_stats": inbox_stats,
            "okf_collection": {
                "count": len(okf_entries),
                "entries": [
                    {k: v for k, v in e.items() if show_details or k != "content"}
                    for e in okf_entries
                ]
            },
            "chroma_collection": {
                "collection_name": col_name,
                "count": len(chroma_entries),
                "entries": [
                    {k: v for k, v in e.items() if show_details or k != "content"}
                    for e in chroma_entries
                ]
            }
        }
        print(json.dumps(result, indent=2))
        return

    # Human-readable terminal output
    print("=" * 80)
    print("🧠 LOCAL AGENT MEMORY & RETRIEVAL SYSTEM")
    print("=" * 80)
    print("Multi-tiered local storage for agent learnings, architectural policies, and context.")
    if search_query:
        print(f"🔍 Filtered by search keyword: '{search_query}'")
    print()

    # Host & Storage Status Box
    print("📁 Storage Layout & Host Status:")
    print("-" * 80)
    root_status = "✅ Present" if mem_root.exists() else "❌ Not found"
    okf_status = f"✅ Present ({len(okf_entries)} policies)" if mem_okf.exists() else "❌ Not found"
    chroma_db_file = mem_db / "chroma.sqlite3"
    chroma_status = f"✅ Present ({len(chroma_entries)} records in '{col_name}')" if chroma_db_file.exists() else "❌ Not found"
    inbox_status = f"✅ Present ({inbox_stats['pending']} pending, {inbox_stats['processed']} processed)" if mem_inbox.exists() else "❌ Not found"

    print(f"  • Root Directory  : {str(mem_root):<40} [{root_status}]")
    print(f"  • OKF Policies    : {str(mem_okf):<40} [{okf_status}]")
    print(f"  • ChromaDB Vector : {str(mem_db):<40} [{chroma_status}]")
    print(f"  • Ingest Inbox    : {str(mem_inbox):<40} [{inbox_status}]")
    print("-" * 80)

    # 1. OKF Deterministic Policies Section
    if not chroma_only:
        print("\n" + "=" * 80)
        print(f"📋 DETERMINISTIC RULES & POLICIES (OKF) — {len(okf_entries)} items")
        print("=" * 80)
        print("High-rigidity policies, ADR summaries, and architectural standards (Markdown).\n")

        if not okf_entries:
            if search_query:
                print("  ℹ️  No OKF policies matched the search query.")
            else:
                print(f"  ℹ️  No policies currently stored in {mem_okf}")
        else:
            for i, entry in enumerate(okf_entries, 1):
                size_str = format_size(entry["size_bytes"])
                domain_str = f" | Domain: {entry['domain']}" if entry.get("domain") else ""
                print(f"[{i}] {entry['title']}")
                print(f"    • File     : {entry['filename']} ({size_str})")
                print(f"    • Type     : {entry['type']}{domain_str}")
                print(f"    • Modified : {entry['updated']}")
                if entry.get("summary"):
                    print("    • Summary  :")
                    print(wrap_text(entry["summary"], indent="        "))

                if show_details:
                    print("    • Content  :")
                    border = "        " + "-" * 68
                    print(border)
                    for c_line in entry["content"].splitlines():
                        print(f"        {c_line}")
                    print(border)
                print()

    # 2. ChromaDB Semantic Context Section
    if not okf_only:
        print("=" * 80)
        print(f"🔍 SEMANTIC MEMORY & INCIDENT CONTEXT (ChromaDB) — {len(chroma_entries)} items")
        print("=" * 80)
        print(f"Vector-indexed troubleshooting logs, bug fixes, and context in collection '{col_name}'.\n")

        if not chroma_entries:
            if search_query:
                print("  ℹ️  No ChromaDB records matched the search query.")
            else:
                print(f"  ℹ️  No records currently stored in ChromaDB ({mem_db})")
        else:
            for i, entry in enumerate(chroma_entries, 1):
                domain_str = f" | Domain: {entry['domain']}" if entry.get("domain") else ""
                print(f"[{i}] {entry['title']}")
                print(f"    • ID       : {entry['id']}")
                print(f"    • Source   : {entry['source']}")
                print(f"    • Type     : {entry['type']}{domain_str}")
                print(f"    • Indexed  : {entry['created']}")
                if entry.get("summary"):
                    print("    • Excerpt  :")
                    print(wrap_text(entry["summary"], indent="        "))

                if show_details:
                    print("    • Content  :")
                    border = "        " + "-" * 68
                    print(border)
                    for c_line in entry["content"].splitlines():
                        print(f"        {c_line}")
                    print(border)
                print()

    # 3. Footer & Quick Tips
    print("=" * 80)
    print("💡 Memory Tips & Commands:")
    print("-" * 80)
    print("  • Search memories   : ./setup.sh --memory -q <keyword>")
    print("  • Full text details : ./setup.sh --memory --details")
    print("  • Ingest knowledge  : python3 ~/memory_system/capture_knowledge.py <file.md>")
    print("  • Drop for ingest   : cp <notes.md> ~/memory_system/inbox/")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="Inspect and search knowledge stored in local OKF and ChromaDB memory systems."
    )
    parser.add_argument("-q", "--search", dest="search", default=None,
                        help="Search stored memory entries by keyword (title, summary, or content)")
    parser.add_argument("-d", "--details", dest="details", action="store_true",
                        help="Display full document content instead of just summaries")
    parser.add_argument("--okf", action="store_true",
                        help="Show only OKF rules and architectural policies")
    parser.add_argument("--chroma", action="store_true",
                        help="Show only ChromaDB semantic memory entries")
    parser.add_argument("--json", action="store_true",
                        help="Output memory records in structured JSON format for agent harnesses")

    args = parser.parse_args()
    display_memory(
        search_query=args.search,
        show_details=args.details,
        okf_only=args.okf,
        chroma_only=args.chroma,
        json_output=args.json
    )

if __name__ == "__main__":
    main()
