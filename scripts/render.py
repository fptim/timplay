#!/usr/bin/env python3
"""Render timplay stage(s) to self-contained HTML files.

Reads <project-dir>/project.json, injects the FULL project into the matching asset
template(s), and writes the output HTML into the project folder.

Usage:
    render.py <project-dir> <stage> [--template=<path>]
    stage ∈ features | userflow | wireframe | all

--template overrides the asset template for a single stage (not 'all'). Use it to render from a
frontend-design-styled variant of a template that still contains the __TIMPLAY_DATA__ token and the
original data-binding/sync script, so the styled output keeps live data and cross-page sync.

The whole project.json is embedded in every page (not just one stage's slice) so that
all pages share one source of truth: each page persists the entire project to a shared
localStorage key, and edits made in one page sync to the others. The template contains
the literal token  __TIMPLAY_DATA__  which is replaced with the project JSON literal.
'all' renders every stage that has content. Import/Export round-trips project.json.
"""
import json
import sys
import time
from pathlib import Path

STAGES = {
    "features":  ("features-template.html",  "features.html"),
    "userflow":  ("userflow-template.html",  "userflow.html"),
    "wireframe": ("wireframe-template.html", "wireframe.html"),
}
TOKEN = "__TIMPLAY_DATA__"

# Each stage's content must hold a non-empty list under this key, or the rendered
# page would crash on first paint. Validated before rendering.
STAGE_LIST_KEY = {"features": "requirements", "userflow": "versions", "wireframe": "screens"}


def embed_json(data: dict) -> str:
    """Serialize for embedding inside a <script> block.

    json.dumps does NOT escape '/', '<', or the JS line separators, so a product
    string containing '</script>' would close the script element early (stored XSS /
    broken HTML). Neutralize the sequences that matter inside a script context. The
    escapes stay valid JSON-as-JS (\\/ in a string is just /, \\uXXXX is the char).
    """
    s = json.dumps(data, ensure_ascii=False)
    return (s.replace("</", "<\\/")
             .replace("<!--", "<\\!--")
             .replace(" ", "\\u2028")
             .replace(" ", "\\u2029"))


def render_stage(proj_dir: Path, stage: str, data: dict, template: Path = None) -> int:
    content = data.get(stage)
    if not content:
        print(f"error: project.json has no '{stage}' content yet — fill it before rendering",
              file=sys.stderr)
        return 1
    key = STAGE_LIST_KEY[stage]
    if not isinstance(content, dict) or not isinstance(content.get(key), list):
        print(f"error: '{stage}.{key}' must be a list — check project.json against "
              f"references/data-schema.md", file=sys.stderr)
        return 1
    tmpl_name, out_name = STAGES[stage]
    # template override lets a frontend-design-styled variant be used while keeping data binding
    tmpl_path = Path(template).resolve() if template else Path(__file__).resolve().parent.parent / "assets" / tmpl_name
    if not tmpl_path.exists():
        print(f"error: template not found: {tmpl_path}", file=sys.stderr)
        return 1
    html = tmpl_path.read_text(encoding="utf-8")
    if TOKEN not in html:
        print(f"error: token {TOKEN} missing from {tmpl_name}", file=sys.stderr)
        return 1
    # Embed the FULL project so every page is a complete, syncable source of truth.
    html = html.replace(TOKEN, embed_json(data))
    out_path = proj_dir / out_name
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    template = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--template=")), None)
    if len(args) != 2 or (args[1] not in STAGES and args[1] != "all"):
        print(__doc__)
        return 2

    proj_dir = Path(args[0]).resolve()
    stage = args[1]
    if template and stage == "all":
        print("error: --template can only be used with a single stage, not 'all'", file=sys.stderr)
        return 2
    proj_file = proj_dir / "project.json"
    if not proj_file.exists():
        print(f"error: {proj_file} not found — run init_project.py first", file=sys.stderr)
        return 1

    try:
        data = json.loads(proj_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: {proj_file} is not valid JSON — {e.msg} at line {e.lineno}, column {e.colno}",
              file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("error: project.json must be a JSON object", file=sys.stderr)
        return 1
    # Stamp render time so pages can tell a fresh render from stale localStorage
    # (the templates only adopt the stored copy when its updatedAt is newer).
    data.setdefault("meta", {})["updatedAt"] = int(time.time() * 1000)

    if stage == "all":
        rc = 0
        rendered = 0
        for st in STAGES:
            if data.get(st):
                if render_stage(proj_dir, st, data) == 0:
                    rendered += 1
                else:
                    rc = 1
        if rendered == 0:
            print("error: no stage has content yet — nothing to render", file=sys.stderr)
            return 1
        return rc

    return render_stage(proj_dir, stage, data, Path(template) if template else None)


if __name__ == "__main__":
    raise SystemExit(main())
