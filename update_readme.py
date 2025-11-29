"""
Script: update_readme.py
Updates GitHub profile README with music stats and repo cards.
"""

import os
from datetime import datetime, timezone

import requests
from supabase import create_client

try:
    import dotenv

    dotenv.load_dotenv()

except ImportError:
    pass

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def read_template(path: str) -> str:
    """Read template file."""
    with open(path, "r", encoding="utf-8") as template_file:
        return template_file.read()


def fetch_track(target: str):
    """Fetch top track from Supabase."""
    res = supabase.table(target).select("*").limit(1).execute()
    return res.data[0] if res.data else None


def create_svg(track: dict, filename: str, label: str = ""):
    """Generate SVG from template."""
    os.makedirs("data/tracks", exist_ok=True)

    svg_template = read_template("data/templates/track_template.svg")

    svg_filled = (
        svg_template.replace("{{ track_name }}", track.get("track_name", "No Data"))
        .replace("{{ artist_name }}", track.get("artist_name", ""))
        .replace("{{ play_count }}", str(track.get("play_count", 0)))
        .replace("{{ label }}", label)
    )

    with open(f"data/tracks/{filename}", "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_filled)
    print(f"✅ SVG generated: data/tracks/{filename}")


def fetch_repo_info(repo_name: str):
    """Fetch repo info from GitHub API."""
    if not GITHUB_TOKEN:
        print("⚠️ GITHUB_TOKEN not found. Skipping repo stats.")
        return None

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{repo_name}"

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"❌ Failed to fetch {repo_name}: {res.status_code}")
            return None
    except requests.RequestException as e:
        print(f"❌ Error fetching {repo_name}: {e}")
        return None


def get_language_color(language: str) -> str:
    """Get color for language."""
    colors = {
        "Python": "#3572A5",
        "JavaScript": "#F1E05A",
        "TypeScript": "#2B7489",
        "HTML": "#E34C26",
        "CSS": "#563D7C",
        "Vue": "#41B883",
        "Jupyter Notebook": "#DA5B0B",
        "Shell": "#89E051",
    }
    return colors.get(language, "#CCCCCC")


def wrap_text(text: str, max_len: int = 50) -> tuple[str, str]:
    """Wrap text to 2 lines."""
    words = text.split()
    line1 = ""
    line2 = ""

    current_line = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 <= max_len:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            if not line1:
                line1 = " ".join(current_line)
                current_line = [word]
                current_len = len(word)
            else:
                # If line1 is filled, put everything else in line2 (truncated)
                remaining = " ".join(words[words.index(word) :])
                if len(remaining) > max_len:
                    line2 = remaining[: max_len - 3] + "..."
                else:
                    line2 = remaining
                break
    else:
        if not line1:
            line1 = " ".join(current_line)
        else:
            line2 = " ".join(current_line)

    return line1, line2


def create_repo_svg(repo_data: dict, filename: str):
    """Generate repo card SVG."""
    if not repo_data:
        return

    os.makedirs("data/repos", exist_ok=True)
    svg_template = read_template("data/templates/repo_card_template.svg")

    name = repo_data.get("name", "Unknown")
    description = repo_data.get("description") or "No description provided."

    line1, line2 = wrap_text(description)

    language = repo_data.get("language") or "Unknown"
    stars = repo_data.get("stargazers_count", 0)
    forks = repo_data.get("forks_count", 0)

    lang_color = get_language_color(language)

    svg_filled = (
        svg_template.replace("{{ name }}", name)
        .replace("{{ description_line_1 }}", line1)
        .replace("{{ description_line_2 }}", line2)
        .replace("{{ language }}", language)
        .replace("{{ language_color }}", lang_color)
        .replace("{{ stars }}", str(stars))
        .replace("{{ forks }}", str(forks))
    )

    with open(f"data/repos/{filename}", "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_filled)
    print(f"✅ Repo SVG generated: data/repos/{filename}")


def generate_readme() -> str:
    """Generate README with timestamp."""
    template = read_template("data/templates/readme_template.md")
    updated_time = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")
    return template.replace("{{ updated_time }}", updated_time)


def main():
    """Main execution function."""
    print("🎧 Fetching tracks...")

    top_track = fetch_track("top_tracks_all_time")
    today_track = fetch_track("top_tracks_today")

    if top_track:
        create_svg(top_track, "top_track.svg", label="Total Plays")
    if today_track:
        create_svg(today_track, "today_track.svg", label="Today's Plays")

    print("📦 Fetching repo stats...")
    repos = [
        "k4nkan/k4nkan",
        "k4nkan/k4nkan.github.io",
        "k4nkan/save-spotify-logs",
        "k4nkan/DailyLogs",
    ]

    for repo in repos:
        data = fetch_repo_info(repo)
        safe_name = repo.replace("/", "_").replace("-", "_").replace(".", "_")
        create_repo_svg(data, f"repo_{safe_name}.svg")

    readme = generate_readme()
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(readme)

    print("✅ README.md updated successfully!")


if __name__ == "__main__":
    main()
