#!/usr/bin/env python3
"""Render a timplay stage to a self-contained HTML file.

Reads <project-dir>/project.json, injects the relevant data slice into the matching
asset template, and writes the output HTML into the project folder.

Usage:
    render.py <project-dir> <stage>
    stage ∈ features | userflow | wireframe

The template contains the literal token  __TIMPLAY_DATA__  which is replaced with a
JSON literal. The produced HTML embeds the data inline (works offline-of-data) and the
page's own Import/Export buttons let users round-trip an updated project.json.
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


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[2] not in STAGES:
        print(__doc__)
        return 2

    proj_dir = Path(sys.argv[1]).resolve()
    stage = sys.argv[2]
    proj_file = proj_dir / "project.json"
    if not proj_file.exists():
        print(f"error: {proj_file} not found — run init_project.py first", file=sys.stderr)
        return 1

    data = json.loads(proj_file.read_text(encoding="utf-8"))
    if not data.get(stage):
        print(f"error: project.json has no '{stage}' content yet — fill it before rendering",
              file=sys.stderr)
        return 1

    # Slice passed to the page: stage data + meta + (roles for features/labels).
    payload = {
        "meta": data.get("meta", {}),
        "prd": data.get("prd") or {},
        stage: data[stage],
    }

    tmpl_name, out_name = STAGES[stage]
    tmpl_path = Path(__file__).resolve().parent.parent / "assets" / tmpl_name
    html = tmpl_path.read_text(encoding="utf-8")
    if TOKEN not in html:
        print(f"error: token {TOKEN} missing from {tmpl_name}", file=sys.stderr)
        return 1
    html = html.replace(TOKEN, json.dumps(payload, ensure_ascii=False))

    out_path = proj_dir / out_name
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
