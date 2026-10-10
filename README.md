# 쇼츠 제작: 명령어와 환경설정

Blender 애니메이션 + Higgsfield 보조 영상 + Typecast **필재**를 사용하는 작업 환경입니다. 이 저장소에는 실행 명령, 설정 문서, Typecast 연결 스크립트만 보관합니다. 대본·주제별 제작 코드·영상·음성·자막·이미지·Blender 원본은 각 작업 환경에서 별도로 관리합니다.

- [환경설정과 실행 명령](docs/workflow-commands.md)
- [Typecast API 연결 안내](docs/typecast-api.md)
- [작업 인계와 제작 기준](HANDOFF.md)
- [제작 설정](config/higgsfield-typecast.json)

현재 레퍼런스: https://www.youtube.com/shorts/q5C9HCN2QY4

제작 기준은 **애니메이션을 계속 진행하며, 내레이션이 화면의 변화와 다음 결과를 이어서 설명하는 것**입니다. 다음 주제는 이 레퍼런스를 분석한 뒤 다시 정합니다. 음성은 필재로 유지합니다.

API 키는 로컬에만 보관합니다. Windows 연결 스크립트는 키를 숨김 입력으로 받아 사용자 계정에 묶인 암호화 파일로 저장합니다. 다른 PC에서는 키와 Higgsfield 연결을 다시 설정해야 합니다.

이전 커밋에 있던 제작 결과물은 최신 버전의 추적 대상에서 제외했습니다. 과거 커밋의 기록은 유지됩니다.
