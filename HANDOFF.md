# 작업 인계: Blender + Higgsfield + Typecast 필재

기준일: 2026-10-10 (Asia/Seoul)

## 확정된 목표

참고 채널 https://www.youtube.com/channel/UCEtLvsrVXP7QtodFwcyFckA 의 원리 설명 형식을 유지하며 주제 선정·대본·TTS·영상 생성·편집까지 제작합니다. 핵심 구조와 움직임은 **Blender**, 보조 도입은 **Higgsfield**, 음성은 **Typecast 필재**로 확정했습니다. 첫 주제는 스프링식 체크밸브, 50초·9:16입니다. 별도 썸네일과 유튜브 게시를 요청하지 않았습니다. 공개 GitHub 저장소에 결과와 소스를 계속 업데이트하도록 요청했습니다.

## 최신 결과

outputs/checkvalve-hybrid-final.mp4가 최신 완성본입니다. 도입 8초는 Higgsfield, 본문 42초는 Blender입니다. 필재 음성은 outputs/piljae-v2.wav, 제목·설명·대본은 outputs/checkvalve-hybrid-title-description.txt에 있습니다.

Blender 원본은 outputs/blender/checkvalve.blend이며 구동 키프레임으로 재생됩니다. 소스와 측정된 발화에 맞춘 시간표는 src/blender/에 있습니다. 이번 샘플은 540×960 본문 렌더를 최종 1080×1920 편집에서 확대했습니다. 같은 소스로 높은 해상도를 다시 렌더링할 수 있습니다.

검수: 영상·음성 50초, 1080×1920·24fps, 자막 24개, 대본 91단어 모두 포함, Whisper 정렬 90.40%, 전체 디코딩 통과, 시작·부품 설명·열림·마지막 자막 화면 확인. 상세 기록은 docs/hybrid-verification.json과 docs/hybrid-production-run.json입니다.

## 계정과 비용

Higgsfield Plus 연결을 확인했습니다. 실제 사용량은 22.5크레딧: 이미지 생성·글자 제거 수정 합계 2.5, 10초 영상 1개 20. 확인 시 잔액은 77.5이며 다음 실행 때 다시 조회하세요.

Typecast API 인증 후 실제 필재 original 음성과 ssfm-v30 지원을 확인했습니다. voice_id는 tc_68257f68bc6e3c161ab5078d입니다. 다음 실행에서도 이름과 지원 모델을 조회하세요. API 키와 음성 ID는 다릅니다.

30.95초 초안 대신 382자 최종 대본으로 44.6초 음성을 만들었으며 자연 속도 1.0을 유지했습니다. Typecast 청구 금액은 조회하지 않았습니다. 기존 InJoon 버전은 최신 결과가 아닙니다.

키는 로컬 work/typecast-key.xml에 보관하고 Git에서 제외했습니다. 다른 PC에서는 로컬 인증을 다시 설정해야 하며 키를 채팅·문서·저장소에 넣지 않습니다.

## 재사용 순서

1. 한 가지 원리를 설명할 주제를 정하고 공식 자료로 구조·작동 조건을 확인합니다.
2. 대본으로 실제 필재 음성을 생성하고 길이를 측정해 문장을 조정합니다.
3. 최종 발화로 장면 전환·자막 시간표를 만듭니다.
4. Blender에서 고정 부품·이동 부품을 나눠 만들고 연동한 키프레임으로 구동합니다.
5. Higgsfield 보조 장면을 생성하고 글자·형태 변화·완료 상태를 확인합니다.
6. Higgsedit로 필재 음성·영상·제목·부품 설명을 합칩니다. 생성 영상의 원래 오디오는 섞지 않습니다.
7. 자막을 분석·검증·삽입하고 길이·음성 끝·단어 누락·한글 화면을 검수합니다.
8. MP4와 제목·설명·대본, 원본·소스·검수 기록을 전달하고 Git을 업데이트합니다.

실행법은 outputs/hybrid-production-guide.md를 참고하세요. Higgsfield는 연결 도구로 실행하며 src/prepare_production.py는 입력 준비 도구입니다. 단독으로 모든 생성·편집을 실행하는 자동화 프로그램은 아닙니다.

## 설명 범위와 이전 이력

이 영상은 스프링식 체크밸브의 개념도입니다. 물은 마개를 관통하지 않고 열린 주변 틈을 통과합니다. 압력 차가 줄면 스프링이 닫고 역압도 닫힘을 돕습니다. 최소 개방 압력 차는 열리기 시작하는 조건이며 실제 압력·누설량을 계산한 유체 시뮬레이션이 아닙니다.

처음에는 당시 무료 계정에서 Higgsfield 생성이 거부돼 2D + InJoon 영상을 만들었습니다. 이후 사용자가 혼합 경로를 선택하고 Higgsfield 결제와 Typecast 키 설정을 진행해 필재 버전을 제작했습니다. 참고 영상 https://www.youtube.com/shorts/b3UHruGWlXg 의 실제 음성 제공자는 확정하지 못했으며 최신 제작은 사용자 선택에 따라 필재를 사용합니다.
