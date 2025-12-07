
import base64
import os

def read_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_repo_svg(repo_cfg: dict, repo_info: dict, filename: str):
    template_path = "data/templates/repo_card_template.svg"
    template = read_template(template_path)

    icon_path = repo_cfg["icon"]
    # Check if it looks like a local file path and exists
    if not icon_path.startswith("http") and os.path.exists(icon_path):
        with open(icon_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("utf-8")
            # Assuming PNG for now based on file extension
            mime_type = "image/png"
            if icon_path.endswith(".svg"):
                mime_type = "image/svg+xml"
            icon_url = f"data:{mime_type};base64,{b64_data}"
    else:
        icon_url = icon_path

    svg = (
        template.replace("{{ icon_url }}", icon_url)
        .replace("{{ repo_name }}", repo_cfg["name"])
        .replace("{{ repo_description }}", repo_info["description"])
        .replace("{{ last_update }}", repo_info["updated_at"])
    )

    os.makedirs("data/repos", exist_ok=True)
    out_path = f"data/repos/{filename}"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    return out_path
