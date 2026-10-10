# Blender + Higgsfield + Typecast 필재 제작

2026-10-10에 사용자 선택으로 이 경로를 실제 제작했습니다.

## 역할과 실제 작업

- Blender 5.2.2 LTS: 시트·마개·스프링·고정 지지대와 단면 하우징을 새로 제작. 마개 이동과 스프링 압축을 동일한 개방 값으로 연결하고 24fps 키프레임으로 저장했습니다.
- Higgsfield: 외형 도입 이미지를 만들고 원하지 않은 글자를 제거하는 수정 1회를 진행한 뒤 10초 영상 1개를 생성했습니다. 도입 영상의 첫 8초를 사용합니다.
- Typecast 필재: 실제 API 음성 목록에서 필재와 `ssfm-v30` 지원을 확인했습니다. 30.95초 초안 대신 확장한 최종 대본으로 44.6초 음성을 생성했습니다. 음성 속도는 1.0입니다.
- Higgsedit: 도입 영상·Blender 본문·필재 음성을 결합하고 한국어 제목과 부품 설명을 넣습니다. 생성 영상의 원래 오디오는 사용하지 않습니다.
- 자막: 최종 필재 WAV를 Whisper로 분석해 시간표를 만들고 표시 문구는 실제 최종 대본을 사용합니다. 초기 인식 결과가 낮아 medium으로 다시 검증했습니다. 일치율 90.40%, 대본·자막 91단어가 모두 포함됐습니다.

영상 구성은 도입 8초 + 본문 42초로 총 50초입니다. 끝부분은 개방·닫힘 원리를 움직임으로 정리합니다. 별도 썸네일과 유튜브 게시를 진행하지 않습니다.

## 비용 기록

Higgsfield 실제 계정 잔액: 시작 100 → 생성 완료 후 77.5. 사용량은 **22.5크레딧**입니다.

| 작업 | 개수 | 견적 크레딧 |
|---|---:|---:|
| Seedream 1K 이미지 및 글자 제거 수정 | 2 | 2.5 |
| MiniMax 2K·10초 도입 영상 | 1 | 20 |
| 합계 | | 22.5 |

Typecast API 사용료는 별도입니다. 두 요청의 대본 문자 수는 261자와 382자이며 실제 청구 내역을 대신하는 수치는 아닙니다.

## 다시 만들거나 수정하기

1. `src/blender/narration-script.txt`를 수정합니다.
2. 로컬 API 키가 없다면 `outputs/connect-typecast.ps1`을 기본 실행해 인증합니다. 인증 파일은 `work/typecast-key.xml`에 저장되며 Git에서 제외합니다.
3. 음성을 새 이름으로 생성합니다. 기존 파일은 덮어쓰지 않습니다.

```powershell
.\outputs\connect-typecast.ps1 -GenerateNarration -ScriptPath (Join-Path (Get-Location) 'src\blender\narration-script.txt') -OutputPath (Join-Path (Get-Location) 'outputs\piljae-next.wav')
```

4. 최종 음성의 발화를 분석해 `src/blender/timing.json`과 편집 스크립트의 제목 구간을 맞춥니다. 이전 자막 시간표는 다른 음성에 그대로 쓰지 않습니다.
5. Blender에서 장면을 생성·렌더링합니다.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --python src\blender\checkvalve_scene.py -- --preview --timing src\blender\timing.json
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --python src\blender\checkvalve_scene.py -- --render --timing src\blender\timing.json --start-frame 193
```

`--draft`는 렌더 크기를 540×960으로 줄입니다. 이번 샘플의 본문은 이 크기로 렌더링하고 최종 1080×1920 편집에서 확대했습니다. 위 두 번째 명령은 `--draft`가 없어 1080×1920으로 렌더링합니다. 프레임 파일은 `work/hybrid/frames/`에 생성합니다.

6. 프레임을 24fps MP4로 인코딩합니다. Higgsfield 보조 영상은 같은 연결 도구에서 생성한 완료 결과를 사용합니다.
7. Higgsfield 처리 환경에서 `src/blender/assemble-higgsedit.jsx`로 편집합니다. `HYBRID_ASSET_DIR`에 실제 입력 폴더의 절대 경로를 설정하세요. 필요한 입력은 `hook.mp4`, `blender-body.mp4`, `piljae.wav`, `NotoSansCJKkr-Bold.otf`입니다.
8. 최종 음성으로 자막을 분석·검증하고 설치된 자막 처리 도구로 삽입한 뒤 길이·음성 끝·대본 누락·화면을 검수합니다.

`.blend`에는 구동 키프레임이 저장되어 있어 Python 핸들러 없이도 움직입니다. 이 영상은 작동 원리를 설명하는 개념 애니메이션이며 유체 압력·누설량을 계산한 시뮬레이션은 아닙니다.
