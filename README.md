# timplay

> 아이디어부터 클릭 가능한 프로토타입까지 — 제품 기획을 4단계로 도와주는 AI 코딩 에이전트용 스킬

`timplay`는 하나의 제품 아이디어를 **PRD → 기능명세서 → 유저플로우 → 와이어프레임** 순서로
구체화하는 스킬입니다. [Claude Code](https://claude.com/claude-code)에 최적화돼 있지만,
핵심은 표준 `SKILL.md` + Python 스크립트라서 다른 스킬 지원 런타임이나 임의의 에이전트에서도
쓸 수 있습니다(아래 [런타임별 사용](#런타임별-사용) 참고). 모든 단계가 하나의
`project.json`을 공유하기 때문에, 각 단계는 이전 단계의 결과 위에서 이어집니다.

## 주요 기능

| 단계 | 산출물 | 설명 |
|---|---|---|
| **1. PRD** | `prd.md` (Markdown) | 개요·핵심 가치·타겟/시나리오·성공 지표·속성(역할/환경)의 5개 섹션을 질문으로 채워 작성 |
| **2. 기능명세서** | `features.html` | 요구사항 → 기능 → 상세 기능 3단 트리. **드래그앤드롭 정렬**, 펼침/접힘, 상세 패널 |
| **3. 유저플로우** | `userflow.html` | 노드(시작/섹션 최상위/페이지/행동)·연결선·섹션으로 화면 흐름 시각화. 드래그 이동·이름 변경·연결 편집·버전 관리 |
| **4. 와이어프레임** | `wireframe.html` | 유저플로우의 페이지를 **클릭 가능한 프로토타입**으로. 기본 shadcn 스타일(런타임에 프론트엔드 디자인 스킬이 있으면 적용), 데스크탑/모바일 전환 |

- **단계 종속성**: 각 단계는 이전 단계가 완료되어야 진행됩니다. 누락 시 안내 후 멈춥니다.
- **편집 라운드트립**: 모든 HTML은 브라우저에서 편집 → **JSON 내보내기/불러오기**로 원본에 반영됩니다. Chromium(Chrome·Edge)에서 로컬 서버로 열면 **내보내기**가 다운로드 대신 같은 `project.json`을 **그 자리에서 덮어쓰기** 합니다(처음 한 번 파일 지정 후 유지). 그 외 환경에서는 다운로드로 폴백됩니다.
- **출력 언어**: 생성되는 **문서 내용**(PRD, 기능/플로우/화면 텍스트)은 입력 언어를 따릅니다. 단,
  HTML의 **UI 크롬**(버튼·헤더·안내문 등)은 현재 한국어로 고정되어 있습니다(다국어화는 추후 과제).

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

## 런타임별 사용

표준 `SKILL.md` + Python 스크립트 구조라, 런타임에 따라 **설치 위치와 호출 방식만** 다릅니다.

| 런타임 | 설치 위치 | 호출 |
|---|---|---|
| **Claude Code** | `~/.claude/skills/timplay` 또는 `<프로젝트>/.claude/skills/timplay` | 세션 재시작 후 `/timplay` 또는 자연어 |
| **Copilot CLI · Gemini CLI** 등 스킬 지원 런타임 | 각 런타임의 스킬 디렉토리 | 그 런타임의 스킬 호출 방식 |
| **Codex 등 Skill 호출 기능이 없는 에이전트** | 폴더를 그대로 두고 `SKILL.md`를 가이드로 사용 | 아래 *스크립트 직접 실행* |

> Stage 4(와이어프레임)의 "프론트엔드 디자인 스킬 적용"은 **선택적 보강**입니다. 그런 스킬이 있는
> 런타임에서만 적용되고, 없으면(대부분의 경우, 특히 Codex) 내장 템플릿으로 그대로 생성됩니다.

### 스크립트 직접 실행 (Skill 호출 기능이 없어도)

`SKILL.md` 절차대로 `project.json`을 채우고 스크립트만 실행하면 됩니다. 외부 의존성 없이 Python 3
표준 라이브러리만 사용합니다.

```bash
python3 scripts/init_project.py "<제품명>" --language ko   # 프로젝트 폴더 + project.json 생성
# SKILL.md / references 가이드대로 project.json 편집
python3 scripts/render.py <프로젝트폴더> all                # 내용 있는 모든 단계 HTML 생성
```

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
- `scripts/render.py <폴더> <features|userflow|wireframe|all> [--template=<경로>]` — `project.json` 전체를 HTML 템플릿에 주입(`all`은 전체 단계 일괄 생성)

## 요구사항

- AI 코딩 에이전트: [Claude Code](https://claude.com/claude-code) 권장. 다른 스킬 지원 런타임이나
  임의 에이전트(예: Codex)에서도 스크립트를 직접 실행해 사용 가능 (위 [런타임별 사용](#런타임별-사용))
- Python 3 (스크립트 실행용, 표준 라이브러리만 사용 — 외부 패키지 불필요)
- 생성된 HTML은 Tailwind와 SortableJS를 CDN에서 불러오므로 **열람 시 인터넷 연결**이 필요합니다.
- **제자리 저장(같은 파일 덮어쓰기)** 은 File System Access API를 쓰므로 Chromium 계열 브라우저 + 보안 컨텍스트(`http://localhost` 또는 `https`)가 필요합니다. 파일을 더블클릭해 `file://`로 열면 이 기능은 비활성화되고 다운로드로 폴백되므로, 프로젝트 폴더에서 `python3 -m http.server` 등으로 띄워 여는 것을 권장합니다.

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
