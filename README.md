# 쇼츠 제작: 명령어, 환경설정, 주제별 텍스트

Blender 애니메이션 + Higgsfield 보조 영상 + Typecast **필재** 내레이션으로 50초 9:16 공학 원리 쇼츠를 만드는 작업 환경입니다.

레퍼런스: https://www.youtube.com/shorts/q5C9HCN2QY4 (문제 → 해결 동작 → 새로운 난관 → 추가 해결 → 완성)

**현재 주제: 타워크레인 톱 클라이밍** — [`topics/tower-crane/`](topics/tower-crane/)  
다음 주제: 침매터널 — [`topics/immersed-tunnel/`](topics/immersed-tunnel/)

## 구조

| 경로 | 내용 |
|---|---|
| [config/higgsfield-typecast.json](config/higgsfield-typecast.json) | 전역 규칙: 길이, 음성, 길이 예산, 레이아웃(가로 중앙 정렬), 자막, 공통 검수 조건 |
| [docs/immersion-guide.md](docs/immersion-guide.md) | 몰입형 포맷: 훅, 오픈 루프, 화면 리듬, 진행 칩, 루프 엔딩 |
| [docs/claude-code-prompt.md](docs/claude-code-prompt.md) | 매 주제에 그대로 쓰는 Claude Code 실행 프롬프트 |
| [docs/workflow-commands.md](docs/workflow-commands.md) | 환경설정과 실행 명령 |
| [docs/typecast-api.md](docs/typecast-api.md) | Typecast 필재 API 연결 |
| `topics/<slug>/` | 주제별 텍스트: brief.md, narration.txt, title-description.txt, topic.json |
| `topics/_template/` | 새 주제 시작용 빈 양식 |
| [HANDOFF.md](HANDOFF.md) | 제작 이력과 인계 |

## 새 주제 진행 순서

1. 주제 선정 (기준: [immersion-guide.md 5장](docs/immersion-guide.md))
2. `topics/_template/`을 `topics/<slug>/`로 복사하고 원리·대본·제목·설명·장면표 작성
3. `config/higgsfield-typecast.json`의 `active_topic`과 `topic_config` 변경
4. [Claude Code 프롬프트](docs/claude-code-prompt.md)의 `<slug>`를 바꿔 실행

## 보관 원칙

- Git: 명령어, 설정, 연결 스크립트, 주제별 **텍스트**만 보관합니다.
- 로컬 전용: `work/<slug>/`(음성, Blender, 렌더, job 기록), `outputs/`(완성 영상, 자막, 검수 결과), API 키.
- API 키는 Windows 연결 스크립트가 숨김 입력으로 받아 사용자 계정에 묶인 암호화 파일로 저장합니다. 다른 PC에서는 키와 Higgsfield 연결을 다시 설정합니다.
- 이전 커밋의 제작 결과물 기록은 히스토리에 남아 있습니다.
