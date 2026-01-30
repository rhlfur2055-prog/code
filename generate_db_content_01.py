# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open('src/data/contents/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 01_기초 섹션
db_contents = {
    "01_기초/db-intro": {
        "title": "데이터베이스 소개",
        "description": "데이터베이스의 개념과 필요성을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 데이터베이스가 뭐야?",
                "content": """## 🔥 한 줄 요약
> **데이터를 체계적으로 저장하고 관리하는 시스템** - "엑셀의 진화 버전"

---

## 💡 왜 배워야 하나?

### 실무에서:
- **모든 서비스의 핵심**: 회원정보, 주문, 결제... 다 DB에 저장
- **취업 필수**: 백엔드 공고 100% "SQL 능숙자"
- **연봉 협상 무기**: DB 최적화 가능하면 시니어 대우

### 현실 예시:
```
🏢 쿠팡에서 "아이폰" 검색 → 0.1초 만에 10만 개 상품 출력
📱 인스타에서 좋아요 누르면 → 전세계 어디서든 반영
🎮 롤에서 전적 검색 → 과거 1000판 기록 즉시 조회
```

---

## 🎯 핵심 개념

### 📚 도서관으로 이해하기

**파일 시스템 (엑셀)**
```
📁 고객.xlsx
📁 주문.xlsx
📁 상품.xlsx
→ 파일 열고, 찾고, 수정하고... 느림!
→ 동시에 여러 명이 수정하면? 충돌!
```

**데이터베이스**
```
🏛️ 도서관 시스템
→ 사서(DBMS)가 책 관리
→ 색인(인덱스)으로 빠른 검색
→ 여러 명이 동시에 대출 가능
```

### DB vs 파일 비교

| 구분 | 파일(엑셀) | 데이터베이스 |
|-----|----------|------------|
| 동시 접근 | ❌ 충돌 | ✅ 가능 |
| 검색 속도 | 느림 | 빠름 (인덱스) |
| 데이터 무결성 | 없음 | 제약조건 |
| 백업/복구 | 수동 | 자동화 |
| 보안 | 없음 | 권한 관리 |

### DBMS 종류

```
🔵 관계형 (RDBMS)
├── MySQL (무료, 가장 대중적)
├── PostgreSQL (무료, 기능 풍부)
├── Oracle (유료, 대기업)
└── SQL Server (MS, 윈도우)

🟢 NoSQL
├── MongoDB (문서형)
├── Redis (키-값, 캐시)
└── Elasticsearch (검색)
```"""
            },
            {
                "type": "code",
                "title": "💻 첫 번째 SQL",
                "content": """### 데이터 조회의 시작

```sql
-- 모든 고객 정보 조회
SELECT * FROM customers;

-- 특정 컬럼만 조회
SELECT name, email FROM customers;

-- 조건으로 필터링
SELECT * FROM customers WHERE age >= 20;

-- 정렬
SELECT * FROM customers ORDER BY created_at DESC;
```

### 데이터 구조 예시

```
customers 테이블
+----+--------+-------------------+-----+
| id | name   | email             | age |
+----+--------+-------------------+-----+
| 1  | 김철수  | kim@example.com   | 25  |
| 2  | 이영희  | lee@example.com   | 30  |
| 3  | 박민수  | park@example.com  | 22  |
+----+--------+-------------------+-----+
```

### Python에서 DB 연결

```python
import mysql.connector

# DB 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="myapp"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM customers")
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 어떤 DB를 선택할까?

```
🟢 MySQL
├── 스타트업, 중소기업
├── 무료 + 쉬운 학습곡선
└── 대부분의 웹 서비스

🔵 PostgreSQL
├── 복잡한 쿼리, GIS 데이터
├── JSON 지원 우수
└── 스타트업에서 인기 상승 중

🟡 Oracle
├── 대기업, 금융권
├── 비싸지만 안정적
└── DBA 연봉이 높음
```

### 학습 로드맵

```
1단계: SQL 기초 (SELECT, INSERT, UPDATE, DELETE)
2단계: JOIN, 서브쿼리
3단계: 인덱스, 실행계획
4단계: 트랜잭션, 락
5단계: 성능 최적화
```"""
            }
        ]
    },

    "01_기초/rdbms": {
        "title": "관계형 데이터베이스",
        "description": "RDBMS의 핵심 개념과 구조를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 RDBMS란?",
                "content": """## 🔥 한 줄 요약
> **테이블 간 관계로 데이터를 관리** - "엑셀 시트를 연결한 것"

---

## 💡 왜 배워야 하나?

### 취업 시장:
- 백엔드 공고 **95%**: "MySQL/PostgreSQL 경험"
- 데이터 분석 공고 **100%**: "SQL 필수"
- 연봉 1억 DBA: RDBMS 전문가

### 현실 예시:
```
🛒 쿠팡 주문 시스템
├── 회원 테이블 (누가 샀는지)
├── 상품 테이블 (뭘 샀는지)
├── 주문 테이블 (언제 샀는지)
└── 배송 테이블 (어디로 보내는지)
→ 4개 테이블이 관계로 연결!
```

---

## 🎯 핵심 개념

### 📊 테이블 구조

```
┌─────────────────────────────────────┐
│           customers 테이블           │
├────┬────────┬──────────────┬────────┤
│ id │ name   │ email        │ age    │  ← Row (행, 레코드)
├────┼────────┼──────────────┼────────┤
│ 1  │ 김철수  │ kim@test.com │ 25     │
│ 2  │ 이영희  │ lee@test.com │ 30     │
└────┴────────┴──────────────┴────────┘
  ↑      ↑          ↑           ↑
  Column (열, 필드, 속성)
```

### 🔑 키(Key)의 종류

```sql
-- Primary Key (기본키): 유일하게 식별
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- 이게 PK
    email VARCHAR(100) UNIQUE,
    name VARCHAR(50)
);

-- Foreign Key (외래키): 다른 테이블 참조
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,  -- users.id를 참조
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 관계의 종류

```
1:1 (일대일)
├── 유저 ↔ 프로필
└── 하나의 유저는 하나의 프로필만

1:N (일대다) ⭐ 가장 흔함
├── 유저 ↔ 주문
└── 한 유저가 여러 주문 가능

N:M (다대다)
├── 학생 ↔ 수업
└── 중간 테이블 필요 (수강신청)
```"""
            },
            {
                "type": "code",
                "title": "💻 테이블 설계 예시",
                "content": """### 쇼핑몰 DB 설계

```sql
-- 1. 회원 테이블
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 상품 테이블
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    stock INT DEFAULT 0,
    category VARCHAR(50)
);

-- 3. 주문 테이블 (users와 1:N 관계)
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_price INT NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. 주문상세 테이블 (orders, products와 관계)
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 관계 조회 (JOIN)

```sql
-- 회원별 주문 내역 조회
SELECT
    u.name AS 회원명,
    o.id AS 주문번호,
    o.total_price AS 총액,
    o.created_at AS 주문일
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.id = 1;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### RDBMS 선택 가이드

| DB | 장점 | 단점 | 추천 |
|----|-----|-----|------|
| MySQL | 쉬움, 무료, 빠름 | 기능 제한 | 웹서비스 |
| PostgreSQL | 기능 풍부, JSON | 설정 복잡 | 복잡한 쿼리 |
| Oracle | 안정성, 성능 | 비용 | 대기업 |

### 설계 원칙

```
✅ 정규화: 중복 제거 (3NF까지)
✅ 적절한 인덱스: 검색 성능
✅ 외래키 설정: 데이터 무결성
✅ 명명 규칙: snake_case 추천
```"""
            }
        ]
    },

    "01_기초/rdbms-concept": {
        "title": "RDBMS 핵심 개념",
        "description": "스키마, 테이블, 제약조건의 개념을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 스키마와 제약조건",
                "content": """## 🔥 한 줄 요약
> **스키마 = 설계도, 제약조건 = 규칙** - "건물 청사진 + 안전 규정"

---

## 💡 왜 배워야 하나?

### 실무 사고 예방:
```
❌ 제약조건 없이 개발
├── 이메일 중복 가입 → 고객 항의
├── 마이너스 재고 → 주문 불가 사태
├── 존재하지 않는 유저의 주문 → 데이터 꼬임
└── 복구에 3일 걸림 + 야근

✅ 제약조건 설정
└── DB가 알아서 막아줌!
```

---

## 🎯 핵심 개념

### 📋 스키마(Schema)

```
스키마 = 데이터베이스 구조 정의

┌─────────────────────────────────┐
│  Database: shopping_mall        │
├─────────────────────────────────┤
│  Schema                         │
│  ├── users 테이블               │
│  │   ├── id (PK)               │
│  │   ├── email (UNIQUE)        │
│  │   └── name                  │
│  ├── products 테이블            │
│  └── orders 테이블              │
└─────────────────────────────────┘
```

### 🔒 제약조건 종류

```sql
-- 1. NOT NULL: 필수값
email VARCHAR(100) NOT NULL

-- 2. UNIQUE: 중복 불가
email VARCHAR(100) UNIQUE

-- 3. PRIMARY KEY: 유일 식별자
id INT PRIMARY KEY

-- 4. FOREIGN KEY: 참조 무결성
user_id INT REFERENCES users(id)

-- 5. CHECK: 값 범위 제한
price INT CHECK (price >= 0)

-- 6. DEFAULT: 기본값
status VARCHAR(20) DEFAULT 'active'
```

### 제약조건 실전 예시

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,           -- 상품명 필수
    price INT NOT NULL CHECK (price > 0), -- 0원 이상
    stock INT DEFAULT 0 CHECK (stock >= 0), -- 재고 0 이상
    status ENUM('active', 'inactive', 'deleted') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```"""
            },
            {
                "type": "code",
                "title": "💻 제약조건 활용",
                "content": """### 제약조건 위반 시

```sql
-- 1. NOT NULL 위반
INSERT INTO users (email, name) VALUES (NULL, '김철수');
-- Error: Column 'email' cannot be null

-- 2. UNIQUE 위반
INSERT INTO users (email, name) VALUES ('kim@test.com', '김철수');
INSERT INTO users (email, name) VALUES ('kim@test.com', '이영희');
-- Error: Duplicate entry 'kim@test.com' for key 'email'

-- 3. FOREIGN KEY 위반
INSERT INTO orders (user_id, total_price) VALUES (9999, 50000);
-- Error: Cannot add or update a child row:
--        a foreign key constraint fails
```

### CASCADE 옵션

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE    -- 유저 삭제 시 주문도 삭제
        ON UPDATE CASCADE    -- 유저 ID 변경 시 같이 변경
);

-- 옵션 종류
-- CASCADE: 같이 삭제/수정
-- SET NULL: NULL로 설정
-- RESTRICT: 삭제/수정 막음 (기본값)
-- NO ACTION: RESTRICT와 동일
```

### 제약조건 추가/삭제

```sql
-- 기존 테이블에 제약조건 추가
ALTER TABLE users
ADD CONSTRAINT uk_email UNIQUE (email);

-- 제약조건 삭제
ALTER TABLE users
DROP CONSTRAINT uk_email;

-- 인덱스 확인
SHOW INDEX FROM users;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 제약조건 베스트 프랙티스

```
✅ 항상 PK 설정 (AUTO_INCREMENT 추천)
✅ 이메일, 주민번호 등은 UNIQUE
✅ 가격, 수량은 CHECK로 음수 방지
✅ FK로 데이터 무결성 보장
✅ created_at, updated_at 자동 설정

❌ 모든 컬럼에 NOT NULL (유연성 저하)
❌ CHECK 남발 (애플리케이션에서 검증)
❌ CASCADE DELETE 무분별 사용
```

### 제약조건 vs 애플리케이션 검증

```
DB 제약조건: 최후의 보루 (절대 뚫리면 안 됨)
앱 검증: 사용자 친화적 에러 메시지

→ 둘 다 해야 함!
```"""
            }
        ]
    },

    # 02_SQL 섹션
    "02_SQL/sql-intro": {
        "title": "SQL 기초",
        "description": "SQL 언어의 기본 문법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 SQL이란?",
                "content": """## 🔥 한 줄 요약
> **데이터베이스와 대화하는 언어** - "DB야, 이 데이터 줘!"

---

## 💡 왜 배워야 하나?

### 취업 필수:
- 백엔드 개발자 공고 **100%**: SQL 필수
- 데이터 분석가 공고 **100%**: SQL 필수
- PM/기획자도 SQL 알면 연봉 UP

### 현실 예시:
```
📊 "이번 달 매출 얼마야?"
→ SELECT SUM(price) FROM orders WHERE created_at >= '2024-01-01'
→ 0.001초 만에 답변!

📈 "VIP 고객 100명 뽑아줘"
→ SELECT * FROM users ORDER BY total_purchase DESC LIMIT 100
```

---

## 🎯 핵심 개념

### SQL 종류

```
📝 DDL (Data Definition Language) - 구조 정의
├── CREATE: 생성
├── ALTER: 수정
├── DROP: 삭제
└── TRUNCATE: 데이터 전체 삭제

📝 DML (Data Manipulation Language) - 데이터 조작
├── SELECT: 조회
├── INSERT: 삽입
├── UPDATE: 수정
└── DELETE: 삭제

📝 DCL (Data Control Language) - 권한 제어
├── GRANT: 권한 부여
└── REVOKE: 권한 회수

📝 TCL (Transaction Control Language)
├── COMMIT: 확정
├── ROLLBACK: 취소
└── SAVEPOINT: 저장점
```

### SELECT 문법 순서

```sql
SELECT column_name    -- 5. 출력할 컬럼
FROM table_name       -- 1. 테이블 선택
WHERE condition       -- 2. 조건 필터링
GROUP BY column       -- 3. 그룹화
HAVING condition      -- 4. 그룹 필터링
ORDER BY column       -- 6. 정렬
LIMIT n               -- 7. 개수 제한
```"""
            },
            {
                "type": "code",
                "title": "💻 기본 SQL 문법",
                "content": """### SELECT (조회)

```sql
-- 전체 조회
SELECT * FROM users;

-- 특정 컬럼 조회
SELECT name, email FROM users;

-- 조건 조회
SELECT * FROM users WHERE age >= 20;

-- 정렬
SELECT * FROM users ORDER BY created_at DESC;

-- 개수 제한
SELECT * FROM users LIMIT 10;

-- 중복 제거
SELECT DISTINCT category FROM products;
```

### INSERT (삽입)

```sql
-- 단일 삽입
INSERT INTO users (name, email, age)
VALUES ('김철수', 'kim@test.com', 25);

-- 다중 삽입
INSERT INTO users (name, email, age) VALUES
('이영희', 'lee@test.com', 30),
('박민수', 'park@test.com', 22);
```

### UPDATE (수정)

```sql
-- 특정 행 수정
UPDATE users SET age = 26 WHERE id = 1;

-- 여러 컬럼 수정
UPDATE users SET age = 26, name = '김철수2' WHERE id = 1;

-- ⚠️ WHERE 없으면 전체 수정!
UPDATE users SET age = 26;  -- 위험!
```

### DELETE (삭제)

```sql
-- 특정 행 삭제
DELETE FROM users WHERE id = 1;

-- ⚠️ WHERE 없으면 전체 삭제!
DELETE FROM users;  -- 위험!
```"""
            },
            {
                "type": "common-mistake",
                "title": "⚠️ 흔한 실수",
                "content": """### 1. WHERE 없는 UPDATE/DELETE

```sql
-- 💀 전 직원 월급이 0원이 되는 사고
UPDATE employees SET salary = 0;

-- ✅ 항상 WHERE 먼저 확인
SELECT * FROM employees WHERE id = 1;  -- 먼저 확인
UPDATE employees SET salary = 0 WHERE id = 1;
```

### 2. 작은따옴표 vs 큰따옴표

```sql
-- ❌ 큰따옴표 (DB마다 다름)
SELECT * FROM users WHERE name = "김철수";

-- ✅ 작은따옴표 (표준)
SELECT * FROM users WHERE name = '김철수';
```

### 3. NULL 비교

```sql
-- ❌ = NULL은 항상 FALSE
SELECT * FROM users WHERE phone = NULL;

-- ✅ IS NULL 사용
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;
```"""
            }
        ]
    },

    "02_SQL/dml-select": {
        "title": "SELECT 완벽 가이드",
        "description": "데이터 조회의 모든 것을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 SELECT 마스터하기",
                "content": """## 🔥 한 줄 요약
> **DB에서 원하는 데이터만 뽑아오기** - SQL의 80%는 SELECT

---

## 💡 왜 배워야 하나?

### 실무 현실:
```
📊 기획자: "어제 가입한 유저 중 결제한 사람 뽑아주세요"
📈 마케터: "30대 여성 중 최근 3개월 미접속자 리스트요"
🔧 개발자: 버그 추적하려면 데이터 조회 필수

→ SELECT 못하면 일 못함
```

---

## 🎯 핵심 문법

### 기본 구조

```sql
SELECT [DISTINCT] column1, column2, ...
FROM table_name
[WHERE condition]
[GROUP BY column]
[HAVING condition]
[ORDER BY column [ASC|DESC]]
[LIMIT number];
```

### 실행 순서 (중요!)

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

1️⃣ FROM: 어느 테이블?
2️⃣ WHERE: 어떤 조건?
3️⃣ GROUP BY: 어떻게 묶을까?
4️⃣ HAVING: 그룹 조건
5️⃣ SELECT: 뭘 출력할까?
6️⃣ ORDER BY: 어떻게 정렬?
7️⃣ LIMIT: 몇 개까지?
```

### WHERE 조건 연산자

```sql
-- 비교 연산자
=, <>, !=, <, >, <=, >=

-- 범위
BETWEEN 10 AND 20

-- 목록
IN ('A', 'B', 'C')

-- 패턴 매칭
LIKE 'kim%'      -- kim으로 시작
LIKE '%@gmail%'  -- @gmail 포함
LIKE '___'       -- 정확히 3글자

-- NULL 체크
IS NULL, IS NOT NULL

-- 논리 연산
AND, OR, NOT
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 SELECT",
                "content": """### 조건 조합

```sql
-- AND, OR 조합
SELECT * FROM users
WHERE age >= 20
  AND age <= 30
  AND status = 'active';

-- BETWEEN 사용
SELECT * FROM users
WHERE age BETWEEN 20 AND 30;

-- IN 사용
SELECT * FROM products
WHERE category IN ('전자기기', '의류', '식품');

-- LIKE 패턴
SELECT * FROM users
WHERE email LIKE '%@gmail.com';
```

### 정렬과 제한

```sql
-- 단일 정렬
SELECT * FROM products ORDER BY price DESC;

-- 다중 정렬
SELECT * FROM products
ORDER BY category ASC, price DESC;

-- 페이징 (OFFSET)
SELECT * FROM products
ORDER BY id
LIMIT 10 OFFSET 20;  -- 21번째부터 10개
```

### 집계 함수

```sql
-- 기본 집계
SELECT
    COUNT(*) AS 총개수,
    SUM(price) AS 총합,
    AVG(price) AS 평균,
    MAX(price) AS 최대값,
    MIN(price) AS 최소값
FROM products;

-- GROUP BY와 함께
SELECT
    category,
    COUNT(*) AS 상품수,
    AVG(price) AS 평균가격
FROM products
GROUP BY category
HAVING COUNT(*) >= 5;
```

### 별칭(Alias) 사용

```sql
-- 컬럼 별칭
SELECT
    name AS 상품명,
    price AS 가격,
    price * 0.1 AS 부가세
FROM products;

-- 테이블 별칭
SELECT u.name, o.total_price
FROM users u
JOIN orders o ON u.id = o.user_id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### SELECT 성능 팁

```sql
-- ❌ 느림: SELECT *
SELECT * FROM users;

-- ✅ 빠름: 필요한 컬럼만
SELECT id, name, email FROM users;

-- ❌ 느림: LIKE '%keyword%'
SELECT * FROM products WHERE name LIKE '%아이폰%';

-- ✅ 빠름: LIKE 'keyword%' (앞부분 고정)
SELECT * FROM products WHERE name LIKE '아이폰%';

-- ❌ 느림: 함수로 컬럼 감싸기
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- ✅ 빠름: 범위 조건
SELECT * FROM users
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';
```

### 디버깅 순서

```
1. SELECT * 로 전체 확인
2. WHERE 조건 하나씩 추가
3. 원하는 결과 나오면 컬럼 정리
4. EXPLAIN으로 성능 확인
```"""
            }
        ]
    },

    "02_SQL/dml-insert": {
        "title": "INSERT 완벽 가이드",
        "description": "데이터 삽입의 모든 것을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 INSERT 마스터하기",
                "content": """## 🔥 한 줄 요약
> **테이블에 새 데이터 추가** - 회원가입, 주문생성 등 모든 '생성' 작업

---

## 💡 왜 배워야 하나?

### 실무 필수:
```
회원가입 → INSERT INTO users
상품등록 → INSERT INTO products
주문생성 → INSERT INTO orders
로그기록 → INSERT INTO logs

→ INSERT 모르면 데이터 생성 불가
```

---

## 🎯 핵심 문법

### 기본 구조

```sql
-- 1. 컬럼 명시 (권장)
INSERT INTO table_name (col1, col2, col3)
VALUES (val1, val2, val3);

-- 2. 컬럼 생략 (비권장)
INSERT INTO table_name
VALUES (val1, val2, val3);  -- 모든 컬럼 순서대로

-- 3. 다중 삽입
INSERT INTO table_name (col1, col2)
VALUES
    (val1, val2),
    (val3, val4),
    (val5, val6);
```

### INSERT 옵션들

```sql
-- 1. INSERT IGNORE: 에러 무시
INSERT IGNORE INTO users (email, name)
VALUES ('duplicate@test.com', '김철수');
-- 중복 시 에러 대신 무시

-- 2. ON DUPLICATE KEY UPDATE: 중복 시 업데이트
INSERT INTO users (email, name, login_count)
VALUES ('kim@test.com', '김철수', 1)
ON DUPLICATE KEY UPDATE
    login_count = login_count + 1;

-- 3. REPLACE: 중복 시 삭제 후 삽입
REPLACE INTO users (email, name)
VALUES ('kim@test.com', '김철수');
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 INSERT",
                "content": """### 기본 삽입

```sql
-- 단일 삽입
INSERT INTO users (email, name, age)
VALUES ('kim@test.com', '김철수', 25);

-- 다중 삽입 (훨씬 빠름!)
INSERT INTO users (email, name, age) VALUES
    ('lee@test.com', '이영희', 30),
    ('park@test.com', '박민수', 22),
    ('choi@test.com', '최지원', 28);
```

### SELECT로 삽입

```sql
-- 다른 테이블에서 복사
INSERT INTO users_backup (email, name, age)
SELECT email, name, age
FROM users
WHERE created_at < '2024-01-01';

-- 집계 결과 삽입
INSERT INTO daily_stats (date, total_orders, total_revenue)
SELECT
    CURDATE(),
    COUNT(*),
    SUM(total_price)
FROM orders
WHERE DATE(created_at) = CURDATE();
```

### 자동 생성 값 처리

```sql
-- AUTO_INCREMENT ID 얻기
INSERT INTO orders (user_id, total_price)
VALUES (1, 50000);

SELECT LAST_INSERT_ID();  -- 방금 생성된 ID

-- Python에서
cursor.execute("INSERT INTO orders ...")
order_id = cursor.lastrowid
```

### 트랜잭션과 함께

```sql
START TRANSACTION;

INSERT INTO orders (user_id, total_price)
VALUES (1, 50000);

SET @order_id = LAST_INSERT_ID();

INSERT INTO order_items (order_id, product_id, quantity)
VALUES (@order_id, 100, 2);

COMMIT;
```"""
            },
            {
                "type": "common-mistake",
                "title": "⚠️ 흔한 실수",
                "content": """### 1. 컬럼 순서 불일치

```sql
-- ❌ 컬럼 개수/순서 불일치
INSERT INTO users (name, email, age)
VALUES ('kim@test.com', '김철수');
-- Error: Column count doesn't match

-- ✅ 정확히 매칭
INSERT INTO users (email, name, age)
VALUES ('kim@test.com', '김철수', 25);
```

### 2. 문자열 이스케이프

```sql
-- ❌ 작은따옴표 오류
INSERT INTO products (name) VALUES ('Kim's Shop');

-- ✅ 이스케이프
INSERT INTO products (name) VALUES ('Kim''s Shop');
-- 또는
INSERT INTO products (name) VALUES ("Kim's Shop");
```

### 3. 대량 삽입 시 성능

```sql
-- ❌ 느림: 건건이 INSERT
for item in items:
    INSERT INTO table VALUES (item);

-- ✅ 빠름: 배치 INSERT (1000건씩)
INSERT INTO table VALUES
    (item1), (item2), ... (item1000);
```"""
            }
        ]
    },

    "02_SQL/insert-update-delete": {
        "title": "UPDATE/DELETE 완벽 가이드",
        "description": "데이터 수정과 삭제를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 UPDATE와 DELETE",
                "content": """## 🔥 한 줄 요약
> **UPDATE = 수정, DELETE = 삭제** - 가장 위험한 SQL!

---

## 💡 왜 위험한가?

### 실제 사고:
```
🔴 2017년 GitLab 사고
- 실수로 프로덕션 DB DELETE
- 300GB 데이터 손실
- 18시간 서비스 중단

🔴 2023년 모 스타트업
- WHERE 없이 UPDATE 실행
- 전체 회원 비밀번호 초기화
- 10만 명 로그인 불가
```

---

## 🎯 핵심 문법

### UPDATE 기본

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;

-- ⚠️ WHERE 없으면 전체 수정!
```

### DELETE 기본

```sql
DELETE FROM table_name
WHERE condition;

-- ⚠️ WHERE 없으면 전체 삭제!
```

### 안전한 실행 순서

```sql
-- 1단계: SELECT로 대상 확인
SELECT * FROM users WHERE status = 'inactive';
-- 결과: 100건 확인

-- 2단계: 트랜잭션 시작
START TRANSACTION;

-- 3단계: UPDATE/DELETE 실행
DELETE FROM users WHERE status = 'inactive';

-- 4단계: 결과 확인
SELECT * FROM users WHERE status = 'inactive';
-- 결과: 0건 확인 (정상)

-- 5단계: 확정 또는 취소
COMMIT;    -- 확정
-- ROLLBACK;  -- 취소
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 UPDATE/DELETE",
                "content": """### UPDATE 예제

```sql
-- 단일 컬럼 수정
UPDATE users
SET status = 'inactive'
WHERE last_login < '2024-01-01';

-- 다중 컬럼 수정
UPDATE products
SET
    price = price * 1.1,  -- 10% 인상
    updated_at = NOW()
WHERE category = '전자기기';

-- CASE 문으로 조건별 수정
UPDATE users
SET membership = CASE
    WHEN total_purchase >= 1000000 THEN 'VIP'
    WHEN total_purchase >= 500000 THEN 'Gold'
    ELSE 'Normal'
END;

-- JOIN UPDATE
UPDATE orders o
JOIN users u ON o.user_id = u.id
SET o.shipping_address = u.default_address
WHERE o.shipping_address IS NULL;
```

### DELETE 예제

```sql
-- 조건 삭제
DELETE FROM logs
WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- LIMIT으로 안전하게
DELETE FROM old_data
WHERE created_at < '2020-01-01'
LIMIT 10000;  -- 1만건씩 삭제

-- JOIN DELETE
DELETE o
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'deleted';
```

### Soft Delete (권장)

```sql
-- ❌ 물리 삭제 (복구 불가)
DELETE FROM users WHERE id = 1;

-- ✅ 논리 삭제 (복구 가능)
UPDATE users
SET
    deleted_at = NOW(),
    status = 'deleted'
WHERE id = 1;

-- 조회 시 삭제된 데이터 제외
SELECT * FROM users WHERE deleted_at IS NULL;
```"""
            },
            {
                "type": "tip",
                "title": "💡 안전 수칙",
                "content": """### UPDATE/DELETE 체크리스트

```
□ WHERE 절 있는지 확인
□ SELECT로 대상 먼저 확인
□ 트랜잭션 사용
□ 백업 확인
□ 실행 전 동료 검토 (프로덕션)
```

### MySQL Safe Mode

```sql
-- Safe Mode 활성화
SET SQL_SAFE_UPDATES = 1;

-- 이제 WHERE 없이 실행 불가
UPDATE users SET status = 'inactive';
-- Error: You are using safe update mode

-- KEY 조건 필수
UPDATE users SET status = 'inactive' WHERE id = 1;
-- OK
```

### 실무 규칙

```
1. 프로덕션 직접 수정 금지
2. 스테이징에서 먼저 테스트
3. DBA 또는 시니어 검토 후 실행
4. 실행 로그 남기기
5. 롤백 스크립트 준비
```"""
            }
        ]
    },

    "02_SQL/where-clause": {
        "title": "WHERE 절 마스터",
        "description": "조건 필터링의 모든 것을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 WHERE 절 완벽 정복",
                "content": """## 🔥 한 줄 요약
> **원하는 데이터만 걸러내는 필터** - SQL의 핵심!

---

## 🎯 연산자 총정리

### 비교 연산자

```sql
=     같다
<>    다르다 (또는 !=)
>     크다
<     작다
>=    크거나 같다
<=    작거나 같다
```

### 범위 연산자

```sql
-- BETWEEN: 범위 (양 끝 포함)
WHERE age BETWEEN 20 AND 30
-- = WHERE age >= 20 AND age <= 30

-- NOT BETWEEN
WHERE age NOT BETWEEN 20 AND 30
```

### 목록 연산자

```sql
-- IN: 목록 중 하나
WHERE status IN ('active', 'pending', 'approved')

-- NOT IN
WHERE status NOT IN ('deleted', 'banned')
```

### 패턴 연산자

```sql
-- LIKE: 패턴 매칭
%   0개 이상의 문자
_   정확히 1개의 문자

LIKE 'kim%'      -- kim으로 시작
LIKE '%kim'      -- kim으로 끝
LIKE '%kim%'     -- kim 포함
LIKE 'kim_'      -- kim + 1글자
LIKE '___'       -- 정확히 3글자
```

### NULL 연산자

```sql
-- IS NULL: NULL인 것
WHERE phone IS NULL

-- IS NOT NULL: NULL 아닌 것
WHERE phone IS NOT NULL

-- ⚠️ = NULL은 항상 FALSE!
WHERE phone = NULL  -- 작동 안 함!
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 WHERE",
                "content": """### 논리 연산자 조합

```sql
-- AND: 모든 조건 만족
SELECT * FROM users
WHERE age >= 20
  AND status = 'active'
  AND email LIKE '%@gmail.com';

-- OR: 하나라도 만족
SELECT * FROM products
WHERE category = '전자기기'
   OR category = '가전제품';

-- NOT: 부정
SELECT * FROM users
WHERE NOT (status = 'deleted' OR status = 'banned');

-- 복합 조건 (괄호 중요!)
SELECT * FROM orders
WHERE (status = 'pending' OR status = 'processing')
  AND total_price > 50000
  AND created_at >= '2024-01-01';
```

### 날짜 조건

```sql
-- 특정 날짜
WHERE DATE(created_at) = '2024-01-15'

-- 날짜 범위
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01'

-- 최근 7일
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)

-- 이번 달
WHERE YEAR(created_at) = YEAR(NOW())
  AND MONTH(created_at) = MONTH(NOW())
```

### 서브쿼리와 함께

```sql
-- IN + 서브쿼리
SELECT * FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE total_price > 100000
);

-- EXISTS
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
);
```"""
            },
            {
                "type": "tip",
                "title": "💡 성능 팁",
                "content": """### 인덱스를 타는 조건

```sql
-- ✅ 인덱스 사용
WHERE id = 1
WHERE email = 'test@test.com'
WHERE created_at >= '2024-01-01'
WHERE name LIKE 'kim%'

-- ❌ 인덱스 못 씀
WHERE YEAR(created_at) = 2024  -- 함수 사용
WHERE name LIKE '%kim%'         -- 앞에 %
WHERE age + 1 = 25              -- 연산
WHERE UPPER(email) = 'TEST'     -- 함수 사용
```

### OR vs IN

```sql
-- ❌ 느림
WHERE status = 'a' OR status = 'b' OR status = 'c'

-- ✅ 빠름
WHERE status IN ('a', 'b', 'c')
```

### NOT IN 주의

```sql
-- ⚠️ NULL이 포함되면 결과 없음!
SELECT * FROM users
WHERE id NOT IN (1, 2, NULL);  -- 항상 0건!

-- ✅ NOT EXISTS 사용
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM blacklist b
    WHERE b.user_id = u.id
);
```"""
            }
        ]
    },

    "02_SQL/ddl": {
        "title": "DDL - 테이블 생성/수정/삭제",
        "description": "데이터베이스 구조를 정의하는 DDL을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 DDL이란?",
                "content": """## 🔥 한 줄 요약
> **DB 구조를 정의하는 SQL** - CREATE, ALTER, DROP

---

## 💡 왜 배워야 하나?

### 실무 필수:
```
🏗️ 새 기능 개발 → CREATE TABLE
📝 요구사항 변경 → ALTER TABLE
🗑️ 레거시 정리 → DROP TABLE

→ DDL 모르면 스키마 수정 불가
```

---

## 🎯 핵심 문법

### CREATE TABLE

```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...
    table_constraints
);
```

### 주요 데이터 타입

```
📊 숫자
├── INT: 정수 (-21억 ~ 21억)
├── BIGINT: 큰 정수
├── DECIMAL(10,2): 정확한 소수 (금액용)
└── FLOAT, DOUBLE: 부동소수점

📝 문자
├── VARCHAR(n): 가변 길이 (최대 n자)
├── CHAR(n): 고정 길이 (정확히 n자)
└── TEXT: 긴 텍스트

📅 날짜/시간
├── DATE: 날짜 (2024-01-15)
├── TIME: 시간 (14:30:00)
├── DATETIME: 날짜+시간
└── TIMESTAMP: UTC 기준 시간

🔘 기타
├── BOOLEAN: true/false
├── ENUM: 열거형
├── JSON: JSON 데이터
└── BLOB: 바이너리 데이터
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 DDL",
                "content": """### CREATE TABLE 예제

```sql
-- 회원 테이블
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    status ENUM('active', 'inactive', 'deleted') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_status_created (status, created_at)
);

-- 주문 테이블 (FK 포함)
CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

### ALTER TABLE 예제

```sql
-- 컬럼 추가
ALTER TABLE users ADD COLUMN birth_date DATE;

-- 컬럼 수정
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);

-- 컬럼 이름 변경
ALTER TABLE users CHANGE COLUMN phone mobile VARCHAR(30);

-- 컬럼 삭제
ALTER TABLE users DROP COLUMN birth_date;

-- 인덱스 추가
ALTER TABLE users ADD INDEX idx_name (name);

-- 인덱스 삭제
ALTER TABLE users DROP INDEX idx_name;

-- 외래키 추가
ALTER TABLE orders
ADD FOREIGN KEY (user_id) REFERENCES users(id);
```

### DROP 명령어

```sql
-- 테이블 삭제 (주의!)
DROP TABLE users;

-- 테이블 존재하면 삭제
DROP TABLE IF EXISTS users;

-- 데이터만 삭제 (구조 유지)
TRUNCATE TABLE logs;

-- 데이터베이스 삭제
DROP DATABASE test_db;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 컬럼 타입 선택 가이드

```
ID → BIGINT (INT 한계 21억)
금액 → DECIMAL (절대 FLOAT 사용 금지)
상태 → ENUM 또는 VARCHAR
날짜 → TIMESTAMP (UTC 자동 변환)
긴 텍스트 → TEXT
짧은 텍스트 → VARCHAR
```

### DDL 실행 주의사항

```
⚠️ 프로덕션 DDL은 위험!
├── 락 발생 가능
├── 대용량 테이블은 시간 오래 걸림
└── 서비스 영향 가능

✅ 안전한 방법
├── 점검 시간에 실행
├── pt-online-schema-change 사용
└── 테스트 환경에서 먼저 검증
```

### 마이그레이션 도구 활용

```
Flask: Flask-Migrate (Alembic)
Django: Django Migrations
Node.js: Knex, Prisma
Java: Flyway, Liquibase

→ DDL 직접 실행보다 마이그레이션 도구 사용 권장
```"""
            }
        ]
    },

    "02_SQL/group-by": {
        "title": "GROUP BY 완벽 가이드",
        "description": "데이터 그룹화와 집계를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 GROUP BY란?",
                "content": """## 🔥 한 줄 요약
> **같은 값끼리 묶어서 집계** - "카테고리별 매출", "월별 가입자"

---

## 💡 왜 배워야 하나?

### 실무 필수:
```
📊 "이번 달 일별 매출 보여줘"
📈 "카테고리별 상품 개수는?"
👥 "지역별 회원 수 통계"

→ GROUP BY 없이는 리포트 불가능
```

---

## 🎯 핵심 개념

### 기본 문법

```sql
SELECT column1, AGG_FUNC(column2)
FROM table
WHERE condition
GROUP BY column1
HAVING agg_condition
ORDER BY column1;
```

### 집계 함수

```sql
COUNT(*)      -- 행 개수
COUNT(column) -- NULL 제외 개수
SUM(column)   -- 합계
AVG(column)   -- 평균
MAX(column)   -- 최대값
MIN(column)   -- 최소값
GROUP_CONCAT(column) -- 문자열 연결 (MySQL)
```

### 실행 순서

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

1️⃣ FROM: 테이블 선택
2️⃣ WHERE: 그룹화 전 필터링
3️⃣ GROUP BY: 그룹화
4️⃣ HAVING: 그룹화 후 필터링
5️⃣ SELECT: 출력
6️⃣ ORDER BY: 정렬
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 GROUP BY",
                "content": """### 기본 집계

```sql
-- 카테고리별 상품 수
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;

-- 결과:
-- 전자기기 | 150
-- 의류     | 230
-- 식품     | 80

-- 카테고리별 평균 가격
SELECT
    category,
    COUNT(*) AS cnt,
    AVG(price) AS avg_price,
    MAX(price) AS max_price,
    MIN(price) AS min_price
FROM products
GROUP BY category;
```

### 날짜별 집계

```sql
-- 일별 주문 통계
SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_price) AS daily_revenue
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at)
ORDER BY order_date;

-- 월별 가입자 수
SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS new_users
FROM users
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month;
```

### 다중 컬럼 GROUP BY

```sql
-- 카테고리 + 상태별 집계
SELECT
    category,
    status,
    COUNT(*) AS cnt
FROM products
GROUP BY category, status
ORDER BY category, status;

-- 결과:
-- 전자기기 | active   | 100
-- 전자기기 | inactive | 50
-- 의류     | active   | 200
```

### HAVING으로 그룹 필터링

```sql
-- 주문 5회 이상인 고객
SELECT
    user_id,
    COUNT(*) AS order_count,
    SUM(total_price) AS total_spent
FROM orders
GROUP BY user_id
HAVING COUNT(*) >= 5
ORDER BY total_spent DESC;

-- 평균 가격 10만원 이상인 카테고리
SELECT
    category,
    AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) >= 100000;
```"""
            },
            {
                "type": "common-mistake",
                "title": "⚠️ 흔한 실수",
                "content": """### 1. SELECT에 비집계 컬럼

```sql
-- ❌ 에러: name이 GROUP BY에 없음
SELECT user_id, name, COUNT(*)
FROM orders
GROUP BY user_id;

-- ✅ GROUP BY에 포함하거나
SELECT user_id, name, COUNT(*)
FROM orders
GROUP BY user_id, name;

-- ✅ 집계 함수 사용
SELECT user_id, MAX(name), COUNT(*)
FROM orders
GROUP BY user_id;
```

### 2. WHERE vs HAVING

```sql
-- ❌ WHERE에서 집계 함수 사용 불가
SELECT user_id, COUNT(*)
FROM orders
WHERE COUNT(*) >= 5  -- 에러!
GROUP BY user_id;

-- ✅ HAVING 사용
SELECT user_id, COUNT(*)
FROM orders
GROUP BY user_id
HAVING COUNT(*) >= 5;
```

### 3. 집계 전후 필터링 혼동

```sql
-- WHERE: 그룹화 전 필터링 (개별 행)
-- HAVING: 그룹화 후 필터링 (그룹)

SELECT category, COUNT(*)
FROM products
WHERE price > 10000      -- 1만원 이상 상품만 대상
GROUP BY category
HAVING COUNT(*) >= 10;   -- 그 중 10개 이상인 카테고리만
```"""
            }
        ]
    },

    "02_SQL/aggregate-function": {
        "title": "집계 함수 마스터",
        "description": "COUNT, SUM, AVG 등 집계 함수를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 집계 함수 총정리",
                "content": """## 🔥 한 줄 요약
> **여러 행을 하나의 값으로 계산** - COUNT, SUM, AVG, MAX, MIN

---

## 🎯 주요 집계 함수

### COUNT

```sql
COUNT(*)       -- 전체 행 수 (NULL 포함)
COUNT(column)  -- NULL 제외 개수
COUNT(DISTINCT column) -- 중복 제외 개수
```

### SUM / AVG

```sql
SUM(column)    -- 합계 (NULL 무시)
AVG(column)    -- 평균 (NULL 무시)
```

### MAX / MIN

```sql
MAX(column)    -- 최대값
MIN(column)    -- 최소값
-- 숫자, 문자, 날짜 모두 가능
```

### 기타 함수

```sql
-- MySQL
GROUP_CONCAT(column)           -- 값들을 문자열로 연결
GROUP_CONCAT(DISTINCT column)  -- 중복 제외 연결

-- 표준 SQL
STDDEV(column)    -- 표준편차
VARIANCE(column)  -- 분산
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 집계",
                "content": """### 기본 집계

```sql
-- 전체 통계
SELECT
    COUNT(*) AS 전체주문수,
    COUNT(DISTINCT user_id) AS 주문고객수,
    SUM(total_price) AS 총매출,
    AVG(total_price) AS 평균주문액,
    MAX(total_price) AS 최대주문액,
    MIN(total_price) AS 최소주문액
FROM orders
WHERE status = 'completed';
```

### 조건부 집계

```sql
-- CASE와 함께 (피벗 테이블)
SELECT
    DATE(created_at) AS date,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN status = 'completed' THEN total_price ELSE 0 END) AS revenue
FROM orders
GROUP BY DATE(created_at);

-- NULL 처리
SELECT
    AVG(COALESCE(rating, 0)) AS avg_rating,  -- NULL을 0으로
    AVG(rating) AS avg_rating_no_null        -- NULL 제외
FROM reviews;
```

### GROUP_CONCAT 활용

```sql
-- 카테고리별 상품명 나열
SELECT
    category,
    GROUP_CONCAT(name SEPARATOR ', ') AS products
FROM products
GROUP BY category;

-- 결과: 전자기기 | 아이폰, 갤럭시, 맥북

-- 정렬해서 연결
SELECT
    user_id,
    GROUP_CONCAT(
        product_name
        ORDER BY created_at DESC
        SEPARATOR ' → '
    ) AS purchase_history
FROM orders
GROUP BY user_id;
```

### 윈도우 함수 (고급)

```sql
-- 전체 합계와 개별 값 동시에
SELECT
    id,
    total_price,
    SUM(total_price) OVER() AS grand_total,
    total_price * 100.0 / SUM(total_price) OVER() AS percentage
FROM orders;

-- 누적 합계
SELECT
    DATE(created_at) AS date,
    SUM(total_price) AS daily_revenue,
    SUM(SUM(total_price)) OVER(ORDER BY DATE(created_at)) AS cumulative
FROM orders
GROUP BY DATE(created_at);
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### NULL 주의사항

```sql
-- COUNT(*)는 NULL 포함
-- COUNT(column)은 NULL 제외
-- SUM, AVG는 NULL 무시

-- 예시
-- data: [10, 20, NULL, 30]
COUNT(*)      = 4
COUNT(value)  = 3
SUM(value)    = 60
AVG(value)    = 20  -- 60/3, NULL 제외
```

### 성능 팁

```sql
-- ❌ 느림: COUNT(DISTINCT)는 비용 큼
SELECT COUNT(DISTINCT user_id) FROM orders;

-- ✅ 빠름: 근사값으로 대체 (대용량)
SELECT APPROX_COUNT_DISTINCT(user_id) FROM orders;  -- BigQuery
```

### 소수점 처리

```sql
-- 정확한 계산
SELECT ROUND(AVG(price), 2) AS avg_price;

-- 금액 계산 시
SELECT CAST(SUM(price) AS DECIMAL(12,2));
```"""
            }
        ]
    },

    "02_SQL/subquery": {
        "title": "서브쿼리 마스터",
        "description": "쿼리 안의 쿼리, 서브쿼리를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 서브쿼리란?",
                "content": """## 🔥 한 줄 요약
> **쿼리 안에 또 다른 쿼리** - 복잡한 조건을 단계별로 해결

---

## 💡 왜 배워야 하나?

### 실무 예시:
```
📊 "평균보다 비싼 상품 목록"
→ 평균 가격 구하고 → 그 값보다 큰 것 조회
→ 서브쿼리 필요!

👥 "주문한 적 있는 고객만"
→ 주문 테이블에서 user_id 목록 → users에서 조회
→ 서브쿼리 필요!
```

---

## 🎯 서브쿼리 유형

### 위치에 따른 분류

```sql
-- 1. SELECT 절 (스칼라 서브쿼리)
SELECT name,
       (SELECT AVG(price) FROM products) AS avg_price
FROM products;

-- 2. FROM 절 (인라인 뷰)
SELECT * FROM (
    SELECT user_id, COUNT(*) AS cnt
    FROM orders
    GROUP BY user_id
) AS order_stats
WHERE cnt >= 5;

-- 3. WHERE 절 (가장 흔함)
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

### 반환값에 따른 분류

```sql
-- 단일 값 (스칼라)
WHERE price > (SELECT AVG(price) FROM products)

-- 단일 열 (리스트)
WHERE user_id IN (SELECT user_id FROM vip_users)

-- 다중 열
WHERE (user_id, product_id) IN (
    SELECT user_id, product_id FROM wishlist
)

-- 테이블 (FROM절)
FROM (SELECT ...) AS derived_table
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 서브쿼리",
                "content": """### WHERE 절 서브쿼리

```sql
-- 평균보다 비싼 상품
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 주문한 적 있는 고객
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- 주문한 적 없는 고객
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM orders);
```

### EXISTS / NOT EXISTS

```sql
-- EXISTS: 존재 여부 확인 (효율적)
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
);

-- NOT EXISTS
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
);
```

### 상관 서브쿼리

```sql
-- 각 카테고리의 최고가 상품
SELECT * FROM products p1
WHERE price = (
    SELECT MAX(price)
    FROM products p2
    WHERE p2.category = p1.category
);

-- 각 고객의 최근 주문
SELECT * FROM orders o1
WHERE created_at = (
    SELECT MAX(created_at)
    FROM orders o2
    WHERE o2.user_id = o1.user_id
);
```

### FROM 절 서브쿼리 (Derived Table)

```sql
-- 주문 5회 이상 고객의 총 매출
SELECT
    u.name,
    stats.order_count,
    stats.total_spent
FROM users u
JOIN (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(total_price) AS total_spent
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) >= 5
) AS stats ON u.id = stats.user_id;
```"""
            },
            {
                "type": "tip",
                "title": "💡 서브쿼리 vs JOIN",
                "content": """### 언제 무엇을 쓸까?

```sql
-- 서브쿼리가 나은 경우
-- 1. 존재 여부만 확인
WHERE EXISTS (SELECT 1 FROM ...)

-- 2. 집계값과 비교
WHERE price > (SELECT AVG(price) FROM ...)

-- JOIN이 나은 경우
-- 1. 여러 테이블 데이터 함께 출력
-- 2. 대용량 데이터 (보통 더 빠름)
```

### 성능 비교

```sql
-- ❌ 느림: IN + 서브쿼리 (대용량)
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE status = 'vip');

-- ✅ 빠름: JOIN
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'vip';

-- ✅ EXISTS도 효율적
SELECT * FROM orders o
WHERE EXISTS (
    SELECT 1 FROM users u
    WHERE u.id = o.user_id AND u.status = 'vip'
);
```

### NOT IN 주의!

```sql
-- ⚠️ NULL이 있으면 결과 없음!
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM blacklist);
-- blacklist에 NULL이 있으면 항상 0건

-- ✅ NOT EXISTS 사용
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM blacklist b WHERE b.user_id = u.id
);
```"""
            }
        ]
    },

    "02_SQL/case-when": {
        "title": "CASE WHEN 조건문",
        "description": "SQL에서 조건 분기를 처리하는 방법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 CASE WHEN이란?",
                "content": """## 🔥 한 줄 요약
> **SQL의 if-else문** - 조건에 따라 다른 값 반환

---

## 💡 왜 배워야 하나?

### 실무 필수:
```
📊 "등급별로 다른 할인율 적용"
📈 "상태 코드를 한글로 변환"
👥 "연령대별 그룹 분류"

→ CASE 없이는 조건 분기 불가
```

---

## 🎯 기본 문법

### 단순 CASE

```sql
CASE column
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE default_result
END
```

### 검색 CASE (더 유연)

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

### 실제 예시

```sql
-- 상태 코드 → 한글
SELECT
    id,
    status,
    CASE status
        WHEN 'pending' THEN '대기중'
        WHEN 'processing' THEN '처리중'
        WHEN 'completed' THEN '완료'
        WHEN 'cancelled' THEN '취소'
        ELSE '알수없음'
    END AS status_korean
FROM orders;

-- 가격대 분류
SELECT
    name,
    price,
    CASE
        WHEN price < 10000 THEN '저가'
        WHEN price < 50000 THEN '중가'
        WHEN price < 100000 THEN '고가'
        ELSE '프리미엄'
    END AS price_tier
FROM products;
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 CASE WHEN",
                "content": """### 조건부 계산

```sql
-- 등급별 할인 적용
SELECT
    name,
    price,
    membership,
    CASE membership
        WHEN 'VIP' THEN price * 0.8     -- 20% 할인
        WHEN 'Gold' THEN price * 0.9    -- 10% 할인
        ELSE price
    END AS final_price
FROM products p
JOIN users u ON p.seller_id = u.id;

-- 배송비 계산
SELECT
    id,
    total_price,
    CASE
        WHEN total_price >= 50000 THEN 0
        WHEN total_price >= 30000 THEN 2500
        ELSE 3000
    END AS shipping_fee
FROM orders;
```

### 집계와 함께 (피벗 테이블)

```sql
-- 상태별 집계 (행 → 열)
SELECT
    DATE(created_at) AS date,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending
FROM orders
GROUP BY DATE(created_at);

-- 결과:
-- date       | total | completed | cancelled | pending
-- 2024-01-15 | 100   | 80        | 10        | 10

-- 월별 상품 카테고리 매출
SELECT
    DATE_FORMAT(o.created_at, '%Y-%m') AS month,
    SUM(CASE WHEN p.category = '전자기기' THEN oi.price ELSE 0 END) AS electronics,
    SUM(CASE WHEN p.category = '의류' THEN oi.price ELSE 0 END) AS clothing,
    SUM(CASE WHEN p.category = '식품' THEN oi.price ELSE 0 END) AS food
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY DATE_FORMAT(o.created_at, '%Y-%m');
```

### UPDATE/WHERE에서 활용

```sql
-- 조건부 UPDATE
UPDATE users
SET membership = CASE
    WHEN total_purchase >= 1000000 THEN 'VIP'
    WHEN total_purchase >= 500000 THEN 'Gold'
    ELSE 'Normal'
END;

-- ORDER BY에서 커스텀 정렬
SELECT * FROM orders
ORDER BY CASE status
    WHEN 'pending' THEN 1
    WHEN 'processing' THEN 2
    WHEN 'shipped' THEN 3
    WHEN 'delivered' THEN 4
    ELSE 5
END;
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### CASE vs IF

```sql
-- MySQL IF 함수 (단순 조건)
SELECT IF(price > 10000, '비쌈', '저렴') AS price_label;

-- CASE (복잡한 조건)
SELECT CASE
    WHEN price < 10000 THEN '저가'
    WHEN price < 50000 THEN '중가'
    ELSE '고가'
END AS price_tier;

-- IF는 2가지 분기만 가능
-- CASE는 여러 분기 가능
```

### NULL 처리

```sql
-- CASE에서 NULL 체크
SELECT
    name,
    CASE
        WHEN phone IS NULL THEN '미등록'
        ELSE phone
    END AS phone
FROM users;

-- COALESCE/IFNULL이 더 간단
SELECT
    name,
    COALESCE(phone, '미등록') AS phone
FROM users;
```

### ELSE 생략 주의

```sql
-- ELSE 없으면 NULL 반환
SELECT CASE status
    WHEN 'active' THEN '활성'
    WHEN 'inactive' THEN '비활성'
    -- status가 'deleted'면? → NULL
END AS status_korean;

-- 항상 ELSE 넣는 것 권장
```"""
            }
        ]
    },

    "02_SQL/string-function": {
        "title": "문자열 함수",
        "description": "SQL에서 문자열을 다루는 함수들을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 문자열 함수 총정리",
                "content": """## 🔥 한 줄 요약
> **문자열 조작의 모든 것** - 자르고, 붙이고, 변환하고

---

## 🎯 주요 함수

### 길이 / 변환

```sql
LENGTH(str)      -- 바이트 길이
CHAR_LENGTH(str) -- 문자 길이 (한글도 1)
UPPER(str)       -- 대문자로
LOWER(str)       -- 소문자로
```

### 추출 / 자르기

```sql
LEFT(str, n)     -- 왼쪽에서 n자
RIGHT(str, n)    -- 오른쪽에서 n자
SUBSTRING(str, start, length)  -- 부분 문자열
TRIM(str)        -- 양쪽 공백 제거
LTRIM(str)       -- 왼쪽 공백 제거
RTRIM(str)       -- 오른쪽 공백 제거
```

### 연결 / 치환

```sql
CONCAT(str1, str2, ...)  -- 문자열 연결
CONCAT_WS(sep, str1, str2, ...) -- 구분자로 연결
REPLACE(str, from, to)   -- 문자열 치환
```

### 검색 / 포맷

```sql
LOCATE(substr, str)  -- 위치 찾기 (1부터)
INSTR(str, substr)   -- 위치 찾기
LPAD(str, len, pad)  -- 왼쪽 채우기
RPAD(str, len, pad)  -- 오른쪽 채우기
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 문자열 함수",
                "content": """### 기본 사용

```sql
-- 이름 처리
SELECT
    name,
    UPPER(name) AS upper_name,
    LOWER(name) AS lower_name,
    CHAR_LENGTH(name) AS name_length
FROM users;

-- 이메일에서 도메인 추출
SELECT
    email,
    SUBSTRING(email, LOCATE('@', email) + 1) AS domain
FROM users;
-- kim@gmail.com → gmail.com

-- 전화번호 포맷팅
SELECT
    phone,
    CONCAT(
        LEFT(phone, 3), '-',
        SUBSTRING(phone, 4, 4), '-',
        RIGHT(phone, 4)
    ) AS formatted_phone
FROM users;
-- 01012345678 → 010-1234-5678
```

### 데이터 정제

```sql
-- 공백 제거
SELECT TRIM(name) FROM users;

-- 특수문자 제거
SELECT REPLACE(REPLACE(phone, '-', ''), ' ', '')
FROM users;

-- 마스킹 처리
SELECT
    name,
    CONCAT(LEFT(email, 3), '****@',
           SUBSTRING(email, LOCATE('@', email) + 1)) AS masked_email
FROM users;
-- kim@gmail.com → kim****@gmail.com

-- 주민번호 마스킹
SELECT CONCAT(LEFT(ssn, 6), '-*******') AS masked_ssn
FROM users;
-- 900101-1234567 → 900101-*******
```

### 검색과 조건

```sql
-- 특정 문자 포함 여부
SELECT * FROM users
WHERE LOCATE('@gmail', email) > 0;

-- 특정 패턴으로 시작
SELECT * FROM users
WHERE LEFT(phone, 3) = '010';

-- 이름 검색 (대소문자 무시)
SELECT * FROM products
WHERE LOWER(name) LIKE LOWER('%iphone%');
```

### 숫자 포맷

```sql
-- 천단위 콤마
SELECT FORMAT(price, 0) AS formatted_price
FROM products;
-- 1234567 → 1,234,567

-- 금액 표시
SELECT CONCAT('₩', FORMAT(price, 0)) AS price_display
FROM products;
-- 50000 → ₩50,000

-- 자릿수 맞추기
SELECT LPAD(id, 6, '0') AS order_number
FROM orders;
-- 123 → 000123
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 인덱스와 함수

```sql
-- ❌ 인덱스 못 씀
WHERE LOWER(email) = 'test@test.com'
WHERE LEFT(phone, 3) = '010'

-- ✅ 인덱스 사용
WHERE email = 'test@test.com'
WHERE phone LIKE '010%'
```

### CONCAT NULL 주의

```sql
-- NULL이 있으면 전체가 NULL
SELECT CONCAT('Hello', NULL, 'World');
-- 결과: NULL

-- CONCAT_WS는 NULL 무시
SELECT CONCAT_WS(' ', 'Hello', NULL, 'World');
-- 결과: Hello World

-- COALESCE로 NULL 처리
SELECT CONCAT(first_name, ' ', COALESCE(middle_name, ''), last_name);
```

### DB별 차이

```
MySQL: CONCAT, SUBSTRING
PostgreSQL: ||로 연결, SUBSTRING
Oracle: ||로 연결, SUBSTR
SQL Server: +로 연결, SUBSTRING
```"""
            }
        ]
    },

    "02_SQL/date-function": {
        "title": "날짜 함수",
        "description": "SQL에서 날짜/시간을 다루는 함수들을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 날짜 함수 총정리",
                "content": """## 🔥 한 줄 요약
> **날짜/시간 조작의 모든 것** - 추출, 계산, 포맷팅

---

## 💡 왜 배워야 하나?

### 실무 필수:
```
📊 "이번 달 매출" → 날짜 범위 조건
📈 "월별 통계" → 날짜 그룹화
👥 "7일 이내 가입자" → 날짜 계산
```

---

## 🎯 주요 함수

### 현재 날짜/시간

```sql
NOW()              -- 현재 날짜+시간 (2024-01-15 14:30:00)
CURDATE()          -- 현재 날짜 (2024-01-15)
CURTIME()          -- 현재 시간 (14:30:00)
CURRENT_TIMESTAMP  -- NOW()와 동일
```

### 날짜 추출

```sql
YEAR(date)         -- 연도 (2024)
MONTH(date)        -- 월 (1~12)
DAY(date)          -- 일 (1~31)
HOUR(time)         -- 시 (0~23)
MINUTE(time)       -- 분 (0~59)
SECOND(time)       -- 초 (0~59)
DAYOFWEEK(date)    -- 요일 (1=일, 7=토)
WEEKDAY(date)      -- 요일 (0=월, 6=일)
```

### 날짜 연산

```sql
DATE_ADD(date, INTERVAL n unit)  -- 더하기
DATE_SUB(date, INTERVAL n unit)  -- 빼기
DATEDIFF(date1, date2)           -- 일수 차이
TIMESTAMPDIFF(unit, dt1, dt2)    -- 단위별 차이
```

### 포맷팅

```sql
DATE_FORMAT(date, format)  -- 날짜 → 문자열
STR_TO_DATE(str, format)   -- 문자열 → 날짜
```"""
            },
            {
                "type": "code",
                "title": "💻 실전 날짜 함수",
                "content": """### 날짜 추출

```sql
-- 연/월/일 추출
SELECT
    created_at,
    YEAR(created_at) AS year,
    MONTH(created_at) AS month,
    DAY(created_at) AS day,
    DAYNAME(created_at) AS day_name
FROM orders;

-- 시간 추출
SELECT
    created_at,
    HOUR(created_at) AS hour,
    DATE_FORMAT(created_at, '%p') AS am_pm  -- AM/PM
FROM orders;
```

### 날짜 연산

```sql
-- 7일 전 ~ 오늘
SELECT * FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 다음 달 1일
SELECT DATE_ADD(
    LAST_DAY(NOW()),
    INTERVAL 1 DAY
) AS next_month_first;

-- 가입 후 경과일
SELECT
    name,
    created_at,
    DATEDIFF(NOW(), created_at) AS days_since_join
FROM users;

-- 나이 계산
SELECT
    name,
    birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
FROM users;
```

### 기간 조회

```sql
-- 이번 달
SELECT * FROM orders
WHERE YEAR(created_at) = YEAR(NOW())
  AND MONTH(created_at) = MONTH(NOW());

-- 더 효율적인 방법
SELECT * FROM orders
WHERE created_at >= DATE_FORMAT(NOW(), '%Y-%m-01')
  AND created_at < DATE_ADD(DATE_FORMAT(NOW(), '%Y-%m-01'), INTERVAL 1 MONTH);

-- 최근 30일 일별 통계
SELECT
    DATE(created_at) AS date,
    COUNT(*) AS order_count
FROM orders
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date;
```

### 포맷팅

```sql
-- 다양한 포맷
SELECT
    created_at,
    DATE_FORMAT(created_at, '%Y-%m-%d') AS date_only,
    DATE_FORMAT(created_at, '%Y년 %m월 %d일') AS korean,
    DATE_FORMAT(created_at, '%H:%i:%s') AS time_only,
    DATE_FORMAT(created_at, '%Y-%m') AS year_month
FROM orders;

-- 문자열 → 날짜
SELECT STR_TO_DATE('2024-01-15', '%Y-%m-%d');
SELECT STR_TO_DATE('15/01/2024', '%d/%m/%Y');
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 인덱스와 날짜 함수

```sql
-- ❌ 인덱스 못 씀 (함수 사용)
WHERE YEAR(created_at) = 2024
WHERE DATE(created_at) = '2024-01-15'

-- ✅ 인덱스 사용 (범위 조건)
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
WHERE created_at >= '2024-01-15' AND created_at < '2024-01-16'
```

### 타임존 주의

```sql
-- TIMESTAMP: 서버 타임존 자동 변환
-- DATETIME: 그대로 저장

-- UTC로 저장 권장
INSERT INTO logs (created_at)
VALUES (UTC_TIMESTAMP());

-- 조회 시 변환
SELECT CONVERT_TZ(created_at, 'UTC', 'Asia/Seoul');
```

### 자주 쓰는 패턴

```sql
-- 이번 주
WHERE YEARWEEK(created_at) = YEARWEEK(NOW())

-- 지난 달
WHERE created_at >= DATE_SUB(DATE_FORMAT(NOW(), '%Y-%m-01'), INTERVAL 1 MONTH)
  AND created_at < DATE_FORMAT(NOW(), '%Y-%m-01')

-- 분기별
SELECT
    QUARTER(created_at) AS quarter,
    SUM(total_price)
FROM orders
GROUP BY QUARTER(created_at);
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

print(f"✅ 01_기초, 02_SQL 섹션 업데이트 완료: {len(db_contents)}개 토픽")
