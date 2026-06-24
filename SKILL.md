---
name: timplay
description: Product planning assistant that produces a connected set of planning artifacts through four dependent stages — (1) PRD in Markdown, (2) Features specification as an interactive directory-view HTML with drag-and-drop reordering, (3) User Flow as an editable node/edge/section HTML diagram, and (4) Wireframe as a clickable shadcn-style HTML prototype (desktop/mobile). Use when the user wants to plan a product, write a PRD or 기획서, define a feature spec / 기능명세서, design a user flow / 유저플로우, build a clickable wireframe / 와이어프레임, or asks for "timplay". Each stage reads the previous stage's output from a shared project.json.
---

# timplay

Guides a product from idea to clickable prototype through four stages. All stages share one
source of truth — `project.json` in a per-product folder — so each stage builds on the last.

## Output language

Generate all document text and HTML UI labels in the **language of the user's input** (Korean
input → Korean output). Store it in `meta.language` and stay consistent across every stage.

## Project workspace

One folder per product holds everything. Create it once with the init script:

```bash
scripts/init_project.py "<product name>" --path <dir> --language <ko|en|...>
```

This prints the project directory and creates `project.json` (every stage `null` except `meta`).
The folder ends up as:

```
timplay-projects/<slug>/
├── project.json     # single source of truth — read & update this every stage
├── prd.md           # stage 1 render
├── features.html    # stage 2 render
├── userflow.html    # stage 3 render
└── wireframe.html   # stage 4 render
```

The full `project.json` shape is the contract between stages — read **[references/data-schema.md](references/data-schema.md)** before writing any stage data.

## Dependency gates (enforce in order)

Each stage requires the previous one. **Before starting a stage, check `project.json`** and if the
prerequisite is missing or empty, stop and tell the user which stage to complete first — do not
fabricate upstream content.

| Stage | Requires | Gate check |
|---|---|---|
| 1 PRD | — | always allowed |
| 2 Features | PRD done | `prd` non-null, attributes.roles populated |
| 3 User Flow | Features done | `features.requirements` non-empty |
| 4 Wireframe | User Flow done | a `userflow` version with `page` nodes exists |

Example gate message: "와이어프레임은 유저플로우가 필요합니다. 아직 유저플로우가 없어 먼저 3단계를 진행할게요."

## Workflow

For each stage: gather/update data → write it into `project.json` → render → tell the user the output path.
Whenever a stage's data changes, re-run its render so the HTML stays in sync.

### Stage 1 — PRD (Markdown)

Read **[references/prd-guide.md](references/prd-guide.md)** for the five required sections, the
gap-closing interview checklist, and the exact `prd.md` heading format.

1. Interview the user to fill every PRD field (overview, core value, target & scenario, metrics,
   attributes). Ask in small batches; use AskUserQuestion for discrete choices. Do not invent facts.
2. Write the `prd` object into `project.json` **and** render `prd.md` (plain Markdown — no script needed).
3. `attributes.roles` and `attributes.environments` feed later stages; confirm them explicitly.

### Stage 2 — Features (interactive HTML directory view)

A three-level tree: 요구사항(requirement) → 기능(feature) → 상세 기능(spec). The rendered page is a
3-column directory view (requirements | features+specs | detail) with drag-and-drop reordering,
expandable specs, and JSON import/export — matching the reference UI.

1. Derive requirements from PRD goals/scenarios; break each into features (assign a `roleId` from
   `prd.attributes.roles`) and specs. Write `features` into `project.json` per the schema.
2. Render: `scripts/render.py <project-dir> features` → writes `features.html`.

### Stage 3 — User Flow (editable node/edge/section diagram)

Visualizes how feature screens connect. Built from nodes (`start`, `sectionTop`, `page`, `action`),
edges (흐름), and sections (섹션 bands). Supports multiple versions (원본 + 수정본). The rendered page
has the legend, drag-to-move nodes, double-click rename, link mode for drawing edges, click-to-delete
edges, deletable sections/versions, and JSON import/export.

1. Group features into sections; lay out nodes with `x`/`y` coordinates and connect with edges.
   `page` nodes become wireframe screens in stage 4. Write `userflow` per the schema.
2. Link nodes to features/specs with each node's `ref` (`{type, id}` → a stage-2 feature or spec).
   In the HTML, a node's ✎ button opens that feature/spec in an editable drawer; those edits are the
   same data the 기능명세서 shows, so the two stages stay in sync. Set `ref` for `page`/`action`
   nodes that correspond to a feature whenever possible.
3. Render: `scripts/render.py <project-dir> userflow` → writes `userflow.html`.

### Stage 4 — Wireframe (clickable shadcn-style prototype)

Turns each `page` node into a screen of simple UI elements with screen-to-screen navigation.
Single-file HTML, Tailwind CDN, shadcn-style components. Desktop layout = top nav + side menu;
mobile layout = bottom tab bar. The prototype is clickable (button/card/list `linkTo` navigates).

1. Pick a `userflow` version (`userflowVersionId`) and `device`. For each `page`/`sectionTop` node,
   define a screen with `elements` (heading/text/button/input/image/card/list/divider) and set
   `linkTo` on interactive elements using userflow edges as the guide. Add `nav` entries for the menu.
   Write `wireframe` per the schema.
2. Render: `scripts/render.py <project-dir> wireframe` → writes `wireframe.html`.

## One source of truth — edit once, reflect everywhere

`project.json` is the single source of truth, and **every** rendered page embeds the **whole**
project (not just its own stage). Treat any edit — wherever it happens — as a change to that one
source, then propagate it to all documents:

- **A change to one stage can affect others.** Editing a feature's title/spec changes what the
  userflow node drawer and (if referenced) the wireframe show; changing roles in the PRD changes
  feature role options. After updating `project.json`, re-render everything in one step:
  `scripts/render.py <project-dir> all` (renders every stage that has content). Also re-render
  `prd.md` if the PRD changed.
- **In the browser, pages already self-sync.** All timplay HTML pages share one `localStorage`
  key (`timplay:project:<slug>`), so an edit in 기능명세서 and an edit via a 유저플로우 node drawer
  update each other live across open tabs. The userflow node ✎ drawer edits the very same feature
  data as the 기능명세서.

**Edit round-trip with the user:** every page has **불러오기 (Import)** / **내보내기 (Export)**.
When the user edits in the browser and exports the updated `project.json`, take that file as the new
source of truth: overwrite the project's `project.json`, then `render.py <project-dir> all` so every
document reflects it.

## Scripts

- `scripts/init_project.py "<name>" [--path .] [--slug ..] [--language ko]` — scaffold a project folder + `project.json`.
- `scripts/render.py <project-dir> <features|userflow|wireframe|all>` — embed the full `project.json`
  into the matching `assets/*-template.html` and write the stage's HTML into the project folder. Use
  `all` to re-render every stage that has content (the default after any data change).
  (PRD has no render step — write `prd.md` directly.)

The HTML pages load Tailwind and SortableJS from CDNs, so viewing them needs internet access.
