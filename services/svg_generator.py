
import os

def read_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_repo_svg(repo_cfg: dict, repo_info: dict, filename: str):
    template_path = "data/templates/repo_card_template.svg"
    template = read_template(template_path)

    svg = (
        template.replace("{{ icon_url }}", repo_cfg["icon"])
        .replace("{{ repo_name }}", repo_cfg["name"])
        .replace("{{ repo_description }}", repo_info["description"])
        .replace("{{ last_update }}", repo_info["updated_at"])
    )

    os.makedirs("data/repos", exist_ok=True)
    out_path = f"data/repos/{filename}"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    return out_path
