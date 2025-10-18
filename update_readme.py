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


def fetch_top_track():
    """Supabaseから再生数トップの曲を1件取得"""
    res = supabase.table("top_tracks_all_time").select("*").limit(1).execute()
    return res.data[0] if res.data else None


def create_svg(track: dict):
    """透過背景・中央配置・白背景黒文字・1曲だけ表示するSVGを生成"""
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
circle {{
  fill: none;
  stroke: #000;
  stroke-width: 2;
  cx: 150;
  cy: 150;
  r: 100;
  transform-origin: 150px 150px;
  animation: rotate 10s linear infinite;
}}
text {{
  fill: #000;
  text-anchor: middle;
  font-family: 'Arial', sans-serif;
}}
</style>

<rect width="100%" height="100%" fill="transparent" />
<circle />
<text x="150" y="135" font-size="14">{artist_name}</text>
<text x="150" y="160" font-size="18" font-weight="bold">{track_name}</text>
<text x="150" y="185" font-size="12">({play_count} plays)</text>
</svg>"""

    with open("data/top_track.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✅ SVG generated: data/top_track.svg")


def generate_readme(track: dict) -> str:
    """README.md を生成"""

    track_name = track.get("track_name", "No Data")
    artist_name = track.get("artist_name", "")
    play_count = track.get("play_count", 0)

    updated_time = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")

    return f"""
### 🫠  [k4nkan](https://kanta.it.com/)  

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

### 🎵 Favorite
<img src="./data/top_track.svg" alt="Top Track" width="300">

---

### 📚 Log
- _[Last updated](https://github.com/k4nkan/k4nkan/actions): {updated_time}_
"""


if __name__ == "__main__":
    print("🎧 Fetching top track...")
    track = fetch_top_track()
    if not track:
        print("⚠️ No track data found.")
        exit(1)

    create_svg(track)
    readme = generate_readme(track)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md updated successfully!")
