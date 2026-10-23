# CareerGround Portable 0.3.0

경력 정리와 이력서부터 면접 준비·모의 면접·복습까지 ChatGPT에서 이어가는 무료 오픈소스 플러그인입니다.
CareerGround 자체 서버·DB·MCP·로그인·API 키·별도 앱 설치가 필요하지 않습니다.
MIT 라이선스는 [LICENSE](LICENSE)를 따릅니다.

## 시작하기

플러그인을 설치한 새 대화에서 다음처럼 요청하세요.

- “CareerGround 시작 방법을 알려줘.”
- “경력을 정리해서 JD 없이 기본 이력서를 만들고 싶어.”
- “선택한 이력서와 JD로 면접 질문을 준비해줘.”
- “파일 없이 운영 엔지니어 모의 면접을 코칭 방식으로 시작해줘. 질문은 하나씩 해줘.”
- “면접은 여기까지 하고 답변을 복습해줘.”

경력/이력서: setup → career-collect → career-review → base-resume → jd-discover → resume-tailor.
면접: interview-prepare → mock-interview → interview-reflect.
기존 interview-export/interview-review는 handoff/result 1.0 호환을 위해 유지합니다.

텍스트만으로 면접 전 과정을 진행할 수 있습니다. 코칭은 답변마다 피드백을 받고,
실전 연습은 마지막에 종합 피드백을 받습니다. 한 번에 질문 하나를 진행하고 언제든 멈출 수 있습니다.
프로젝트는 자료 재사용을 돕는 선택 사항이며 면접에 파일이나 JSON은 필수가 아닙니다.
경력 기준 파일을 쓰는 경우에는 사용자가 선택한 ID·버전을 확인합니다.

## 무료 사용과 음성

CareerGround 자체 이용료는 없습니다. ChatGPT의 모델·도구·음성·검색·파일 업로드와 사용량은
사용자 계정·기기·지역·제공 상태에 따라 다릅니다. 모든 계정의 설치·음성 접근이나 무제한 사용을
약속하지 않습니다. 제한에 도달해도 별도 API나 유료 크레딧으로 자동 전환하지 않습니다.

이용 가능한 환경에서 ChatGPT 기본 음성을 켜 연습할 수 있습니다. 플러그인이 마이크·음성 인식·
음성 합성을 별도로 실행하지 않습니다. 전사 확인 후 평가하며, 수정 전 답변의 평가·후보는
오래된 기록으로 제외합니다. 실제 음성 인식 정확도·정확한 타이머·백그라운드 지속은 보장하지 않습니다.

## 사실과 피드백

이력서 문장은 확인한 경력과 출처에 연결합니다. 사실 확인과 이력서/면접 사용 허용은 별개입니다.
공동 기여·사용 금지·미측정 수치를 지킵니다. 면접 답변, AI 피드백과 새 사실 후보를 구분하며
새 사실은 별도 검토 전 pending입니다. profile/resume를 자동 수정하지 않습니다.

## 저장과 재개

저장 요청 시 선택 자료, 질문, 답변 revision, 확인 여부, 피드백, 후보와 다음 단계를 담은
세션 JSON 및 읽기용 Markdown을 만들 수 있습니다. 파일 도구가 없으면 복사 가능한 요약을 제공합니다.
새 대화에서는 저장한 파일이나 요약을 직접 제공하세요. 자동 저장·프로젝트 생성·이동이나
모든 과거 대화의 기억을 보장하지 않습니다.

Python과 jsonschema가 이미 있는 환경에서는 다음 구조 검사를 실행할 수 있습니다.
일반 사용에는 코드 실행이 필요하지 않습니다. 없으면 구조 검사 미실행으로 표시합니다.

```bash
python references/interview.py session.json --review session.md
python references/portable.py career-workspace-vNN.json --review career-workspace-vNN.md
python references/exchange.py handoff-vNN.json --result result-vNN.json
```

[공통 규칙](references/workflow.md), [면접 규칙](references/interview-workflow.md),
[세션 schema](references/schemas/interview-session-1.0.schema.json),
[기존 전달 계약](references/exchange-contract.md)을 참고하세요.
검사 통과는 사실 인증·사용자 신원·문장 의미·모델 지침 준수의 증명이 아닙니다.

## 개인정보와 지원 범위

개인 자료를 플러그인 배포물에 넣지 않습니다. 선택한 자료는 ChatGPT에서 처리하므로
기밀 자료는 공개 범위를 검토하고 불필요한 개인정보는 지워서 제공하세요.
ChatGPT 대화·프로젝트·Library·메모리와 다운로드·백업은 각각 관리·삭제합니다.
플러그인 제거로 모든 사본이 삭제되지는 않습니다.

실제 시험한 계정·기기·음성 범위는 공개 저장소의 지원 현황을 따릅니다.
텍스트로 음성 미지원 상황을 가정한 시험은 실제 무료 계정/기기 시험을 대신하지 않습니다.
