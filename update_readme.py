"""
🎧 Script: update_readme.py
─────────────────────────────
Fetches music listening stats from Supabase views
and updates the GitHub profile README with a stylish summary.
─────────────────────────────
Date: 2025-10-18
"""

import os
from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_track(target: str):
    """Supabaseから再生数トップの曲を1件取得"""
    res = supabase.table(target).select("*").limit(1).execute()
    return res.data[0] if res.data else None


def create_svg(track: dict, filename: str):
    """透過背景・中央配置・空グラデーション・白文字で1曲表示するSVG"""
    os.makedirs("data", exist_ok=True)

    track_name = track.get("track_name", "No Data")
    artist_name = track.get("artist_name", "")
    play_count = track.get("play_count", 0)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300">
<style>
@keyframes rotate {{
  0% {{ transform: rotate(0deg); }}
  100% {{ transform: rotate(360deg); }}
}}
.rotating {{
  transform-origin: 150px 150px;
  animation: rotate 5s linear infinite;
}}
text {{
  fill: #fff;
  text-anchor: middle;
  font-family: 'Arial', sans-serif;
}}
</style>

<rect width="100%" height="100%" fill="transparent" />

<defs>
  <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#fbc2eb"/>
    <stop offset="100%" stop-color="#a6c1ee"/>
  </linearGradient>
</defs>

<g class="rotating">
    <circle cx="150" cy="150" r="125" fill="url(#skyGradient)" stroke="#fff" stroke-width="8"/>
</g>

<text x="150" y="125" font-size="20" fill="#ffffff">{artist_name}</text>
<text x="150" y="160" font-size="28" font-weight="bold" fill="#ffffff">{track_name}</text>
<text x="150" y="190" font-size="20" fill="#eeeeee">({play_count} plays)</text>

</svg>"""

    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ SVG generated: data/{filename}")


def generate_readme(top_track: dict | None, today_track: dict | None) -> str:
    """README.md を生成"""
    updated_time = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")

    return f"""
## 🫠  [k4nkan](https://kanta.it.com/)  

<table>
<tr>
<td align="center">Overview</td>
<td align="center">Languages</td>
<tr>
<td>
    <a href="https://github.com/k4nkan">
        <img height="150px" src="https://github-readme-stats.vercel.app/api?username=k4nkan&count_private=true&show_icons=true" />
    </a>
</td>
<td>
    <a href="https://github.com/k4nkan">
        <img height="150px" src="https://github-readme-stats.vercel.app/api/top-langs/?username=k4nkan&layout=compact" />
    </a>
</td>
</tr>
</table>

---

## 🎵 Favorite Tracks
<table border="0" cellspacing="0" cellpadding="0">
<tr>
<td align="center">Total</td>
<td align="center">Today</td>
</tr>
<tr>
<td align="center">
    <img src="./data/top_track.svg" alt="Top Track" width="150">
</td>
<td align="center">
    <img src="./data/today_track.svg" alt="Today's Track" width="150">
</td>
</tr>
</table>

---

## 📚 Log
- _[Last updated](https://github.com/k4nkan/k4nkan/actions): {updated_time}_
"""


if __name__ == "__main__":
    print("🎧 Fetching tracks...")
    top_track = fetch_track("top_tracks_all_time")
    today_track = fetch_track("top_tracks_today")

    if top_track:
        create_svg(top_track, "top_track.svg")
    if today_track:
        create_svg(today_track, "today_track.svg")

    readme = generate_readme(top_track, today_track)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md updated successfully!")
