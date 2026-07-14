#!/usr/bin/env python3
"""
create-mr.py — Automatically create/update a GitLab Merge Request.

Usage:
  python3 scripts/create-mr.py                    # MR from current branch → upstream/main
  python3 scripts/create-mr.py --title "My title"  # Custom title
  python3 scripts/create-mr.py --source feat-xyz    # Custom source branch

Authentication:
  Uses credentials from git credential store (git config --global credential.helper store).
  Or set GITLAB_USERNAME and GITLAB_PASSWORD environment variables.

Configuration (env vars):
  GITLAB_URL          — GitLab instance URL (default: http://localhost:8002)
  UPSTREAM_PROJECT    — Target project path (default: imitoy/ai-team)
  FORK_PROJECT        — Source fork path (default: hermes-bot/ai-team)
  GITLAB_USERNAME     — GitLab username (default: hermes-bot)
  GITLAB_PASSWORD     — GitLab password
"""

import os
import re
import subprocess
import sys
import argparse

GITLAB_URL = os.environ.get("GITLAB_URL", "http://localhost:8002")
UPSTREAM = os.environ.get("UPSTREAM_PROJECT", "imitoy/ai-team")
FORK = os.environ.get("FORK_PROJECT", "hermes-bot/ai-team")
USERNAME = os.environ.get("GITLAB_USERNAME", "hermes-bot")
PASSWORD = os.environ.get("GITLAB_PASSWORD", "")


def get_git_credential(url: str) -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input=f"url={url}\n",
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")
        user, pwd = "", ""
        for line in lines:
            if line.startswith("username="):
                user = line.split("=", 1)[1]
            elif line.startswith("password="):
                pwd = line.split("=", 1)[1]
        return user, pwd
    except Exception:
        return "", ""


def get_current_branch() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return r.stdout.strip()
    except Exception:
        return "main"


def get_tip_commit_message() -> str:
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True, text=True, timeout=5
        )
        return r.stdout.strip()
    except Exception:
        return ""


def create_merge_request(
    source_branch: str,
    target_branch: str = "main",
    title: str | None = None,
    description: str | None = None,
) -> str | None:
    import requests as req

    username = USERNAME
    password = PASSWORD
    if not password:
        user, pwd = get_git_credential(GITLAB_URL)
        if user and pwd:
            username = user
            password = pwd

    if not password:
        print("Error: No password. Set GITLAB_PASSWORD or configure git credential store.")
        return None

    session = req.Session()

    # Login
    login_resp = session.get(f"{GITLAB_URL}/users/sign_in")
    m = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', login_resp.text)
    login_token = m.group(1) if m else ""
    session.post(f"{GITLAB_URL}/users/sign_in", data={
        "user[login]": username,
        "user[password]": password,
        "authenticity_token": login_token,
    }, allow_redirects=True)

    # Get MR creation page
    params = {
        "merge_request[source_branch]": source_branch,
        "merge_request[target_branch]": target_branch,
    }
    new_mr_url = f"{GITLAB_URL}/{FORK}/-/merge_requests/new"
    mr_page = session.get(new_mr_url, params=params)

    # Check if MR already exists
    existing = re.findall(r'href="(/[^"]*merge_request[^"]*\d+)"', mr_page.text)
    for link in existing:
        if UPSTREAM in link and "merge_requests" in link:
            print(f"  ✓ MR already exists: {GITLAB_URL}{link}")
            return f"{GITLAB_URL}{link}"

    # Try to create
    m = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', mr_page.text)
    csrf = m.group(1) if m else ""
    if not csrf:
        print("Error: Cannot find CSRF token on MR page")
        print("  (page may have unexpected content, try --source with a different branch)")
        return None

    # Extract target project ID from the page
    tp_match = re.search(r'target_project_id[^=]*=(\d+)', mr_page.text)
    target_project_id = tp_match.group(1) if tp_match else ""

    # Also extract diff_head_sha
    sha_match = re.search(r'name="merge_request_diff_head_sha"[^>]*value="([^"]+)"', mr_page.text)
    diff_sha = sha_match.group(1) if sha_match else ""

    if not title:
        title = get_tip_commit_message() or f"Merge branch '{source_branch}'"
    if not description:
        description = (
            f"Auto-generated merge request from `{source_branch}` → `{UPSTREAM}:{target_branch}`\n\n"
            f"Created by scripts/create-mr.py"
        )

    create_data = {
        "authenticity_token": csrf,
        "merge_request_diff_head_sha": diff_sha,
        "merge_request[source_branch]": source_branch,
        "merge_request[target_branch]": target_branch,
        "merge_request[target_project_id]": target_project_id,
        "merge_request[title]": title,
        "merge_request[description]": description,
    }

    create_url = f"{GITLAB_URL}/{FORK}/-/merge_requests"
    result = session.post(create_url, data=create_data, allow_redirects=False)

    if result.status_code == 302:
        location = result.headers.get("Location", "")
        print(f"  ✓ MR created: {location}")
        return location
    else:
        print(f"  ✗ Failed (HTTP {result.status_code}): {result.text[:200]}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Auto-create GitLab Merge Request")
    parser.add_argument("--source", default=None)
    parser.add_argument("--target", default="main")
    parser.add_argument("--title", default=None)
    parser.add_argument("--description", default=None)
    args = parser.parse_args()

    source = args.source or get_current_branch()
    print(f"MR: {FORK}:{source} → {UPSTREAM}:{args.target}")

    url = create_merge_request(source, args.target, args.title, args.description)
    if url:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())