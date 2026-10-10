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

## Higgsfield와 최종 편집

Higgsfield 이미지·영상 생성은 연결된 도구에서 실행합니다. 이 저장소에 Higgsfield API 인증 토큰이나 주제별 제작 소스를 넣지 않습니다. 구조의 정확성이 필요한 움직임은 Blender로 만들고 필요한 보조 장면만 생성합니다.

필재 발화를 기준으로 영상·장면 전환·제목·자막을 맞춥니다. 생성 영상의 원래 음성을 제외하고 최종 필재 음성만 사용합니다. 장면별 움직임이 멈추지 않는지, 화면 변화와 설명의 인과관계가 맞는지 검수합니다.

완성 결과물은 로컬 outputs/에 보관하며 Git에서는 제외합니다. 키·작업 캐시·개별 제작 소스도 추적하지 않습니다.
