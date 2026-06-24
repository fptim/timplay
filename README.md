# timplay

> 아이디어부터 클릭 가능한 프로토타입까지 — 제품 기획을 4단계로 도와주는 Claude Code 스킬

`timplay`는 하나의 제품 아이디어를 **PRD → 기능명세서 → 유저플로우 → 와이어프레임** 순서로
구체화하는 [Claude Code](https://claude.com/claude-code) 스킬입니다. 모든 단계가 하나의
`project.json`을 공유하기 때문에, 각 단계는 이전 단계의 결과 위에서 이어집니다.

## 주요 기능

| 단계 | 산출물 | 설명 |
|---|---|---|
| **1. PRD** | `prd.md` (Markdown) | 개요·핵심 가치·타겟/시나리오·성공 지표·속성(역할/환경)의 5개 섹션을 질문으로 채워 작성 |
| **2. 기능명세서** | `features.html` | 요구사항 → 기능 → 상세 기능 3단 트리. **드래그앤드롭 정렬**, 펼침/접힘, 상세 패널 |
| **3. 유저플로우** | `userflow.html` | 노드(시작/섹션 최상위/페이지/행동)·연결선·섹션으로 화면 흐름 시각화. 드래그 이동·이름 변경·연결 편집·버전 관리 |
| **4. 와이어프레임** | `wireframe.html` | 유저플로우의 페이지를 **클릭 가능한 프로토타입**으로. shadcn 스타일, 데스크탑/모바일 전환 |

- **단계 종속성**: 각 단계는 이전 단계가 완료되어야 진행됩니다. 누락 시 안내 후 멈춥니다.
- **편집 라운드트립**: 모든 HTML은 브라우저에서 편집 → **JSON 내보내기/불러오기**로 원본에 반영됩니다.
- **출력 언어 자동 추종**: 입력 언어(한국어 등)에 맞춰 모든 문서·UI 텍스트를 생성합니다.

## 설치

### 방법 A — 개인용 (내 모든 프로젝트에서 사용)

```bash
git clone https://github.com/fptim/timplay.git ~/.claude/skills/timplay
```

### 방법 B — 특정 프로젝트용 (팀과 git으로 공유)

```bash
git clone https://github.com/fptim/timplay.git <프로젝트>/.claude/skills/timplay
```

설치 후 **Claude Code 세션을 새로 시작**하면 스킬이 로드됩니다. (스킬은 세션 시작 시 인식됩니다.)

## 사용법

설치 후 아래 둘 중 한 가지로 호출합니다.

**자연어로 요청** — 스킬이 자동으로 트리거됩니다:

```
"독서 기록 앱 PRD 작성해줘"
"이 제품 기능명세서 만들어줘"
"유저플로우 그려줘" · "와이어프레임 만들어줘"
"timplay로 기획 도와줘"
```

**슬래시 명령**:

```
/timplay
```

언제 시작하든 1단계(PRD)부터 진행하며, 선행 단계가 없으면 먼저 해당 단계를 안내합니다.

## 작동 방식

스킬은 제품마다 폴더 하나를 만들고, 그 안의 `project.json`을 단일 원본으로 사용합니다.

```
timplay-projects/<제품-slug>/
├── project.json     # 단일 원본 (모든 단계가 읽고 갱신)
├── prd.md           # 1단계 산출물
├── features.html    # 2단계 산출물
├── userflow.html    # 3단계 산출물
└── wireframe.html   # 4단계 산출물
```

내부적으로 두 개의 스크립트를 사용합니다:

- `scripts/init_project.py "<제품명>"` — 프로젝트 폴더와 `project.json` 골격 생성
- `scripts/render.py <폴더> <features|userflow|wireframe>` — `project.json` 데이터를 HTML 템플릿에 주입

## 요구사항

- [Claude Code](https://claude.com/claude-code)
- Python 3 (스크립트 실행용, 표준 라이브러리만 사용)
- 생성된 HTML은 Tailwind와 SortableJS를 CDN에서 불러오므로 **열람 시 인터넷 연결**이 필요합니다.

## 저장소 구조

```
timplay/
├── SKILL.md                      # 스킬 정의 + 4단계 워크플로
├── README.md                     # 이 문서
├── references/
│   ├── prd-guide.md              # PRD 작성 가이드 + 질문 체크리스트
│   └── data-schema.md            # project.json 스키마 (단계 간 데이터 계약)
├── scripts/
│   ├── init_project.py
│   └── render.py
└── assets/
    ├── features-template.html
    ├── userflow-template.html
    └── wireframe-template.html
```

## 기여 / 피드백

이슈와 PR을 환영합니다: https://github.com/fptim/timplay/issues
