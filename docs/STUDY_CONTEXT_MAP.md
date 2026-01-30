# 📚 Study Context Map - AI가 이해하는 학습 구조

## 🗺️ 폴더 구조 → 학습 주제 매핑

이 파일은 AI가 당신의 질문을 적절한 파일로 자동 연결하도록 도와줍니다.

## Java 학습 경로

### 기초 단계 (study/java/01_기본)
```
질문 예시: "Java 배열 사용법", "반복문 종류"
관련 파일: 
- java-array.html
- java-loop.html
- java-condition.html
```

### 객체지향 (study/java/02_객체지향프로그래밍)
```
질문 예시: "상속 vs 인터페이스", "다형성 예제"
관련 파일:
- inheritance.html
- interface.html
- polymorphism.html
- java-oop-essence.html
```

### 컬렉션 (study/java/04_컬렉션)
```
질문 예시: "ArrayList vs LinkedList", "HashMap 내부 구조"
관련 파일:
- arraylist-vs-linkedlist.html
- hashmap-internal.html
- collection-compare.html
```

### JVM & 성능 (study/java/07_JVM)
```
질문 예시: "가비지 컬렉션 동작 원리", "JVM 메모리 구조"
관련 파일:
- gc-concept.html
- jvm-memory.html
- jvm-architecture.html
```

## Spring 학습 경로

### Spring 기초 (study/spring/01_기본)
```
질문 예시: "Spring Boot 프로젝트 구조", "application.yml 설정"
관련 파일:
- springboot-start.html
- application-yml.html
- project-structure.html
```

### DI/IoC (study/spring/02_핵심개념)
```
질문 예시: "의존성 주입이란?", "빈 생명주기"
관련 파일:
- di-concept.html
- bean-lifecycle.html
- configuration.html
```

### JPA 기초 (study/spring/05_JPA기초)
```
질문 예시: "엔티티 매핑", "영속성 컨텍스트"
관련 파일:
- jpa-intro.html
- entity-basic.html
- persistence-context.html
```

### JPA 실전 (study/spring/07_JPA실전)
```
질문 예시: "N+1 문제 해결", "fetch join", "QueryDSL"
관련 파일:
- n-plus-one.html
- fetch-join.html
- querydsl-intro.html
```

## Algorithm 학습 경로

### 자료구조 기초
```
질문 예시: "스택과 큐 차이", "해시맵 사용법"
관련 폴더:
- study/algorithm/04_스택큐/
- study/algorithm/05_해시/
```

### 그래프 탐색
```
질문 예시: "DFS vs BFS", "최단경로 알고리즘"
관련 폴더:
- study/algorithm/09_그래프/
- study/algorithm/10_최단경로/
```

### 동적 계획법
```
질문 예시: "DP 개념", "배낭 문제", "LIS"
관련 파일:
- study/algorithm/11_DP/dp-concept.html
- study/algorithm/11_DP/dp-knapsack.html
```

## AI & Machine Learning 경로

### AI 기초
```
질문 예시: "딥러닝이란?", "활성화 함수 종류"
관련 파일:
- study/ai/01_기초/deep-learning-intro.html
- study/ai/01_기초/activation-function.html
```

### 컴퓨터 비전
```
질문 예시: "YOLO 사용법", "CNN 구조", "이미지 분류"
관련 파일:
- study/ai/02_컴퓨터비전/yolo-object-detection.html
- study/ai/02_컴퓨터비전/cnn-intro.html
```

### Python 데이터 분석
```
질문 예시: "Pandas DataFrame", "Numpy 배열 연산"
관련 파일:
- study/python/11_pandas/pandas-dataframe.html
- study/python/10_numpy/numpy-operation.html
```

## Database 학습 경로

### SQL 기초
```
질문 예시: "JOIN 종류", "GROUP BY 사용법"
관련 폴더:
- study/db/02_SQL/
- study/db/03_JOIN/
```

### 트랜잭션 & 동시성
```
질문 예시: "격리 수준", "락 종류", "MVCC"
관련 파일:
- study/db/05_트랜잭션/isolation-level.html
- study/db/05_트랜잭션/lock.html
```

### 성능 최적화
```
질문 예시: "인덱스 설계", "쿼리 튜닝", "샤딩"
관련 폴더:
- study/db/04_인덱스/
- study/db/07_최적화/
```

## Network 학습 경로

### HTTP & REST
```
질문 예시: "HTTP 메서드", "REST API 설계", "상태 코드"
관련 파일:
- study/network/03_HTTP/http-method.html
- study/network/04_REST/rest-design.html
```

### 인증 & 보안
```
질문 예시: "JWT vs Session", "OAuth2 흐름", "CORS 설정"
관련 파일:
- study/network/05_인증/jwt.html
- study/network/06_CORS/cors-concept.html
```

## 🎯 학습 시나리오별 파일 추천

### 시나리오 1: Spring Boot API 개발
```
1단계: study/spring/01_기본/springboot-start.html
2단계: study/spring/03_웹MVC/rest-controller.html
3단계: study/spring/05_JPA기초/jpa-intro.html
4단계: study/spring/09_검증/validation-basic.html
5단계: study/spring/11_Security/jwt-intro.html
```

### 시나리오 2: 알고리즘 코딩테스트 준비
```
1단계: study/algorithm/01_기초/time-complexity.html
2단계: study/algorithm/02_배열/two-pointer.html
3단계: study/algorithm/09_그래프/dfs.html
4단계: study/algorithm/11_DP/dp-concept.html
5단계: study/algorithm/15_실전/coding-test-tip.html
```

### 시나리오 3: AI 프로젝트 개발
```
1단계: study/ai/01_기초/ai-ml-concept.html
2단계: study/ai/02_컴퓨터비전/yolo-object-detection.html
3단계: study/python/10_numpy/numpy-intro.html
4단계: study/python/11_pandas/pandas-dataframe.html
5단계: study/ai-tech/01_object-detection/yolo-intro.html
```

### 시나리오 4: Full-Stack 웹 개발
```
프론트: study/react/ (전체)
백엔드: study/spring/ (전체)
DB: study/db/02_SQL/, study/db/03_JOIN/
배포: study/devops/01_Docker/, study/devops/03_클라우드서비스/
```

## 🔗 연관 주제 자동 연결

### Java 학습 시 함께 보면 좋은 파일
```
Java 컬렉션 → Algorithm 자료구조
Java 스트림 → 함수형 프로그래밍
Java 멀티스레딩 → OS 프로세스/스레드
```

### Spring 학습 시 함께 보면 좋은 파일
```
Spring MVC → Network HTTP
Spring Security → 보안 인증
Spring JPA → Database 설계
```

### 면접 준비 파일
```
Java: study/java/12_면접/interview-java-*.html
Spring: study/spring/18_면접/interview-spring-*.html
Algorithm: study/algorithm/15_실전/interview-algorithm.html
Database: study/db/10_면접/interview-db.html
Network: study/network/09_면접/interview-network.html
```

## 💡 AI에게 효과적으로 질문하기

### 패턴 1: 개념 이해
```
"@workspace 파일을 참고해서 [개념]을 설명해줘"
→ AI가 해당 HTML 파일의 내용을 분석하여 설명
```

### 패턴 2: 코드 예제
```
"@workspace [파일명]의 개념을 S-MAS 프로젝트에 적용한 코드 예제"
→ 이론을 실전 코드로 변환
```

### 패턴 3: 연관 학습
```
"@workspace [주제A]와 관련된 다른 학습 파일 추천"
→ AI가 연관 파일들을 찾아줌
```

## 🎓 학습 진도 체크리스트

### Phase 1: Java & Algorithm 기초
- [ ] Java 01~03 폴더 완료
- [ ] Algorithm 01~05 폴더 완료
- [ ] 프로젝트: 간단한 CLI 프로그램

### Phase 2: Spring & Database
- [ ] Spring 01~05 폴더 완료
- [ ] Database 01~03 폴더 완료
- [ ] 프로젝트: REST API CRUD

### Phase 3: 고급 & 실전
- [ ] Spring 06~09 폴더 완료
- [ ] Algorithm 09~11 폴더 완료
- [ ] 프로젝트: S-MAS 같은 복합 시스템

### Phase 4: 전문화
- [ ] AI/DevOps/Security 중 선택
- [ ] 면접 준비 폴더 전체
- [ ] 포트폴리오 프로젝트 완성

---

**이 파일을 프로젝트 루트에 저장하면 AI가 자동으로 참고합니다!**
