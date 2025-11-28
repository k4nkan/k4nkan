"""
🎧 Script: update_readme.py
─────────────────────────────
Fetches music listening stats from Supabase views
and updates the GitHub profile README with a stylish summary.
─────────────────────────────
Date: 2025-10-23
"""

import os
from datetime import datetime, timezone
from supabase import create_client

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def read_template(path: str) -> str:
    """テンプレートファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def fetch_track(target: str):
    """Supabaseから再生数トップの曲を1件取得"""
    res = supabase.table(target).select("*").limit(1).execute()
    return res.data[0] if res.data else None


def create_svg(track: dict, filename: str):
    """テンプレートを使ってSVG生成"""
    os.makedirs("data", exist_ok=True)

    svg_template = read_template("templates/track_template.svg")

    svg_filled = (
        svg_template
        .replace("{{ track_name }}", track.get("track_name", "No Data"))
        .replace("{{ artist_name }}", track.get("artist_name", ""))
        .replace("{{ play_count }}", str(track.get("play_count", 0)))
    )

    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        f.write(svg_filled)
    print(f"✅ SVG generated: data/{filename}")


def generate_readme() -> str:
    """READMEテンプレートに時刻を埋め込み"""
    template = read_template("templates/readme_template.md")
    updated_time = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")
    return template.replace("{{ updated_time }}", updated_time)


if __name__ == "__main__":
    print("🎧 Fetching tracks...")

    top_track = fetch_track("top_tracks_all_time")
    today_track = fetch_track("top_tracks_today")

    if top_track:
        create_svg(top_track, "top_track.svg")
    if today_track:
        create_svg(today_track, "today_track.svg")

    readme = generate_readme()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md updated successfully!")
