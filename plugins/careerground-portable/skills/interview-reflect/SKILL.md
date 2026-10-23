---
name: interview-reflect
description: Reflect on a mock interview from the current conversation or a saved session, separate confirmed answers from feedback, and propose pending career facts for separate review.
---

# 면접 복습과 다음 연습

[공통 규칙](references/workflow.md)과 [면접 규칙](references/interview-workflow.md)을 적용한다.
사용자의 명시적 요청이 이 스킬의 기본 진행 방식보다 우선한다.

현재 대화 또는 사용자가 선택한 세션/답변으로 복습한다. 원문을 읽을 수 없으면 요청하며
기억으로 답변을 복원하지 않는다. 세션 파일은 [interview.py](references/interview.py)와
[schema](references/schemas/interview-session-1.0.schema.json)로 검사하고 미실행 시 미검증으로 표시한다.
기존 handoff/result 1.0 파일을 재검토하는 요청은 `interview-review`를 사용한다.

- 답한 문항과 미응답 문항, 확인한 최신 답변 revision을 구분한다.
- 수정 전 평가·후보는 stale로 제외한다. 미확인 음성 전사는 평가·경력 후보로 사용하지 않는다.
- 질문/사용자 답변/AI 피드백을 구분해 강점과 다음 연습 과제를 각각 1~3개 제안한다.
  근거가 부족하면 판단을 보류한다. 점수·합격 확률·객관적 경력 인증을 만들어 내지 않는다.
- 새 경력 사실 후보는 정확한 답변 원문과 질문 ID·답변 revision을 연결해 pending으로 제시한다.
  사실의 정확성과 이력서/면접 사용 허용은 별개로 `career-review`에서 확인한다.
  AI 요약·예시 답변을 사용자 원문으로 바꾸거나 기준 profile/resume를 자동 수정하지 않는다.
- 새 대화용 요약에는 선택 자료·제약·진행 상태·다음 질문을 담는다. 민감한 전체 원문은
  사용자가 요청한 범위만 포함한다. 다운로드/프로젝트 등록 여부는 실제 확인한 상태로 보고한다.

다음 연습은 보완할 답변 하나부터 시작할 수 있다. 복습 후 곧바로 전체 면접을 반복하도록 강요하지 않는다.
