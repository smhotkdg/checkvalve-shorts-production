# 쇼츠 제작: 명령어, 환경설정, 주제별 텍스트

Blender 애니메이션 + Higgsfield 보조 영상 + Typecast **필재** 내레이션으로 50초 9:16 공학 원리 쇼츠를 만드는 작업 환경입니다.

레퍼런스 ('이런거지' 채널)
- 기본 포맷 `principle_info`(원리 + 마지막 정보): https://www.youtube.com/shorts/5UjFpjehQwc
- 보조 포맷 `problem_solution`(문제 → 해결 → 새 난관 → 추가 해결 → 완성): https://www.youtube.com/shorts/q5C9HCN2QY4

**다음 제작 주제: 냉장고** — [`topics/refrigerator/`](topics/refrigerator/) · 냉기를 만드는 게 아니라 열을 옮기는 기계, 끝 정보는 문을 열어 둬도 방이 더워지는 이유

공통 기준(2026-10-11): 단순하고 한눈에 이해되는 3D(`visual_clarity`), 화면 텍스트는 고정 제목과 자막뿐(진행 칩 없음), 자막 배경 패널 없음(레이아웃 v4), 한국어·영어 두 세트.

다른 초안: [`운하 갑문`](topics/canal-lock/) · [`침매터널`](topics/immersed-tunnel/) / 완료: [`타워크레인`](topics/tower-crane/)

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

- Git: 명령어, 설정, 연결 스크립트, 주제별 **텍스트**만 보관합니다.
- 로컬 전용: `work/<slug>/`(음성, Blender, 렌더, job 기록), `outputs/`(완성 영상, 자막, 검수 결과), API 키.
- API 키는 Windows 연결 스크립트가 숨김 입력으로 받아 사용자 계정에 묶인 암호화 파일로 저장합니다. 다른 PC에서는 키와 Higgsfield 연결을 다시 설정합니다.
- 이전 커밋의 제작 결과물 기록은 히스토리에 남아 있습니다.
