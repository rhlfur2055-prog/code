# CLAUDE.md — CodeMaster Next 프로젝트 컨텍스트

## 프로젝트 개요
CodeMaster Next는 40일 완성 풀스택 개발자 부트캠프 + PCCE 시험 대비 플랫폼이다.
966개 학습 콘텐츠, 16개 카테고리, 마이크로서비스 아키텍처(Next.js + Spring Boot + FastAPI).

## 기술 스택
- Frontend: Next.js 14, React 18.2, TypeScript, Tailwind CSS
- Backend: Spring Boot 3.2.1 (:8080), FastAPI (:8000)
- DB: MySQL 8.0, Redis 7
- AI: YOLO v8, Whisper, EasyOCR
- Infra: Docker Compose, Nginx

## 핵심 디렉토리
- `src/app/` — Next.js App Router 페이지
- `src/components/` — React 컴포넌트
- `src/hooks/` — 커스텀 Hooks (useAuth, useApi, useProgress 등)
- `src/data/contents/` — 카테고리별 학습 JSON (java.json, spring.json, python.json 등)
- `src/data/pcce/` — PCCE 시험 대비 콘텐츠 (common/ + python/ 21일 커리큘럼)
- `src/types/` — TypeScript 타입 (Content, Category, CATEGORIES, ROADMAP)
- `backend/spring-ai-api/` — Spring Boot JWT 인증 + AI 프록시
- `backend/python-ai-server/` — FastAPI AI 서버

## 데이터 흐름
브라우저 → Next.js(:3000) → Spring Boot(:8080) → MySQL/Redis
                                    └→ FastAPI(:8000) → AI 모델

## 코딩 규칙
- TypeScript strict mode 사용
- 새 컴포넌트 → `src/components/`에 배치
- 새 Hook → `src/hooks/`에 배치
- 학습 데이터 → `src/data/contents/` (기존 Content 타입 스키마 유지)
- PCCE 데이터 → `src/data/pcce/`
- Docker 포트(3000, 8080, 8000) 임의 변경 금지

## 슬래시 명령어

### 학습 & 개발 명령어
- `/day [번호]` — 특정 학습일 핵심 요약 + 실무 코드
- `/vibe` — 현재 코드의 전체 아키텍처 흐름 설명
- `/debug` — Docker/풀스택 연동 에러 해결
- `/next` — 진도 기반 다음 단계 추천
- `/build [기능명]` — 새 기능 설계 + 구현
- `/review` — 코드 리뷰 (성능, 보안, 가독성)
- `/status` — 프로젝트 현황 (git status, docker 상태, 학습 진도율 한눈에 보기)

### PCCE 시험 대비 명령어
- `/pcce` — PCCE 시험 대비 모드 (빈칸채우기, 한줄수정, 코드작성 유형 집중)
- `/mock [문제수]` — PCCE 모의시험 모드. 실전처럼 빈칸채우기+한줄수정+코드작성 문제를 섞어서 출제. 기본값 10문제. 채점 결과와 정답 해설까지 제공.
- `/weak` — 취약 유형 분석. 이전 대화에서 틀린 문제 패턴을 분석하고, 약한 유형을 진단한 뒤 보강 문제를 자동 출제.
- `/sheet [주제]` — 치트시트 생성. 지정한 주제(예: 리스트, 문자열, 딕셔너리)를 시험 직전에 볼 수 있는 1페이지 핵심 요약표로 생성.
- `/compare A vs B` — 개념 비교. 헷갈리는 두 개념(예: list vs tuple, for vs while)을 표 형태로 차이점 정리.

## PCCE 모드 규칙
`/pcce` 입력 시 PCCE 1타 강사 페르소나로 전환:
- 초보자도 이해하는 쉬운 비유 사용
- 시험에 안 나오는 지엽적 내용 과감히 생략
- 답변 마지막에 반드시 [오늘의 1타 비법] 3줄 요약
- 문제 유형: 빈칸 채우기 / 한 줄 수정 / 코드 작성

## 40일 로드맵
Day 1-7: Java(80) → Day 8-14: Spring(100) → Day 15-17: Python(60)
→ Day 18-21: Algorithm(80) → Day 22-23: DB(50) → Day 24: Network(40)
→ Day 25: OS(40) → Day 26: CleanCode(30) → Day 27: Security(30)
→ Day 28: DevOps(40) → Day 29: Tools(30) → Day 30: Git(40)
→ Day 31-33: HTML/CSS(30) → Day 34-36: JS(40) → Day 37-38: React(30)
→ Day 39-40: AI(40) + 특강: PCCE 시험대비(21일분)
