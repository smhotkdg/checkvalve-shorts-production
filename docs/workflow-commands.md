# 환경설정과 실행 명령

아래 명령의 `<slug>`는 주제 폴더 이름입니다(현재 `immersed-tunnel`). 주제별 작업 파일은 `work/<slug>/`에 둡니다.

## 한 번에 시작

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-production.ps1 -Slug <slug>
```

최신 main 받기 → 주제 파일·Typecast 키·Python·Blender·FFmpeg·Claude Code 점검 → `work/<slug>/claude-prompt.txt` 생성 → Claude Code 실행 순서입니다. `-NoLaunch`는 점검과 프롬프트 생성만 합니다.

## 필요한 환경

- Python 3: Typecast 연결 스크립트는 표준 라이브러리만 사용합니다.
- Blender: 현재 PC에서 5.2.2 LTS를 사용했습니다.
- FFmpeg: 렌더 프레임 인코딩, 속도 처리, 믹스에 사용합니다.
- Higgsfield: 연결된 계정과 크레딧이 필요합니다.
- Typecast: API 키가 필요합니다. Studio 이용과 API 이용은 별도입니다.

## Typecast 필재

저장소 폴더에서 PowerShell로 실행합니다. 기본 실행은 목소리 목록 조회만 합니다.

```powershell
.\scripts\connect-typecast.ps1
```

생성은 API 크레딧을 사용합니다. 기존 출력은 덮어쓰지 않습니다.

```powershell
New-Item -ItemType Directory -Force -Path work\<slug> | Out-Null
.\scripts\connect-typecast.ps1 -GenerateNarration -ScriptPath (Join-Path (Get-Location) 'topics\<slug>\narration.txt') -OutputPath (Join-Path (Get-Location) 'work\<slug>\piljae.wav')
ffprobe -v error -show_entries format=duration -of json work\<slug>\piljae.wav
```

원음이 46초를 넘으면 대본을 줄여 다시 생성합니다. 속도 처리는 피치를 유지하는 atempo를 쓰며, 자막 타이밍은 처리 전 음성에서 추정하지 않습니다. 최종 업로드된 음성을 다시 받아 실제 사용 오디오로 Whisper 분석을 합니다.

```bash
ffmpeg -i work/<slug>/piljae.wav -af 'atempo=0.94,apad,atrim=0:50' -ar 44100 -ac 1 work/<slug>/narration-final.wav
python3 "$HF_WORKFLOWS/video-montage/scripts/audio_to_captions.py" work/<slug>/narration-final.wav --srt work/<slug>/caps.srt --json work/<slug>/caption-report.json --script work/<slug>/script.json --language ko --model medium --max-words 4 --max-chars 22 --minimum-similarity .90
```

## Blender 렌더

`work/<slug>/scene.blend`에 모델과 키프레임을 저장합니다. 출력 경로는 반드시 절대 경로로 넘깁니다. 상대 경로는 드라이브 루트 기준으로 해석될 수 있습니다. 프레임 구간은 `topics/<slug>/topic.json`과 실측 타이밍으로 정합니다.

```powershell
New-Item -ItemType Directory -Force -Path work\<slug>\render | Out-Null
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background (Join-Path (Get-Location) 'work\<slug>\scene.blend') --render-output (Join-Path (Get-Location) 'work\<slug>\render\frame_') --render-format PNG --frame-start <START> --frame-end <END> --render-anim
ffmpeg -framerate 24 -start_number <START> -i work/<slug>/render/frame_%04d.png -frames:v <COUNT> -c:v libx264 -crf 19 -pix_fmt yuv420p work/<slug>/blender-body.mp4
```

Blender는 EEVEE, AgX, PBR 재질, 베벨, 환경광 차폐를 씁니다. 전체 장면과 근접 장면을 교대하고 각 장면 안에서도 카메라 시차와 실제 물체의 움직임을 유지합니다. 고정되어야 하는 구조는 움직이지 않게 하고, 불가능한 관통이나 공중 연결이 나오지 않게 합니다.

## Higgsfield

연결된 도구에서 실행합니다. 이 저장소에 Higgsfield 토큰이나 제작 소스를 넣지 않습니다. 클립 구성은 `topic.json`의 `video.clips`를 따릅니다. 승인된 Blender 프레임을 시작 이미지로 쓰고, 도착 상태가 중요한 장면은 끝 프레임도 지정합니다. 생성 전 견적·잔액 확인과 사용자 승인, 생성 후 방향·구조·순서 검수를 합니다.

## 사운드와 편집

필재와 효과음을 먼저 믹스한 50초 오디오를 한 번 배치합니다. Higgsedit의 cut 기본 트랙에 같은 시간대 오디오를 두 번 넣으면 충돌합니다. 자막 분석에는 혼합 파일 대신 깨끗한 필재를 씁니다.

```bash
ffmpeg -v error -y -i work/<slug>/narration-final.wav -i work/<slug>/sound-design.wav -filter_complex '[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]' -map '[a]' -c:a pcm_s16le work/<slug>/mixed-audio.wav
```

편집 스크립트는 주제별로 `work/<slug>/edit.jsx`에 둡니다.

```bash
higgsedit build work/<slug>/edit.jsx
ffprobe -v error -show_entries stream=codec_type,width,height,duration:format=duration -of json outputs/<slug>-final.mp4
ffmpeg -v error -i outputs/<slug>-final.mp4 -f null -
```

레이아웃(v2): 1080×1920 원본을 꽉 채워 배치하고 텍스트는 오버레이로 올립니다. 상단 0~300px와 하단 1450px 아래(쇼츠 UI가 덮는 영역), 오른쪽 버튼 열(x 960 이상, y 900~1920)에는 텍스트를 두지 않습니다. 제목·진행 칩은 300~470px, 주요 동작은 470~1250px, 자막 패널은 1250~1450px입니다. 원본 영상에 높이 1200px를 지정해 이중 중앙 정렬이 생기는 구성을 피합니다. 자막은 설치된 스킬 버너를 쓰며 자체 FFmpeg 자막 필터로 재구현하지 않습니다.

가로 중앙 정렬 검수 예시: 최종 영상의 시작·중간·끝 프레임을 뽑아 제목 띠(300~470px)와 자막 패널(1250~1450px)에서 텍스트 픽셀의 좌우 경계를 측정하고, 좌우 여백 차이가 2px 이하인지 확인합니다.

```bash
ffmpeg -v error -y -ss 25 -i outputs/<slug>-final.mp4 -frames:v 1 work/<slug>/check-mid.png
```

렌더 옵션: depth 8, bitrate 7000000, concurrency 2, shards 5. 편집 환경 메모리가 제한되어 렌더를 동시에 중복 실행하지 않습니다.

로컬 파일을 연결된 도구로 옮길 때는 업로드 슬롯을 받은 뒤 파일이 있는 환경에서 curl PUT을 실행하고 HTTP 200을 확인한 후 업로드를 확정합니다. 파일 바이트를 텍스트나 base64로 중계하지 않습니다. 비밀키와 서명된 업로드 주소를 Git에 저장하지 않습니다.
