# CareerGround Portable

경력 정리 → 이력서 → 면접 준비 → 모의 면접 → 복습을 ChatGPT에서 이어가는 무료 오픈소스 플러그인입니다.

CareerGround 자체 서버, 회원가입, 별도 앱이나 AI API 키가 필요하지 않습니다.
텍스트만으로 전체 면접 흐름을 사용할 수 있고, 지원되는 환경에서는 ChatGPT 기본 음성을 선택할 수 있습니다.
MIT 라이선스로 사용·수정·재배포할 수 있습니다.

## 사용하기

ChatGPT에서 CareerGround Portable을 설치한 새 대화에 다음 중 하나를 입력하세요.

- “경력을 정리해서 기본 이력서를 만들고 싶어.”
- “선택한 이력서와 JD로 면접 질문을 준비해줘.”
- “파일 없이 운영 엔지니어 모의 면접을 시작해줘. 질문은 하나씩 해줘.”
- “면접 답변을 복습하고 다음에 연습할 내용을 정리해줘.”

프로젝트는 선택 사항입니다. 면접은 목표 직무만으로도 시작할 수 있습니다.
코칭은 답변마다 피드백을 받고 실전 연습은 마지막에 종합 피드백을 받습니다.
기준 경력 파일을 사용하면 출처·버전·사용 허용을 확인해 재사용합니다.

## 설치와 공개 상태

GitHub 소스 공개와 ChatGPT 공개 플러그인 디렉터리 배포는 별개입니다.
공개 디렉터리 게시 전에는 누구나 이름으로 검색·설치할 수 있다고 약속하지 않습니다.
현재 상태는 [지원 현황](SUPPORT.md)을 확인하세요.

ChatGPT 계정에 개인용 플러그인 ZIP 추가 기능이 제공되면 릴리스의
`careerground-portable-0.3.0.zip`을 사용할 수 있습니다. 해당 메뉴가 없는 계정에는
ZIP 설치 가능성을 보장하지 않습니다. 공개 디렉터리 심사·게시 상태를 확인하세요.

Codex의 Git marketplace 설치는 `.agents/plugins/marketplace.json`을 사용하는 개발자용 경로입니다.
ChatGPT 웹·모바일의 일반 사용자 설치를 대신하는 것으로 설명하지 않습니다.

## 무료 제공 범위

CareerGround는 무료입니다. ChatGPT의 모델·검색·파일·음성과 사용량은 각자의 계정·기기·지역·
제공 상태를 따릅니다. 무제한 사용과 모든 계정의 동일한 음성 기능을 보장하지 않습니다.
제한에 도달해도 별도 API나 결제로 자동 전환하지 않습니다.

## 사실을 다루는 방식

문장을 경력·출처에 연결하고 공동 기여, 미측정 수치와 사용 금지를 유지합니다.
면접 답변, AI 피드백과 새 사실 후보를 구분합니다. 새 사실은 사용자가 정확한 내용과
이력서/면접 사용을 별도 검토하기 전에는 pending이며 경력 기준본에 자동 반영하지 않습니다.
음성 전사는 확인 후 평가합니다. 수정 전 답변의 평가는 오래된 기록으로 제외합니다.

## 저장과 개인정보

저장 요청 시 세션 JSON과 읽기용 요약을 만들 수 있습니다. 파일 도구가 없으면 복사 가능한
요약으로 이어갑니다. 새 대화에는 선택한 파일이나 요약을 직접 제공하세요.
자동 저장·프로젝트 등록·완전한 기억·모든 사본의 동시 삭제는 보장하지 않습니다.

플러그인에 개인 자료를 배포하지 않습니다. 사용자가 선택한 자료는 ChatGPT에서 처리됩니다.
공개 이슈에는 실제 이력서나 개인정보를 첨부하지 마세요. [개인정보 안내](PRIVACY.md)를 참고하세요.

## 개발과 검증

Python 3.12 이상과 jsonschema를 사용합니다. 개발 환경은 다음처럼 준비합니다.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -p 'test_portable*.py' -q
.venv/bin/python scripts/check_portable_plugin.py
.venv/bin/python scripts/build_chatgpt_plugin.py --variant portable --output /tmp/careerground-portable-0.3.0.zip
```

이 검사는 파일 구조·참조와 패키징을 확인합니다. 실제 설치 환경의 모델 응답·음성·무료 계정
지원 시험과 구분합니다. [기여 안내](CONTRIBUTING.md), [플러그인 설명](plugins/careerground-portable/README.md)을 참고하세요.

이 저장소는 공개 대상으로 선정한 Portable 소스와 합성 예제만 담습니다.
별도 Android 앱, 서버, 인증 설정, 개인 시험 기록과 기존 개발 Git 이력은 포함하지 않습니다.
