# Claude Code 실행 프롬프트

가장 쉬운 방법은 저장소 루트(로컬 `work/typecast-key.xml`이 있는 기존 클론)에서 아래 명령을 실행하는 것입니다. 최신 main을 받고, 필요한 도구를 점검한 뒤, 아래 프롬프트의 `<slug>`를 채워 `work/<slug>/claude-prompt.txt`로 만들고 Claude Code를 엽니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-production.ps1 -Slug refrigerator
# 점검과 프롬프트 생성만: -NoLaunch / Blender 경로가 다르면: -BlenderPath 'D:\...\blender.exe'
```

직접 붙여 넣을 때는 `<slug>`를 주제 폴더 이름으로 바꿉니다. 현재 다음 제작 주제는 `refrigerator`(원리 + 마지막 정보 포맷)입니다. `canal-lock`(단순화 반영)과 `immersed-tunnel` 초안도 보관합니다.

```text
이 저장소에서 50초 9:16 쇼츠를 한국어 세트와 영어 세트로 제작해 줘. 주제 폴더는 topics/<slug>/ 이야.
두 세트는 같은 화면 편집과 효과음을 쓰고, 나레이션·자막·고정 제목만 다르게 만들어(config의 language_sets).
이번 기준 세 가지를 꼭 지켜: (1) 3D는 config의 visual_clarity대로 단순하고 한눈에 이해되게, (2) 화면 텍스트는 고정 제목 하나와 자막뿐이고 진행 칩·단계 제목·부품 이름표는 넣지 않기, (3) 자막과 제목 뒤에 배경 패널·띠·상자를 넣지 않고 외곽선과 그림자만 쓰기.

먼저 읽기: README.md, HANDOFF.md, docs/immersion-guide.md, docs/workflow-commands.md, docs/typecast-api.md, config/higgsfield-typecast.json, topics/<slug>/ 의 brief.md, narration.txt, narration.en.txt(있으면), title-description.txt, title-description.en.txt(있으면), topic.json.
전역 규칙은 config, 주제별 규칙은 topic.json이 우선이야. 두 파일의 guards는 전부 지켜.

1. 대본 점검
- narration.txt가 brief.md의 정확성 기준과 맞는지 확인해. 사실 오류가 있으면 고칠 문장을 제안하고 내 승인을 받아. 표현은 임의로 바꾸지 마.
- topic.json의 format을 확인해. principle_info면 끝 정보(final_info)가 원리에서 바로 나오는지 확인해.

2. 필재 음성
- .\scripts\connect-typecast.ps1 로 필재 조회만 먼저 실행하고 voice_id와 ssfm-v30 지원을 확인해.
- 현재 Typecast 잔액과 예상 사용량을 보여 주고 내 승인 후 생성해. 출력: work/<slug>/piljae.wav (덮어쓰기 금지).
- 원음 길이를 측정해. config의 length_budget(원음 46초 이하)을 조금 넘으면 영상 길이를 늘리는 안(예: 51초)과 대본 축약안을 함께 보여 주고 내가 고르게 해. 속도를 올리거나 잘라서 맞추지 마.
- atempo 0.94 → apad → atrim 50초로 narration-final.wav를 만들고, 실제 사용할 호스팅 오디오를 Whisper로 분석해 문장별 시작·끝 시간을 work/<slug>/timing.json에 저장해.
- 실측 시간으로 topic.json의 clips timeline과 brief.md 장면표를 갱신해.

2-1. 영어 음성 (config의 voice_en, 화면 기준은 필재 timing.json)
- narration.en.txt가 없으면 한국어 문장마다 한 줄씩 영어 대본을 새로 써서(같은 사실·같은 순서, 직역 금지) 내 승인을 받아. 각 줄은 해당 한국어 문장 구간 안에 끝나는 길이로 쓰고, 훅 반응어는 한국어 펀치인 시점 근처에 오게 해.
- 부드럽고 설명형인 성인 남성 영어 음성을 쓴다. voice_en.name_eng가 비어 있으면 .\scripts\connect-typecast.ps1 -ListVoices -Gender male -UseCase 'E-learning/Explainer' 로 후보와 미리듣기 URL을 보여 주고 내가 고르게 해.
- 잔액과 예상 사용량(영어는 글자 수만큼)을 보여 주고 승인 후 -VoiceName <이름> -Language eng 로 생성. 출력: work/<slug>/en-voice.wav (덮어쓰기 금지).
- atempo 0.94 후 문장 사이 무음에서 잘라 각 영어 문장을 같은 한국어 문장의 시작 시각에 배치해 narration-final-en.wav(영상 길이와 동일)를 만들어. 다음 문장 시작 전에 끝나지 않으면 해당 줄을 줄여 다시 생성하자고 제안해. 속도를 올리거나 자르지 마.
- Whisper(영어)로 work/<slug>/timing-en.json을 저장해.

3. Blender
- topic.json의 blender.groups에 있는 것만 만들어 work/<slug>/scene.blend에 저장해. 목록에 없는 부품·소품·반복 디테일은 넣지 마. EEVEE, AgX, 밝고 고른 조명, 작은 베벨.
- config visual_clarity와 topic.json color_roles를 따라: 기본 시점 하나를 60% 이상, 같은 좌→우 방향, 지금 말하는 부분만 뚜렷이 움직이고, 처음 언급되는 부품은 노란 테두리 빛 약 1.5초. 안개·파티클 효과·피사계심도·어두운 장면 금지.
- 모든 움직임을 timing.json의 문장 시간에 맞춰 키프레임으로 동기화해. 1초 넘게 멈춘 화면이 없게 하고 시작·끝은 0.4초 이상 가속·감속. 와이드 샷엔 사람 실루엣 하나로 크기 비교.
- 먼저 brief.md의 스타일 프레임 4장만 렌더해서 나에게 보여 줘. 각 장을 360px 흑백으로 줄인 버전도 같이 보여 주고, 장마다 '시청자가 볼 것 하나'를 적어. 내가 승인하기 전엔 전체 렌더와 유료 생성을 하지 마.
- 렌더 출력 경로는 절대 경로로 넘겨.
- Higgsfield 생성 전에 각 비트의 대표 프레임을 PNG로 뽑아 guards와 대조하고, 나에게 보여 준 뒤 진행해.

4. Higgsfield
- topic.json의 clips대로 Kling 3 Pro 무음, 9:16, 승인된 Blender 프레임을 시작 이미지로 사용해. end_frame이 있으면 지정해. 프롬프트에 같은 단순한 모양·색 유지, 새 물체·사람 무리·글자·사실적 잡동사니 금지를 넣어.
- 생성 전 견적과 잔액을 보여 주고 승인을 받아. 모든 job_id를 work/<slug>/jobs.json에 저장해. 결과가 불명확한 요청은 자동 재시도하지 마.
- 결과의 이동 방향, 구조, 물리 순서를 guards와 대조해. 틀리면 기준 프레임을 보강해서 다시 생성할지 나에게 물어봐.

5. 사운드
- topic.json의 sound_design대로 원본 효과음 트랙을 만들고 필재와 미리 믹스해(필재가 항상 가장 크게). 자막 분석엔 깨끗한 필재만 써.
- 같은 효과음 트랙을 영어 나레이션과도 따로 믹스해(mixed-audio-en.wav). 영어 자막 분석엔 깨끗한 영어 음성만 써.

6. 편집
- 1080×1920·24fps, 원본 화면은 꽉 채우고 텍스트는 오버레이. config의 layout(v3)을 따라:
  상단 0~500px 텍스트 금지, 500~660px 영상 내내 같은 고정 제목 한 줄(topic.json title_fixed), 660~1140px 주요 동작의 중심, 1140~1380px 자막(한 줄·두 줄 블록 중심 y=1260), 1380px 아래와 오른쪽 버튼 열은 텍스트 금지.
  진행 칩·단계 번호·단계별 제목·부품 이름표는 넣지 마. 고정 좌표를 모든 폰의 공식 safe area로 간주하지 말고 기종별 표시 비율과 UI로 확인해.
  Blender 카메라와 생성 클립 구도도 주요 동작이 660~1140px 중심에 오도록 잡아.
- 자막: Noto Sans CJK KR Bold, 3.8%, 폭 74% 이내(외곽선 포함), 최대 4어절·22자·두 줄, caption_keywords는 #FFD400 노란색.
- 자막과 제목 뒤에 배경 상자·띠·패널·블러를 넣지 마. 흰 글자 + 8px 어두운 외곽선 + 부드러운 그림자만. 읽기 어려우면 구도나 배경 밝기를 조정해.
- 가로 중앙 정렬 필수: 제목과 자막 각 줄 모두 x=540 기준 정확히 가운데, 좌우 여백 대칭.
- 훅 반응어는 짧은 저음과 노란색으로 강조하되 위치·크기 상한을 지켜. topic.json visual_direction이 있으면 그 질감·가속감속·카메라 상한을 우선 적용해. 강한 펀치인 없이 기본 시점과 중간 거리 화면을 유지해.
- 핵심 순간(brief.md에 슬로모션으로 표시된 장면)은 속도 램프와 저음 효과로 강조해.
- 마지막 프레임이 첫 프레임 구도와 이어지게 맞춰.
- 영어 세트: 같은 화면 편집에 영어 믹스 오디오, 영어 자막(config captions_en: 최대 5단어·26자·두 줄, caption_keywords_en 노란색), 영어 고정 제목(title_fixed_en)을 올려. 영어 세트에는 한국어 글자를 넣지 마. 레이아웃·중앙 정렬 규칙은 한국어와 같아.

7. 검수 (전부 통과해야 완료)
- ffprobe: 영상·음성 길이가 같고 계획 길이(기본 50.000초, 늘리기로 정했으면 그 길이)와 일치, 1080×1920, 24fps. 전체 디코딩 통과.
- 자막 문구가 narration.txt와 일치, 정렬 유사도 0.90 이상, 누락 없음.
- 시작·중간·끝 프레임을 360px 폭으로 확인: 겹침, 글꼴, 대비, 크기. 보수적인 폰 UI 가림 마스크(상단 500px, 하단 540px, 오른쪽 버튼 열)와 9:16·9:19.5·9:20 표시 예시를 겹쳐서 텍스트가 마스크에 닿지 않는지 확인하고, 그 미리보기 이미지를 나에게 보여 줘.
- 가장 긴 두 줄 자막과 반응어도 같은 안전 영역 안에 있는지 확인해. 단면·부품 설명 중에도 전체 구조를 파악할 수 있어야 해.
- 화면에 고정 제목과 자막 외의 글자가 없는지, 자막·제목 뒤에 배경 패널이 없는지 확인해.
- 대표 프레임을 360px 흑백으로 줄여 무엇이 움직이는지 1초 안에 보이는지 다시 확인해.
- 같은 프레임에서 제목·자막 텍스트의 좌우 여백 차이 2px 이하인지 측정. 넘으면 고치고 다시 렌더해.
- 1초 넘게 변화 없는 구간이 없는지 프레임 차이로 확인.
- 첫 프레임과 마지막 프레임 구도 비교.
- 영어 세트도 같은 항목을 검수해(자막은 narration.en.txt와 일치, 유사도 0.90 이상, 각 영어 문장이 다음 한국어 문장 시작 전에 끝나는지, 영어 세트에 한국어 글자가 없는지).
- 결과를 outputs/<slug>-verification.json에 ko·en 두 세트로 저장해.

8. 전달
- 한국어: outputs/<slug>-final.mp4, outputs/<slug>.srt / 영어: outputs/<slug>-final-en.mp4, outputs/<slug>.en.srt / outputs/<slug>-verification.json.
- title-description.txt와 title-description.en.txt의 제목 후보·설명·해시태그를 실제 결과에 맞게 다듬어서 최종본을 함께 보여 줘.
- 썸네일 제작과 유튜브 게시는 하지 마.

9. Git
- topics/<slug>/의 텍스트, docs, config 변경만 커밋해. 영상·음성·Blender 파일·키·서명 URL은 절대 커밋하지 마.
- HANDOFF.md에 이번 제작 결과(실측 길이, 사용 크레딧, job_id 위치, 검수 결과)를 짧게 추가해.
```
