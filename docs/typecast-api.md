# Typecast 필재 API 연결 준비

상태: 2026-10-10 실제 API 인증과 필재 조회·음성 생성에 성공했습니다. 다른 PC에서는 로컬 키를 다시 설정해야 합니다.

## 확인한 공식 자료

- [필재 소개](https://typecast.ai/kr/learn/typecast-piljae-ai-voice-youtube-shorts/): Studio 제공 확인용. API 제공 여부의 증거는 아닙니다.
- [공식 API 문서](https://typecast.ai/docs/)
- [API 대시보드](https://typecast.ai/developers/api/)
- [API 요금 안내](https://typecast.ai/kr/pricing/api/)

Studio 구독과 API 이용은 별도입니다. 가격·크레딧·상업 이용 조건은 계정과 현재 공식 안내에서 확인하세요.

## Windows에서 키를 입력하고 필재만 조회

저장소 폴더에서 PowerShell로 실행합니다.

```powershell
.\scripts\connect-typecast.ps1
# 필요한 경우 Python 실행 파일 직접 지정
.\scripts\connect-typecast.ps1 -PythonCommand 'C:\path\to\python.exe'
```

입력은 화면에 표시하지 않습니다. 키는 Windows 사용자 계정에 묶인 암호화 파일 `work/typecast-key.xml`로 보관하며 Git에서 제외합니다. 다른 PC에서는 다시 입력해야 합니다. 키를 바꾸려면 해당 로컬 파일을 삭제하고 다시 입력합니다.

기본 실행은 목소리 목록 조회만 수행하며 음성을 생성하지 않습니다. 다른 환경에서는 `TYPECAST_API_KEY` 환경 변수를 안전하게 설정한 뒤 실행합니다.

```sh
python src/typecast_api_bridge.py
```

클라이언트는 Python 표준 라이브러리만 사용합니다. `API_KEY_NOT_CONFIGURED`는 키가 없는 상태입니다. 인증 성공이나 필재 지원을 뜻하지 않습니다.

## 인증 확인 후 음성 생성

발화 대본은 로컬 `work/project/narration.txt`에 준비합니다. 제목·설명·해시태그를 TTS에 넣지 않습니다. 환경 변수에 키가 설정된 터미널에서:

```sh
python src/typecast_api_bridge.py --generate --script work/project/narration.txt --out work/project/piljae.wav
```

명시적인 `--generate` 호출은 계정의 크레딧을 사용합니다. 이번 제작에서는 실제 필재 초안과 최종 음성을 생성했습니다. `POST /v1/text-to-speech`에 `ssfm-v30`, 조회한 `voice_id`, WAV 출력과 자연 속도(`audio_tempo=1.0`)를 보냅니다. 기존 출력이 있으면 덮어쓰지 않습니다. 주제별 대본과 생성 음성은 Git에 포함하지 않습니다.

키나 HTTP 오류 본문을 출력하지 않고 인증 정보를 포함한 리디렉션도 따르지 않습니다. 네트워크 오류로 결과가 불명확한 경우 재생성을 자동 반복하지 않습니다.

실제 목록에서 필재 original 음성과 ssfm-v30 지원을 확인했고 WAV 형식과 길이도 검증했습니다. 최종 음성은 44.6초입니다. 다음 실행에서도 실제 계정의 목록을 확인하며 임의의 voice_id나 다른 음성으로 대체하지 않습니다.
