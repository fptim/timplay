# project.json schema

`project.json` is the single source of truth for one product. Every stage reads from it
and writes its own slice back. Keep it valid JSON (UTF-8, no comments). The HTML stages
import/export this same shape, so round-trips must preserve unknown fields.

## Top-level shape

```json
{
  "meta":      { "...": "product identity + language" },
  "prd":       { "...": "stage 1" },
  "features":  { "...": "stage 2" },
  "userflow":  { "...": "stage 3" },
  "wireframe": { "...": "stage 4" }
}
```

A stage is considered **complete** when its key holds non-empty content (see "Dependency
gates" in SKILL.md). New projects start with every stage `null` except `meta`.

## meta

```json
"meta": {
  "productName": "초보 독자를 위한 독서 기록 앱",
  "slug": "reading-tracker",
  "language": "ko",          // detected from user input: ko, en, ja, ...
  "createdAt": "2026-06-24",
  "updatedAt": "2026-06-24"
}
```

`language` drives all generated text. Match the user's input language.

## prd (stage 1)

Mirrors the five required PRD sections. Saved both here and rendered to `prd.md`.

```json
"prd": {
  "overview":       { "oneLiner": "", "goals": ["", ""], "background": "" },
  "coreValue":      { "problem": "", "solution": "", "differentiation": "" },
  "targetScenario": {
    "userGroups": [ { "name": "초보 독자", "description": "" } ],
    "scenarios":  [ { "title": "", "story": "" } ]
  },
  "metrics":        { "kpis": [ { "name": "", "target": "" } ], "risks": ["", ""], "openIssues": ["" ] },
  "attributes":     {
    "category": "생산성 / 라이프스타일",
    "roles":        [ { "id": "reader",  "name": "독자" }, { "id": "admin", "name": "관리자" } ],
    "environments": ["web", "ios"]                      // web | ios | android | desktop
  }
}
```

`attributes.roles` is reused by stage 2 (feature ownership) and `attributes.environments`
informs stage 4 device choices.

## features (stage 2)

Three-level tree: requirement → feature → spec. `order` is the integer used for
drag-and-drop reordering (lower = higher in list). IDs are stable; the HTML view keys on them.

```json
"features": {
  "requirements": [
    {
      "id": "R-1", "title": "책 검색 및 기록", "order": 0,
      "features": [
        {
          "id": "F-1", "title": "책 검색 기능", "order": 0,
          "roleId": "reader",                 // references prd.attributes.roles[].id
          "status": "todo",                   // todo | doing | done
          "importance": "high",               // low | medium | high
          "description": "사용자가 읽은 책을 검색·기록한다.",
          "acceptanceCriteria": [
            { "text": "제목·저자·ISBN으로 검색할 수 있다.", "done": false }
          ],
          "specs": [
            { "id": "S-1", "title": "책 상세 정보 조회", "order": 0, "description": "" }
          ]
        }
      ]
    }
  ]
}
```

ID convention: `R-<n>` requirements, `F-<n>` features, `S-<n>` specs — unique within the file.

## userflow (stage 3)

Supports multiple versions (originals + revisions), matching the right-rail version list in
the reference UI. Each version is an independent node/edge/section graph.

```json
"userflow": {
  "activeVersionId": "uf-1",
  "versions": [
    {
      "id": "uf-1", "name": "새 유저플로우 1", "createdAt": "2026-06-24",
      "parentId": null,                       // set when this is a revision ("수정본")
      "sections": [ { "id": "sec-1", "title": "인증, 온보딩", "order": 0 } ],
      "nodes": [
        { "id": "n-1", "type": "start",      "label": "시작",        "sectionId": "sec-1", "x": 40,  "y": 60 },
        { "id": "n-2", "type": "sectionTop", "label": "랜딩 페이지",  "sectionId": "sec-1", "x": 220, "y": 60 },
        { "id": "n-3", "type": "page",       "label": "로그인",      "sectionId": "sec-1", "x": 420, "y": 110, "ref": { "type": "feature", "id": "F-1" } },
        { "id": "n-4", "type": "action",     "label": "주문 입력",   "sectionId": "sec-1", "x": 420, "y": 30,  "ref": { "type": "spec", "id": "S-1" } }
      ],
      "edges": [ { "id": "e-1", "from": "n-1", "to": "n-2" } ]
    }
  ]
}
```

Node `type` ∈ `start` | `sectionTop` (섹션 최상위 페이지) | `page` | `action` (행동).
`x`/`y` are canvas pixel coordinates. `page` nodes become wireframe screens in stage 4.

`ref` (optional) links a node to a feature or spec from stage 2:
`{ "type": "feature" | "spec", "id": "<feature or spec id>" }`. In the userflow HTML the node's
✎ button opens that feature/spec in an editable drawer; edits write back to `features.*` and are
the SAME data the 기능명세서 page shows — so editing in either place stays in sync. Keep `ref` ids
valid against `features`; a dangling `ref` simply shows the link picker again.

## wireframe (stage 4)

References one userflow version. Screens are derived from that version's `page` and
`sectionTop` nodes; links are derived from edges between them.

```json
"wireframe": {
  "userflowVersionId": "uf-1",
  "device": "desktop",                        // desktop | mobile
  "nav": [ { "screenId": "n-2", "label": "홈" } ],   // top/side/bottom menu entries
  "screens": [
    {
      "id": "n-3",                            // matches the userflow node id
      "title": "로그인",
      "elements": [
        { "type": "heading", "text": "로그인" },
        { "type": "input",   "label": "이메일", "placeholder": "you@example.com" },
        { "type": "input",   "label": "비밀번호", "inputType": "password" },
        { "type": "button",  "text": "로그인", "variant": "primary", "linkTo": "n-2" },
        { "type": "text",    "text": "계정이 없으신가요?" },
        { "type": "button",  "text": "회원가입", "variant": "ghost", "linkTo": "n-5" }
      ]
    }
  ]
}
```

Element `type` ∈ `heading` | `text` | `button` | `input` | `image` | `card` | `list` | `divider`.
`linkTo` (on buttons/cards/list items) points at another screen id to make the prototype clickable.
`variant` for buttons ∈ `primary` | `secondary` | `ghost` | `destructive`.
