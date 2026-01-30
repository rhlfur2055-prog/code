# 🚀 VS Code AI 바이브코딩 실전 예제

## 📝 바로 복붙해서 쓰는 명령어 모음

### 1️⃣ 개념 학습 시리즈

#### Java 컬렉션 마스터하기
```
@workspace study/java/04_컬렉션/hashmap-internal.html 파일을 보고 HashMap의 내부 동작을 3단계로 설명해줘:
1. 초급: 비유를 들어서 쉽게
2. 중급: 해시 충돌 해결 방법
3. 고급: S-MAS 프로젝트에서 어떻게 활용할 수 있는지
```

#### Spring JPA N+1 문제 완전 정복
```
@workspace study/spring/07_JPA실전/n-plus-one.html 파일을 분석해서:
1. N+1 문제가 발생하는 실제 코드 예제
2. 해결 방법 3가지 (fetch join, entity graph, batch size)
3. S-MAS 프로젝트의 주차장-리뷰 관계에 적용하는 코드
```

#### 알고리즘 DFS/BFS 실전
```
@workspace study/algorithm/09_그래프/ 폴더의 dfs.html과 bfs.html을 참고해서:
1. DFS와 BFS의 차이를 표로 정리
2. 각각 언제 사용하는지 실제 문제 예시
3. 백준 1260번 문제 풀이 코드 (주석 상세히)
```

### 2️⃣ 프로젝트 적용 시리즈

#### Redis 캐싱 적용하기
```
@workspace study/spring/09_캐시/ 폴더를 참고해서 S-MAS 프로젝트의 ParkingController에 Redis 캐싱을 적용해줘:
- 주차장 목록 조회 API에 캐시 적용
- TTL 5분 설정
- Cache-Aside 패턴 사용
- 주석으로 각 부분 설명
```

#### JWT 인증 구현하기
```
@workspace study/spring/12_Security/jwt-implement.html 파일을 보고 S-MAS에 JWT 인증을 구현해줘:
- JwtTokenProvider 클래스
- SecurityConfig 설정
- JwtAuthenticationFilter
- 리프레시 토큰 처리 로직 포함
```

#### YOLO 객체 인식 통합
```
@workspace study/ai-tech/01_object-detection/yolo-intro.html과 study/ai/02_컴퓨터비전/yolo-object-detection.html을 참고해서:
S-MAS의 번호판 인식 기능에 YOLOv8을 적용하는 전체 코드를 작성해줘
- 모델 로딩
- 실시간 추론
- Spring Boot API 연동
```

### 3️⃣ 코드 리뷰 & 최적화

#### JPA 성능 최적화
```
@workspace study/spring/07_JPA실전/ 폴더의 내용을 참고해서 내 ParkingRepository 코드를 리뷰하고 최적화해줘:

[여기에 내 코드 붙여넣기]

체크 포인트:
1. N+1 문제 여부
2. 불필요한 쿼리
3. 인덱스 활용
4. fetch 전략
```

#### 트랜잭션 설계 검토
```
@workspace study/spring/08_트랜잭션/ 폴더를 참고해서 내 PaymentService의 트랜잭션 처리가 올바른지 검토해줘:

[여기에 내 코드]

확인 사항:
- 격리 수준 적절성
- 전파 속성 설정
- 롤백 조건
- 성능 개선 포인트
```

### 4️⃣ 면접 준비 시리즈

#### Java 면접 대비
```
@workspace study/java/12_면접/ 폴더의 모든 interview-*.html 파일을 분석해서:
1. 가장 자주 나오는 질문 Top 10
2. 각 질문에 대한 모범 답안
3. 꼬리 질문과 대응 방법
4. 실제 코드로 증명하는 방법
```

#### Spring 면접 시뮬레이션
```
@workspace study/spring/18_면접/ 폴더를 참고해서 Spring 면접 시뮬레이션을 진행해줘:
- 10개 질문을 순서대로 내줘
- 내가 답변하면 피드백
- 부족한 부분은 관련 HTML 파일 링크 제공
- 최종 점수와 개선 포인트
```

### 5️⃣ 학습 로드맵

#### 초보자용 3개월 플랜
```
@workspace 전체 study 폴더를 분석해서 3개월 동안 Spring Boot 백엔드 개발자가 되기 위한 학습 로드맵을 만들어줘:
- 주차별 학습 목표
- 필수로 봐야 할 HTML 파일들
- 주차별 미니 프로젝트
- 최종 목표: S-MAS 같은 프로젝트 혼자 만들기
```

#### AI 엔지니어 전향 로드맵
```
@workspace study/ai/, study/ai-tech/, study/python/ 폴더를 참고해서:
백엔드 개발자가 AI 엔지니어로 전향하기 위한 6개월 로드맵
- 선수 지식 체크리스트
- 단계별 학습 파일
- 실습 프로젝트 (YOLO, LangChain 등)
- 포트폴리오 프로젝트 아이디어
```

### 6️⃣ 실전 문제 해결

#### 쿼리 성능 개선
```
@workspace study/db/07_최적화/ 폴더를 참고해서 이 느린 쿼리를 개선해줘:

[느린 쿼리 SQL]

분석 내용:
1. EXPLAIN 결과 해석
2. 인덱스 추가 제안
3. 쿼리 재작성
4. Before/After 성능 비교 예상
```

#### 동시성 문제 해결
```
@workspace study/java/06_멀티스레딩/ 폴더를 참고해서:
S-MAS의 주차장 예약 시스템에서 발생할 수 있는 동시성 문제를 분석하고 해결책을 제시해줘
- Race Condition 발생 시나리오
- DB 락 vs Java synchronized
- 낙관적 락 vs 비관적 락
- 실제 코드 구현
```

### 7️⃣ 비교 분석

#### 자료구조 비교
```
@workspace study/algorithm/04_스택큐/, study/algorithm/05_해시/ 폴더를 참고해서:
Stack, Queue, HashMap의 시간복잡도를 표로 비교하고, 각각 어떤 상황에 적합한지 실제 코딩테스트 문제 예시와 함께 설명해줘
```

#### 프레임워크 비교
```
@workspace study/python/08_웹/ 폴더의 fastapi-intro.html, django-intro.html, flask-intro.html을 비교해서:
FastAPI, Django, Flask의 장단점을 표로 정리하고, AI 백엔드 서버를 만들 때 어느 것이 적합한지 추천해줘
```

### 8️⃣ 프로젝트별 맞춤 학습

#### S-MAS 프로젝트 고도화
```
@workspace 전체 study 폴더를 분석해서 S-MAS 프로젝트를 다음 레벨로 올리기 위해 적용할 수 있는 기술들을 추천해줘:
- 현재: Spring Boot + JPA + React + YOLO
- 목표: 대규모 트래픽 처리 + 실시간 분석
- 예산: 개인 프로젝트 수준
- 우선순위별로 제시
```

#### 새 프로젝트 기획
```
@workspace study/spring/, study/react/, study/db/ 폴더를 참고해서:
"실시간 헬스케어 모니터링 시스템" 프로젝트를 기획해줘
- 기술 스택 선정 근거
- ERD 설계
- API 명세
- 주차별 개발 계획
- 포트폴리오 작성 팁
```

### 9️⃣ 코드 변환

#### Java → Python
```
@workspace study/java/04_컬렉션/arraylist-vs-linkedlist.html과 study/python/ 폴더를 참고해서:
이 Java 코드를 Python의 Pythonic한 방식으로 변환해줘

[Java 코드]

변환 시 설명:
- Java의 ArrayList → Python의 list
- 제네릭 처리
- 스트림 → 리스트 컴프리헨션
```

#### 명령형 → 함수형
```
@workspace study/java/05_함수형/ 폴더를 참고해서 이 명령형 코드를 함수형으로 리팩토링해줘:

[명령형 코드]

리팩토링 포인트:
- for문 → Stream API
- if문 → filter/map
- 가독성 개선
```

### 🔟 테스트 코드 작성

#### JUnit5 테스트 작성
```
@workspace study/spring/14_테스트/ 폴더를 참고해서 이 Service 클래스의 테스트 코드를 작성해줘:

[Service 클래스 코드]

테스트 시나리오:
- 정상 케이스
- 예외 케이스
- 경계값 테스트
- Mockito를 사용한 단위 테스트
```

## 💡 효율적인 사용 팁

### 🎯 질문 공식
```
@workspace [파일/폴더 경로] + [구체적 요청] + [프로젝트 적용 방법]
```

### 🔄 반복 학습 패턴
```
1단계: @workspace /explain [개념]
2단계: @workspace /quiz [개념]  
3단계: @workspace /implement [개념]
4단계: @workspace /review [내 코드]
```

### 📊 학습 효과 측정
```
매주 금요일: @workspace study/[분야]/면접/ 폴더로 자가 테스트
→ 부족한 부분 파악
→ 다음 주 학습 계획 수립
```

## 🚀 고급 활용법

### 멀티 파일 참조
```
@workspace study/spring/05_JPA기초/jpa-intro.html, study/spring/07_JPA실전/n-plus-one.html, study/db/04_인덱스/index-design.html 이 세 파일을 종합해서:
JPA + Database 최적화의 Best Practice를 정리해줘
```

### 프로젝트 전체 분석
```
@workspace study/ 폴더 전체를 스캔해서:
내가 아직 학습하지 않은 중요한 주제들을 찾아서 우선순위와 함께 추천해줘
- 현재 레벨: Spring Boot 중급
- 목표: 시니어 개발자
- 관심사: 백엔드 + AI
```

---

## 📚 이 예제들을 사용하는 방법

1. **복사**: 원하는 명령어 전체를 복사
2. **수정**: [대괄호] 부분을 내 상황에 맞게 수정
3. **실행**: VS Code Copilot Chat에 붙여넣기
4. **반복**: 답변을 보고 추가 질문

## 🎓 학습 목표별 추천 명령어

### 코딩테스트 준비 → 1️⃣, 6️⃣, 7️⃣, 🔟 섹션
### 프로젝트 개발 → 2️⃣, 3️⃣, 8️⃣ 섹션  
### 면접 준비 → 4️⃣, 5️⃣ 섹션
### 코드 품질 개선 → 3️⃣, 9️⃣, 🔟 섹션

---

**💡 Tip**: 이 파일을 북마크해두고 필요할 때마다 복붙하세요!
