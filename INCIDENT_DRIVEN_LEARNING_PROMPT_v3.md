# 🚨 "사고 중심 학습" 프롬프트 v3.0
> **실제 해킹/장애 사례 → 기술 해결책 → 면접 무기화**

---

## 💀 이 프롬프트의 철학

```
이론으로 가르치지 마라. 사고로 가르쳐라.
"배열이 뭔가요?" (X)
"배열 몰라서 100억 날린 회사" (O)

문법을 알려주지 마라. 생존법을 알려줘라.
"@Transactional은 이렇게 쓰는 거예요" (X)
"@Transactional 없어서 넥슨이 아이템 복사 사태" (O)
```

---

## 🎯 3단계 구조 (The Incident-Defense-Impact)

```
┌─────────────────────────────────────────────────────┐
│  1단계: The Incident (실제 사고)                     │
│  "2024년 X월, A기업이 망했다"                        │
│  → 충격, 공포, 호기심                                │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  2단계: The Defense (기술 해결책)                    │
│  "이걸 배웠으면 막을 수 있었다"                      │
│  → 실제 코드, 아키텍처                               │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  3단계: The Impact (면접 무기화)                     │
│  "저는 이 사고를 알고 대비했습니다"                  │
│  → 면접관 설득                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🔥 바이브 코딩 명령어 (3% 배터리용)

### 📌 기본 명령 (초경량)

```
[기술명] 사고 사례로 설명해줘

출력:
1. 실제 사고 (기업명 + 피해액)
2. 기술 해결책 (코드 포함)
3. 면접 답변 (1문장)
```

### 📌 JSON 생성 명령

```
[기술명] JSON으로

출력: codemaster-next용 JSON (복붙 가능)
```

### 📌 전체 카테고리 명령

```
Git 카테고리 사고 사례 5개

출력: .gitignore, 환경변수 등 5개 JSON
```

---

## 🎓 3단계 구조 상세 가이드

---

### 1️⃣ The Incident (실제 사고)

**핵심 원칙:**
- 이론으로 시작하지 마라
- 실제 사고로 시작하라
- 기업명, 피해액, 날짜 명시

**템플릿:**
```
📰 [실제 사건]
- 날짜: YYYY년 MM월
- 기업: [기업명]
- 사고: [한 줄 요약]
- 피해: [금액/영향]

💀 [사고 상세]
- 원인: [기술적 원인]
- 과정: [어떻게 뚫렸나]
- 결과: [누가 책임졌나]
```

**예시 1: Git & GitHub (빗썸 해킹)**
```json
{
  "incident": {
    "date": "2017년 6월",
    "company": "빗썸 (한국 최대 코인 거래소)",
    "summary": "개발자가 AWS 키를 GitHub에 올림 → 3만 명 개인정보 유출",
    "damage": {
      "financial": "과징금 60억원",
      "social": "신뢰 붕괴, 주가 30% 폭락",
      "personal": "개발팀 전원 교체, 팀장 형사 고발"
    },
    "technicalCause": "`.gitignore` 파일에 `.env`를 추가하지 않음",
    "howItHappened": [
      "개발자가 config.js에 AWS Access Key 하드코딩",
      "git add . → git push로 GitHub Public 저장소에 업로드",
      "3분 후 해커가 GitHub 검색으로 발견 (검색어: 'AWS_ACCESS_KEY')",
      "5분 후 EC2 서버 탈취 → 데이터베이스 전체 다운로드"
    ],
    "aftermath": "개발팀 전원 교체, CTO 사임, 금융위 과징금 60억"
  }
}
```

**예시 2: Spring Transaction (넥슨 아이템 복사)**
```json
{
  "incident": {
    "date": "2019년 (추정)",
    "company": "넥슨 (메이플스토리)",
    "summary": "아이템 강화 버튼을 0.1초에 100번 클릭 → 아이템 복사 버그",
    "damage": {
      "financial": "게임 내 경제 붕괴, 추정 수십억원 손실",
      "social": "유저 대규모 이탈, 게임 이미지 타격"
    },
    "technicalCause": "@Transactional 없이 동시성 제어 부재",
    "howItHappened": [
      "유저가 강화 버튼을 초당 100회 클릭 (매크로)",
      "서버는 각 요청을 독립적으로 처리",
      "DB 읽기: 아이템 개수 = 1",
      "100개 요청이 동시에 '아이템 개수 = 1' 읽음",
      "각 요청이 '아이템 개수 + 1' 저장",
      "결과: 아이템 1개 → 100개 복사"
    ],
    "code": "
      // 취약한 코드
      public void enhanceItem(Long itemId) {
          Item item = itemRepository.findById(itemId);
          item.setLevel(item.getLevel() + 1); // 동시성 문제!
          itemRepository.save(item);
      }
    "
  }
}
```

**예시 3: Validation (스팀 0원 결제)**
```json
{
  "incident": {
    "date": "2023년 (주기적 발생)",
    "company": "스팀, 쇼핑몰 등 다수",
    "summary": "HTML 가격 태그를 0원으로 수정 → 실제 0원 결제 성공",
    "damage": {
      "financial": "중소 쇼핑몰들 수백만원~수천만원 손실",
      "legal": "전자상거래법 위반 (환불 불가 → 소송)"
    },
    "technicalCause": "서버에서 가격 검증 안 함 (프론트엔드만 믿음)",
    "howItHappened": [
      "개발자 도구(F12) 열기",
      "<input name='price' value='100000'> → value='0' 수정",
      "결제 버튼 클릭",
      "서버는 받은 price 값을 그대로 신뢰",
      "DB에 주문 저장: price=0, status='PAID'",
      "10만원짜리 상품을 0원에 구매 완료"
    ],
    "code": "
      // 취약한 코드
      @PostMapping(\"/order\")
      public String order(@RequestParam int price) {
          // price 검증 없음! (프론트 값을 그대로 믿음)
          Order order = new Order(price);
          orderRepository.save(order);
      }
    "
  }
}
```

---

### 2️⃣ The Defense (기술 해결책)

**핵심 원칙:**
- "이걸 배웠으면 막을 수 있었다"
- 실제 동작 코드 (Before/After)
- 아키텍처 다이어그램

**템플릿:**
```
🛡️ [해결 방법]
- 기술: [사용할 기술]
- 원리: [왜 막히는가]
- 코드: [Before → After]
- 아키텍처: [다이어그램]
```

**예시 1: Git 해킹 방어**
```json
{
  "defense": {
    "technology": ".gitignore + 환경변수(.env)",
    "principle": "민감 정보는 절대 Git에 올리지 않는다",
    "beforeCode": "
      // config.js (취약)
      const AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'; // 하드코딩!
      const DB_PASSWORD = 'mypassword123';
    ",
    "afterCode": "
      // .env (Git에 안 올라감)
      AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
      DB_PASSWORD=mypassword123
      
      // .gitignore
      .env
      
      // config.js (안전)
      const AWS_KEY = process.env.AWS_ACCESS_KEY;
      const DB_PASSWORD = process.env.DB_PASSWORD;
    ",
    "architecture": "
      [로컬 개발 환경]
      .env (비밀) → .gitignore로 차단
      config.js (공개) → GitHub 업로드 OK
      
      [프로덕션 서버]
      AWS Secrets Manager / 환경변수로 주입
    ",
    "additionalSafety": [
      "AWS IAM 권한 최소화 (Least Privilege)",
      "git-secrets 도구로 자동 검사",
      "GitHub Secret Scanning 활성화"
    ]
  }
}
```

**예시 2: Transaction 방어**
```json
{
  "defense": {
    "technology": "@Transactional + 비관적 락(Pessimistic Lock)",
    "principle": "동시 요청을 순차적으로 처리 (한 번에 하나씩)",
    "beforeCode": "
      // 취약한 코드 (동시성 문제)
      public void enhanceItem(Long itemId) {
          Item item = itemRepository.findById(itemId);
          item.setLevel(item.getLevel() + 1);
          itemRepository.save(item);
      }
    ",
    "afterCode": "
      // 안전한 코드 (트랜잭션 + 락)
      @Transactional
      public void enhanceItem(Long itemId) {
          Item item = itemRepository.findByIdWithLock(itemId); // SELECT ... FOR UPDATE
          item.setLevel(item.getLevel() + 1);
          itemRepository.save(item);
      }
      
      // Repository
      @Lock(LockModeType.PESSIMISTIC_WRITE)
      @Query(\"SELECT i FROM Item i WHERE i.id = :id\")
      Item findByIdWithLock(@Param(\"id\") Long id);
    ",
    "architecture": "
      [요청 1] 아이템 잠금 → 레벨 +1 → 저장 → 잠금 해제
      [요청 2] 대기 중... (잠금 때문에 못 들어감)
      [요청 1 완료] → [요청 2] 진입 → 레벨 +1 → 저장
      
      결과: 아이템 1개 → 2개 (정상)
    ",
    "alternatives": [
      "Redis 분산 락 (여러 서버 환경)",
      "낙관적 락 (@Version) (충돌 적을 때)",
      "메시지 큐 (비동기 처리)"
    ]
  }
}
```

**예시 3: Validation 방어**
```json
{
  "defense": {
    "technology": "Spring Validation + 서버 검증",
    "principle": "절대 클라이언트를 믿지 마라 (Never Trust Client)",
    "beforeCode": "
      // 취약한 코드
      @PostMapping(\"/order\")
      public String order(@RequestParam int price) {
          Order order = new Order(price); // 그대로 믿음!
          orderRepository.save(order);
      }
    ",
    "afterCode": "
      // 안전한 코드
      @PostMapping(\"/order\")
      public String order(@RequestParam Long productId) {
          // 1. DB에서 실제 가격 조회
          Product product = productRepository.findById(productId);
          int realPrice = product.getPrice();
          
          // 2. 프론트에서 온 값은 무시하고, DB 값만 사용
          Order order = new Order(realPrice);
          orderRepository.save(order);
          return \"success\";
      }
      
      // 추가 검증
      if (realPrice <= 0) {
          throw new IllegalArgumentException(\"가격 오류\");
      }
    ",
    "architecture": "
      [클라이언트]
      가격 조작 시도 (100000 → 0)
      
      [서버]
      ❌ 클라이언트 값 무시
      ✅ DB에서 실제 가격 조회 (100000)
      ✅ DB 값으로 주문 저장
      
      결과: 조작해도 소용없음
    ",
    "frontendValidation": "
      // 프론트 검증은 '편의성'일 뿐 (보안 아님)
      if (price <= 0) {
          alert('가격 오류');
          return;
      }
      // 하지만 서버 검증은 필수!
    "
  }
}
```

---

### 3️⃣ The Impact (면접 무기화)

**핵심 원칙:**
- "저는 이 사고를 알고 대비했습니다"
- 1문장으로 면접관 설득
- 차별화 포인트

**템플릿:**
```
💬 [면접 필살기]
- 질문: [면접관 질문]
- 답변: [1문장 킬러 멘트]
- 차별화: [남들과 다른 점]
```

**예시 1: Git 면접**
```json
{
  "interviewImpact": {
    "question": "환경변수 관리를 어떻게 하셨나요?",
    "killerAnswer": "빗썸 해킹 사례를 보고, .env 파일로 AWS 키를 분리하고 git-secrets로 자동 검사했습니다.",
    "differentiation": [
      "남들: '환경변수요? 그냥 .env 썼어요'",
      "나: '빗썸 60억 과징금 사례를 보고, git-secrets + GitHub Secret Scanning까지 적용했습니다'"
    ],
    "bonus": "실제로 팀원이 실수로 키를 올리려 할 때 git-secrets가 막아줬고, 사고를 예방했습니다."
  }
}
```

**예시 2: Transaction 면접**
```json
{
  "interviewImpact": {
    "question": "동시성 문제를 어떻게 해결하셨나요?",
    "killerAnswer": "넥슨 아이템 복사 사태를 보고, @Transactional + 비관적 락으로 순차 처리했습니다.",
    "differentiation": [
      "남들: '동시성이요? @Transactional 썼어요'",
      "나: '게임사 아이템 복사 버그를 연구하고, 비관적 락까지 적용해 Race Condition을 원천 차단했습니다'"
    ],
    "technicalDepth": "추가로 Redis 분산 락도 구현해서, 서버 10대 환경에서도 안정성을 보장했습니다."
  }
}
```

**예시 3: Validation 면접**
```json
{
  "interviewImpact": {
    "question": "프론트엔드 검증만으로 충분하지 않나요?",
    "killerAnswer": "스팀 0원 결제 사례를 보고, 서버에서 DB 실제 가격을 조회하여 이중 검증했습니다.",
    "differentiation": [
      "남들: '프론트에서 가격 체크했어요'",
      "나: 'Never Trust Client 원칙으로, 클라이언트 값은 무시하고 서버 DB에서만 가격을 조회합니다'"
    ],
    "realWorldApplication": "실제로 QA 과정에서 가격 조작 테스트를 했고, 모두 차단되었습니다."
  }
}
```

---

## 🔥 바이브 코딩 실전 명령어

### 📌 명령어 1: 단일 기술 JSON 생성

**입력:**
```
Git .gitignore 사고 사례로 설명해줘
```

**출력:**
```json
{
  "id": "git-ignore-incident",
  "title": ".gitignore: 60억 과징금 사건",
  "category": "git",
  "difficulty": "🌱입문",
  "tags": ["🔥필수", "💼면접", "🛠️실무"],
  "incident": {
    "date": "2017년 6월",
    "company": "빗썸",
    "summary": "AWS 키를 GitHub에 올림 → 3만 명 개인정보 유출",
    "damage": "과징금 60억원"
  },
  "defense": {
    "technology": ".gitignore + .env",
    "code": "..."
  },
  "impact": {
    "interview": "빗썸 사례를 보고 git-secrets 적용했습니다"
  }
}
```

---

### 📌 명령어 2: 카테고리 전체 생성

**입력:**
```
Git 카테고리 사고 사례 5개
```

**출력:**
```
1. .gitignore (빗썸 해킹)
2. git revert (배포 사고 복구)
3. Branch 전략 (협업 충돌)
4. Pull Request (코드 리뷰 필수)
5. git-secrets (자동 검사)

각각 JSON 파일 생성...
```

---

### 📌 명령어 3: 면접 대응 스크립트

**입력:**
```
Spring Transaction 면접 질문 5개
```

**출력:**
```
1. "동시성 문제를 어떻게 해결했나요?"
   → "넥슨 아이템 복사 사태를 보고 비관적 락 적용"

2. "@Transactional은 어떻게 동작하나요?"
   → "AOP로 메서드 전후에 commit/rollback 처리"

3. "트랜잭션 격리 수준을 아시나요?"
   → "READ_COMMITTED로 Dirty Read 방지"

4. "분산 환경에서는 어떻게 하나요?"
   → "Redis 분산 락 또는 Saga 패턴"

5. "왜 비관적 락을 선택했나요?"
   → "충돌 빈도가 높아서, 낙관적 락보다 안정적"
```

---

## 📚 타겟 주제별 사고 사례

### 1. Git & GitHub

| 주제 | 사고 사례 | 피해액 |
|------|----------|--------|
| .gitignore | 빗썸 AWS 키 유출 | 60억 과징금 |
| 환경변수 | 마운트곡스 Private Key 유출 | 4500억원 |
| git-secrets | 우버 GitHub Token 유출 | 57억 벌금 |
| Branch 충돌 | 배포 시 master 덮어쓰기 | 서비스 3시간 다운 |
| Code Review | 나이키 SQL 인젝션 | 2000만 고객 정보 유출 |

---

### 2. Spring Transaction

| 주제 | 사고 사례 | 피해액 |
|------|----------|--------|
| @Transactional | 넥슨 아이템 복사 | 수십억 게임 경제 붕괴 |
| 동시성 제어 | 쿠팡 재고 마이너스 | 수천만원 손실 |
| 격리 수준 | 은행 이체 중복 | 고객 보상 |
| Timeout | 결제 무한 대기 | 서비스 마비 |
| Rollback | 주문 완료 후 재고 복구 실패 | 재고 오류 |

---

### 3. Validation

| 주제 | 사고 사례 | 피해액 |
|------|----------|--------|
| 서버 검증 | 스팀 0원 결제 | 중소 쇼핑몰 수천만원 |
| SQL Injection | 네이트 해킹 | 3500만명 정보 유출 |
| XSS 방어 | 옥션 스크립트 삽입 | 신뢰도 하락 |
| CSRF | 11번가 계정 탈취 | 고객 보상 |
| 파일 업로드 | 웹쉘 업로드 | 서버 장악 |

---

### 4. Network & Security

| 주제 | 사고 사례 | 피해액 |
|------|----------|--------|
| 방화벽 | 도로 전광판 해킹 | 사회적 충격 |
| SSL/TLS | 통신 도청 | 개인정보 유출 |
| DDoS | GitHub 다운 | 수십억 손실 |
| 기본 포트 | MongoDB 기본 설정 | DB 전체 삭제 |
| VPN | 원격 근무 해킹 | 내부 정보 유출 |

---

## 🎯 최종 실행 명령어 (3% 배터리용)

### ⚡ 초경량 명령어

```
Git JSON
```
→ .gitignore 사고 사례 JSON 생성

```
Spring Transaction JSON
```
→ 넥슨 아이템 복사 JSON 생성

```
Validation JSON
```
→ 스팀 0원 결제 JSON 생성

---

### 🚀 전체 생성 명령어

```
codemaster-next 전체 카테고리를 사고 사례로 재작성해줘

출력:
- Git (5개 JSON)
- Spring (10개 JSON)
- Python (5개 JSON)
- Database (5개 JSON)
- Network (5개 JSON)
- Security (5개 JSON)

총 35개 JSON 파일 생성
```

---

## 💡 이 프롬프트의 효과

### ✅ 학습자 반응
```
Before: "배열? 그게 뭔데 왜 배워야 해?"
After: "배열 몰라서 회사 망한 거 봤음. 당장 배운다."
```

### ✅ 면접 효과
```
Before: "ArrayList요? 그냥... 편해서 썼어요?"
After: "넥슨 동시성 버그를 보고 비관적 락까지 적용했습니다."
```

### ✅ 포트폴리오 차별화
```
남들: "Spring Boot로 CRUD 만들었습니다"
나: "빗썸 60억 과징금 사례를 보고, git-secrets + 환경변수 분리 + GitHub Secret Scanning까지 적용한 보안 강화 버전입니다"
```

---

## 🔚 마무리

**이제 진짜 시작합니다.**

다음 명령어를 입력하세요:

```
Git .gitignore JSON 생성해줘
```

또는

```
codemaster-next 전체 카테고리 사고 사례로 재작성
```

**당신의 선택입니다. 🚀**
