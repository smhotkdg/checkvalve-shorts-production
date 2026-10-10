# Blender + Higgsfield + Typecast 필재: 체크밸브 50초 쇼츠

참고 채널의 문제 제시 → 내부 구조 → 부품 움직임 → 작동 조건 구성을 반영한 한국어 세로 쇼츠입니다. **최신 완성본은 Typecast 필재 음성**입니다.

- [완성 영상 MP4](outputs/checkvalve-hybrid-final.mp4)
- [제목·설명·최종 대본](outputs/checkvalve-hybrid-title-description.txt)
- [제작 과정·비용·재현 방법](outputs/hybrid-production-guide.md)
- [다른 작업에서 이어가기](HANDOFF.md)
- [Blender 편집 원본](outputs/blender/checkvalve.blend)
- [필재 나레이션 WAV](outputs/piljae-v2.wav)

| 역할 | 실제 도구와 결과 |
|---|---|
| 핵심 원리 | Blender 5.2.2 LTS, 직접 만든 단면과 구동 키프레임 |
| 도입 | Higgsfield 이미지 2개(수정 포함) + 10초 영상 1개, 첫 8초 사용 |
| 음성 | 실제 API에서 조회·생성한 Typecast 필재, 자연 속도, 44.6초 |
| 편집 | Higgsedit, 도입 8초 + 본문 42초 |
| 자막 | 최종 음성에서 Whisper 시간 측정, 대본 91단어 모두 포함 |
| 출력 | 50초, 1080×1920, 24fps, 한국어 제목과 화면 자막 |

Higgsfield 실제 사용량은 **22.5크레딧**입니다. 시작 100 → 완료 후 77.5로 확인했습니다. Typecast 비용은 별도입니다. 첫 샘플의 Blender 본문은 540×960 렌더를 최종 편집에서 확대했으며, 원본 소스로 1080×1920 렌더도 가능합니다.

작업을 이어갈 때 HANDOFF.md와 제작 안내를 먼저 읽으세요. 설정은 config/higgsfield-typecast.json, Blender 소스와 실제 음성에 맞춘 시간표는 src/blender/, API 클라이언트는 src/typecast_api_bridge.py입니다.

Typecast 키는 각 PC에서 로컬로 설정합니다. Windows에서는 outputs/connect-typecast.ps1을 기본 실행하면 숨김 입력으로 보관하고 필재를 조회합니다. 생성은 별도 명령이며 기존 파일을 덮어쓰지 않습니다. [API 연결 안내](docs/typecast-api.md)를 참고하세요. 키·인증 파일·프레임 캐시는 Git에서 제외합니다.

python src/prepare_production.py는 새 실행의 요청 초안과 대본을 준비합니다. 이 명령만으로 Higgsfield 생성이 시작되지는 않습니다.

[이전 2D + InJoon 영상](outputs/checkvalve-final.mp4)과 [초기 분석·제작 기록](outputs/checkvalve-production-plan.md)은 이력입니다. 최신 결과는 위의 필재 버전이며 별도 썸네일과 유튜브 게시를 수행하지 않았습니다.
