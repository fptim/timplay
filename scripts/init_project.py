#!/usr/bin/env python3
"""Create a new timplay project folder with a skeleton project.json.

Usage:
    init_project.py "<product name>" [--path .] [--slug my-slug] [--language ko]

Creates <path>/timplay-projects/<slug>/project.json with every stage null except meta.
Prints the absolute project directory path on success.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    return s or "product"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("name", help="product name")
    p.add_argument("--path", default=".", help="base directory (default: cwd)")
    p.add_argument("--slug", default=None, help="folder slug (default: derived from name)")
    p.add_argument("--language", default="ko", help="output language code (default: ko)")
    args = p.parse_args()

    slug = args.slug or slugify(args.name)
    today = date.today().isoformat()
    proj_dir = Path(args.path).resolve() / "timplay-projects" / slug
    proj_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "meta": {
            "productName": args.name,
            "slug": slug,
            "language": args.language,
            "createdAt": today,
            "updatedAt": today,
        },
        "prd": None,
        "features": None,
        "userflow": None,
        "wireframe": None,
    }
    out = proj_dir / "project.json"
    if out.exists():
        print(f"project.json already exists at {out} — leaving it untouched", file=sys.stderr)
    else:
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(proj_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
