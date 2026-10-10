# 환경설정과 실행 명령

## 필요한 환경

- Python 3: Typecast 연결 스크립트는 표준 라이브러리만 사용합니다.
- Blender: 현재 PC에서 5.2.2 LTS를 사용했습니다. 별도 프로그램입니다.
- FFmpeg: 렌더 프레임을 영상으로 합칠 때 필요합니다.
- Higgsfield: 연결된 계정과 해당 모델을 사용할 크레딧이 필요합니다.
- Typecast: API 키가 필요합니다. Studio 이용과 API 이용은 별도입니다.

제작 미디어와 주제별 Blender 파일·대본은 이 저장소에 포함하지 않습니다. 아래 명령의 입력 파일은 작업 환경에서 별도로 준비합니다.

## Typecast 필재 연결

저장소 폴더에서 PowerShell로 실행합니다.

```powershell
.\scripts\connect-typecast.ps1
```

기본 실행은 목소리 목록 조회만 수행합니다. 로컬 work/typecast-key.xml은 Windows 사용자 계정에 묶여 암호화되므로 다른 PC에서는 다시 입력합니다.

대본은 UTF-8 텍스트로 work/project/narration.txt에 준비한 뒤 생성합니다. 이 명령은 API 크레딧을 사용합니다.

```powershell
.\scripts\connect-typecast.ps1 -GenerateNarration -ScriptPath (Join-Path (Get-Location) 'work\project\narration.txt') -OutputPath (Join-Path (Get-Location) 'work\project\piljae.wav')
```

기존 출력은 덮어쓰지 않습니다. 음성 생성 후 실제 길이를 측정하고 장면·자막 시간을 맞춥니다.

## Blender 렌더

주제별 모델링·키프레임을 별도로 작성해 work/project/scene.blend에 저장합니다. 예시 명령은 입력 장면에 저장된 해상도·프레임 속도·구간을 사용합니다.

```powershell
New-Item -ItemType Directory -Force -Path work\render | Out-Null
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background work\project\scene.blend --render-output work\render\frame_ --render-format PNG --render-anim
```

24fps, frame_0001.png부터 시작하는 렌더의 인코딩 예시입니다. 다른 설정이면 번호와 속도를 실제 값으로 바꿉니다.

```powershell
ffmpeg -framerate 24 -start_number 1 -i work\render\frame_%04d.png -c:v libx264 -pix_fmt yuv420p work\project\blender-body.mp4
ffprobe -v error -show_entries format=duration -of json work\project\piljae.wav
```

현재 50초 구성은 Higgsfield 수중 도입 5초·정비 6초·출항 8초 + Blender 원리 설명 31초입니다. Blender 장면은 전체 50초·24fps로 설계하되 5~42초에 해당하는 121~1008 프레임을 준비합니다. 정비 6초는 편집에서 생성 영상으로 교체하므로 Blender 입력 37초 중 31초를 사용합니다. 입력 장면이 다른 구간으로 설계되어 있으면 실제 구간을 사용합니다.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background work\project\scene.blend --render-output work\render\frame_ --render-format PNG --frame-start 121 --frame-end 1008 --render-anim
ffmpeg -framerate 24 -start_number 121 -i work\render\frame_%04d.png -frames:v 888 -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -movflags +faststart work\project\blender-body.mp4
```

## Higgsfield와 최종 편집

Higgsfield 이미지·영상 생성은 연결된 도구에서 실행합니다. 이 저장소에 Higgsfield API 인증 토큰이나 주제별 제작 소스를 넣지 않습니다. 구조의 정확성이 필요한 움직임은 Blender로 만들고 필요한 보조 장면만 생성합니다.

필재 발화를 기준으로 영상·장면 전환·제목·자막을 맞춥니다. 생성 영상의 원래 음성을 제외하고 최종 필재 음성만 사용합니다. 장면별 움직임이 멈추지 않는지, 화면 변화와 설명의 인과관계가 맞는지 검수합니다.

현재 모델 설정은 MiniMax H3 2K 5초 도입, Kling 3 Pro 무음 6초 정비, Kling 3 Pro 무음 8초 출항입니다. 모두 9:16이며 각 장면의 Blender 기준 프레임을 시작 이미지로 씁니다. 출항에는 정확한 도착 상태의 끝 프레임도 지정합니다. 별도 이미지 생성은 필요하지 않습니다. 실제 모델 비용을 조회한 후 생성합니다. 2026-10-10 기준 합계는 첫 시도 31크레딧이며, 이번 재제작은 제외한 출항 시도까지 포함해 47크레딧을 사용했습니다. 비용만을 줄이기 위해 필요한 액션 장면이나 카메라 움직임을 생략하지 않습니다. 생성 후 이동 방향·게이트 통과·지지 구조를 검수하고 오류가 있으면 기준 프레임을 보강해 수정합니다.

최종 편집은 연결된 Higgsedit의 1080×1920·24fps 타임라인에서 수중 도입 0~5초, Blender 5~27.28초, 생성 정비 27.28~33.28초, Blender 33.28~42초, 생성 출항 42~50초로 배치합니다. 필재 음성은 0초 시작입니다. 실제 음성 길이와 장면을 측정해 이 구간을 조정합니다. 자막은 최종 음성을 Whisper로 분석한 뒤 정확한 원본 대본과 대조합니다. 한국어 글꼴 Noto Sans CJK KR Bold를 사용하고, 자막을 넣은 뒤 시작·중간·끝 화면과 영상·음성 길이를 다시 확인합니다.

Blender는 EEVEE 조명과 재질, 원근 카메라를 사용합니다. 전체 장면·접근 장면·받침 근접 장면을 교대로 구성하고, 각 장면에서도 카메라 시차와 실제 물체의 움직임을 유지합니다. 낮은 음량의 배경 리듬과 작업·물·금속·출항 효과음을 별도 트랙으로 더하며 내레이션을 우선합니다.

현재 편집 스크립트에서는 필재와 효과음을 먼저 믹스한 50초 오디오를 한 번 배치합니다. Higgsedit의 cut 기본 트랙에 같은 시간의 오디오를 두 번 넣으면 충돌하므로, 별도 트랙을 지원하는 편집 방식을 쓰거나 다음과 같이 오디오 입력을 미리 합칩니다. 자막 분석에는 이 혼합 파일 대신 깨끗한 필재 원본을 사용합니다.

```bash
ffmpeg -v error -y -i work/project/piljae.wav -i work/project/sound-design.wav -filter_complex '[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]' -map '[a]' -c:a pcm_s16le work/project/mixed-audio.wav
```

Higgsedit 제작 스크립트는 저장소에 포함하지 않습니다. 별도로 준비한 주제별 편집 스크립트가 연결된 실행 환경의 work/project/edit.jsx에 있을 때 다음 명령으로 실행합니다.

```bash
higgsedit build work/project/edit.jsx
ffprobe -v error -show_entries stream=codec_type,width,height,duration:format=duration -of json work/project/final.mp4
ffmpeg -v error -i work/project/final.mp4 -f null -
```

현재 연결된 편집 환경은 메모리가 제한되어 있으므로 렌더를 동시에 중복 실행하지 않습니다. 편집 스크립트의 p.render 옵션은 depth 8, bitrate 6500000, concurrency 2, shards 5를 사용합니다. 2K 생성 영상과 1080p 프레임을 함께 처리할 때 기본 동시 작업 수보다 메모리를 안정적으로 사용합니다.

로컬 제작 파일을 연결된 도구로 옮길 때는 업로드 슬롯을 받은 뒤 파일이 있는 환경에서 curl PUT을 실행하고, HTTP 200을 확인한 후 업로드를 확정합니다. 파일 바이트를 텍스트나 base64로 중계하지 않습니다. 비밀키와 서명된 업로드 주소를 Git에 저장하지 않습니다.

완성 결과물은 로컬 outputs/에 보관하며 Git에서는 제외합니다. 키·작업 캐시·개별 제작 소스도 추적하지 않습니다.

## 상세 모델과 더 읽기 쉬운 자막 기준

현재 설정 파일의 활성 주제는 외부 톱 클라이밍 타워크레인입니다. 과거 드라이독 예시와 타임라인을 새 주제에 그대로 적용하지 않습니다. Blender 본문 입력은 5~44초, 121~1056 프레임이며 생성 연결부 장면 4초를 교체해 Blender 35초와 생성 영상 15초를 사용합니다. 실제 발화와 승인된 구조를 기준으로 구간을 다시 측정합니다.

렌더 출력 경로는 반드시 절대 경로로 넘깁니다. Blender가 상대 출력 경로를 드라이브 루트 기준으로 해석할 수 있습니다.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background (Join-Path (Get-Location) 'work\project\scene.blend') --render-output (Join-Path (Get-Location) 'work\render\frame_') --render-format PNG --frame-start 121 --frame-end 1056 --render-anim
ffmpeg -framerate 24 -start_number 121 -i work/render/frame_%04d.png -frames:v 936 -c:v libx264 -crf 19 -pix_fmt yuv420p work/project/blender-body.mp4
```

장비는 기초·고정 마스트·상부·클라이밍 케이지·유압 잭·삽입 마스트를 별도 그룹으로 모델링합니다. 전체 이동과 유압 로드 스트로크를 연결하고 새 부재의 레일 높이와 삽입 끝 상태를 확인합니다. 강재의 격자, 연결 플랜지·육각 볼트, 호스와 케이블을 보존합니다. 하중 균형·지지·클리어런스를 확인하고 불가능한 관통이나 공중 연결부가 나오지 않게 합니다.

필재 속도 조정에는 피치를 유지하는 atempo를 쓰되, 자막 타이밍은 조정 전 음성에서 추정하지 않습니다. 최종 업로드된 음성을 다시 받아 실제 사용 오디오에서 Whisper로 분석합니다.

```bash
ffmpeg -i piljae.wav -af 'atempo=0.94,apad,atrim=0:50' -ar 44100 -ac 1 narration-final.wav
python3 "$HF_WORKFLOWS/video-montage/scripts/audio_to_captions.py" narration-final.wav --srt caps.srt --json caption-report.json --script script.json --language ko --model medium --max-words 4 --max-chars 22 --minimum-similarity .90
```

영상 본문 창은 1080×1920 원본을 배치하고 상단 0~280px와 하단 1480px 이후에 제목·자막 패널을 올립니다. 원본 영상에 높이 1200px를 지정해 이중 중앙 정렬이 생기는 구성을 피합니다. 제목과 자막은 Noto Sans CJK KR Bold, 자막 크기 기준 3.8%·폭 80%·하단 여백 15%·최대 두 줄입니다. 문장을 4어절·22자 이내로 짧게 나누면 일괄 축소를 줄일 수 있습니다. 실제 제목·자막이 들어간 시작·중간·끝 프레임을 360px 너비로 보고 겹침, 글꼴, 대비와 크기를 확인합니다. 자막 생성은 설치된 스킬 버너를 사용하며 자체 FFmpeg 자막 필터로 재구현하지 않습니다.
