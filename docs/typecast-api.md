# Typecast 필재 API 연결 준비

상태: 연결 코드 준비 완료. 인증 미완료, 실제 음성 목록 조회와 생성은 미실행.

## 확인한 공식 자료

- [필재 소개](https://typecast.ai/kr/learn/typecast-piljae-ai-voice-youtube-shorts/): Studio 제공 확인용. API 제공 여부의 증거는 아닙니다.
- [공식 API 문서](https://typecast.ai/docs/)
- [API 대시보드](https://typecast.ai/developers/api/)
- [API 요금 안내](https://typecast.ai/kr/pricing/api/)

Studio 구독과 API 이용은 별도입니다. 가격·크레딧·상업 이용 조건은 계정과 현재 공식 안내에서 확인하세요.

## Windows에서 키를 입력하고 필재만 조회

저장소 폴더에서 PowerShell로 실행합니다.

```powershell
.\outputs\connect-typecast.ps1
# 필요한 경우 Python 실행 파일 직접 지정
.\outputs\connect-typecast.ps1 -PythonCommand 'C:\path\to\python.exe'
```

입력은 화면에 표시하지 않습니다. 키는 Windows 사용자 계정에 묶인 암호화 파일 `work/typecast-key.xml`로 보관하며 Git에서 제외합니다. 다른 PC에서는 다시 입력해야 합니다. 키를 바꾸려면 해당 로컬 파일을 삭제하고 다시 입력합니다.

기본 실행은 목소리 목록 조회만 수행하며 음성을 생성하지 않습니다. 다른 환경에서는 `TYPECAST_API_KEY` 환경 변수를 안전하게 설정한 뒤 실행합니다.

```sh
python src/typecast_api_bridge.py
```

클라이언트는 Python 표준 라이브러리만 사용합니다. `API_KEY_NOT_CONFIGURED`는 키가 없는 상태입니다. 인증 성공이나 필재 지원을 뜻하지 않습니다.

## 인증 확인 후 음성 생성

`src/checkvalve/script.json`에서 말할 문장만 UTF-8 텍스트로 저장합니다. 제목·설명·해시태그를 TTS에 넣지 않습니다. 환경 변수에 키가 설정된 터미널에서:

```sh
python src/typecast_api_bridge.py --generate --script work/narration-script.txt --out outputs/piljae.wav
```

명시적인 `--generate` 호출은 계정의 크레딧을 사용합니다. 이 인계에서는 실행하지 않았습니다. `POST /v1/text-to-speech`에 `ssfm-v30`, 조회한 `voice_id`, WAV 출력과 자연 속도(`audio_tempo=1.0`)를 보냅니다. 기존 출력이 있으면 덮어쓰지 않습니다.

키나 HTTP 오류 본문을 출력하지 않고 인증 정보를 포함한 리디렉션도 따르지 않습니다. 네트워크 오류로 결과가 불명확한 경우 재생성을 자동 반복하지 않습니다.

실제 API 응답으로 검증해야 하는 준비 코드입니다. 현재 확인한 것은 문법 검사와 키 미등록 시 중단 동작이며 서버 연결 성공·필재 생성 성공은 아직 확인하지 않았습니다.
