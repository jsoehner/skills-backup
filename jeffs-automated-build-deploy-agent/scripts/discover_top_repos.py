#!/usr/bin/env python3
"""Discover the top N most active non-fork, non-archived GitHub repositories by commit count."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

GRAPHQL_QUERY = """
query($login: String!, $limit: Int!) {
  user(login: $login) {
    repositories(first: $limit, isFork: false, isArchived: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes {
        name
        nameWithOwner
        isPrivate
        pushedAt
        updatedAt
        primaryLanguage { name }
        defaultBranchRef {
          name
          target {
            ... on Commit {
              history(first: 1) {
                totalCount
              }
            }
          }
        }
      }
    }
  }
}
"""


def rank_repositories(nodes: list[dict], top: int = 25) -> list[dict]:
    """Rank repository GraphQL nodes by descending commit count, then name."""
    return sorted(
        (
            {
                "name": n["name"],
                "nameWithOwner": n["nameWithOwner"],
                "isPrivate": n["isPrivate"],
                "primaryLanguage": (n.get("primaryLanguage") or {}).get("name") or "None",
                "commits": ((n.get("defaultBranchRef") or {}).get("target") or {}).get("history", {}).get("totalCount", 0),
                "defaultBranch": (n.get("defaultBranchRef") or {}).get("name") or "main",
                "pushedAt": n["pushedAt"],
            }
            for n in nodes
            if isinstance(n, dict)
        ),
        key=lambda r: (-r["commits"], r["name"].lower()),
    )[:top]


def format_tsv(ranked: list[dict]) -> str:
    lines = []
    for idx, r in enumerate(ranked, 1):
        vis = "private" if r["isPrivate"] else "public"
        lines.append(f"{idx}\t{r['commits']}\t{r['name']}\t{vis}\t{r['primaryLanguage']}\t{r['pushedAt']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rank non-fork GitHub repos by commit activity.")
    parser.add_argument("--owner", default="jsoehner", help="GitHub username (default: jsoehner)")
    parser.add_argument("--top", type=int, default=25, help="Number of top active repos to return (default: 25)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of TSV")
    args = parser.parse_args(argv)

    proc = subprocess.run(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={GRAPHQL_QUERY}",
            "-f",
            f"login={args.owner}",
            "-F",
            "limit=100",
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode

    payload = json.loads(proc.stdout)
    user = (payload.get("data") or {}).get("user")
    if not isinstance(user, dict):
        errors = payload.get("errors") or [{"message": f"User '{args.owner}' not found"}]
        print(json.dumps(errors), file=sys.stderr)
        return 1

    nodes = (user.get("repositories") or {}).get("nodes") or []
    ranked = rank_repositories(nodes, top=args.top)

    if args.json:
        print(json.dumps(ranked, indent=2))
    else:
        tsv = format_tsv(ranked)
        if tsv:
            print(tsv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
