"""
This module generates the README file.
"""
from datetime import datetime, timezone

def read_template(path: str) -> str:
    """Read the template file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_readme(repo_cards_html: str) -> str:
    """Generate the README content with updated repo cards."""
    template = read_template("data/templates/readme_template.md")
    updated = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")

    return (
        template.replace("{{ repo_cards }}", repo_cards_html)
                .replace("{{ updated_time }}", updated)
    )
