# 체크밸브 50초 쇼츠 제작 및 작업 인계

한국어 세로 쇼츠의 완성 영상, 제작 기록, 제목·설명·대본, 직접 만든 2D 애니메이션 소스와 Typecast API 연결 준비 자료입니다. 다른 PC나 다른 AI 작업에서 이 저장소를 열어 이어서 진행할 수 있습니다.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 완성 영상 | 50.000초 / 1080×1920 / 24fps / H.264 + AAC |
| 현재 적용 음성 | Microsoft `ko-KR-InJoonNeural` |
| 자막 | 한국어 23개, 화면에 삽입 완료 |
| 별도 썸네일 | 사용자 선택에 따라 제작하지 않음 |
| Typecast 필재 | Studio 제공 확인. 계정별 API 목록 조회와 실제 음성 생성은 미완료 |
| API 연결 | 클라이언트 준비, 인증 키 미등록. 필재 음성 생성·영상 적용 전 |
| 유튜브 게시 | 미진행 |

- [완성 MP4 다운로드](outputs/checkvalve-final.mp4)
- [제작 기록·채널 분석·검수](outputs/checkvalve-production-plan.md)
- [제목·설명·실제 대본](outputs/checkvalve-title-description.txt)
- **작업을 이어갈 때 먼저 읽기:** [HANDOFF.md](HANDOFF.md)
- [Typecast API 연결 방법](docs/typecast-api.md)

## 파일 구성

```text
HANDOFF.md                     상황과 다음 작업 조건
outputs/checkvalve-final.mp4    현재 납품본 (InJoon 음성)
outputs/checkvalve-*.md/txt     제작 기록과 게시용 문구
outputs/connect-typecast.ps1   Windows API 키 입력 및 읽기 전용 확인
src/typecast_api_bridge.py     Typecast 공식 REST API 클라이언트
src/checkvalve/render.py       직접 제작한 2D 애니메이션
src/checkvalve/tts.py           현재 영상의 TTS 제작 소스
src/checkvalve/narration.json   기존 음성의 단어별 시간 기록
src/checkvalve/script.json      최종 대본
src/checkvalve/caps.srt         기존 음성에 맞춘 23개 자막
docs/verification.json         기존 완성본의 검수 결과
```

## 제작 소스 실행

Python 3, FFmpeg(영상 인코딩 및 libass 자막 지원), 한국어 글꼴이 필요합니다.

```sh
python -m pip install -r requirements.txt
# src/checkvalve/fonts/NotoSansCJKkr-Bold.otf에 글꼴 배치 후
python src/checkvalve/render.py --preview
python src/checkvalve/tts.py
python src/checkvalve/render.py
```

글꼴은 [Noto CJK 공식 저장소](https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/Korean)에서 받을 수 있습니다. 글꼴 바이너리를 포함하지 않으며 라이선스는 원 저장소를 참고하세요.

렌더러는 `final_clean.mp4`(자막 삽입 전)를 만듭니다. 납품본의 자막 삽입 단계는 Higgsfield 처리 환경에서 수행했으며 해당 서비스의 내부 도구는 포함하지 않습니다. 제공한 SRT를 지원하는 편집기 또는 FFmpeg로 삽입할 수 있습니다. TTS를 다시 생성하면 발화 시간이 달라질 수 있으므로 기존 SRT를 사용하기 전에 실제 음성과 비교해야 합니다.

필재로 교체할 때는 장면 전환에 사용하는 `narration.json`의 시간도 다시 측정해야 합니다. 기존 시간표로 최종 적용 완료 처리하지 마세요. 완성 MP4를 재생하는 데 위 프로그램은 필요하지 않습니다.

API 키와 로그인 정보는 포함하지 않습니다. `work/`와 로컬 인증 파일은 Git에서 제외합니다.
