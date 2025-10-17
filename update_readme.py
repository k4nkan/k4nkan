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
    emoji = "💿" if play_count > 5 else "🎵" if play_count > 1 else "🎶"
    return f"{emoji} **{track['track_name']}** — *{track['artist_name']}* ({play_count} plays)"


def generate_readme(all_time: list, today: list) -> str:
    """Generate README.md content based on Supabase data."""
    # Header section
    header = """# 🎧 My Spotify Listening Stats

---

"""

    # All-time favorites section
    section1 = "## 🔁 All-Time Favorites\n\n"
    if not all_time:
        section1 += "_No data available yet._\n"
    else:
        section1 += "\n".join([f"- {format_track_row(t)}" for t in all_time])
        section1 += "\n"

    # Divider
    divider = "\n\n---\n\n"

    # Today's top tracks section
    section2 = "## ☀️ Today's Most Played\n\n"
    if not today:
        section2 += "_No songs played today yet._\n"
    else:
        section2 += "\n".join([f"- {format_track_row(t)}" for t in today])
        section2 += "\n"

    # Footer section
    footer = f"""
---

🕒 _Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_

"""

    return header + section1 + divider + section2 + footer


if __name__ == "__main__":
    print("Fetching data from Supabase views...")

    all_time = fetch_view("top_tracks_all_time", 5)
    today = fetch_view("top_tracks_today", 5)

    print(f"Fetched {len(all_time)} all-time tracks, {len(today)} today tracks.")

    readme = generate_readme(all_time, today)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("README.md updated successfully")
