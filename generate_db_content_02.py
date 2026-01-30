# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open('src/data/contents/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 03_JOIN 섹션
db_contents = {
    "03_JOIN/join-intro": {
        "title": "JOIN 소개",
        "description": "테이블 조인의 기본 개념을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 JOIN이란?",
                "content": """## 🔥 한 줄 요약
> **여러 테이블을 연결해서 조회** - "회원정보 + 주문정보를 한 번에"

---

## 💡 왜 배워야 하나?

### 실무 현실:
```
🛒 "김철수님의 주문내역 보여줘"
→ users 테이블 (이름)
→ orders 테이블 (주문정보)
→ products 테이블 (상품정보)
→ JOIN 해야 한 화면에 표시!

📊 모든 실무 쿼리의 80%는 JOIN 포함
```

---

## 🎯 핵심 개념

### 왜 테이블을 나눌까?

```
❌ 하나의 거대한 테이블
┌────┬────────┬───────────┬────────┬─────────┬────────┐
│ 주문ID │ 고객명 │ 고객이메일 │ 상품명 │ 상품가격 │ 수량   │
├────┼────────┼───────────┼────────┼─────────┼────────┤
│ 1  │ 김철수 │ kim@test  │ 아이폰  │ 1000000 │ 1     │
│ 2  │ 김철수 │ kim@test  │ 맥북   │ 2000000 │ 1     │
│ 3  │ 김철수 │ kim@test  │ 에어팟  │ 300000  │ 2     │
└────┴────────┴───────────┴────────┴─────────┴────────┘
→ 김철수 정보가 3번 중복! 이메일 바꾸면 3곳 수정!

✅ 정규화된 테이블
users: id, name, email
products: id, name, price
orders: id, user_id, product_id, quantity
→ 중복 없음, 관계로 연결!
```

### JOIN 종류

```
INNER JOIN: 양쪽 모두 있는 것만 (교집합)
LEFT JOIN: 왼쪽 전체 + 오른쪽 매칭
RIGHT JOIN: 오른쪽 전체 + 왼쪽 매칭
FULL OUTER JOIN: 양쪽 전체 (합집합)
CROSS JOIN: 모든 조합 (곱집합)
SELF JOIN: 자기 자신과 조인
```"""
            },
            {
                "type": "code",
                "title": "💻 기본 JOIN",
                "content": """### 샘플 데이터

```sql
-- users 테이블
| id | name   |
|----|--------|
| 1  | 김철수  |
| 2  | 이영희  |
| 3  | 박민수  |

-- orders 테이블
| id | user_id | product   | price   |
|----|---------|-----------|---------|
| 1  | 1       | 아이폰     | 1000000 |
| 2  | 1       | 맥북       | 2000000 |
| 3  | 2       | 갤럭시     | 900000  |
```

### INNER JOIN

```sql
SELECT u.name, o.product, o.price
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 결과: (주문 있는 유저만)
| name   | product | price   |
|--------|---------|---------|
| 김철수  | 아이폰   | 1000000 |
| 김철수  | 맥북     | 2000000 |
| 이영희  | 갤럭시   | 900000  |
-- 박민수는 주문이 없어서 제외됨!
```

### LEFT JOIN

```sql
SELECT u.name, o.product, o.price
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 결과: (모든 유저)
| name   | product | price   |
|--------|---------|---------|
| 김철수  | 아이폰   | 1000000 |
| 김철수  | 맥북     | 2000000 |
| 이영희  | 갤럭시   | 900000  |
| 박민수  | NULL     | NULL    |
-- 박민수도 포함 (주문정보는 NULL)
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### JOIN 선택 가이드

```
INNER JOIN: 양쪽 다 있어야 의미있을 때
  예) 주문한 고객의 주문내역

LEFT JOIN: 왼쪽 기준으로 전체 필요할 때
  예) 모든 고객의 주문내역 (주문 없어도 표시)

RIGHT JOIN: 거의 안 씀 (LEFT로 순서 바꾸면 됨)

CROSS JOIN: 모든 조합 필요할 때
  예) 색상 × 사이즈 조합 생성
```

### 성능 팁

```sql
-- JOIN 컬럼에 인덱스 필수!
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- JOIN 순서도 성능에 영향
-- 작은 테이블을 먼저 (옵티마이저가 자동 최적화)
```"""
            }
        ]
    },

    "03_JOIN/join-concept": {
        "title": "JOIN 개념 완벽 정리",
        "description": "다양한 JOIN의 동작 원리를 시각적으로 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 JOIN 시각화",
                "content": """## 🎯 벤다이어그램으로 이해하기

```
테이블 A          테이블 B
   ┌───┐            ┌───┐
   │   │            │   │
   │ ● │────────────│ ● │
   │   │            │   │
   └───┘            └───┘

INNER JOIN: 교집합 (●●)
LEFT JOIN: A 전체 + 교집합
RIGHT JOIN: B 전체 + 교집합
FULL OUTER JOIN: A ∪ B
```

---

## 🎯 실제 예시로 이해하기

### 샘플 데이터

```
employees (직원)           departments (부서)
+----+--------+-------+    +----+----------+
| id | name   | dept_id|   | id | name     |
+----+--------+-------+    +----+----------+
| 1  | 김철수  | 10    |    | 10 | 개발팀    |
| 2  | 이영희  | 20    |    | 20 | 마케팅팀  |
| 3  | 박민수  | 30    |    | 40 | 인사팀    |
| 4  | 최지원  | NULL  |    +----+----------+
+----+--------+-------+
```

### 각 JOIN 결과

```sql
-- INNER JOIN: 부서 있는 직원만
김철수 - 개발팀
이영희 - 마케팅팀
(박민수: dept_id=30인데 부서테이블에 없음 → 제외)
(최지원: dept_id=NULL → 제외)

-- LEFT JOIN: 모든 직원
김철수 - 개발팀
이영희 - 마케팅팀
박민수 - NULL
최지원 - NULL

-- RIGHT JOIN: 모든 부서
김철수 - 개발팀
이영희 - 마케팅팀
NULL   - 인사팀 (직원 없음)
```"""
            },
            {
                "type": "code",
                "title": "💻 JOIN 비교",
                "content": """### 모든 JOIN 비교

```sql
-- INNER JOIN
SELECT e.name, d.name AS dept
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;
-- 결과: 2행 (김철수-개발팀, 이영희-마케팅팀)

-- LEFT JOIN
SELECT e.name, d.name AS dept
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
-- 결과: 4행 (모든 직원)

-- RIGHT JOIN
SELECT e.name, d.name AS dept
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;
-- 결과: 3행 (모든 부서)

-- FULL OUTER JOIN (MySQL은 지원 안 함)
SELECT e.name, d.name AS dept
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;
-- 결과: 5행 (모든 직원 + 모든 부서)

-- MySQL에서 FULL OUTER JOIN 구현
SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id
UNION
SELECT e.name, d.name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.id;
```

### JOIN 조건 (ON vs WHERE)

```sql
-- ON: JOIN 조건
-- WHERE: 필터링 조건

-- 차이 예시 (LEFT JOIN에서 중요!)
-- ON에 조건
SELECT * FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id AND d.name = '개발팀';
-- 모든 직원 나오고, 개발팀 아니면 부서정보만 NULL

-- WHERE에 조건
SELECT * FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
WHERE d.name = '개발팀';
-- 개발팀 직원만 나옴 (INNER JOIN과 동일한 결과)
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 흔한 실수

```sql
-- ❌ LEFT JOIN 후 WHERE로 NULL 제외
SELECT * FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
-- 주문 없는 유저 제외됨 (INNER JOIN과 동일)

-- ✅ 의도대로 하려면
SELECT * FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'completed';
-- 모든 유저 + completed 주문만 (없으면 NULL)
```

### JOIN 성능 체크리스트

```
□ JOIN 컬럼에 인덱스 있는지
□ 불필요한 JOIN 없는지
□ SELECT *  대신 필요한 컬럼만
□ EXPLAIN으로 실행계획 확인
```"""
            }
        ]
    },

    "03_JOIN/inner-join": {
        "title": "INNER JOIN",
        "description": "가장 기본이 되는 INNER JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 INNER JOIN 완벽 이해",
                "content": """## 🔥 한 줄 요약
> **양쪽 테이블에 모두 있는 것만 조회** - 교집합!

---

## 💡 언제 쓸까?

```
✅ INNER JOIN 사용
├── 주문한 고객의 주문내역 (주문 있어야 의미)
├── 재고 있는 상품 목록 (재고 없으면 불필요)
└── 부서 배정된 직원 목록

❌ LEFT JOIN 사용해야 할 때
├── 모든 고객 + 주문내역 (주문 없어도 표시)
└── 모든 상품 + 재고현황
```

---

## 🎯 문법

```sql
-- 명시적 JOIN (권장)
SELECT columns
FROM table1
INNER JOIN table2 ON table1.col = table2.col;

-- INNER 생략 가능
SELECT columns
FROM table1
JOIN table2 ON table1.col = table2.col;

-- 암시적 JOIN (비권장, 레거시)
SELECT columns
FROM table1, table2
WHERE table1.col = table2.col;
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 INNER JOIN",
                "content": """### 기본 사용

```sql
-- 주문내역 조회 (고객명 포함)
SELECT
    o.id AS order_id,
    u.name AS customer_name,
    o.total_price,
    o.created_at
FROM orders o
INNER JOIN users u ON o.user_id = u.id;
```

### 다중 테이블 JOIN

```sql
-- 주문 상세내역 (고객 + 상품 정보)
SELECT
    o.id AS order_id,
    u.name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed';
```

### 집계와 함께

```sql
-- 고객별 주문 통계
SELECT
    u.name,
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.total_price) AS total_spent,
    MAX(o.created_at) AS last_order
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) >= 3
ORDER BY total_spent DESC;
```

### 같은 테이블 값 비교

```sql
-- USING 문법 (컬럼명 같을 때)
SELECT *
FROM orders o
INNER JOIN users u USING (user_id);  -- ON o.user_id = u.user_id

-- 여러 컬럼으로 JOIN
SELECT *
FROM order_items oi
INNER JOIN inventory inv
    ON oi.product_id = inv.product_id
    AND oi.warehouse_id = inv.warehouse_id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### INNER JOIN vs LEFT JOIN 선택

```sql
-- 질문: "주문 없는 고객도 보여야 하나?"
-- YES → LEFT JOIN
-- NO → INNER JOIN

-- 대부분의 리포트는 INNER JOIN
-- "주문 고객 목록" = INNER JOIN
-- "전체 고객 현황" = LEFT JOIN
```

### 성능 최적화

```sql
-- 1. 인덱스 확인
EXPLAIN SELECT * FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- 2. 필요한 컬럼만
SELECT u.name, o.total_price  -- ✅
-- SELECT *  -- ❌

-- 3. 조건은 JOIN 전에 (서브쿼리)
SELECT u.name, o.total_price
FROM (SELECT * FROM users WHERE status = 'active') u
INNER JOIN orders o ON u.id = o.user_id;
```"""
            }
        ]
    },

    "03_JOIN/left-join": {
        "title": "LEFT JOIN",
        "description": "왼쪽 테이블 기준의 LEFT JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 LEFT JOIN 완벽 이해",
                "content": """## 🔥 한 줄 요약
> **왼쪽 테이블 전체 + 오른쪽 매칭** - 왼쪽은 무조건 다 나옴!

---

## 💡 언제 쓸까?

```
✅ LEFT JOIN 사용
├── "모든 고객" + 주문내역 (주문 없어도 표시)
├── "모든 상품" + 리뷰 (리뷰 없어도 표시)
├── "전체 직원" + 프로젝트 (미배정도 표시)
└── NULL 체크가 필요할 때

❌ INNER JOIN이 나은 경우
├── 매칭된 것만 필요할 때
└── 양쪽 다 있어야 의미있을 때
```

---

## 🎯 시각화

```
users (왼쪽)              orders (오른쪽)
┌────────────┐          ┌────────────┐
│ 김철수 ─────┼──────────┼─→ 주문1    │
│ 이영희 ─────┼──────────┼─→ 주문2    │
│ 박민수     │          │            │
│ 최지원     │          │            │
└────────────┘          └────────────┘
     ↓
LEFT JOIN 결과
┌─────────┬─────────┐
│ 김철수   │ 주문1    │
│ 이영희   │ 주문2    │
│ 박민수   │ NULL    │  ← 매칭 없음
│ 최지원   │ NULL    │  ← 매칭 없음
└─────────┴─────────┘
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 LEFT JOIN",
                "content": """### 기본 사용

```sql
-- 모든 고객 + 주문정보
SELECT
    u.name,
    u.email,
    o.id AS order_id,
    o.total_price
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### NULL 활용 패턴

```sql
-- 주문 없는 고객만 찾기
SELECT u.name, u.email
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- 최근 30일 구매 없는 고객
SELECT u.name, u.email
FROM users u
LEFT JOIN (
    SELECT DISTINCT user_id
    FROM orders
    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
) recent_orders ON u.id = recent_orders.user_id
WHERE recent_orders.user_id IS NULL;
```

### 집계와 함께

```sql
-- 모든 고객별 주문 통계 (0건도 포함)
SELECT
    u.name,
    COUNT(o.id) AS order_count,  -- NULL은 카운트 안 됨
    COALESCE(SUM(o.total_price), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- 결과
-- 김철수 | 5 | 500000
-- 이영희 | 2 | 200000
-- 박민수 | 0 | 0  ← 주문 없음
```

### 다중 LEFT JOIN

```sql
-- 모든 상품 + 리뷰 + 주문수량
SELECT
    p.name AS product_name,
    COUNT(DISTINCT r.id) AS review_count,
    AVG(r.rating) AS avg_rating,
    SUM(oi.quantity) AS total_sold
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name;
```"""
            },
            {
                "type": "common-mistake",
                "title": "⚠️ 흔한 실수",
                "content": """### ON vs WHERE 차이

```sql
-- ❌ LEFT JOIN 의미 없어짐
SELECT * FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
-- → 주문 없는 유저 제외됨 (INNER JOIN과 동일)

-- ✅ 의도대로
SELECT * FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'completed';
-- → 모든 유저 + completed 주문만 (없으면 NULL)
```

### COUNT(*) vs COUNT(column)

```sql
-- ❌ 모든 행 카운트
SELECT u.name, COUNT(*) AS cnt
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.name;
-- 주문 없어도 1로 나옴

-- ✅ 주문 ID 카운트 (NULL 제외)
SELECT u.name, COUNT(o.id) AS cnt
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.name;
-- 주문 없으면 0
```

### NULL 비교

```sql
-- ❌ = NULL은 항상 FALSE
WHERE o.status = NULL

-- ✅ IS NULL 사용
WHERE o.id IS NULL
```"""
            }
        ]
    },

    "03_JOIN/right-join": {
        "title": "RIGHT JOIN",
        "description": "오른쪽 테이블 기준의 RIGHT JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 RIGHT JOIN",
                "content": """## 🔥 한 줄 요약
> **오른쪽 테이블 전체 + 왼쪽 매칭** - LEFT JOIN의 반대!

---

## 💡 현실적인 조언

```
🤔 RIGHT JOIN은 거의 안 씀!

이유:
├── LEFT JOIN으로 테이블 순서만 바꾸면 됨
├── 가독성이 떨어짐
└── 코드 리뷰 시 혼란 유발

결론: LEFT JOIN만 써도 됨!
```

---

## 🎯 LEFT JOIN으로 변환

```sql
-- RIGHT JOIN
SELECT * FROM orders o
RIGHT JOIN users u ON o.user_id = u.id;

-- LEFT JOIN으로 변환 (동일 결과)
SELECT * FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```"""
            },
            {
                "type": "code",
                "title": "💻 RIGHT JOIN 예제",
                "content": """### 기본 사용

```sql
-- 모든 부서 + 직원 (직원 없는 부서도 포함)
SELECT
    d.name AS department,
    e.name AS employee
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN으로 동일하게
SELECT
    d.name AS department,
    e.name AS employee
FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id;
```

### 언제 쓸 수 있나?

```sql
-- 여러 JOIN 중에 RIGHT가 자연스러울 때
SELECT
    o.id,
    oi.product_id,
    p.name
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
RIGHT JOIN products p ON oi.product_id = p.id;
-- 모든 상품 + 주문정보 (주문 없는 상품 포함)

-- 하지만 이것도 LEFT JOIN으로 리팩토링 가능
SELECT
    p.name,
    o.id,
    oi.product_id
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 코딩 컨벤션

```
대부분의 팀:
├── LEFT JOIN만 사용
├── 테이블 순서로 방향 조절
└── 코드 리뷰 시 RIGHT JOIN → LEFT JOIN 변환 요청

예외:
├── 레거시 코드
├── 특수한 상황
└── ORM이 자동 생성한 경우
```

### 면접 TIP

```
Q: LEFT JOIN과 RIGHT JOIN의 차이?
A: 기준 테이블의 위치 차이.
   실무에서는 가독성을 위해 LEFT JOIN만 사용하고,
   테이블 순서를 바꿔서 원하는 결과를 얻습니다.
```"""
            }
        ]
    },

    "03_JOIN/full-outer-join": {
        "title": "FULL OUTER JOIN",
        "description": "양쪽 테이블 전체를 조회하는 FULL OUTER JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 FULL OUTER JOIN",
                "content": """## 🔥 한 줄 요약
> **양쪽 테이블 전체 조회** - 합집합!

---

## 💡 언제 쓸까?

```
✅ FULL OUTER JOIN 사용
├── 데이터 일치성 검사
├── 누락 데이터 찾기
└── 마이그레이션 검증

⚠️ 주의
├── MySQL은 지원 안 함!
├── PostgreSQL, Oracle, SQL Server 지원
└── MySQL은 UNION으로 구현
```

---

## 🎯 시각화

```
users                      orders
┌────────────┐          ┌────────────┐
│ 김철수 ─────┼──────────┼─→ 주문1    │
│ 이영희     │          │ 주문2 ───────┼─ user_id=999 (없는 유저)
│ 박민수     │          │            │
└────────────┘          └────────────┘

FULL OUTER JOIN 결과:
| user_name | order_id |
|-----------|----------|
| 김철수     | 1        |
| 이영희     | NULL     |
| 박민수     | NULL     |
| NULL      | 2        | ← user_id=999
```"""
            },
            {
                "type": "code",
                "title": "💻 FULL OUTER JOIN 구현",
                "content": """### PostgreSQL / Oracle / SQL Server

```sql
-- 직접 지원
SELECT
    u.name AS user_name,
    o.id AS order_id
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;
```

### MySQL 구현 (UNION 사용)

```sql
-- LEFT JOIN + RIGHT JOIN
SELECT u.name, o.id AS order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id

UNION

SELECT u.name, o.id AS order_id
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

### 실전 예제: 데이터 검증

```sql
-- 두 테이블 간 불일치 찾기
SELECT
    old.id AS old_id,
    new.id AS new_id,
    old.email AS old_email,
    new.email AS new_email
FROM old_users old
FULL OUTER JOIN new_users new ON old.id = new.id
WHERE old.id IS NULL OR new.id IS NULL;

-- MySQL 버전
SELECT old.id, new.id, old.email, new.email
FROM old_users old LEFT JOIN new_users new ON old.id = new.id
WHERE new.id IS NULL
UNION
SELECT old.id, new.id, old.email, new.email
FROM old_users old RIGHT JOIN new_users new ON old.id = new.id
WHERE old.id IS NULL;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 사용 빈도

```
INNER JOIN: 70%
LEFT JOIN: 25%
FULL OUTER JOIN: 4%
RIGHT JOIN: 1%

→ FULL OUTER JOIN은 데이터 검증/마이그레이션 시 주로 사용
```

### 성능 주의

```sql
-- FULL OUTER JOIN은 비용이 큼
-- 대용량 테이블에서는 주의

-- 대안: 작은 범위로 제한
SELECT * FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
   OR o.created_at >= '2024-01-01';
```"""
            }
        ]
    },

    "03_JOIN/cross-join": {
        "title": "CROSS JOIN",
        "description": "모든 조합을 생성하는 CROSS JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 CROSS JOIN",
                "content": """## 🔥 한 줄 요약
> **모든 조합 생성** - 곱집합 (Cartesian Product)

---

## 💡 언제 쓸까?

```
✅ CROSS JOIN 사용
├── 색상 × 사이즈 조합 생성
├── 날짜 × 카테고리 조합
├── 테스트 데이터 생성
└── 매트릭스 구조 필요 시

⚠️ 주의
├── 결과 행 수 = A 행수 × B 행수
├── 1000 × 1000 = 100만 행!
└── 메모리 폭발 주의
```

---

## 🎯 시각화

```
colors (3행)        sizes (4행)
┌────────┐         ┌────────┐
│ Red    │         │ S      │
│ Blue   │    ×    │ M      │
│ Green  │         │ L      │
└────────┘         │ XL     │
                   └────────┘
                      ↓
CROSS JOIN = 3 × 4 = 12행
Red-S, Red-M, Red-L, Red-XL
Blue-S, Blue-M, Blue-L, Blue-XL
Green-S, Green-M, Green-L, Green-XL
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 CROSS JOIN",
                "content": """### 기본 사용

```sql
-- 색상 × 사이즈 조합
SELECT
    c.name AS color,
    s.name AS size
FROM colors c
CROSS JOIN sizes s;

-- 암시적 CROSS JOIN (동일)
SELECT c.name, s.name
FROM colors c, sizes s;
```

### 실전 예제: 날짜별 카테고리 매출 (0 포함)

```sql
-- 1. 날짜 테이블 생성
WITH dates AS (
    SELECT DATE_ADD('2024-01-01', INTERVAL n DAY) AS date
    FROM (SELECT 0 n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) numbers
),
categories AS (
    SELECT DISTINCT category FROM products
)

-- 2. CROSS JOIN으로 모든 조합 생성
SELECT
    d.date,
    c.category,
    COALESCE(SUM(o.total_price), 0) AS revenue
FROM dates d
CROSS JOIN categories c
LEFT JOIN orders o ON DATE(o.created_at) = d.date
    AND o.category = c.category
GROUP BY d.date, c.category;

-- 결과: 날짜 × 카테고리 조합 (매출 없으면 0)
```

### 테스트 데이터 생성

```sql
-- 1~100 숫자 생성
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT n FROM numbers;

-- 10명 유저 × 100개 상품 조합 생성
INSERT INTO test_orders (user_id, product_id)
SELECT u.id, p.id
FROM (SELECT id FROM users LIMIT 10) u
CROSS JOIN (SELECT id FROM products LIMIT 100) p;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 실수 방지

```sql
-- ❌ 실수로 CROSS JOIN
SELECT * FROM orders, users;  -- 위험!
-- 100만 주문 × 10만 유저 = 1000억 행

-- ✅ 명시적 JOIN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id;
```

### CROSS JOIN 대안

```sql
-- 적은 조합이면 VALUES 사용
SELECT * FROM (
    VALUES ('S'), ('M'), ('L'), ('XL')
) AS sizes(name);

-- 또는 UNION
SELECT 'S' AS size
UNION SELECT 'M'
UNION SELECT 'L';
```"""
            }
        ]
    },

    "03_JOIN/self-join": {
        "title": "SELF JOIN",
        "description": "같은 테이블을 조인하는 SELF JOIN을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 SELF JOIN",
                "content": """## 🔥 한 줄 요약
> **같은 테이블을 자기 자신과 조인** - 계층 구조, 비교에 사용

---

## 💡 언제 쓸까?

```
✅ SELF JOIN 사용
├── 조직도 (상사-부하 관계)
├── 카테고리 계층 (대분류-중분류)
├── 같은 테이블 내 비교
└── 친구 관계, 팔로우 관계

예시:
├── "김부장의 팀원들은?"
├── "전자기기의 하위 카테고리는?"
└── "나보다 비싼 상품은?"
```

---

## 🎯 시각화

```
employees 테이블
+----+--------+------------+
| id | name   | manager_id |
+----+--------+------------+
| 1  | 김사장  | NULL       |
| 2  | 박부장  | 1          |
| 3  | 이과장  | 2          |
| 4  | 최대리  | 2          |
+----+--------+------------+

SELF JOIN
employees e1 (직원) ─┐
                    ├─→ 결과
employees e2 (상사) ─┘

+--------+--------+
| 직원    | 상사    |
+--------+--------+
| 박부장  | 김사장   |
| 이과장  | 박부장   |
| 최대리  | 박부장   |
+--------+--------+
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 SELF JOIN",
                "content": """### 조직도 조회

```sql
-- 직원과 상사 정보
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- 같은 상사를 둔 동료 찾기
SELECT
    e1.name AS employee1,
    e2.name AS employee2,
    m.name AS same_manager
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.manager_id
    AND e1.id < e2.id  -- 중복 제거
JOIN employees m ON e1.manager_id = m.id;
```

### 계층 구조 (카테고리)

```sql
-- categories: id, name, parent_id
SELECT
    c.name AS category,
    p.name AS parent_category
FROM categories c
LEFT JOIN categories p ON c.parent_id = p.id;

-- 3단계 계층 조회
SELECT
    c1.name AS level1,
    c2.name AS level2,
    c3.name AS level3
FROM categories c1
LEFT JOIN categories c2 ON c2.parent_id = c1.id
LEFT JOIN categories c3 ON c3.parent_id = c2.id
WHERE c1.parent_id IS NULL;
```

### 같은 테이블 내 비교

```sql
-- 자신보다 비싼 상품 찾기
SELECT
    p1.name AS product,
    p1.price,
    p2.name AS more_expensive,
    p2.price
FROM products p1
JOIN products p2 ON p1.category = p2.category
    AND p1.price < p2.price
ORDER BY p1.name, p2.price;

-- 같은 날 가입한 유저
SELECT
    u1.name AS user1,
    u2.name AS user2,
    DATE(u1.created_at) AS join_date
FROM users u1
JOIN users u2 ON DATE(u1.created_at) = DATE(u2.created_at)
    AND u1.id < u2.id;  -- 중복 제거
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 중복 제거 패턴

```sql
-- 조합 중복 제거
-- (A,B)와 (B,A)가 같은 경우

-- ❌ 중복 발생
JOIN ON e1.manager_id = e2.manager_id

-- ✅ id 비교로 중복 제거
JOIN ON e1.manager_id = e2.manager_id AND e1.id < e2.id
```

### Recursive CTE (깊은 계층)

```sql
-- MySQL 8.0+, PostgreSQL
WITH RECURSIVE org_tree AS (
    -- 시작점 (사장)
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 재귀 (부하 직원)
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree ORDER BY level, id;
```"""
            }
        ]
    },

    "03_JOIN/join-compare": {
        "title": "JOIN 비교 총정리",
        "description": "모든 JOIN 유형을 비교하고 선택 기준을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 JOIN 총정리",
                "content": """## 🎯 JOIN 비교표

| JOIN 유형 | 결과 | 사용 빈도 | 용도 |
|----------|------|----------|------|
| INNER | 교집합 | ⭐⭐⭐⭐⭐ | 매칭된 것만 |
| LEFT | 왼쪽 전체 | ⭐⭐⭐⭐ | 왼쪽 기준 전체 |
| RIGHT | 오른쪽 전체 | ⭐ | 거의 안 씀 |
| FULL OUTER | 합집합 | ⭐⭐ | 데이터 검증 |
| CROSS | 곱집합 | ⭐⭐ | 조합 생성 |
| SELF | 자기참조 | ⭐⭐⭐ | 계층/비교 |

---

## 🎯 선택 가이드

```
Q: 매칭 안 되는 행도 필요한가?
├── NO → INNER JOIN
└── YES → LEFT/RIGHT/FULL
    ├── 왼쪽 테이블 기준? → LEFT JOIN
    ├── 오른쪽 테이블 기준? → LEFT JOIN (순서 바꿔서)
    └── 양쪽 다? → FULL OUTER JOIN

Q: 모든 조합이 필요한가?
└── YES → CROSS JOIN

Q: 같은 테이블 내 관계/비교?
└── YES → SELF JOIN
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 비교",
                "content": """### 같은 데이터, 다른 JOIN

```sql
-- 데이터: users 4명, orders 3건 (1명만 주문)

-- INNER JOIN: 주문한 유저만
SELECT u.name, o.id FROM users u
INNER JOIN orders o ON u.id = o.user_id;
-- 결과: 3행 (1명 × 3주문)

-- LEFT JOIN: 모든 유저
SELECT u.name, o.id FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- 결과: 6행 (3주문 + 3명 NULL)

-- RIGHT JOIN: 모든 주문
SELECT u.name, o.id FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
-- 결과: 3행 (모든 주문 + 유저정보)

-- CROSS JOIN: 모든 조합
SELECT u.name, o.id FROM users u
CROSS JOIN orders o;
-- 결과: 12행 (4명 × 3주문)
```

### 성능 비교

```sql
-- INNER JOIN이 가장 빠름 (결과 작음)
-- LEFT JOIN은 왼쪽 테이블 전체 스캔
-- CROSS JOIN은 폭발적 증가 주의

-- EXPLAIN으로 확인
EXPLAIN SELECT * FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 면접 대비",
                "content": """### 자주 묻는 질문

```
Q: INNER JOIN vs LEFT JOIN 차이?
A: INNER는 양쪽 매칭만, LEFT는 왼쪽 전체 포함

Q: LEFT JOIN에서 오른쪽 테이블 값이 NULL인 행만 찾으려면?
A: WHERE right_table.id IS NULL

Q: CROSS JOIN 결과 행 수는?
A: A 테이블 행 수 × B 테이블 행 수

Q: JOIN 성능 최적화는?
A: JOIN 컬럼 인덱스, 필요한 컬럼만 SELECT,
   작은 테이블 먼저, EXPLAIN으로 확인
```"""
            }
        ]
    },

    "03_JOIN/practice-join": {
        "title": "JOIN 실전 연습",
        "description": "다양한 JOIN 시나리오를 실습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 실전 문제",
                "content": """## 📋 시나리오

```
쇼핑몰 DB
- users: 회원 정보
- products: 상품 정보
- orders: 주문 정보
- order_items: 주문 상세
- reviews: 리뷰
```

---

## 🎯 문제 목록

1. **주문한 고객 목록** (INNER JOIN)
2. **주문 없는 고객 찾기** (LEFT JOIN + NULL)
3. **고객별 주문 통계** (LEFT JOIN + 집계)
4. **상품별 리뷰 현황** (LEFT JOIN)
5. **VIP 고객의 최근 구매 상품** (다중 JOIN)"""
            },
            {
                "type": "code",
                "title": "💻 풀이",
                "content": """### 1. 주문한 고객 목록

```sql
SELECT DISTINCT
    u.id,
    u.name,
    u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### 2. 주문 없는 고객 찾기

```sql
SELECT u.id, u.name, u.email
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### 3. 고객별 주문 통계

```sql
SELECT
    u.id,
    u.name,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total_price), 0) AS total_spent,
    MAX(o.created_at) AS last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_spent DESC;
```

### 4. 상품별 리뷰 현황

```sql
SELECT
    p.id,
    p.name AS product_name,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 1) AS avg_rating
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name
ORDER BY review_count DESC;
```

### 5. VIP 고객의 최근 구매 상품

```sql
SELECT
    u.name AS customer,
    p.name AS product,
    oi.quantity,
    o.created_at
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE u.membership = 'VIP'
  AND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY o.created_at DESC;
```"""
            },
            {
                "type": "tip",
                "title": "💡 연습 팁",
                "content": """### JOIN 작성 순서

```
1. 필요한 테이블 파악
2. 관계(FK) 확인
3. 기준 테이블 결정
4. JOIN 유형 선택
5. SELECT 컬럼 정리
6. WHERE/GROUP BY 추가
7. EXPLAIN으로 성능 확인
```

### 디버깅 팁

```sql
-- 1. 각 JOIN 단계별로 확인
SELECT * FROM users u
-- 여기서 결과 확인
INNER JOIN orders o ON u.id = o.user_id;
-- 다시 확인

-- 2. 행 수 비교
SELECT COUNT(*) FROM users;           -- 100
SELECT COUNT(*) FROM orders;          -- 500
SELECT COUNT(*) FROM users u
INNER JOIN orders o ON u.id = o.user_id;  -- 500
-- INNER JOIN 결과가 orders와 같으면 모든 주문에 유저 있음
```"""
            }
        ]
    },

    # 04_인덱스 섹션
    "04_인덱스/index-concept": {
        "title": "인덱스 개념",
        "description": "인덱스의 원리와 필요성을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스란?",
                "content": """## 🔥 한 줄 요약
> **데이터 검색을 빠르게 하는 목차** - 책의 색인과 동일!

---

## 💡 왜 배워야 하나?

### 실제 사고 사례:
```
🔴 드로우 앱 사태 (2023)
├── 나이키 한정판 드로우 시작
├── 100만 명 동시 접속
├── 로그인에 3초 걸림 → 인덱스 없는 쿼리
├── 서버 다운, 100만 명 이탈
└── 인덱스 추가 후 0.01초로 해결

🔴 일반적인 상황
├── 회원 100만 명 테이블
├── SELECT * FROM users WHERE email = 'kim@test.com'
├── 인덱스 없음: 100만 행 전체 스캔 (2초)
├── 인덱스 있음: 바로 찾음 (0.001초)
└── 2000배 차이!
```

---

## 🎯 핵심 개념

### 📚 도서관 비유

```
책 1000권에서 "파이썬" 찾기

❌ 인덱스 없음 (Full Table Scan)
└── 1000권 전부 확인 → 느림!

✅ 인덱스 있음 (Index Scan)
└── 색인에서 "파이썬" → 바로 위치 확인
```

### 인덱스 동작 원리

```
users 테이블 (100만 행)
+----+------------------+------+
| id | email            | name |
+----+------------------+------+
| 1  | kim@test.com     | 김철수 |
| 2  | lee@test.com     | 이영희 |
| ... | ...             | ...  |
+----+------------------+------+

email 인덱스 (B-Tree 구조)
        ┌─────────────────┐
        │    m@...        │
        └────────┬────────┘
           ┌─────┴─────┐
       ┌───┴───┐   ┌───┴───┐
       │ a-l   │   │ n-z   │
       └───────┘   └───────┘

→ kim@test.com 검색: 3단계만에 찾음!
```"""
            },
            {
                "type": "code",
                "title": "💻 인덱스 생성/확인",
                "content": """### 인덱스 생성

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_email ON users(email);

-- 복합 인덱스 (여러 컬럼)
CREATE INDEX idx_status_created ON orders(status, created_at);

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_email_unique ON users(email);

-- 테이블 생성 시 인덱스
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(100),
    name VARCHAR(50),
    INDEX idx_email (email),
    INDEX idx_name (name)
);
```

### 인덱스 확인

```sql
-- 테이블의 인덱스 확인
SHOW INDEX FROM users;

-- 쿼리가 인덱스를 사용하는지 확인
EXPLAIN SELECT * FROM users WHERE email = 'kim@test.com';
-- type: ref, possible_keys: idx_email 확인
```

### 인덱스 삭제

```sql
-- 인덱스 삭제
DROP INDEX idx_email ON users;

-- ALTER TABLE로 삭제
ALTER TABLE users DROP INDEX idx_email;
```"""
            },
            {
                "type": "tip",
                "title": "💡 인덱스 핵심 정리",
                "content": """### 인덱스를 만들어야 하는 컬럼

```
✅ 인덱스 필요
├── WHERE 조건에 자주 사용
├── JOIN 조건 (FK)
├── ORDER BY 대상
├── 유니크해야 하는 컬럼

❌ 인덱스 불필요
├── 데이터가 적은 테이블 (1000건 이하)
├── 값의 종류가 적은 컬럼 (성별: M/F)
├── INSERT/UPDATE가 매우 빈번한 테이블
```

### 인덱스 비용

```
장점: 조회 속도 ⬆️
단점:
├── INSERT 느려짐 (인덱스도 갱신)
├── UPDATE 느려짐 (인덱스 재구성)
├── 저장 공간 추가 필요
└── 과도한 인덱스 = 성능 저하
```"""
            }
        ]
    },

    "04_인덱스/index-structure": {
        "title": "인덱스 구조",
        "description": "B-Tree, Hash 등 인덱스 내부 구조를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스 내부 구조",
                "content": """## 🔥 B-Tree 인덱스 (가장 일반적)

```
               ┌─────────────┐
               │  50         │  ← Root Node
               └──────┬──────┘
            ┌─────────┴─────────┐
       ┌────┴────┐         ┌────┴────┐
       │ 25      │         │ 75      │  ← Branch Node
       └────┬────┘         └────┬────┘
      ┌─────┴─────┐       ┌─────┴─────┐
   ┌──┴──┐     ┌──┴──┐ ┌──┴──┐     ┌──┴──┐
   │10,20│     │30,40│ │60,70│     │80,90│  ← Leaf Node
   └─────┘     └─────┘ └─────┘     └─────┘

특징:
├── 정렬된 상태 유지
├── 범위 검색 가능 (BETWEEN, >, <)
├── O(log N) 검색 시간
└── 대부분의 DB 기본 인덱스
```

---

## 🔥 Hash 인덱스

```
해시 함수: email → 해시값

"kim@test.com" → hash() → 위치 3
"lee@test.com" → hash() → 위치 7

특징:
├── = 검색 매우 빠름 O(1)
├── 범위 검색 불가 (>, <, BETWEEN)
├── Memory 엔진에서 주로 사용
└── MySQL InnoDB는 내부적으로 해시 인덱스 일부 사용
```

---

## 🔥 Full-Text 인덱스

```
"오늘 날씨가 좋습니다" 검색

역인덱스 구조:
오늘 → [문서1, 문서5, 문서10]
날씨 → [문서1, 문서3, 문서8]
좋습니다 → [문서1, 문서2]

특징:
├── 텍스트 검색 특화
├── LIKE '%keyword%' 대체
└── MATCH ... AGAINST 문법
```"""
            },
            {
                "type": "code",
                "title": "💻 인덱스 유형별 사용",
                "content": """### B-Tree 인덱스 (기본)

```sql
-- 일반 인덱스 (B-Tree)
CREATE INDEX idx_email ON users(email);

-- 적합한 쿼리
SELECT * FROM users WHERE email = 'kim@test.com';  -- = 검색
SELECT * FROM users WHERE email LIKE 'kim%';       -- 접두사 검색
SELECT * FROM users WHERE created_at > '2024-01-01';  -- 범위
SELECT * FROM users ORDER BY created_at;           -- 정렬
```

### Hash 인덱스 (Memory 엔진)

```sql
-- Memory 테이블에서 Hash 인덱스
CREATE TABLE cache_data (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT
) ENGINE=MEMORY;

-- Hash 인덱스 명시
CREATE INDEX idx_key USING HASH ON cache_data(key);

-- 적합한 쿼리 (= 검색만)
SELECT * FROM cache_data WHERE key = 'session_123';
```

### Full-Text 인덱스

```sql
-- Full-Text 인덱스 생성
CREATE FULLTEXT INDEX idx_content ON articles(title, content);

-- 검색 쿼리
SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('파이썬 웹개발');

-- 불린 모드 (AND, OR, NOT)
SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('+파이썬 +웹개발' IN BOOLEAN MODE);
```"""
            },
            {
                "type": "tip",
                "title": "💡 인덱스 선택 가이드",
                "content": """### 언제 어떤 인덱스?

```
B-Tree (기본):
├── 대부분의 경우
├── =, >, <, BETWEEN, LIKE 'abc%'
└── ORDER BY, GROUP BY

Hash:
├── = 검색만 사용
├── 캐시 테이블
└── 메모리 테이블

Full-Text:
├── 텍스트 검색
├── LIKE '%keyword%' 대체
└── 게시글, 상품 검색
```

### 클러스터드 vs 논클러스터드

```
클러스터드 인덱스 (Primary Key):
├── 테이블당 1개만
├── 데이터가 인덱스 순서로 물리적 정렬
└── PK 검색 가장 빠름

논클러스터드 인덱스 (일반 인덱스):
├── 테이블당 여러 개 가능
├── 별도의 인덱스 구조
└── Leaf Node에 PK 포함 → PK로 다시 검색
```"""
            }
        ]
    },

    "04_인덱스/index-types": {
        "title": "인덱스 종류",
        "description": "단일, 복합, 커버링 인덱스 등을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스 종류 총정리",
                "content": """## 🎯 인덱스 종류

### 1. 단일 컬럼 인덱스
```sql
CREATE INDEX idx_email ON users(email);
-- WHERE email = 'test@test.com' 빠름
```

### 2. 복합 인덱스 (Composite)
```sql
CREATE INDEX idx_status_created ON orders(status, created_at);
-- 컬럼 순서 중요! (왼쪽부터 사용)
```

### 3. 유니크 인덱스
```sql
CREATE UNIQUE INDEX idx_email ON users(email);
-- 중복 불가 + 검색 최적화
```

### 4. 커버링 인덱스
```sql
-- 인덱스만으로 쿼리 완료 (테이블 접근 X)
CREATE INDEX idx_covering ON orders(status, user_id, total_price);
SELECT user_id, total_price FROM orders WHERE status = 'completed';
```

### 5. 클러스터드 인덱스
```sql
-- Primary Key가 자동으로 클러스터드 인덱스
-- 테이블당 1개, 데이터 물리적 정렬
```"""
            },
            {
                "type": "code",
                "title": "💻 복합 인덱스 핵심",
                "content": """### 복합 인덱스 순서가 중요한 이유

```sql
-- 인덱스: (status, created_at)
CREATE INDEX idx_status_created ON orders(status, created_at);

-- ✅ 인덱스 사용
WHERE status = 'completed'                    -- 첫 번째 컬럼
WHERE status = 'completed' AND created_at > '2024-01-01'  -- 둘 다

-- ❌ 인덱스 못 씀
WHERE created_at > '2024-01-01'              -- 두 번째 컬럼만
```

### 복합 인덱스 설계 원칙

```sql
-- 1. 카디널리티 높은 것 먼저 (값 종류 많은 것)
-- user_id: 100만 가지 vs status: 5가지
CREATE INDEX idx_bad ON orders(status, user_id);    -- ❌
CREATE INDEX idx_good ON orders(user_id, status);   -- ✅

-- 2. 등호 조건 먼저, 범위 조건 나중에
-- 범위 조건 이후 컬럼은 인덱스 효과 없음
CREATE INDEX idx ON orders(status, created_at, user_id);
WHERE status = 'completed'           -- 인덱스 O
  AND created_at > '2024-01-01'     -- 인덱스 O (범위)
  AND user_id = 1;                   -- 인덱스 X (범위 이후)
```

### 커버링 인덱스 예제

```sql
-- 쿼리에 필요한 모든 컬럼이 인덱스에 있으면
-- 테이블 접근 없이 인덱스만으로 결과 반환

CREATE INDEX idx_covering ON orders(status, user_id, total_price);

-- 이 쿼리는 테이블 접근 X (Extra: Using index)
SELECT user_id, SUM(total_price)
FROM orders
WHERE status = 'completed'
GROUP BY user_id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 인덱스 설계 가이드",
                "content": """### 복합 인덱스 vs 단일 인덱스

```
복합 인덱스 (a, b, c) 하나로 커버:
├── WHERE a = ?
├── WHERE a = ? AND b = ?
├── WHERE a = ? AND b = ? AND c = ?

단일 인덱스 3개보다 효율적!
```

### 실무 설계 패턴

```sql
-- 1. 자주 쓰는 쿼리 분석
SELECT * FROM orders WHERE user_id = ? AND status = ?;
SELECT * FROM orders WHERE status = ? ORDER BY created_at;

-- 2. 인덱스 설계
CREATE INDEX idx_user_status ON orders(user_id, status);
CREATE INDEX idx_status_created ON orders(status, created_at);
```

### 인덱스 개수 제한

```
권장: 테이블당 5~10개 이하
├── 너무 많으면 INSERT/UPDATE 느림
├── 비슷한 인덱스 통합 검토
└── 사용 안 하는 인덱스 삭제
```"""
            }
        ]
    },

    "04_인덱스/index-design": {
        "title": "인덱스 설계",
        "description": "효율적인 인덱스 설계 전략을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스 설계 전략",
                "content": """## 🎯 인덱스 설계 프로세스

```
1단계: 쿼리 분석
├── 어떤 쿼리가 자주 실행되나?
├── WHERE, JOIN, ORDER BY 조건은?
└── 느린 쿼리 로그 분석

2단계: 인덱스 후보 도출
├── WHERE 조건 컬럼
├── JOIN 조건 컬럼 (FK)
├── ORDER BY 컬럼

3단계: 복합 인덱스 설계
├── 자주 함께 쓰이는 컬럼 묶기
├── 카디널리티 순서 고려
└── 커버링 인덱스 가능성 검토

4단계: 테스트 및 모니터링
├── EXPLAIN으로 확인
├── 슬로우 쿼리 모니터링
└── 불필요한 인덱스 제거
```

---

## 🎯 설계 원칙

### 카디널리티 (Cardinality)
```
카디널리티 = 고유값의 개수

높음 (인덱스 효과적):
├── user_id: 100만 가지
├── email: 100만 가지
└── order_id: 500만 가지

낮음 (인덱스 비효율):
├── gender: 2가지 (M/F)
├── status: 5가지
└── is_active: 2가지 (Y/N)
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 인덱스 설계",
                "content": """### 쇼핑몰 orders 테이블

```sql
-- 테이블 구조
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status ENUM('pending','paid','shipped','delivered','cancelled'),
    total_price DECIMAL(12,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 자주 사용되는 쿼리 분석
-- Q1: 특정 유저의 주문 목록
SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC;

-- Q2: 상태별 주문 (관리자)
SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC;

-- Q3: 기간별 매출 통계
SELECT DATE(created_at), SUM(total_price)
FROM orders
WHERE created_at BETWEEN ? AND ?
GROUP BY DATE(created_at);
```

### 인덱스 설계

```sql
-- Q1용: user_id + created_at
CREATE INDEX idx_user_created ON orders(user_id, created_at DESC);

-- Q2용: status + created_at
CREATE INDEX idx_status_created ON orders(status, created_at DESC);

-- Q3용: created_at (+ 커버링)
CREATE INDEX idx_created_price ON orders(created_at, total_price);
```

### EXPLAIN으로 검증

```sql
EXPLAIN SELECT * FROM orders
WHERE user_id = 1 ORDER BY created_at DESC LIMIT 10;

-- 확인 항목
-- type: ref (인덱스 사용)
-- key: idx_user_created
-- Extra: Using index condition
```"""
            },
            {
                "type": "tip",
                "title": "💡 인덱스 설계 체크리스트",
                "content": """### 설계 체크리스트

```
□ WHERE 조건 컬럼에 인덱스?
□ JOIN 컬럼(FK)에 인덱스?
□ ORDER BY 컬럼이 인덱스에 포함?
□ 복합 인덱스 순서 최적화?
□ 커버링 인덱스 가능?
□ 중복/유사 인덱스 없는지?
□ 카디널리티 낮은 단독 인덱스 없는지?
```

### 안티패턴

```sql
-- ❌ 모든 컬럼에 인덱스
CREATE INDEX idx1 ON users(id);      -- PK 이미 있음
CREATE INDEX idx2 ON users(name);
CREATE INDEX idx3 ON users(email);
CREATE INDEX idx4 ON users(phone);
CREATE INDEX idx5 ON users(address);
-- INSERT/UPDATE 느려짐!

-- ✅ 필요한 것만
CREATE INDEX idx_email ON users(email);  -- 로그인
CREATE INDEX idx_phone ON users(phone);  -- 본인인증
```"""
            }
        ]
    },

    "04_인덱스/index-bad-case": {
        "title": "인덱스가 안 타는 경우",
        "description": "인덱스가 사용되지 않는 상황을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스 무효화 케이스",
                "content": """## 🎯 인덱스가 안 타는 경우

### 1. 컬럼에 함수/연산 사용
```sql
-- ❌ 인덱스 안 탐
WHERE YEAR(created_at) = 2024
WHERE price * 1.1 > 10000
WHERE LOWER(email) = 'test@test.com'

-- ✅ 인덱스 탐
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
WHERE price > 10000 / 1.1
WHERE email = 'test@test.com'  -- 대소문자 무시하려면 CI 콜레이션
```

### 2. LIKE '%keyword'
```sql
-- ❌ 인덱스 안 탐 (앞에 %)
WHERE name LIKE '%철수'

-- ✅ 인덱스 탐
WHERE name LIKE '김%'
```

### 3. OR 조건
```sql
-- ❌ 비효율적
WHERE status = 'A' OR user_id = 1

-- ✅ UNION 또는 각각 인덱스
SELECT * FROM orders WHERE status = 'A'
UNION
SELECT * FROM orders WHERE user_id = 1;
```

### 4. NOT, <>, != 조건
```sql
-- ❌ 인덱스 비효율
WHERE status != 'deleted'
WHERE status <> 'cancelled'
WHERE status NOT IN ('deleted', 'cancelled')

-- ✅ 가능하면 긍정 조건으로
WHERE status IN ('active', 'pending', 'completed')
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 예제",
                "content": """### 날짜 검색 최적화

```sql
-- ❌ 함수 사용 (인덱스 X)
SELECT * FROM orders
WHERE DATE(created_at) = '2024-01-15';

SELECT * FROM orders
WHERE YEAR(created_at) = 2024 AND MONTH(created_at) = 1;

-- ✅ 범위 조건 (인덱스 O)
SELECT * FROM orders
WHERE created_at >= '2024-01-15'
  AND created_at < '2024-01-16';

SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01';
```

### 문자열 검색 최적화

```sql
-- ❌ LIKE '%keyword%' (인덱스 X)
SELECT * FROM products
WHERE name LIKE '%아이폰%';

-- ✅ Full-Text 인덱스 사용
CREATE FULLTEXT INDEX idx_name ON products(name);
SELECT * FROM products
WHERE MATCH(name) AGAINST('아이폰');

-- ✅ 또는 별도 검색 엔진 (Elasticsearch)
```

### 복합 인덱스 순서

```sql
-- 인덱스: (status, user_id, created_at)

-- ✅ 인덱스 사용
WHERE status = 'completed' AND user_id = 1;

-- ❌ 인덱스 안 탐 (첫 번째 컬럼 없음)
WHERE user_id = 1;

-- ⚠️ 부분만 사용
WHERE status = 'completed' AND created_at > '2024-01-01';
-- status만 인덱스 사용, created_at은 필터링
```"""
            },
            {
                "type": "tip",
                "title": "💡 디버깅 팁",
                "content": """### EXPLAIN으로 확인

```sql
EXPLAIN SELECT * FROM orders WHERE YEAR(created_at) = 2024;
-- type: ALL (풀스캔)
-- key: NULL (인덱스 안 씀)

EXPLAIN SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
-- type: range (범위 스캔)
-- key: idx_created_at (인덱스 사용)
```

### 체크리스트

```
인덱스 안 탈 때 확인:
□ 컬럼에 함수/연산 사용했나?
□ LIKE '%...'로 시작하나?
□ 복합 인덱스 순서 맞나?
□ OR 조건 있나?
□ 데이터가 너무 많이 조회되나? (30% 이상)
□ NULL 비교를 = 로 했나?
```"""
            }
        ]
    },

    "04_인덱스/index-anti-pattern": {
        "title": "인덱스 안티패턴",
        "description": "피해야 할 인덱스 사용 패턴을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 인덱스 안티패턴",
                "content": """## 🎯 피해야 할 패턴

### 1. 과도한 인덱스
```
❌ 모든 컬럼에 인덱스
├── INSERT 성능 저하
├── UPDATE 성능 저하
├── 디스크 공간 낭비
└── 옵티마이저 혼란

✅ 필요한 쿼리 기반으로만
```

### 2. 중복 인덱스
```sql
-- ❌ 중복
CREATE INDEX idx1 ON orders(user_id);
CREATE INDEX idx2 ON orders(user_id, status);
-- idx2가 idx1의 역할 커버

-- ✅ 하나로 통합
CREATE INDEX idx ON orders(user_id, status);
```

### 3. 사용 안 하는 인덱스
```sql
-- 인덱스 사용 통계 확인 (MySQL)
SELECT * FROM sys.schema_unused_indexes;

-- 사용 안 하면 삭제
DROP INDEX idx_unused ON table_name;
```

### 4. 카디널리티 낮은 컬럼 단독 인덱스
```sql
-- ❌ 값이 2~3개뿐
CREATE INDEX idx_gender ON users(gender);  -- M/F
CREATE INDEX idx_active ON users(is_active);  -- Y/N

-- ✅ 복합 인덱스에 포함
CREATE INDEX idx ON users(status, gender);
```"""
            },
            {
                "type": "code",
                "title": "💻 안티패턴 예제",
                "content": """### 인덱스 통계 분석

```sql
-- MySQL: 인덱스 사용 현황
SELECT
    TABLE_NAME,
    INDEX_NAME,
    SEQ_IN_INDEX,
    COLUMN_NAME,
    CARDINALITY
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'your_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- 사용되지 않는 인덱스 찾기 (MySQL 8.0+)
SELECT * FROM sys.schema_unused_indexes
WHERE object_schema = 'your_db';

-- 중복 인덱스 찾기
SELECT * FROM sys.schema_redundant_indexes
WHERE table_schema = 'your_db';
```

### 인덱스 정리

```sql
-- 불필요한 인덱스 삭제
DROP INDEX idx_unused ON orders;

-- 중복 인덱스 통합
DROP INDEX idx_user_id ON orders;  -- user_id만
-- idx_user_status (user_id, status) 남김

-- 인덱스 재구성 (조각화 해소)
ALTER TABLE orders ENGINE=InnoDB;  -- MySQL
-- 또는
OPTIMIZE TABLE orders;
```

### 실전 최적화 예제

```sql
-- Before: 인덱스 6개
idx_user_id (user_id)
idx_status (status)
idx_created (created_at)
idx_user_status (user_id, status)
idx_status_created (status, created_at)
idx_user_created (user_id, created_at)

-- After: 인덱스 3개로 정리
idx_user_status_created (user_id, status, created_at)
idx_status_created (status, created_at)
idx_created (created_at)  -- 기간 조회용
```"""
            },
            {
                "type": "tip",
                "title": "💡 인덱스 관리 가이드",
                "content": """### 정기 점검 항목

```
월간 점검:
□ 사용되지 않는 인덱스
□ 중복 인덱스
□ 슬로우 쿼리에서 인덱스 안 타는 쿼리
□ 인덱스 크기 확인

분기별:
□ 인덱스 재구성 (조각화)
□ 통계 정보 업데이트
```

### 인덱스 개수 가이드

```
소규모 테이블 (1만건 이하): 2~3개
중규모 테이블 (100만건 이하): 3~5개
대규모 테이블 (1000만건 이상): 5~10개

넘어가면 검토 필요!
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

print(f"✅ 03_JOIN, 04_인덱스 섹션 업데이트 완료: {len(db_contents)}개 토픽")
