# PRD writing guide (stage 1)

The PRD is the root document. All later stages inherit its roles, environments, and scope.
A PRD is only complete when **all five sections** below are filled with specific, non-placeholder
content. Before writing, interview the user to close every gap — do not invent facts to fill blanks.

## Required sections

| Section | Fields | What "good" looks like |
|---|---|---|
| 개요 (Overview) | `oneLiner`, `goals`, `background` | One sentence a stranger understands; 2–4 concrete product goals; why-now market/business context |
| 핵심 가치 (Core value) | `problem`, `solution`, `differentiation` | A real user pain; how the product removes it; what makes it better than the obvious alternative |
| 타겟 및 시나리오 (Target & scenario) | `userGroups`, `scenarios` | Named user groups with traits; at least one end-to-end usage story in narrative form |
| 성공 지표 (Metrics) | `kpis`, `risks`, `openIssues` | KPIs with a measurable target; honest risks; unresolved questions |
| 속성 설정 (Attributes) | `category`, `roles`, `environments` | Product category; every distinct user role; runtime environments (web/ios/...) |

## Interview checklist

Ask only what is still missing, in small batches (2–3 questions at a time, not all at once).
Use the AskUserQuestion tool when discrete options exist.

**Overview**
- 이 제품을 한 문장으로 정의하면? 누구를 위한 무엇인가?
- 출시로 달성하려는 목표 2–3개는?
- 지금 이걸 만드는 시장/비즈니스 배경은?

**Core value**
- 타겟 사용자가 지금 겪는 가장 큰 불편은?
- 그 문제를 이 제품은 어떤 방식으로 해결하나?
- 기존 대안(경쟁 서비스/수기 방식) 대비 결정적 차별점은?

**Target & scenario**
- 핵심 사용자 그룹은 누구인가? (복수면 각각)
- 대표 사용자가 가입부터 핵심 가치를 경험하기까지의 흐름을 이야기로 풀면?

**Metrics**
- 성공/실패를 가르는 핵심 KPI와 목표 수치는?
- 가장 우려되는 리스크는? 아직 결정 못 한 오픈 이슈는?

**Attributes** (feeds later stages — confirm explicitly)
- 제품 카테고리는?
- 시스템에 등장하는 사용자 역할을 전부 나열하면? (예: 관리자, 고객, 게스트)
- 어떤 환경에서 쓰나? (웹 / iOS / Android / 데스크톱)

## prd.md output format

Render the `prd` object to Markdown with this heading order. Save as `prd.md` in the project folder.

```markdown
# <productName> — PRD

## 1. 개요
**한 줄 정의** — <oneLiner>
**제품 목표**
- <goal>
**배경** — <background>

## 2. 핵심 가치
**문제** — <problem>
**해결 방식** — <solution>
**차별점** — <differentiation>

## 3. 타겟 및 시나리오
### 핵심 사용자 그룹
- **<name>** — <description>
### 사용 시나리오
- **<title>** — <story>

## 4. 성공 지표
### 핵심 KPI
- **<name>**: <target>
### 리스크
- <risk>
### 오픈 이슈
- <issue>

## 5. 속성 설정
- **제품 카테고리**: <category>
- **사용자 역할**: <role.name>, ...
- **사용 환경**: <environment>, ...
```

Keep `prd.md` and `project.json.prd` in sync — write both whenever the PRD changes.
