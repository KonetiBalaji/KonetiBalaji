#!/usr/bin/env python3
"""
Dynamic README Updater for KonetiBalaji GitHub Profile.

Fetches latest public repositories via the GitHub API and updates
the Goals & Focus section and Last Updated timestamp in README.md.
Uses HTML comment markers for reliable section replacement.
"""

from __future__ import annotations

import io
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Windows encoding fix (emoji support in terminals)
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GITHUB_USERNAME = "KonetiBalaji"
README_PATH = "README.md"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2  # seconds — doubles on each retry
REPOS_TO_SHOW = 3

# Section markers (HTML comments — invisible in rendered markdown)
GOALS_START = "<!-- GOALS:START -->"
GOALS_END = "<!-- GOALS:END -->"
UPDATED_START = "<!-- UPDATED:START -->"
UPDATED_END = "<!-- UPDATED:END -->"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RepoInfo:
    """Structured representation of a GitHub repository."""

    name: str
    url: str
    description: str
    language: Optional[str]
    stars: int
    forks: int
    days_ago: int

    @property
    def time_ago(self) -> str:
        """Human-friendly relative time string."""
        if self.days_ago == 0:
            return "today"
        if self.days_ago == 1:
            return "yesterday"
        if self.days_ago < 7:
            return f"{self.days_ago} days ago"
        if self.days_ago < 30:
            weeks = self.days_ago // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        if self.days_ago < 365:
            months = self.days_ago // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        years = self.days_ago // 365
        return f"{years} year{'s' if years != 1 else ''} ago"


# ---------------------------------------------------------------------------
# GitHub API client
# ---------------------------------------------------------------------------
class GitHubAPI:
    """Thin GitHub REST API client with automatic retry and backoff."""

    def __init__(self, token: Optional[str] = None) -> None:
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "KonetiBalaji-README-Updater",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"token {token}"
            log.info("Authenticated with GitHub token")
        else:
            log.warning("No token — using unauthenticated API (60 req/hr limit)")

    # ---- internal -----------------------------------------------------------

    def _request_with_retry(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> Optional[list | dict]:
        """GET *endpoint* with exponential-backoff retry on transient errors."""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, params=params, timeout=30)

                if resp.status_code == 200:
                    return resp.json()

                # Rate-limited
                if resp.status_code == 403:
                    remaining = resp.headers.get("X-RateLimit-Remaining", "?")
                    reset_ts = resp.headers.get("X-RateLimit-Reset", "?")
                    log.error(
                        "Rate-limited (403). Remaining: %s, Reset: %s",
                        remaining,
                        reset_ts,
                    )
                # Server error — retryable
                elif resp.status_code >= 500:
                    log.warning("Server error %s on attempt %d", resp.status_code, attempt)
                else:
                    body = resp.text
                    try:
                        data = resp.json()
                        if isinstance(data, dict):
                            body = data.get("message", body)
                    except (ValueError, KeyError):
                        pass
                    log.error("API error %s: %s", resp.status_code, body)
                    return None

                if attempt < MAX_RETRIES:
                    wait = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    log.info("Retrying in %ds (attempt %d/%d)…", wait, attempt, MAX_RETRIES)
                    time.sleep(wait)

            except requests.exceptions.Timeout:
                log.warning("Timeout on attempt %d/%d", attempt, MAX_RETRIES)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_BASE_DELAY)
            except requests.exceptions.RequestException as exc:
                log.error("Request failed: %s", exc)
                return None

        log.error("All %d attempts exhausted for %s", MAX_RETRIES, endpoint)
        return None

    # ---- public -------------------------------------------------------------

    def get_latest_repos(
        self,
        username: str,
        count: int = REPOS_TO_SHOW,
    ) -> list[RepoInfo]:
        """Return the *count* most-recently-pushed public repos for *username*."""
        data = self._request_with_retry(
            f"/users/{username}/repos",
            params={
                "type": "public",
                "sort": "pushed",
                "direction": "desc",
                "per_page": count,
            },
        )

        if not data:
            return []

        now = datetime.now(timezone.utc)
        repos: list[RepoInfo] = []

        for repo in data[:count]:
            pushed_at = datetime.fromisoformat(
                repo["pushed_at"].replace("Z", "+00:00")
            )
            days_ago = (now - pushed_at).days

            description = repo.get("description") or ""
            if len(description) > 100:
                description = description[:97] + "…"

            repos.append(
                RepoInfo(
                    name=repo["name"],
                    url=repo["html_url"],
                    description=description,
                    language=repo.get("language"),
                    stars=repo["stargazers_count"],
                    forks=repo["forks_count"],
                    days_ago=days_ago,
                )
            )

        return repos


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------

def generate_goals_section(repos: list[RepoInfo]) -> str:
    """Render the *Goals & Focus* section body from a list of repos."""
    if not repos:
        return "Currently building exciting new projects — check back soon!\n"

    lines: list[str] = ["Currently working on my latest projects:\n"]

    for repo in repos:
        # Repo name as bold link
        lines.append(f"**🔭 [{repo.name}]({repo.url})**  ")

        # Description (only when meaningful)
        if repo.description:
            lines.append(f"{repo.description}  ")

        # Metadata chips
        meta: list[str] = []
        if repo.language:
            meta.append(f"`{repo.language}`")
        meta.append(f"*Updated {repo.time_ago}*")
        if repo.stars > 0:
            meta.append(f"⭐ {repo.stars}")
        if repo.forks > 0:
            meta.append(f"🍴 {repo.forks}")

        lines.append(" · ".join(meta))
        lines.append("")  # blank line between repos

    return "\n".join(lines) + "\n"


def generate_timestamp() -> str:
    """Render the auto-update footer timestamp."""
    now = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    return f'<div align="center"><sub>🤖 Auto-updated on {now}</sub></div>\n'


# ---------------------------------------------------------------------------
# Section replacer
# ---------------------------------------------------------------------------

def update_section(
    content: str,
    start_marker: str,
    end_marker: str,
    new_body: str,
) -> str:
    """Replace everything between *start_marker* and *end_marker* (inclusive)."""
    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
    replacement = f"{start_marker}\n{new_body}{end_marker}"
    updated, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        log.warning("Markers not found: %s … %s", start_marker, end_marker)
        return content

    log.info("Updated section: %s", start_marker)
    return updated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    """Entry point — returns 0 on success, 1 on failure."""
    log.info("README Updater starting for %s", GITHUB_USERNAME)

    # Resolve token (GitHub Actions injects GITHUB_TOKEN; PAT_TOKEN is manual)
    token = os.environ.get("PAT_TOKEN") or os.environ.get("GITHUB_TOKEN")

    api = GitHubAPI(token=token)
    repos = api.get_latest_repos(GITHUB_USERNAME)

    if not repos:
        log.error("Failed to fetch repositories — aborting")
        return 1

    log.info("Fetched %d repositories:", len(repos))
    for r in repos:
        log.info("  • %s (%s)", r.name, r.time_ago)

    # Read current README
    try:
        with open(README_PATH, "r", encoding="utf-8") as fh:
            content = fh.read()
    except FileNotFoundError:
        log.error("%s not found", README_PATH)
        return 1

    # Update dynamic sections
    content = update_section(content, GOALS_START, GOALS_END, generate_goals_section(repos))
    content = update_section(content, UPDATED_START, UPDATED_END, generate_timestamp())

    # Write back
    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)

    log.info("README.md updated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())