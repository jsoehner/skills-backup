#!/usr/bin/env python3
"""
Check Fork Guardrail & Upstream Maintenance Status

Evaluates whether a target repository is a GitHub fork and enforces upstream governance rules:
1. Avoid direct updates/modifications to forked repositories unless the upstream source
   is verified abandoned and unmaintained (>18 months inactivity, archived, or deleted).
2. Recommend or perform upstream refresh ('gh repo sync') before considering local changes.

Exit Codes:
  0 - Permitted to proceed (Standalone repository OR verified abandoned adopted fork).
  1 - BLOCKED (Repository is a fork with an active upstream; direct updates prohibited).
  2 - Error during repository inspection.
"""

import os
import sys
import json
import re
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone

def run_command(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def parse_iso_datetime(dt_str: str) -> datetime:
    """Parse ISO datetime string from GitHub API."""
    if not dt_str:
        return datetime.min.replace(tzinfo=timezone.utc)
    clean_dt = dt_str.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(clean_dt)
    except Exception:
        try:
            return datetime.strptime(dt_str[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

def extract_github_slug(remote_url: str) -> str:
    """Extract owner/repo from https or git SSH remote URL."""
    if not remote_url:
        return ""
    # Matches:
    # https://github.com/owner/repo.git
    # git@github.com:owner/repo.git
    # github.com/owner/repo
    m = re.search(r"github\.com[/:]([\w\-\.]+)/([\w\-\.]+?)(\.git)?$", remote_url.strip())
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return ""

def evaluate_repo(target: str, sync_if_needed: bool = False) -> dict:
    result = {
        "target": target,
        "is_git_repo": False,
        "is_fork": False,
        "decision": "UNKNOWN",
        "allowed_to_modify": False,
        "reason": "",
        "repo_slug": None,
        "upstream_parent": None,
        "upstream_archived": False,
        "upstream_last_push": None,
        "upstream_abandoned": False,
        "sync_available": False,
        "sync_status": "NOT_ATTEMPTED",
        "recommended_actions": []
    }

    target_path = Path(target).resolve() if os.path.exists(target) else None
    repo_cwd = str(target_path) if target_path and target_path.is_dir() else None

    repo_slug = ""
    upstream_slug = ""

    # Check git repo existence if local
    if repo_cwd:
        rc, _, _ = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_cwd)
        if rc == 0:
            result["is_git_repo"] = True
            # Get origin URL
            _, origin_url, _ = run_command(["git", "remote", "get-url", "origin"], cwd=repo_cwd)
            repo_slug = extract_github_slug(origin_url)
            # Check upstream remote URL if configured
            _, upstream_url, _ = run_command(["git", "remote", "get-url", "upstream"], cwd=repo_cwd)
            upstream_slug = extract_github_slug(upstream_url)
    elif "/" in target:
        repo_slug = target

    result["repo_slug"] = repo_slug

    gh_available = shutil.which("gh") is not None
    if not gh_available:
        if result["is_git_repo"]:
            if upstream_slug:
                result["is_fork"] = True
                result["upstream_parent"] = upstream_slug
                result["decision"] = "BLOCKED_ACTIVE_UPSTREAM"
                result["reason"] = f"Repository has upstream remote '{upstream_slug}' configured. Direct updates blocked without GitHub API verification."
                result["recommended_actions"].append("Verify upstream repository status or run 'git fetch upstream'.")
                return result
            else:
                result["is_fork"] = False
                result["decision"] = "ALLOWED_STANDALONE"
                result["allowed_to_modify"] = True
                result["reason"] = "Local git repository has no upstream remote configured (standalone)."
                return result
        result["decision"] = "ERROR"
        result["reason"] = "GitHub CLI ('gh') is not installed and target is not a local git repository."
        return result

    # Query repository via gh
    gh_view_cmd = ["gh", "repo", "view"]
    if repo_slug:
        gh_view_cmd.append(repo_slug)
    gh_view_cmd.extend(["--json", "name,owner,isFork,parent,isArchived,pushedAt,defaultBranchRef"])

    rc, stdout, stderr = run_command(gh_view_cmd, cwd=repo_cwd)
    if rc != 0:
        # If gh failed on default remote, fallback to upstream remote check
        if upstream_slug:
            result["is_fork"] = True
            result["upstream_parent"] = upstream_slug
            result["decision"] = "BLOCKED_ACTIVE_UPSTREAM"
            result["reason"] = f"Repository configured with upstream remote '{upstream_slug}'. Direct updates blocked."
            return result
        if result["is_git_repo"]:
            result["is_fork"] = False
            result["decision"] = "ALLOWED_STANDALONE"
            result["allowed_to_modify"] = True
            result["reason"] = f"GitHub metadata query failed ({stderr}). Presumed standalone local repo."
            return result
        result["decision"] = "ERROR"
        result["reason"] = f"Failed to inspect repository via gh CLI: {stderr}"
        return result

    try:
        repo_data = json.loads(stdout)
    except Exception as e:
        result["decision"] = "ERROR"
        result["reason"] = f"Failed to parse gh output: {e}"
        return result

    result["is_fork"] = repo_data.get("isFork", False) or bool(upstream_slug)

    if not result["is_fork"]:
        result["decision"] = "ALLOWED_STANDALONE"
        result["allowed_to_modify"] = True
        result["reason"] = "Repository is a standalone repository (not a fork)."
        result["recommended_actions"].append("Proceed with standard governance, dependency, and workflow operations.")
        return result

    # Repository IS A FORK
    parent_data = repo_data.get("parent")
    parent_full = ""
    if parent_data:
        parent_owner = parent_data.get("owner", {}).get("login", "")
        parent_name = parent_data.get("name", "")
        parent_full = f"{parent_owner}/{parent_name}"
    elif upstream_slug:
        parent_full = upstream_slug

    if not parent_full:
        result["decision"] = "BLOCKED_ACTIVE_UPSTREAM"
        result["reason"] = "Repository is flagged as a fork, but parent metadata could not be resolved."
        result["recommended_actions"].append("Verify fork upstream configuration manually before updating.")
        return result

    result["upstream_parent"] = parent_full

    # Query parent details from GitHub
    rc_p, stdout_p, stderr_p = run_command(["gh", "repo", "view", parent_full, "--json", "isArchived,pushedAt,latestRelease,defaultBranchRef"])
    if rc_p != 0:
        if "Could not resolve to a Repository" in stderr_p or "Not Found" in stderr_p or "404" in stderr_p:
            result["upstream_abandoned"] = True
            result["decision"] = "ALLOWED_ADOPTED_FORK"
            result["allowed_to_modify"] = True
            result["reason"] = f"Upstream parent '{parent_full}' is deleted or inaccessible (404). Repository is an Adopted Fork."
            result["recommended_actions"].append("Document upstream repository deletion in maintenance audit record.")
            return result
        else:
            result["decision"] = "BLOCKED_ACTIVE_UPSTREAM"
            result["reason"] = f"Could not verify status of upstream parent '{parent_full}': {stderr_p}"
            result["recommended_actions"].append("Verify upstream availability before modifying this fork.")
            return result

    try:
        p_info = json.loads(stdout_p)
    except Exception:
        p_info = {}

    is_archived = p_info.get("isArchived", False)
    result["upstream_archived"] = is_archived

    pushed_at_str = p_info.get("pushedAt")
    result["upstream_last_push"] = pushed_at_str
    last_push_dt = parse_iso_datetime(pushed_at_str)
    now_dt = datetime.now(timezone.utc)
    inactivity_period = now_dt - last_push_dt
    days_inactive = inactivity_period.days

    # Abandonment Criteria: Archived OR inactive > 548 days (18 months)
    if is_archived:
        result["upstream_abandoned"] = True
        result["decision"] = "ALLOWED_ADOPTED_FORK"
        result["allowed_to_modify"] = True
        result["reason"] = f"Upstream parent '{parent_full}' is officially archived. Repository is an Adopted Fork."
        result["recommended_actions"].append(f"Proceed with local maintenance on adopted fork '{repo_data.get('name', target)}'.")
        return result

    if days_inactive > 548:
        result["upstream_abandoned"] = True
        result["decision"] = "ALLOWED_ADOPTED_FORK"
        result["allowed_to_modify"] = True
        result["reason"] = f"Upstream parent '{parent_full}' has been inactive for {days_inactive} days (>18 months). Repository is an Adopted Fork."
        result["recommended_actions"].append(f"Proceed with local maintenance on adopted fork '{repo_data.get('name', target)}'.")
        return result

    # Upstream is ACTIVE and MAINTAINED
    result["upstream_abandoned"] = False
    result["decision"] = "BLOCKED_ACTIVE_UPSTREAM"
    result["allowed_to_modify"] = False
    target_display = repo_data.get('name', target)
    owner_display = repo_data.get('owner', {}).get('login', '')
    sync_target = f"{owner_display}/{target_display}" if owner_display else target_display
    result["reason"] = (
        f"Upstream parent '{parent_full}' is ACTIVE (last push {pushed_at_str}, {days_inactive} days ago). "
        "Direct updates, dependency bumps, and unilateral workflow injections on this fork are PROHIBITED."
    )
    result["sync_available"] = True
    result["recommended_actions"].extend([
        f"Refresh fork from upstream using: gh repo sync {sync_target}",
        "If proposing new features or bug fixes, create an isolated topic branch and submit a PR to UPSTREAM parent.",
        "Halt any automated governance or dependency updates on the fork's default branch."
    ])

    if sync_if_needed:
        sync_cmd = ["gh", "repo", "sync", sync_target]
        rc_s, out_s, err_s = run_command(sync_cmd, cwd=repo_cwd)
        if rc_s == 0:
            result["sync_status"] = "SYNCED_SUCCESSFULLY"
        else:
            result["sync_status"] = f"SYNC_FAILED: {err_s or out_s}"

    return result

def main():
    parser = argparse.ArgumentParser(
        description="Check if a target repository is a fork and enforce upstream maintenance guardrails."
    )
    parser.add_argument("target", nargs="?", default=".", help="Local path or remote GitHub repository identifier (default: current directory).")
    parser.add_argument("--sync", action="store_true", help="Attempt to run 'gh repo sync' if the repository is a fork.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output result as JSON for agent harnesses.")
    args = parser.parse_args()

    result = evaluate_repo(args.target, sync_if_needed=args.sync)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 80)
        print("🛡️  FORK & UPSTREAM REPOSITORY GUARDRAIL")
        print("=" * 80)
        print(f"Target Repository : {result['target']}")
        print(f"Repo Slug         : {result.get('repo_slug', 'N/A')}")
        print(f"Is Fork           : {'YES' if result['is_fork'] else 'NO'}")
        if result['is_fork']:
            print(f"Upstream Parent   : {result.get('upstream_parent', 'N/A')}")
            print(f"Upstream Status   : {'ARCHIVED' if result['upstream_archived'] else ('ABANDONED (>18 mo)' if result['upstream_abandoned'] else 'ACTIVE')}")
            print(f"Upstream Last Push: {result.get('upstream_last_push', 'N/A')}")
        print(f"Guardrail Decision: {result['decision']}")
        print(f"Allowed to Modify : {'✅ YES' if result['allowed_to_modify'] else '🛑 NO (BLOCKED)'}")
        print(f"Reason            : {result['reason']}")
        if result['recommended_actions']:
            print("\nRecommended Actions:")
            for act in result['recommended_actions']:
                print(f"  • {act}")
        if result.get("sync_status") != "NOT_ATTEMPTED":
            print(f"\nSync Action       : {result.get('sync_status')}")
        print("=" * 80)

    if result["decision"] == "ERROR":
        sys.exit(2)
    elif result["allowed_to_modify"]:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
