"""
This module fetches repository information from GitHub API.
"""
import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def fetch_repo_info(repo_full: str):
    """Fetch description and updated_at from GitHub API."""
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    url = f"https://api.github.com/repos/{repo_full}"

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if res.status_code != 200:
        return None

    data = res.json()

    description = data.get("description") or "No description provided."
    updated_raw = data.get("updated_at", "")

    return {
        "description": description,
        "updated_at": updated_raw[:10] if updated_raw else "Unknown",
    }
