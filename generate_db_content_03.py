# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open('src/data/contents/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 05_트랜잭션, 06_설계 섹션
db_contents = {
    "05_트랜잭션/transaction-concept": {
        "title": "트랜잭션 개념",
        "description": "트랜잭션의 정의와 필요성을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 트랜잭션이란?",
                "content": """## 🔥 한 줄 요약
> **쪼갤 수 없는 작업 단위** - "다 되거나, 다 안 되거나"

---

## 💡 왜 배워야 하나?

### 실제 사고:
```
🔴 은행 송금 시나리오
1. A 계좌에서 100만원 출금 ✅
2. 서버 다운! 💥
3. B 계좌 입금 안 됨 ❌
→ 100만원 증발!

🟢 트랜잭션 사용
1. 트랜잭션 시작
2. A 계좌 출금
3. B 계좌 입금
4. 둘 다 성공 → COMMIT (확정)
   하나라도 실패 → ROLLBACK (취소)
→ 돈 안전!
```

---

## 🎯 핵심 개념

### 트랜잭션 흐름

```
START TRANSACTION
    ↓
[쿼리 1] INSERT INTO orders ...
    ↓
[쿼리 2] UPDATE inventory SET stock = stock - 1 ...
    ↓
[쿼리 3] INSERT INTO payments ...
    ↓
성공 → COMMIT (DB에 반영)
실패 → ROLLBACK (모두 취소)
```

### 트랜잭션 없으면?

```
❌ 주문 처리 중 에러
1. orders에 주문 생성 ✅
2. inventory 재고 차감 ✅
3. payments 결제 처리 💥 에러!

결과:
- 주문은 있는데 결제 안 됨
- 재고는 줄었는데 돈 안 받음
- 데이터 꼬임 → 수동 복구 필요
```"""
            },
            {
                "type": "code",
                "title": "💻 트랜잭션 사용",
                "content": """### 기본 문법

```sql
-- 트랜잭션 시작
START TRANSACTION;
-- 또는
BEGIN;

-- 쿼리 실행
INSERT INTO orders (user_id, total_price) VALUES (1, 50000);
UPDATE products SET stock = stock - 1 WHERE id = 100;

-- 확정 또는 취소
COMMIT;    -- 성공: DB에 영구 반영
-- ROLLBACK;  -- 실패: 모든 변경 취소
```

### 실전 예제: 주문 처리

```sql
START TRANSACTION;

-- 1. 재고 확인 (FOR UPDATE로 락)
SELECT stock FROM products WHERE id = 100 FOR UPDATE;

-- 2. 재고 부족하면 롤백
-- (애플리케이션에서 체크)

-- 3. 주문 생성
INSERT INTO orders (user_id, total_price, status)
VALUES (1, 50000, 'pending');

SET @order_id = LAST_INSERT_ID();

-- 4. 주문 상세 생성
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (@order_id, 100, 1, 50000);

-- 5. 재고 차감
UPDATE products SET stock = stock - 1 WHERE id = 100;

-- 6. 결제 기록
INSERT INTO payments (order_id, amount, status)
VALUES (@order_id, 50000, 'completed');

-- 모두 성공하면 커밋
COMMIT;
```

### Python에서 트랜잭션

```python
import mysql.connector

conn = mysql.connector.connect(...)
cursor = conn.cursor()

try:
    # 자동 커밋 비활성화
    conn.autocommit = False

    cursor.execute("INSERT INTO orders ...")
    cursor.execute("UPDATE products ...")
    cursor.execute("INSERT INTO payments ...")

    # 모두 성공
    conn.commit()
    print("주문 완료!")

except Exception as e:
    # 에러 발생 시 롤백
    conn.rollback()
    print(f"에러 발생, 롤백: {e}")

finally:
    cursor.close()
    conn.close()
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 트랜잭션 범위

```
❌ 너무 긴 트랜잭션
├── 락 오래 잡고 있음
├── 다른 쿼리 대기
└── 데드락 가능성 증가

✅ 짧게 유지
├── 필요한 쿼리만 포함
├── 외부 API 호출 제외
└── 빠르게 COMMIT
```

### 자동 커밋 주의

```sql
-- MySQL 기본: 자동 커밋 ON
-- 모든 쿼리가 즉시 COMMIT됨

-- 확인
SHOW VARIABLES LIKE 'autocommit';

-- 자동 커밋 끄기 (세션)
SET autocommit = 0;
```"""
            }
        ]
    },

    "05_트랜잭션/acid": {
        "title": "ACID 원칙",
        "description": "트랜잭션의 4가지 특성을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 ACID란?",
                "content": """## 🔥 한 줄 요약
> **트랜잭션이 지켜야 할 4가지 약속** - 데이터 안전의 핵심!

---

## 🎯 ACID 상세

### A - Atomicity (원자성)
```
"다 되거나, 다 안 되거나"

송금: 출금 + 입금
├── 둘 다 성공 → OK
└── 하나만 성공 → 둘 다 취소

= 쪼갤 수 없는 최소 단위
```

### C - Consistency (일관성)
```
"규칙을 항상 만족"

계좌 잔액 >= 0 규칙
├── 출금 전: 잔액 100만원 ✅
├── 출금 후: 잔액 -10만원 ❌
└── 규칙 위반 → 트랜잭션 실패

= 데이터 무결성 유지
```

### I - Isolation (격리성)
```
"다른 트랜잭션과 간섭 없음"

A 트랜잭션: 재고 10 → 9
B 트랜잭션: 재고 10 → 9 (동시에)

격리성 보장:
├── A 먼저 → 재고 9
├── B 나중 → 재고 8
└── 순서대로 처리

= 동시성 제어
```

### D - Durability (지속성)
```
"커밋하면 영구 보존"

COMMIT 후:
├── 서버 다운 → 데이터 유지
├── 정전 → 데이터 유지
└── 재부팅 → 데이터 유지

= 로그 기반 복구
```"""
            },
            {
                "type": "code",
                "title": "💻 ACID 위반 사례",
                "content": """### Atomicity 위반 예시

```sql
-- ❌ 트랜잭션 없이 송금
UPDATE accounts SET balance = balance - 100000 WHERE id = 1;
-- 여기서 에러 발생하면?
UPDATE accounts SET balance = balance + 100000 WHERE id = 2;

-- ✅ 트랜잭션으로 원자성 보장
START TRANSACTION;
UPDATE accounts SET balance = balance - 100000 WHERE id = 1;
UPDATE accounts SET balance = balance + 100000 WHERE id = 2;
COMMIT;
```

### Consistency 위반 예시

```sql
-- 제약조건으로 일관성 보장
ALTER TABLE accounts
ADD CONSTRAINT chk_balance CHECK (balance >= 0);

-- 이제 음수 잔액 불가
UPDATE accounts SET balance = balance - 200000 WHERE id = 1;
-- Error: Check constraint 'chk_balance' is violated
```

### Isolation 문제 예시

```sql
-- 동시에 같은 상품 주문 시
-- Transaction A
SELECT stock FROM products WHERE id = 1;  -- 결과: 1
-- Transaction B
SELECT stock FROM products WHERE id = 1;  -- 결과: 1

-- A: 재고 있네? 주문!
UPDATE products SET stock = 0 WHERE id = 1;
-- B: 나도 재고 있네? 주문!
UPDATE products SET stock = -1 WHERE id = 1;  -- 💀 음수 재고!

-- 해결: FOR UPDATE 락
SELECT stock FROM products WHERE id = 1 FOR UPDATE;
```"""
            },
            {
                "type": "tip",
                "title": "💡 면접 대비",
                "content": """### 자주 묻는 질문

```
Q: ACID 설명해주세요
A:
- Atomicity: 원자성, 전부 성공 or 전부 실패
- Consistency: 일관성, 규칙 항상 만족
- Isolation: 격리성, 트랜잭션 간 간섭 없음
- Durability: 지속성, 커밋 후 영구 보존

Q: ACID 중 가장 중요한 건?
A: 상황에 따라 다름
- 금융: Consistency, Durability
- SNS: Availability (ACID 일부 완화)

Q: NoSQL은 ACID 안 지키나요?
A: BASE 모델 사용 (Eventually Consistent)
   최근엔 MongoDB도 트랜잭션 지원
```"""
            }
        ]
    },

    "05_트랜잭션/isolation-level": {
        "title": "격리 수준",
        "description": "트랜잭션 격리 수준의 종류와 특징을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 격리 수준이란?",
                "content": """## 🔥 한 줄 요약
> **동시 트랜잭션 간 간섭 수준 설정** - 높을수록 안전, 낮을수록 빠름

---

## 🎯 격리 수준 4단계

### 1. READ UNCOMMITTED (가장 낮음)
```
커밋 안 된 데이터도 읽음
→ Dirty Read 발생
→ 거의 안 씀
```

### 2. READ COMMITTED (PostgreSQL 기본)
```
커밋된 데이터만 읽음
→ Dirty Read 해결
→ Non-Repeatable Read 발생
```

### 3. REPEATABLE READ (MySQL 기본)
```
트랜잭션 시작 시점 데이터 읽음
→ Non-Repeatable Read 해결
→ Phantom Read 발생 가능
```

### 4. SERIALIZABLE (가장 높음)
```
완전 순차 실행처럼 동작
→ 모든 문제 해결
→ 성능 최악
```

---

## 🎯 발생 가능한 문제

| 격리 수준 | Dirty Read | Non-Repeatable | Phantom |
|----------|------------|----------------|---------|
| READ UNCOMMITTED | O | O | O |
| READ COMMITTED | X | O | O |
| REPEATABLE READ | X | X | △ |
| SERIALIZABLE | X | X | X |"""
            },
            {
                "type": "code",
                "title": "💻 격리 수준 예제",
                "content": """### Dirty Read (READ UNCOMMITTED)

```sql
-- 트랜잭션 A
START TRANSACTION;
UPDATE accounts SET balance = 0 WHERE id = 1;
-- 아직 COMMIT 안 함

-- 트랜잭션 B (READ UNCOMMITTED)
SELECT balance FROM accounts WHERE id = 1;
-- 결과: 0 (커밋 안 된 데이터!)

-- 트랜잭션 A
ROLLBACK;  -- 취소!
-- B가 읽은 0은 잘못된 데이터였음 (Dirty Read)
```

### Non-Repeatable Read (READ COMMITTED)

```sql
-- 트랜잭션 A
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;
-- 결과: 100만원

-- 트랜잭션 B
UPDATE accounts SET balance = 50 WHERE id = 1;
COMMIT;

-- 트랜잭션 A (같은 트랜잭션)
SELECT balance FROM accounts WHERE id = 1;
-- 결과: 50만원 (값이 바뀜!)
```

### 격리 수준 설정

```sql
-- 현재 격리 수준 확인
SELECT @@transaction_isolation;
-- MySQL 8.0 이전: @@tx_isolation

-- 세션 격리 수준 변경
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 글로벌 격리 수준 변경
SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

### 실전: 재고 관리

```sql
-- REPEATABLE READ에서도 안전한 패턴
START TRANSACTION;

-- FOR UPDATE로 락 획득
SELECT stock FROM products WHERE id = 1 FOR UPDATE;

-- 재고 확인 후 차감
UPDATE products SET stock = stock - 1 WHERE id = 1 AND stock > 0;

-- 영향받은 행이 0이면 재고 부족
-- affected_rows == 0 → 롤백

COMMIT;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 가이드",
                "content": """### 격리 수준 선택

```
READ COMMITTED:
├── PostgreSQL 기본
├── 대부분의 웹 애플리케이션
└── 성능과 안정성 균형

REPEATABLE READ:
├── MySQL 기본
├── 금융, 재고 관리
└── 더 강한 일관성

SERIALIZABLE:
├── 매우 중요한 데이터
├── 성능 희생 감수
└── 거의 안 씀
```

### 실무 팁

```
1. DB 기본 격리 수준 사용 (보통 충분)
2. 중요한 부분은 FOR UPDATE 락
3. 데드락 대비 코드 작성
4. 트랜잭션 짧게 유지
```"""
            }
        ]
    },

    "05_트랜잭션/lock": {
        "title": "DB Lock",
        "description": "데이터베이스 락의 종류와 동작을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 Lock이란?",
                "content": """## 🔥 한 줄 요약
> **동시 접근 충돌 방지 장치** - 화장실 문 잠금과 같음!

---

## 💡 왜 필요한가?

### 실제 사고:
```
🔴 코인 거래소 해킹 (2023)
├── 동시에 같은 코인 출금 요청
├── 잔액 체크 → 둘 다 통과
├── 출금 실행 → 둘 다 성공
├── 잔액 100만원인데 200만원 출금
└── 하루에 100억 손실!

🟢 Lock 사용
├── 첫 번째 요청이 Lock 획득
├── 두 번째 요청 대기
├── 첫 번째 완료 후 두 번째 처리
└── 안전!
```

---

## 🎯 Lock 종류

### Shared Lock (S Lock, 공유 락)
```
읽기용 락
├── 여러 트랜잭션이 동시에 획득 가능
├── 다른 S Lock과 호환
└── X Lock과 충돌

SELECT ... LOCK IN SHARE MODE
```

### Exclusive Lock (X Lock, 배타 락)
```
쓰기용 락
├── 한 트랜잭션만 획득 가능
├── 모든 락과 충돌
└── 데이터 수정 시 자동 획득

SELECT ... FOR UPDATE
```

### 락 호환성
```
        | S Lock | X Lock |
--------|--------|--------|
S Lock  |   O    |   X    |
X Lock  |   X    |   X    |
```"""
            },
            {
                "type": "code",
                "title": "💻 Lock 실전",
                "content": """### SELECT FOR UPDATE

```sql
-- 트랜잭션 A
START TRANSACTION;
SELECT * FROM products WHERE id = 1 FOR UPDATE;
-- id=1 행에 X Lock 획득

-- 트랜잭션 B
SELECT * FROM products WHERE id = 1 FOR UPDATE;
-- 대기... (A가 Lock 해제할 때까지)

-- 트랜잭션 A
UPDATE products SET stock = stock - 1 WHERE id = 1;
COMMIT;  -- Lock 해제

-- 트랜잭션 B
-- 이제 진행 가능
```

### 재고 차감 안전 패턴

```sql
START TRANSACTION;

-- 1. 재고 조회 + Lock
SELECT stock FROM products WHERE id = 100 FOR UPDATE;

-- 2. 재고 확인 (애플리케이션)
-- stock >= 주문수량 확인

-- 3. 재고 차감
UPDATE products SET stock = stock - 1 WHERE id = 100;

-- 4. 주문 생성
INSERT INTO orders (product_id, quantity) VALUES (100, 1);

COMMIT;
```

### 데드락 예방

```sql
-- ❌ 데드락 발생 가능
-- 트랜잭션 A: products → users 순서
-- 트랜잭션 B: users → products 순서

-- ✅ 항상 같은 순서로 Lock
-- 모든 트랜잭션: products → users 순서
START TRANSACTION;
SELECT * FROM products WHERE id = 1 FOR UPDATE;
SELECT * FROM users WHERE id = 1 FOR UPDATE;
-- ...
COMMIT;
```

### 락 대기 타임아웃

```sql
-- 락 대기 시간 설정 (초)
SET innodb_lock_wait_timeout = 5;

-- 타임아웃 시 에러 발생
-- Error: Lock wait timeout exceeded
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 데드락 대처

```python
# Python 예제
import mysql.connector
from mysql.connector import errors

MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):
    try:
        # 트랜잭션 실행
        conn.start_transaction()
        # ...
        conn.commit()
        break
    except errors.DatabaseError as e:
        if e.errno == 1213:  # Deadlock
            conn.rollback()
            time.sleep(0.1 * attempt)  # 점진적 대기
            continue
        raise
```

### Lock 모니터링

```sql
-- 현재 락 상태 (MySQL)
SHOW ENGINE INNODB STATUS;

-- 락 대기 쿼리
SELECT * FROM information_schema.INNODB_LOCKS;
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
```"""
            }
        ]
    },

    "05_트랜잭션/mvcc": {
        "title": "MVCC",
        "description": "Multi-Version Concurrency Control을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 MVCC란?",
                "content": """## 🔥 한 줄 요약
> **여러 버전의 데이터를 유지** - 읽기와 쓰기가 서로 안 막힘!

---

## 💡 왜 필요한가?

### Lock 방식의 문제
```
❌ Lock만 사용하면
├── 쓰기 중 → 읽기 대기
├── 읽기 중 → 쓰기 대기
└── 동시성 떨어짐

✅ MVCC 사용하면
├── 쓰기 중 → 읽기는 이전 버전 읽음
├── 읽기 중 → 쓰기 가능
└── 동시성 향상!
```

---

## 🎯 MVCC 동작 원리

```
1. 데이터 수정 시 새 버전 생성
2. 이전 버전도 유지 (Undo Log)
3. 각 트랜잭션은 시작 시점의 스냅샷 읽음
4. 커밋되면 새 버전이 최신이 됨

시간 →
[V1] ────┬────────────────────────
         │ UPDATE
[V2]     └─────┬──────────────────
               │ 트랜잭션 A 시작
               │ (V2 읽음)
[V3]           └────┬─────────────
                    │ 트랜잭션 B 시작
                    │ (V3 읽음)

A는 V2, B는 V3 읽음 → 서로 안 막힘!
```"""
            },
            {
                "type": "code",
                "title": "💻 MVCC 동작",
                "content": """### MVCC 예제

```sql
-- 초기 데이터
-- products: id=1, name='iPhone', price=1000000

-- 트랜잭션 A 시작
START TRANSACTION;
SELECT * FROM products WHERE id = 1;
-- 결과: price = 1000000

-- 트랜잭션 B (다른 세션)
START TRANSACTION;
UPDATE products SET price = 1100000 WHERE id = 1;
COMMIT;

-- 트랜잭션 A (REPEATABLE READ)
SELECT * FROM products WHERE id = 1;
-- 결과: price = 1000000 (여전히!)
-- MVCC 덕분에 시작 시점 스냅샷 읽음

COMMIT;
-- A 종료 후 새로 조회하면 1100000
```

### 버전 확인 (PostgreSQL)

```sql
-- PostgreSQL에서 버전 정보 확인
SELECT xmin, xmax, * FROM products WHERE id = 1;
-- xmin: 생성 트랜잭션 ID
-- xmax: 삭제 트랜잭션 ID (0이면 유효)
```

### Undo Log (MySQL)

```
UPDATE 실행 시:
1. 현재 데이터를 Undo Log에 복사
2. 테이블에 새 데이터 기록
3. 트랜잭션 정보 기록

롤백 시:
1. Undo Log에서 이전 데이터 복원

읽기 시 (REPEATABLE READ):
1. 현재 데이터 확인
2. 내 트랜잭션 시작 이후 수정이면
3. Undo Log에서 이전 버전 읽음
```"""
            },
            {
                "type": "tip",
                "title": "💡 MVCC 주의사항",
                "content": """### MVCC 오버헤드

```
장점:
├── 읽기/쓰기 동시 처리
├── 높은 동시성
└── 데드락 감소

단점:
├── 저장 공간 증가 (여러 버전)
├── Vacuum 필요 (PostgreSQL)
├── Undo Log 관리 (MySQL)
└── 긴 트랜잭션 주의
```

### 긴 트랜잭션 문제

```sql
-- ❌ 긴 트랜잭션
START TRANSACTION;
SELECT * FROM table1;
-- ... 5분간 다른 작업 ...
SELECT * FROM table1;  -- 여전히 5분 전 스냅샷
COMMIT;

문제:
├── Undo Log 계속 쌓임
├── 저장 공간 증가
└── 성능 저하
```"""
            }
        ]
    },

    # 06_설계 섹션
    "06_설계/pk-fk": {
        "title": "PK와 FK",
        "description": "Primary Key와 Foreign Key의 개념과 사용법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 PK와 FK",
                "content": """## 🔥 한 줄 요약
> **PK = 신분증, FK = 연결고리** - 테이블 관계의 핵심!

---

## 🎯 Primary Key (기본키)

```
특징:
├── 유일한 식별자 (중복 불가)
├── NULL 불가
├── 테이블당 1개만
└── 자동으로 인덱스 생성

예시:
├── users.id
├── orders.id
└── products.id
```

### Foreign Key (외래키)

```
특징:
├── 다른 테이블의 PK 참조
├── 관계 형성
├── 참조 무결성 보장
└── NULL 가능 (선택적 관계)

예시:
├── orders.user_id → users.id
├── order_items.product_id → products.id
└── comments.post_id → posts.id
```

---

## 🎯 관계 표현

```
users (1) ──────< orders (N)
  │                  │
  PK: id             FK: user_id
                     PK: id
                        │
                        ∨
order_items (N) ──────< orders
  FK: order_id
  FK: product_id
       │
       ∨
products (1)
  PK: id
```"""
            },
            {
                "type": "code",
                "title": "💻 PK/FK 설정",
                "content": """### 테이블 생성

```sql
-- PK 설정
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL
);

-- FK 설정
CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- FK 제약조건
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### ON DELETE / ON UPDATE 옵션

```sql
-- CASCADE: 부모 삭제 시 자식도 삭제
FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE;

-- SET NULL: 부모 삭제 시 NULL로 설정
FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE SET NULL;

-- RESTRICT: 자식 있으면 부모 삭제 불가 (기본값)
FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT;

-- NO ACTION: RESTRICT와 동일
```

### FK 추가/삭제

```sql
-- FK 추가
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user
FOREIGN KEY (user_id) REFERENCES users(id);

-- FK 삭제
ALTER TABLE orders
DROP FOREIGN KEY fk_orders_user;

-- FK 확인
SELECT * FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'orders' AND REFERENCED_TABLE_NAME IS NOT NULL;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### PK 선택 가이드

```
✅ 좋은 PK
├── AUTO_INCREMENT (MySQL)
├── SERIAL (PostgreSQL)
├── UUID (분산 시스템)

❌ 나쁜 PK
├── 변경 가능한 값 (이메일, 전화번호)
├── 비즈니스 의미 있는 값
├── 복합 PK (가능하면 피함)
```

### FK 사용 여부

```
✅ FK 사용
├── 데이터 무결성 중요
├── 명확한 관계
├── OLTP 시스템

❌ FK 미사용 (대규모 시스템)
├── 성능 이슈 (FK 체크 오버헤드)
├── 마이크로서비스 (DB 분리)
├── 애플리케이션에서 검증
```"""
            }
        ]
    },

    "06_설계/relationship": {
        "title": "테이블 관계",
        "description": "1:1, 1:N, N:M 관계를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 테이블 관계 유형",
                "content": """## 🎯 관계 종류

### 1:1 (일대일)
```
users ──── user_profiles
한 유저 = 하나의 프로필

예시:
├── 유저 - 프로필
├── 직원 - 급여정보
└── 상품 - 상세설명
```

### 1:N (일대다) ⭐ 가장 흔함
```
users ────< orders
한 유저 = 여러 주문

예시:
├── 유저 - 주문들
├── 게시글 - 댓글들
└── 카테고리 - 상품들
```

### N:M (다대다)
```
students >───< courses
여러 학생 = 여러 수업

예시:
├── 학생 - 수업
├── 상품 - 태그
└── 유저 - 역할

→ 중간 테이블 필요!
```"""
            },
            {
                "type": "code",
                "title": "💻 관계 구현",
                "content": """### 1:1 관계

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE user_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,  -- UNIQUE로 1:1 보장
    bio TEXT,
    avatar_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 또는 같은 테이블에 합치는 것도 방법
```

### 1:N 관계

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50)
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,  -- FK (중복 가능)
    total_price DECIMAL(12,2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 조회
SELECT u.name, o.id, o.total_price
FROM users u
JOIN orders o ON u.id = o.user_id;
```

### N:M 관계 (중간 테이블)

```sql
CREATE TABLE students (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50)
);

CREATE TABLE courses (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

-- 중간 테이블 (연결 테이블)
CREATE TABLE enrollments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(2),

    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE (student_id, course_id)  -- 중복 방지
);

-- 조회: 학생별 수강 과목
SELECT s.name, c.name, e.grade
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 설계 팁",
                "content": """### 관계 선택 가이드

```
1:1 → 테이블 분리 필요한가?
├── 분리: 선택적 데이터, 보안, 성능
└── 합침: 항상 함께 조회

1:N → 가장 일반적
├── FK는 N 쪽에
└── 인덱스 필수

N:M → 중간 테이블 필요
├── 추가 속성 있으면 (등록일, 점수)
└── 복합 UNIQUE로 중복 방지
```

### 중간 테이블 네이밍

```
students + courses
→ enrollments (명사형)
→ student_courses (연결형)

users + roles
→ user_roles (일반적)
→ permissions (의미 부여)
```"""
            }
        ]
    },

    "06_설계/normalization": {
        "title": "정규화",
        "description": "데이터베이스 정규화를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 정규화란?",
                "content": """## 🔥 한 줄 요약
> **중복을 제거하고 데이터를 구조화** - "한 곳에서만 관리"

---

## 💡 왜 필요한가?

```
❌ 정규화 안 된 테이블
┌────┬────────┬──────────┬──────────────┐
│ 주문 │ 고객명  │ 고객전화  │ 상품명        │
├────┼────────┼──────────┼──────────────┤
│ 1  │ 김철수  │ 010-1234 │ 아이폰        │
│ 2  │ 김철수  │ 010-1234 │ 맥북         │
│ 3  │ 김철수  │ 010-1234 │ 에어팟        │
└────┴────────┴──────────┴──────────────┘

문제:
├── 김철수 정보가 3번 중복
├── 전화번호 바뀌면 3곳 수정
├── 수정 누락 시 데이터 불일치
└── 저장 공간 낭비
```

---

## 🎯 정규화 단계

### 1NF (제1정규형)
```
원자값만 가져야 함 (다중 값 X)

❌ 전화번호: "010-1234, 010-5678"
✅ 전화번호 테이블 분리
```

### 2NF (제2정규형)
```
부분 함수 종속 제거

❌ (주문ID, 상품ID) → 상품명
   상품명은 상품ID에만 종속
✅ 상품 테이블 분리
```

### 3NF (제3정규형)
```
이행적 함수 종속 제거

❌ 주문 → 고객ID → 고객명
   고객명은 고객ID에 종속
✅ 고객 테이블 분리
```"""
            },
            {
                "type": "code",
                "title": "💻 정규화 예제",
                "content": """### Before: 비정규화

```sql
-- 모든 정보가 하나의 테이블에
CREATE TABLE orders_denormalized (
    order_id INT,
    customer_name VARCHAR(50),
    customer_phone VARCHAR(20),
    customer_email VARCHAR(100),
    product_name VARCHAR(100),
    product_price INT,
    quantity INT
);
```

### After: 3NF 정규화

```sql
-- 고객 테이블
CREATE TABLE customers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 상품 테이블
CREATE TABLE products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL
);

-- 주문 테이블
CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 주문 상세 테이블
CREATE TABLE order_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,  -- 주문 시점 가격
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 정규화 확인

```sql
-- 데이터 조회 (JOIN 필요)
SELECT
    o.id AS order_id,
    c.name AS customer,
    p.name AS product,
    oi.quantity,
    oi.price
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 정규화 가이드",
                "content": """### 어디까지 정규화?

```
보통 3NF까지 (실무 표준)
├── 1NF: 원자값
├── 2NF: 완전 함수 종속
└── 3NF: 이행 종속 제거

BCNF 이상은 특수 상황에서만
```

### 정규화 Trade-off

```
정규화 ↑
├── 중복 ↓
├── 무결성 ↑
├── 저장공간 ↓
└── JOIN 필요 ↑ (성능 ↓)

역정규화 ↑
├── 중복 ↑
├── 조회 성능 ↑
├── 저장공간 ↑
└── JOIN 불필요
```"""
            }
        ]
    },

    "06_설계/denormalization": {
        "title": "역정규화",
        "description": "성능을 위한 역정규화를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 역정규화란?",
                "content": """## 🔥 한 줄 요약
> **성능을 위해 의도적으로 중복 허용** - "정규화의 반대"

---

## 💡 왜 필요한가?

```
❌ 과도한 정규화 문제
├── 조회 시 JOIN 너무 많음
├── 성능 저하
└── 쿼리 복잡

✅ 역정규화로 해결
├── 자주 함께 조회되는 데이터 합침
├── 계산된 값 미리 저장
└── 조회 성능 향상
```

---

## 🎯 역정규화 기법

### 1. 컬럼 추가 (파생 컬럼)
```sql
-- 주문 테이블에 총액 추가
orders.total_price
-- order_items에서 매번 계산 → 미리 저장

-- 유저 테이블에 주문 수 추가
users.order_count
-- orders 집계 → 미리 저장
```

### 2. 테이블 합치기
```sql
-- users + user_profiles 합침
-- 1:1 관계이고 항상 함께 조회
```

### 3. 테이블 복제
```sql
-- 읽기 전용 테이블
-- 원본: OLTP용, 복제: 통계용
```

### 4. 요약 테이블
```sql
-- daily_sales: 일별 매출 요약
-- monthly_stats: 월별 통계 요약
```"""
            },
            {
                "type": "code",
                "title": "💻 역정규화 예제",
                "content": """### 파생 컬럼 추가

```sql
-- 정규화: 매번 계산
SELECT
    u.id,
    u.name,
    COUNT(o.id) AS order_count,
    SUM(o.total_price) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- 역정규화: 미리 저장
ALTER TABLE users ADD COLUMN order_count INT DEFAULT 0;
ALTER TABLE users ADD COLUMN total_spent DECIMAL(12,2) DEFAULT 0;

-- 주문 생성 시 업데이트 (트리거 또는 애플리케이션)
UPDATE users
SET order_count = order_count + 1,
    total_spent = total_spent + 50000
WHERE id = 1;
```

### 요약 테이블

```sql
-- 일별 매출 요약 테이블
CREATE TABLE daily_sales (
    date DATE PRIMARY KEY,
    total_orders INT,
    total_revenue DECIMAL(15,2),
    avg_order_value DECIMAL(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 매일 집계 (배치)
INSERT INTO daily_sales (date, total_orders, total_revenue, avg_order_value)
SELECT
    DATE(created_at),
    COUNT(*),
    SUM(total_price),
    AVG(total_price)
FROM orders
WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY
ON DUPLICATE KEY UPDATE
    total_orders = VALUES(total_orders),
    total_revenue = VALUES(total_revenue),
    avg_order_value = VALUES(avg_order_value);
```

### 트리거로 동기화

```sql
-- 주문 생성 시 유저 통계 업데이트
DELIMITER //
CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE users
    SET order_count = order_count + 1,
        total_spent = total_spent + NEW.total_price
    WHERE id = NEW.user_id;
END //
DELIMITER ;
```"""
            },
            {
                "type": "tip",
                "title": "💡 역정규화 가이드",
                "content": """### 언제 역정규화?

```
✅ 역정규화 고려
├── 읽기 >> 쓰기 (조회 많음)
├── JOIN이 너무 많음
├── 응답 시간 중요
├── 집계 쿼리 빈번

❌ 역정규화 주의
├── 쓰기 많으면 동기화 부담
├── 데이터 불일치 위험
├── 저장 공간 증가
```

### 동기화 방법

```
1. 트리거: 자동, 실시간, DB 부하
2. 애플리케이션: 명시적, 누락 위험
3. 배치: 주기적, 지연 있음
4. CDC: 변경 감지, 복잡

상황에 맞게 선택!
```"""
            }
        ]
    },

    "06_설계/erd-concept": {
        "title": "ERD 설계",
        "description": "Entity-Relationship Diagram을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 ERD란?",
                "content": """## 🔥 한 줄 요약
> **테이블 관계를 시각화한 다이어그램** - DB 설계의 청사진!

---

## 🎯 ERD 구성요소

### Entity (엔티티)
```
= 테이블
┌───────────────┐
│    users      │
├───────────────┤
│ id (PK)       │
│ name          │
│ email         │
└───────────────┘
```

### Attribute (속성)
```
= 컬럼
├── id: Primary Key
├── name: 필수
├── email: Unique
└── phone: 선택
```

### Relationship (관계)
```
1:1  ──────  (일대일)
1:N  ──────< (일대다)
N:M  >────< (다대다)
```

---

## 🎯 표기법 종류

### IE 표기법 (Crow's Foot)
```
users ──────<──── orders
      1          N (까마귀 발)

| = 1개
○ = 0 또는 1개
< = 다수 (까마귀 발)
```

### Chen 표기법
```
[users]──<주문>──[orders]
  1                N
```"""
            },
            {
                "type": "code",
                "title": "💻 ERD 예제",
                "content": """### 쇼핑몰 ERD (텍스트)

```
┌─────────────┐       ┌─────────────┐
│   users     │       │  products   │
├─────────────┤       ├─────────────┤
│ *id         │       │ *id         │
│ email       │       │ name        │
│ name        │       │ price       │
│ phone       │       │ stock       │
└──────┬──────┘       └──────┬──────┘
       │ 1                   │ 1
       │                     │
       │ N                   │ N
┌──────┴──────┐       ┌──────┴──────┐
│   orders    │       │ order_items │
├─────────────┤       ├─────────────┤
│ *id         │───────│ *id         │
│ user_id(FK) │  1  N │ order_id(FK)│
│ total_price │       │ product_id  │
│ status      │       │ quantity    │
│ created_at  │       │ price       │
└─────────────┘       └─────────────┘
```

### ERD 도구 사용

```sql
-- MySQL Workbench ERD → SQL 생성
-- dbdiagram.io, ERDCloud 등

-- 예: dbdiagram.io 문법
Table users {
  id bigint [pk, increment]
  email varchar(100) [not null, unique]
  name varchar(50) [not null]
}

Table orders {
  id bigint [pk, increment]
  user_id bigint [not null, ref: > users.id]
  total_price decimal(12,2)
  status enum('pending','paid','shipped')
}
```

### ERD에서 SQL 생성

```sql
-- ERD 관계를 SQL로 변환
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    total_price DECIMAL(12,2),
    status ENUM('pending','paid','shipped'),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```"""
            },
            {
                "type": "tip",
                "title": "💡 ERD 설계 팁",
                "content": """### ERD 도구 추천

```
무료:
├── dbdiagram.io (웹, 추천)
├── ERDCloud (한국어)
├── draw.io
└── MySQL Workbench

유료:
├── DataGrip
├── Navicat
└── ERwin
```

### ERD 설계 순서

```
1. 엔티티 도출 (명사 추출)
2. 속성 정의 (각 엔티티의 컬럼)
3. 관계 파악 (동사로 연결)
4. 정규화 검토
5. PK/FK 설정
6. 인덱스 계획
```"""
            }
        ]
    }
}

# Update data
for key, content in db_contents.items():
    if key in data:
        data[key].update({
            "title": content["title"],
            "description": content["description"],
            "sections": content["sections"],
            "isPlaceholder": False
        })

# Save
with open('src/data/contents/db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 05_트랜잭션, 06_설계 섹션 업데이트 완료: {len(db_contents)}개 토픽")
