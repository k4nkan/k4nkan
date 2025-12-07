"""
Main script to update the README.md file.
Fetches repository information, generates SVG cards, and updates the README.
"""

from config.repos import REPOS
from services.repo_fetcher import fetch_repo_info
from services.svg_generator import generate_repo_svg
from services.readme_generator import generate_readme


def main():
    """Main function to update README."""
    card_tags = []

    for repo in REPOS:
        info = fetch_repo_info(repo["full"])
        if not info:
            continue

        # Convert to safe format for filename
        safe = repo["full"].replace("/", "_").replace("-", "_").replace(".", "_")
        filename = f"{safe}.svg"

        generate_repo_svg(repo, info, filename)

        # <img> tag for embedding in README
        card_tag = (
            f'<a href="https://github.com/{repo["full"]}">'
            f'<img src="./data/repos/{filename}" alt="{repo["name"]}" width="350" /></a>'
        )

        card_tags.append(card_tag)

    # Add some spacing between cards
    repo_cards_html = "\n<br/>\n".join(card_tags)
    readme = generate_readme(repo_cards_html)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README updated")


if __name__ == "__main__":
    main()
