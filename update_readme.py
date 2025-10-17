"""
🎧 Script: update_readme.py
─────────────────────────────
Fetches music listening stats from Supabase views
and updates the GitHub profile README with a stylish summary.
─────────────────────────────
Date: 2025-10-17
"""

import os
from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_view(view_name: str, limit: int = 5):
    """Fetch data from a Supabase view."""
    res = supabase.table(view_name).select("*").limit(limit).execute()
    return res.data or []


def format_track_row(track: dict) -> str:
    """Format a track record into a Markdown line with icons."""
    play_count = track.get("play_count", 0)
    return f"**{track['track_name']}** — *{track['artist_name']}* ({play_count} plays)"


def generate_readme(all_time: list, today: list) -> str:
    """Generate README.md content based on Supabase data."""

    # Header section
    header = """

### 🫠  k4nkan
- [ポートフォリオ](https://kanta.it.com/)  
- のびのびやってます  
- 暖かい目で見てください  

<table>
    <tr>
    <td>
        <a href="https://github.com/k4nkan">
            <img height="170px" src="https://github-readme-stats.vercel.app/api?username=k4nkan&count_private=true&show_icons=true" />
        </a>
    </td>
    <td>
        <a href="https://github.com/k4nkan">
            <img height="170px" src="https://github-readme-stats.vercel.app/api/top-langs/?username=k4nkan&layout=compact" />
        </a>
    </td>
    </tr>
</table>

---
"""

    # 🎵 お気に入りの曲
    section1 = "### 🎵 お気に入りの曲\n\n"
    if not all_time:
        section1 += "_No data available yet._\n"
    else:
        section1 += "\n".join([f"- {format_track_row(t)}" for t in all_time])
        section1 += "\n"

    section1 += "\n---\n\n"

    # 🎧 今日聴いた曲
    section2 = "### 🎧 今日聴いた曲\n\n"
    if not today:
        section2 += "_No songs played today yet._\n"
    else:
        section2 += "\n".join([f"- {format_track_row(t)}" for t in today])
        section2 += "\n"

    section2 += "\n---\n\n"

    # 📚 ログセクション
    updated_time = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")
    section3 = "### 📚 Log\n\n"
    section3 += f"- _[Song data last updated](https://github.com/k4nkan/k4nkan/actions): {updated_time}_\n"

    return header + section1 + section2 + section3


if __name__ == "__main__":
    print("Fetching data from Supabase views...")

    all_time = fetch_view("top_tracks_all_time", 5)
    today = fetch_view("top_tracks_today", 5)

    print(f"Fetched {len(all_time)} all-time tracks, {len(today)} today tracks.")

    readme = generate_readme(all_time, today)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("README.md updated successfully ✅")
