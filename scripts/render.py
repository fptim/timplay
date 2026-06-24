#!/usr/bin/env python3
"""Render timplay stage(s) to self-contained HTML files.

Reads <project-dir>/project.json, injects the FULL project into the matching asset
template(s), and writes the output HTML into the project folder.

Usage:
    render.py <project-dir> <stage>
    stage ∈ features | userflow | wireframe | all

The whole project.json is embedded in every page (not just one stage's slice) so that
all pages share one source of truth: each page persists the entire project to a shared
localStorage key, and edits made in one page sync to the others. The template contains
the literal token  __TIMPLAY_DATA__  which is replaced with the project JSON literal.
'all' renders every stage that has content. Import/Export round-trips project.json.
"""
import json
import sys
from pathlib import Path

STAGES = {
    "features":  ("features-template.html",  "features.html"),
    "userflow":  ("userflow-template.html",  "userflow.html"),
    "wireframe": ("wireframe-template.html", "wireframe.html"),
}
TOKEN = "__TIMPLAY_DATA__"


def render_stage(proj_dir: Path, stage: str, data: dict) -> int:
    if not data.get(stage):
        print(f"error: project.json has no '{stage}' content yet — fill it before rendering",
              file=sys.stderr)
        return 1
    tmpl_name, out_name = STAGES[stage]
    tmpl_path = Path(__file__).resolve().parent.parent / "assets" / tmpl_name
    html = tmpl_path.read_text(encoding="utf-8")
    if TOKEN not in html:
        print(f"error: token {TOKEN} missing from {tmpl_name}", file=sys.stderr)
        return 1
    # Embed the FULL project so every page is a complete, syncable source of truth.
    html = html.replace(TOKEN, json.dumps(data, ensure_ascii=False))
    out_path = proj_dir / out_name
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))
    return 0


def main() -> int:
    if len(sys.argv) != 3 or (sys.argv[2] not in STAGES and sys.argv[2] != "all"):
        print(__doc__)
        return 2

    proj_dir = Path(sys.argv[1]).resolve()
    stage = sys.argv[2]
    proj_file = proj_dir / "project.json"
    if not proj_file.exists():
        print(f"error: {proj_file} not found — run init_project.py first", file=sys.stderr)
        return 1

    data = json.loads(proj_file.read_text(encoding="utf-8"))

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

    return render_stage(proj_dir, stage, data)


if __name__ == "__main__":
    raise SystemExit(main())
