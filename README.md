# 쇼츠 제작: 명령어, 환경설정, 주제별 텍스트

콘티 이미지 + Higgsfield 애니메이션 + Typecast **필재**로 9:16 원리·역사 쇼츠를 만드는 작업 환경입니다. 이전 Blender/직접 2D 제작 경로도 보관합니다. 현재는 **한국어만** 제작합니다. 길이는 주제별 초안과 실제 음성 길이로 정합니다.

레퍼런스 ('이런거지' 채널)
- 최신 기준(문제 때문에 구조가 바뀌는 과정): https://www.youtube.com/shorts/41vfH3EtqOM · [장면과 이야기 분석](docs/references/41vfH3EtqOM-analysis.md)
- 이전 기준 `problem_solution`(같은 물체의 실패 → 개선 → 잠금 → 실사용): https://www.youtube.com/shorts/Gko5JrBC020 · [촘촘한 분석](docs/references/Gko5JrBC020-analysis.md)
- 보관 포맷 `principle_info`(원리 + 마지막 정보): https://www.youtube.com/shorts/5UjFpjehQwc
- 보조 포맷 `problem_solution`(문제 → 해결 → 새 난관 → 추가 해결 → 완성): https://www.youtube.com/shorts/q5C9HCN2QY4

**현재 주제는 아르키메데스의 왕관입니다.** 최신 완료본은 콘티의 음영 있는 잉크 일러스트를 유지한 Higgsfield v4, 44초·1080×1920·24fps입니다. [제작 설정](topics/archimedes-crown/higgsfield-v4.json) · [시작/끝 이미지 지침](topics/archimedes-crown/keyframes-v4.md) · [제작 순서와 명령](docs/storyboard-higgsfield-production.md). 필재 원음 재사용, 의미별 한글 줄바꿈과 낮춘 자막 위치를 적용했습니다. 영상·제작 소스는 로컬에만 있습니다.

**모든 영상의 텍스트는 필수 layout v6입니다.** 승인 예시의 제목 위치는 유지(블록 y=260), 최신 요청에 따라 자막만 54px 아래로 이동(블록 y=1360)했습니다. 가로 중앙, 흰색·노란색과 두꺼운 외곽선·그림자, 패널 없음. 한국어·활성 영어·기존 주제 재렌더·새 템플릿 모두 동일. [정확한 비율](docs/text-layout.md). 이전 v1~v5 좌표보다 이 규칙이 우선합니다.

작업 폴더: `C:\Users\cozy0\OneDrive\Desktop\short\checkvalve-shorts-production`. 냉장고의 진행 중 로컬 수정은 보존했습니다.

공통 기준(2026-10-11): 한눈에 이해되는 완전한 장치, 주제별 승인 그림체와 이어지는 동작, 화면 텍스트는 고정 제목과 자막뿐(진행 칩 없음), 자막 배경 패널 없음(레이아웃 v6), 현재 한국어 한 세트. 기존 영어 자료·설정은 보관하며 `language_sets.required`에 `en`을 명시적으로 다시 켜야 새 영어 제작을 합니다.

다른 주제 보관: [`냉장고`](topics/refrigerator/) · [`운하 갑문`](topics/canal-lock/) · [`침매터널`](topics/immersed-tunnel/) / 완료: [`타워크레인`](topics/tower-crane/)

## 구조

| 경로 | 내용 |
|---|---|
| [config/higgsfield-typecast.json](config/higgsfield-typecast.json) | 전역 규칙: 길이, 음성, 길이 예산, 레이아웃(가로 중앙 정렬), 자막, 공통 검수 조건 |
| [docs/immersion-guide.md](docs/immersion-guide.md) | 포맷(원리+정보 / 문제 해결), 단순한 3D 기준, 화면 텍스트 규칙 |
| [docs/claude-code-prompt.md](docs/claude-code-prompt.md) | 매 주제에 그대로 쓰는 Claude Code 실행 프롬프트 |
| [docs/workflow-commands.md](docs/workflow-commands.md) | 환경설정과 실행 명령 |
| [docs/typecast-api.md](docs/typecast-api.md) | Typecast 필재 API 연결 |
| `topics/<slug>/` | 주제별 텍스트: brief.md, narration.txt, narration.en.txt, title-description(.en).txt, topic.json |
| `topics/_template/` | 새 주제 시작용 빈 양식 |
| [HANDOFF.md](HANDOFF.md) | 제작 이력과 인계 |

## 새 주제 진행 순서

1. 주제 선정 (기준: [immersion-guide.md 5장](docs/immersion-guide.md))
2. `topics/_template/`을 `topics/<slug>/`로 복사하고 원리·대본·제목·설명·장면표 작성
3. `config/higgsfield-typecast.json`의 `active_topic`과 `topic_config` 변경
4. 실행: `powershell -ExecutionPolicy Bypass -File .\scripts\start-production.ps1 -Slug <slug>`
   (최신 main을 받고, 도구를 점검한 뒤, [Claude Code 프롬프트](docs/claude-code-prompt.md)를 채워 Claude Code를 엽니다)

## 보관 원칙

- Git: 명령어, 설정, 연결 스크립트, 주제별 제작 입력 **텍스트**만 보관합니다. 완성 미디어·이미지·Blender 제작 소스는 제외합니다.
- 로컬 전용: `work/<slug>/`(음성, Blender, 렌더, job 기록), `outputs/`(완성 영상, 자막, 검수 결과), API 키.
- API 키는 Windows 연결 스크립트가 숨김 입력으로 받아 사용자 계정에 묶인 암호화 파일로 저장합니다. 다른 PC에서는 키와 Higgsfield 연결을 다시 설정합니다.
- 이전 커밋의 제작 결과물 기록은 히스토리에 남아 있습니다.
