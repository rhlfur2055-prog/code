# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open('src/data/contents/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 07_최적화, 08_NoSQL 섹션
db_contents = {
    "07_최적화/explain": {
        "title": "EXPLAIN 실행계획",
        "description": "쿼리 실행계획을 분석하는 방법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 EXPLAIN이란?",
                "content": """## 🔥 한 줄 요약
> **쿼리가 어떻게 실행되는지 미리보기** - 성능 튜닝의 시작!

---

## 💡 왜 배워야 하나?

```
❌ EXPLAIN 없이
├── 쿼리 느린데 왜 느린지 모름
├── 인덱스 있는데 안 타는지 모름
└── 감으로 튜닝 (시간 낭비)

✅ EXPLAIN 사용
├── 인덱스 사용 여부 확인
├── 스캔 방식 파악
├── 병목 지점 발견
└── 정확한 튜닝 가능
```

---

## 🎯 EXPLAIN 항목

```
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+------+------+-------+

주요 항목:
├── type: 접근 방식 (중요!)
├── key: 사용된 인덱스
├── rows: 예상 스캔 행 수
└── Extra: 추가 정보
```"""
            },
            {
                "type": "code",
                "title": "💻 EXPLAIN 분석",
                "content": """### 기본 사용

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@test.com';

-- 결과:
+----+-------------+-------+-------+---------------+-----------+---------+-------+------+-------+
| id | select_type | table | type  | possible_keys | key       | key_len | ref   | rows | Extra |
+----+-------------+-------+-------+---------------+-----------+---------+-------+------+-------+
|  1 | SIMPLE      | users | ref   | idx_email     | idx_email | 403     | const |    1 |       |
+----+-------------+-------+-------+---------------+-----------+---------+-------+------+-------+
```

### type 해석 (좋음 → 나쁨)

```sql
-- system/const: 1행만 (최고)
EXPLAIN SELECT * FROM users WHERE id = 1;
-- type: const

-- eq_ref: 유니크 인덱스로 1행
EXPLAIN SELECT * FROM orders o
JOIN users u ON o.user_id = u.id;
-- type: eq_ref

-- ref: 비유니크 인덱스 (양호)
EXPLAIN SELECT * FROM orders WHERE user_id = 1;
-- type: ref

-- range: 범위 스캔 (양호)
EXPLAIN SELECT * FROM orders WHERE created_at > '2024-01-01';
-- type: range

-- index: 인덱스 전체 스캔 (주의)
EXPLAIN SELECT user_id FROM orders;
-- type: index (커버링)

-- ALL: 풀 테이블 스캔 (최악!)
EXPLAIN SELECT * FROM orders WHERE YEAR(created_at) = 2024;
-- type: ALL (인덱스 못 씀)
```

### Extra 해석

```sql
-- Using index: 커버링 인덱스 (최고!)
-- Using where: WHERE 필터링
-- Using temporary: 임시 테이블 (주의)
-- Using filesort: 정렬 연산 (주의)
-- Using index condition: ICP (좋음)

EXPLAIN SELECT * FROM orders ORDER BY total_price;
-- Extra: Using filesort (인덱스 없이 정렬)
```"""
            },
            {
                "type": "tip",
                "title": "💡 EXPLAIN 팁",
                "content": """### 빠르게 확인

```sql
-- EXPLAIN ANALYZE (MySQL 8.0+, PostgreSQL)
-- 실제 실행 시간까지 표시
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1;

-- 결과:
-- -> Index lookup on orders using idx_user_id
--    (actual time=0.025..0.026 rows=10 loops=1)
```

### 튜닝 체크리스트

```
□ type이 ALL인가? → 인덱스 추가
□ rows가 너무 큰가? → 조건 개선
□ Using filesort? → ORDER BY 인덱스
□ Using temporary? → GROUP BY 개선
□ key가 NULL인가? → 인덱스 설계 확인
```"""
            }
        ]
    },

    "07_최적화/slow-query": {
        "title": "슬로우 쿼리 분석",
        "description": "느린 쿼리를 찾고 분석하는 방법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 슬로우 쿼리란?",
                "content": """## 🔥 한 줄 요약
> **설정 시간보다 오래 걸리는 쿼리** - 성능 병목의 원인!

---

## 💡 왜 중요한가?

```
🔴 슬로우 쿼리 1개의 영향
├── DB 커넥션 점유 (다른 쿼리 대기)
├── CPU/메모리 과다 사용
├── 전체 서비스 응답 지연
└── 최악의 경우 서버 다운

일반적으로:
├── 1초 이상: 슬로우
├── 5초 이상: 심각
└── 10초 이상: 장애 수준
```

---

## 🎯 슬로우 쿼리 설정

### MySQL 설정

```sql
-- 슬로우 쿼리 로그 활성화
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 1초 이상
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- 확인
SHOW VARIABLES LIKE 'slow%';
SHOW VARIABLES LIKE 'long_query_time';
```"""
            },
            {
                "type": "code",
                "title": "💻 슬로우 쿼리 분석",
                "content": """### 슬로우 쿼리 로그 확인

```bash
# 로그 파일 확인
tail -f /var/log/mysql/slow.log

# pt-query-digest로 분석 (Percona Toolkit)
pt-query-digest /var/log/mysql/slow.log > slow_report.txt
```

### 실시간 모니터링

```sql
-- 현재 실행 중인 쿼리
SHOW PROCESSLIST;

-- 긴 쿼리만
SELECT * FROM information_schema.PROCESSLIST
WHERE TIME > 5 AND COMMAND != 'Sleep';

-- 쿼리 강제 종료
KILL [PROCESS_ID];
```

### 문제 쿼리 패턴

```sql
-- 1. 인덱스 없는 풀스캔
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
-- 해결: 범위 조건으로 변경

-- 2. LIKE '%keyword%'
SELECT * FROM products WHERE name LIKE '%아이폰%';
-- 해결: Full-Text 인덱스 또는 검색 엔진

-- 3. 큰 결과셋 SELECT *
SELECT * FROM logs;  -- 100만 행
-- 해결: LIMIT, 필요 컬럼만

-- 4. 복잡한 서브쿼리
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 10);
-- 해결: JOIN으로 변경

-- 5. N+1 쿼리 (애플리케이션)
for user in users:
    SELECT * FROM orders WHERE user_id = user.id
-- 해결: JOIN으로 한 번에
```"""
            },
            {
                "type": "tip",
                "title": "💡 슬로우 쿼리 대응",
                "content": """### 즉시 대응

```
1. SHOW PROCESSLIST로 확인
2. 문제 쿼리 KILL
3. 원인 분석 (EXPLAIN)
4. 인덱스 추가 또는 쿼리 수정
```

### 예방

```
□ 개발 시 EXPLAIN 습관화
□ 슬로우 쿼리 로그 활성화
□ 모니터링 대시보드 설정
□ 쿼리 실행 시간 제한 (ORM)
□ 정기 쿼리 리뷰
```"""
            }
        ]
    },

    "07_최적화/query-optimization": {
        "title": "쿼리 최적화",
        "description": "SQL 쿼리 성능을 개선하는 방법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 쿼리 최적화 원칙",
                "content": """## 🎯 최적화 순서

```
1단계: 인덱스 확인/추가
├── EXPLAIN으로 확인
├── 적절한 인덱스 설계
└── 가장 효과적

2단계: 쿼리 리팩토링
├── 불필요한 연산 제거
├── 서브쿼리 → JOIN
└── 조건 최적화

3단계: 데이터 모델 개선
├── 역정규화 검토
├── 파티셔닝
└── 아키텍처 변경

4단계: 하드웨어/설정
├── DB 설정 튜닝
├── 메모리 증설
└── 읽기 복제본
```"""
            },
            {
                "type": "code",
                "title": "💻 최적화 예제",
                "content": """### SELECT 최적화

```sql
-- ❌ 느림: SELECT *
SELECT * FROM orders WHERE user_id = 1;

-- ✅ 빠름: 필요 컬럼만
SELECT id, total_price, created_at FROM orders WHERE user_id = 1;
```

### WHERE 최적화

```sql
-- ❌ 느림: 함수 사용
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- ✅ 빠름: 범위 조건
SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

### JOIN 최적화

```sql
-- ❌ 느림: 서브쿼리
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total_price > 100000);

-- ✅ 빠름: JOIN
SELECT DISTINCT u.*
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total_price > 100000;
```

### 페이징 최적화

```sql
-- ❌ 느림: OFFSET 큰 값
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 100000;
-- 100,010행 읽고 100,000행 버림

-- ✅ 빠름: 커서 기반
SELECT * FROM products
WHERE id > 100000  -- 마지막 조회 ID
ORDER BY id
LIMIT 10;
```

### GROUP BY 최적화

```sql
-- ❌ 느림: filesort
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;

-- ✅ 빠름: 인덱스 활용
CREATE INDEX idx_user_id ON orders(user_id);
-- 또는 커버링 인덱스
CREATE INDEX idx_user_status ON orders(user_id, status);
```"""
            },
            {
                "type": "tip",
                "title": "💡 최적화 체크리스트",
                "content": """### 쿼리 작성 시

```
□ SELECT * 대신 필요 컬럼만
□ WHERE에 인덱스 컬럼 사용
□ 함수로 컬럼 감싸지 않기
□ LIKE는 앞부분 고정 (abc%)
□ IN보다 EXISTS (대용량)
□ OR 대신 UNION (경우에 따라)
□ LIMIT 항상 사용
```

### 인덱스 활용

```
□ WHERE 조건 컬럼에 인덱스
□ JOIN 컬럼에 인덱스
□ ORDER BY 컬럼 인덱스 포함
□ 커버링 인덱스 고려
□ 복합 인덱스 순서 최적화
```"""
            }
        ]
    },

    "07_최적화/query-tuning": {
        "title": "쿼리 튜닝 실전",
        "description": "실제 쿼리 튜닝 사례를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 튜닝 프로세스",
                "content": """## 🎯 튜닝 단계

```
1. 문제 쿼리 식별
   └── 슬로우 쿼리 로그, 모니터링

2. 현재 상태 분석
   └── EXPLAIN, 실행 시간 측정

3. 원인 파악
   └── 풀스캔? 인덱스 미사용? 잘못된 조인?

4. 개선안 적용
   └── 인덱스, 쿼리 수정, 구조 변경

5. 결과 검증
   └── EXPLAIN, 실행 시간 비교
```"""
            },
            {
                "type": "code",
                "title": "💻 튜닝 사례",
                "content": """### 사례 1: 인덱스 추가

```sql
-- Before: 5초
SELECT * FROM orders WHERE user_id = 100 AND status = 'completed';
-- EXPLAIN: type=ALL, rows=1000000

-- After: 0.01초
CREATE INDEX idx_user_status ON orders(user_id, status);
-- EXPLAIN: type=ref, rows=10
```

### 사례 2: 쿼리 리팩토링

```sql
-- Before: 10초
SELECT * FROM products
WHERE id IN (
    SELECT product_id FROM order_items
    WHERE order_id IN (
        SELECT id FROM orders WHERE created_at > '2024-01-01'
    )
);

-- After: 0.5초
SELECT DISTINCT p.*
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > '2024-01-01';
```

### 사례 3: 커버링 인덱스

```sql
-- Before: 3초
SELECT user_id, COUNT(*), SUM(total_price)
FROM orders
WHERE status = 'completed'
GROUP BY user_id;

-- After: 0.3초
CREATE INDEX idx_covering ON orders(status, user_id, total_price);
-- Extra: Using index (테이블 접근 없음)
```

### 사례 4: 페이징 개선

```sql
-- Before: 8초 (OFFSET 100000)
SELECT * FROM products ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- After: 0.05초 (커서 기반)
SELECT * FROM products
WHERE created_at < '2024-01-15 10:30:00'  -- 이전 페이지 마지막
ORDER BY created_at DESC
LIMIT 20;
```"""
            },
            {
                "type": "tip",
                "title": "💡 튜닝 팁",
                "content": """### 측정 방법

```sql
-- 쿼리 실행 시간 측정
SET profiling = 1;
SELECT * FROM orders WHERE user_id = 1;
SHOW PROFILES;

-- 캐시 무효화 (정확한 측정)
SELECT SQL_NO_CACHE * FROM orders;
```

### 튜닝 우선순위

```
효과 높음:
├── 적절한 인덱스 추가
├── 풀스캔 → 인덱스 스캔
└── N+1 쿼리 해결

효과 중간:
├── 서브쿼리 → JOIN
├── SELECT * → 필요 컬럼
└── 커버링 인덱스

효과 낮음 (복잡도 높음):
├── 파티셔닝
├── 샤딩
└── 캐싱 레이어
```"""
            }
        ]
    },

    "07_최적화/partitioning": {
        "title": "파티셔닝",
        "description": "대용량 테이블 파티셔닝을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 파티셔닝이란?",
                "content": """## 🔥 한 줄 요약
> **큰 테이블을 작은 조각으로 분할** - 관리와 성능 향상!

---

## 💡 왜 필요한가?

```
1억 건 테이블 문제:
├── 풀스캔 시 엄청 느림
├── 인덱스도 거대해짐
├── 백업/복구 오래 걸림
└── 오래된 데이터 삭제 어려움

파티셔닝으로 해결:
├── 2024년 1월 파티션
├── 2024년 2월 파티션
├── ...
└── 필요한 파티션만 스캔!
```

---

## 🎯 파티셔닝 종류

### RANGE: 범위 기준
```
날짜, 숫자 범위로 분할
├── 2024-01 파티션
├── 2024-02 파티션
└── 가장 흔히 사용
```

### LIST: 목록 기준
```
특정 값 목록으로 분할
├── status = 'active' 파티션
├── status = 'deleted' 파티션
└── 값이 정해진 경우
```

### HASH: 해시 기준
```
해시 함수로 균등 분할
├── user_id % 4 = 0 파티션
├── user_id % 4 = 1 파티션
└── 데이터 균등 분산
```"""
            },
            {
                "type": "code",
                "title": "💻 파티셔닝 구현",
                "content": """### RANGE 파티셔닝 (날짜)

```sql
CREATE TABLE orders (
    id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    total_price DECIMAL(12,2),
    created_at DATE NOT NULL,
    PRIMARY KEY (id, created_at)  -- 파티션 키 포함 필수
)
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 쿼리 시 해당 파티션만 스캔
SELECT * FROM orders WHERE created_at >= '2024-01-01';
-- p2024, p_future만 스캔
```

### 파티션 관리

```sql
-- 파티션 추가
ALTER TABLE orders ADD PARTITION (
    PARTITION p2025 VALUES LESS THAN (2026)
);

-- 파티션 삭제 (오래된 데이터 빠른 삭제!)
ALTER TABLE orders DROP PARTITION p2022;

-- 파티션 확인
SELECT PARTITION_NAME, TABLE_ROWS
FROM information_schema.PARTITIONS
WHERE TABLE_NAME = 'orders';
```

### LIST 파티셔닝

```sql
CREATE TABLE logs (
    id BIGINT NOT NULL,
    level ENUM('DEBUG','INFO','WARN','ERROR') NOT NULL,
    message TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (id, level)
)
PARTITION BY LIST COLUMNS(level) (
    PARTITION p_debug VALUES IN ('DEBUG'),
    PARTITION p_info VALUES IN ('INFO'),
    PARTITION p_warn VALUES IN ('WARN'),
    PARTITION p_error VALUES IN ('ERROR')
);
```"""
            },
            {
                "type": "tip",
                "title": "💡 파티셔닝 가이드",
                "content": """### 언제 사용?

```
✅ 파티셔닝 권장
├── 테이블 1000만 건 이상
├── 날짜 기반 조회 빈번
├── 오래된 데이터 정기 삭제
├── 특정 범위 쿼리 많음

❌ 파티셔닝 불필요
├── 작은 테이블
├── 전체 조회가 대부분
├── 파티션 키 없이 조회
```

### 주의사항

```
1. PK에 파티션 키 포함 필수
2. 파티션 프루닝 확인 (EXPLAIN PARTITIONS)
3. 파티션 개수 적절히 (수십~수백)
4. 유니크 인덱스 제약
```"""
            }
        ]
    },

    "07_최적화/sharding": {
        "title": "샤딩",
        "description": "데이터베이스 샤딩 전략을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 샤딩이란?",
                "content": """## 🔥 한 줄 요약
> **여러 DB 서버에 데이터 분산** - 수평 확장의 핵심!

---

## 💡 왜 필요한가?

```
단일 DB 한계:
├── CPU/메모리 한계
├── 디스크 I/O 한계
├── 커넥션 수 한계
└── Scale-up 비용 급증

샤딩으로 해결:
├── DB1: 유저 1~100만
├── DB2: 유저 100만~200만
├── DB3: 유저 200만~300만
└── Scale-out (서버 추가)
```

---

## 🎯 샤딩 전략

### 1. Range 샤딩
```
user_id 1~100만 → Shard1
user_id 100만~200만 → Shard2

장점: 구현 단순
단점: 불균형 가능
```

### 2. Hash 샤딩
```
user_id % 3 = 0 → Shard1
user_id % 3 = 1 → Shard2
user_id % 3 = 2 → Shard3

장점: 균등 분산
단점: 리샤딩 어려움
```

### 3. Directory 샤딩
```
매핑 테이블로 관리
user_id → shard_id 조회 후 접근

장점: 유연함
단점: 매핑 관리 필요
```"""
            },
            {
                "type": "code",
                "title": "💻 샤딩 구현",
                "content": """### 애플리케이션 레벨 샤딩

```python
# Python 예제: Hash 샤딩
class ShardRouter:
    def __init__(self, shard_count=3):
        self.shard_count = shard_count
        self.connections = {
            0: connect('shard0.db'),
            1: connect('shard1.db'),
            2: connect('shard2.db'),
        }

    def get_shard(self, user_id):
        shard_id = user_id % self.shard_count
        return self.connections[shard_id]

    def execute(self, user_id, query, params):
        conn = self.get_shard(user_id)
        return conn.execute(query, params)

# 사용
router = ShardRouter()
router.execute(user_id=12345, query="SELECT * FROM orders WHERE user_id = %s", params=(12345,))
```

### Cross-Shard 쿼리

```python
# 모든 샤드에서 집계
def get_total_revenue():
    total = 0
    for shard_conn in router.connections.values():
        result = shard_conn.execute("SELECT SUM(total_price) FROM orders")
        total += result[0] or 0
    return total
```

### 샤딩 키 선택

```
✅ 좋은 샤딩 키
├── user_id: 유저별 데이터 격리
├── tenant_id: 멀티테넌트
└── region: 지역별 데이터

❌ 나쁜 샤딩 키
├── created_at: 최신 샤드만 핫
├── status: 불균형
└── 자주 바뀌는 값
```"""
            },
            {
                "type": "tip",
                "title": "💡 샤딩 주의사항",
                "content": """### 샤딩의 어려움

```
1. Cross-Shard JOIN 불가
   → 애플리케이션에서 조합

2. Cross-Shard 트랜잭션 복잡
   → 분산 트랜잭션, Saga 패턴

3. 리샤딩 어려움
   → 초기 설계 중요

4. 운영 복잡도 증가
   → 모니터링, 백업, 마이그레이션
```

### 샤딩 전 체크

```
□ 정말 샤딩이 필요한가?
□ 읽기 복제본으로 해결 가능?
□ 캐싱으로 해결 가능?
□ 쿼리 최적화로 해결 가능?
□ 파티셔닝으로 충분한가?

→ 샤딩은 최후의 수단!
```"""
            }
        ]
    },

    # 08_NoSQL 섹션
    "08_NoSQL/nosql-concept": {
        "title": "NoSQL 개념",
        "description": "NoSQL 데이터베이스의 개념과 특징을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 NoSQL이란?",
                "content": """## 🔥 한 줄 요약
> **Not Only SQL** - 관계형이 아닌 다양한 데이터 저장 방식

---

## 💡 왜 등장했나?

```
RDBMS의 한계:
├── 스키마 변경 어려움
├── Scale-out 어려움
├── 비정형 데이터 저장 어려움
└── 대용량 처리 한계

NoSQL로 해결:
├── 유연한 스키마
├── 수평 확장 용이
├── 다양한 데이터 모델
└── 높은 성능
```

---

## 🎯 NoSQL 유형

### 1. 문서형 (Document)
```
MongoDB, CouchDB
├── JSON/BSON 문서 저장
├── 유연한 스키마
└── 예: 상품, 게시글, 로그
```

### 2. 키-값 (Key-Value)
```
Redis, Memcached
├── 단순한 키-값 저장
├── 초고속 읽기/쓰기
└── 예: 캐시, 세션, 장바구니
```

### 3. 컬럼형 (Column-Family)
```
Cassandra, HBase
├── 컬럼 기반 저장
├── 대용량 분석
└── 예: 시계열, 로그, 분석
```

### 4. 그래프 (Graph)
```
Neo4j, Amazon Neptune
├── 노드와 관계 저장
├── 복잡한 관계 탐색
└── 예: SNS, 추천, 사기탐지
```"""
            },
            {
                "type": "code",
                "title": "💻 NoSQL 예시",
                "content": """### MongoDB (문서형)

```javascript
// 유연한 스키마
db.products.insertOne({
    name: "아이폰 15",
    price: 1500000,
    specs: {  // 중첩 객체
        color: ["블랙", "화이트"],
        storage: [128, 256, 512]
    },
    reviews: [  // 배열
        { user: "김철수", rating: 5 },
        { user: "이영희", rating: 4 }
    ]
});

// 쿼리
db.products.find({ "specs.storage": 256 });
```

### Redis (키-값)

```python
import redis
r = redis.Redis()

# 캐싱
r.set("user:1:name", "김철수", ex=3600)  # 1시간 만료
name = r.get("user:1:name")

# 해시
r.hset("user:1", mapping={"name": "김철수", "email": "kim@test.com"})
r.hget("user:1", "name")

# 리스트 (최근 본 상품)
r.lpush("user:1:recent", "product:100")
r.lrange("user:1:recent", 0, 9)  # 최근 10개
```

### Cassandra (컬럼형)

```sql
-- 시계열 데이터
CREATE TABLE sensor_data (
    sensor_id UUID,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- 최근 데이터 조회 (매우 빠름)
SELECT * FROM sensor_data
WHERE sensor_id = ? AND timestamp > '2024-01-01';
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 언제 뭘 쓸까?

```
MongoDB:
├── 유연한 스키마 필요
├── 문서 구조 데이터
└── 빠른 개발 속도

Redis:
├── 캐싱
├── 세션 관리
├── 실시간 랭킹

Cassandra:
├── 대용량 쓰기
├── 시계열 데이터
├── 고가용성 필수

RDBMS:
├── 트랜잭션 중요
├── 복잡한 JOIN
├── 데이터 무결성
```"""
            }
        ]
    },

    "08_NoSQL/sql-vs-nosql": {
        "title": "SQL vs NoSQL",
        "description": "SQL과 NoSQL의 차이점과 선택 기준을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 SQL vs NoSQL",
                "content": """## 🎯 비교표

| 항목 | SQL (RDBMS) | NoSQL |
|------|-------------|-------|
| 스키마 | 고정 스키마 | 유연한 스키마 |
| 확장 | Scale-up | Scale-out |
| 트랜잭션 | ACID | BASE (대부분) |
| 조인 | 지원 | 제한적/없음 |
| 쿼리 | SQL 표준 | DB마다 다름 |
| 일관성 | 강한 일관성 | 최종 일관성 |

---

## 🎯 ACID vs BASE

### ACID (SQL)
```
Atomicity: 원자성
Consistency: 일관성
Isolation: 격리성
Durability: 지속성
→ 강한 일관성, 트랜잭션 보장
```

### BASE (NoSQL)
```
Basically Available: 기본 가용성
Soft state: 일시적 비일관
Eventually consistent: 최종 일관성
→ 가용성 우선, 일관성은 나중에
```"""
            },
            {
                "type": "code",
                "title": "💻 사용 사례",
                "content": """### SQL이 좋은 경우

```sql
-- 금융 거래 (트랜잭션 필수)
START TRANSACTION;
UPDATE accounts SET balance = balance - 100000 WHERE id = 1;
UPDATE accounts SET balance = balance + 100000 WHERE id = 2;
COMMIT;

-- 복잡한 JOIN 쿼리
SELECT u.name, o.total_price, p.name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

### NoSQL이 좋은 경우

```javascript
// 빠르게 변하는 스키마 (MongoDB)
// 오늘: 기본 필드
{ name: "상품A", price: 10000 }

// 내일: 새 필드 추가 (마이그레이션 불필요)
{ name: "상품A", price: 10000, discount: 0.1, tags: ["신상", "인기"] }

// 캐싱 (Redis)
redis.set("user:1:cart", JSON.stringify(cartItems), "EX", 3600);

// 대용량 로그 (Cassandra)
// 초당 수만 건 쓰기
INSERT INTO logs (id, timestamp, message) VALUES (...);
```

### 하이브리드 아키텍처

```
실무에서는 둘 다 사용!

┌─────────────────────────────────────────┐
│              Application                │
├──────────────────┬──────────────────────┤
│     MySQL        │       Redis          │
│  (메인 데이터)    │      (캐시)          │
├──────────────────┼──────────────────────┤
│    MongoDB       │    Elasticsearch     │
│   (로그/문서)     │      (검색)          │
└──────────────────┴──────────────────────┘
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 결정 체크리스트

```
SQL 선택:
□ 트랜잭션 필수 (금융, 결제)
□ 복잡한 관계/JOIN
□ 데이터 무결성 중요
□ 정형화된 데이터
□ 스키마 변경 적음

NoSQL 선택:
□ 빠른 개발/프로토타이핑
□ 유연한 스키마 필요
□ 대용량/고성능
□ 수평 확장 필요
□ 비정형 데이터
```

### 실무 조언

```
1. 기본은 RDBMS로 시작
2. 특정 요구사항에 NoSQL 추가
3. "은탄환"은 없음
4. 요구사항에 맞게 선택
```"""
            }
        ]
    },

    "08_NoSQL/mongodb": {
        "title": "MongoDB",
        "description": "MongoDB의 특징과 기본 사용법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 MongoDB란?",
                "content": """## 🔥 한 줄 요약
> **문서 지향 NoSQL 데이터베이스** - JSON처럼 저장!

---

## 💡 왜 인기 있나?

```
장점:
├── 유연한 스키마 (필드 자유롭게)
├── JSON 직관적 저장
├── 수평 확장 용이
├── 개발 속도 빠름
└── 강력한 쿼리 기능

사용처:
├── 콘텐츠 관리
├── IoT 데이터
├── 실시간 분석
├── 모바일 앱
└── 게임 백엔드
```

---

## 🎯 용어 매핑

```
RDBMS        →  MongoDB
─────────────────────────
Database     →  Database
Table        →  Collection
Row          →  Document
Column       →  Field
Primary Key  →  _id
Index        →  Index
JOIN         →  $lookup (제한적)
```"""
            },
            {
                "type": "code",
                "title": "💻 MongoDB CRUD",
                "content": """### Create (삽입)

```javascript
// 단일 문서
db.users.insertOne({
    name: "김철수",
    email: "kim@test.com",
    age: 30,
    hobbies: ["코딩", "게임"]
});

// 다중 문서
db.users.insertMany([
    { name: "이영희", age: 25 },
    { name: "박민수", age: 35 }
]);
```

### Read (조회)

```javascript
// 전체 조회
db.users.find();

// 조건 조회
db.users.find({ age: { $gte: 30 } });

// 특정 필드만
db.users.find({}, { name: 1, email: 1 });

// 정렬, 제한
db.users.find().sort({ age: -1 }).limit(10);

// 복잡한 조건
db.users.find({
    $or: [
        { age: { $lt: 20 } },
        { age: { $gt: 50 } }
    ],
    status: "active"
});
```

### Update (수정)

```javascript
// 단일 수정
db.users.updateOne(
    { email: "kim@test.com" },
    { $set: { age: 31 } }
);

// 다중 수정
db.users.updateMany(
    { status: "inactive" },
    { $set: { deleted: true } }
);

// 배열 추가
db.users.updateOne(
    { email: "kim@test.com" },
    { $push: { hobbies: "독서" } }
);
```

### Delete (삭제)

```javascript
db.users.deleteOne({ email: "kim@test.com" });
db.users.deleteMany({ status: "deleted" });
```"""
            },
            {
                "type": "tip",
                "title": "💡 MongoDB 팁",
                "content": """### 인덱스

```javascript
// 단일 인덱스
db.users.createIndex({ email: 1 });

// 복합 인덱스
db.users.createIndex({ status: 1, created_at: -1 });

// 유니크 인덱스
db.users.createIndex({ email: 1 }, { unique: true });
```

### 집계 파이프라인

```javascript
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: {
        _id: "$user_id",
        total: { $sum: "$amount" },
        count: { $sum: 1 }
    }},
    { $sort: { total: -1 } },
    { $limit: 10 }
]);
```

### Python 연동

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['mydb']
collection = db['users']

# 삽입
collection.insert_one({"name": "홍길동"})

# 조회
users = collection.find({"age": {"$gte": 20}})
```"""
            }
        ]
    },

    "08_NoSQL/redis": {
        "title": "Redis",
        "description": "Redis의 특징과 기본 사용법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 Redis란?",
                "content": """## 🔥 한 줄 요약
> **인메모리 키-값 저장소** - 초고속 캐시의 왕!

---

## 💡 왜 Redis인가?

```
성능:
├── 메모리 기반 → 초고속 (1ms 미만)
├── 단일 스레드 → 원자성 보장
├── 100,000+ 요청/초
└── DB 부하 90% 감소 가능

사용처:
├── 캐싱 (가장 흔함)
├── 세션 저장
├── 실시간 랭킹
├── Pub/Sub 메시징
├── 분산 락
└── Rate Limiting
```

---

## 🎯 데이터 타입

```
String: 단순 키-값
Hash: 객체 (필드-값)
List: 순서 있는 목록
Set: 중복 없는 집합
Sorted Set: 점수 기반 정렬
```"""
            },
            {
                "type": "code",
                "title": "💻 Redis 사용법",
                "content": """### String (캐싱)

```python
import redis
r = redis.Redis(host='localhost', port=6379)

# 캐싱 기본
r.set('user:1:name', '김철수')
r.get('user:1:name')  # b'김철수'

# TTL 설정 (초)
r.setex('session:abc', 3600, 'user_data')

# 카운터
r.incr('page:home:views')
r.incrby('product:100:stock', -1)
```

### Hash (객체)

```python
# 유저 정보 저장
r.hset('user:1', mapping={
    'name': '김철수',
    'email': 'kim@test.com',
    'age': 30
})

# 단일 필드 조회
r.hget('user:1', 'name')

# 전체 조회
r.hgetall('user:1')

# 필드 수정
r.hincrby('user:1', 'age', 1)
```

### List (최근 목록)

```python
# 최근 본 상품
r.lpush('user:1:recent', 'product:100')
r.lpush('user:1:recent', 'product:101')

# 최근 10개만 유지
r.ltrim('user:1:recent', 0, 9)

# 조회
r.lrange('user:1:recent', 0, -1)
```

### Sorted Set (랭킹)

```python
# 점수 추가
r.zadd('leaderboard', {'user:1': 1500, 'user:2': 2000, 'user:3': 1800})

# 상위 10명
r.zrevrange('leaderboard', 0, 9, withscores=True)

# 특정 유저 순위
r.zrevrank('leaderboard', 'user:1')  # 0부터 시작
```

### 실전: 캐시 패턴

```python
def get_user(user_id):
    # 1. 캐시 확인
    cache_key = f'user:{user_id}'
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. DB 조회
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")

    # 3. 캐시 저장 (1시간)
    r.setex(cache_key, 3600, json.dumps(user))

    return user
```"""
            },
            {
                "type": "tip",
                "title": "💡 Redis 팁",
                "content": """### 메모리 관리

```
# 최대 메모리 설정
maxmemory 2gb
maxmemory-policy allkeys-lru

정책:
├── noeviction: 메모리 초과 시 에러
├── allkeys-lru: 가장 오래된 키 삭제
├── volatile-lru: TTL 있는 것 중 삭제
└── allkeys-random: 랜덤 삭제
```

### 영속성 옵션

```
RDB: 주기적 스냅샷
├── 빠른 복구
├── 데이터 손실 가능

AOF: 모든 쓰기 로그
├── 데이터 손실 최소화
├── 파일 크기 큼

권장: 둘 다 사용
```"""
            }
        ]
    },

    "08_NoSQL/redis-data-type": {
        "title": "Redis 자료구조",
        "description": "Redis의 다양한 자료구조 활용법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 Redis 자료구조 총정리",
                "content": """## 🎯 자료구조별 용도

| 타입 | 용도 | 예시 |
|------|------|------|
| String | 캐싱, 카운터 | 세션, 조회수 |
| Hash | 객체 저장 | 유저 정보 |
| List | 순서 있는 목록 | 최근 본 상품 |
| Set | 중복 없는 집합 | 태그, 팔로워 |
| Sorted Set | 점수 기반 정렬 | 랭킹, 타임라인 |
| Bitmap | 비트 연산 | 출석 체크 |
| HyperLogLog | 카디널리티 추정 | UV 카운트 |"""
            },
            {
                "type": "code",
                "title": "💻 자료구조 실전",
                "content": """### Set (집합 연산)

```python
# 팔로워/팔로잉
r.sadd('user:1:following', 'user:2', 'user:3', 'user:4')
r.sadd('user:2:following', 'user:1', 'user:3', 'user:5')

# 공통 팔로우 (교집합)
common = r.sinter('user:1:following', 'user:2:following')
# {'user:3'}

# 추천 친구 (차집합)
recommend = r.sdiff('user:2:following', 'user:1:following')
# {'user:5'} - user:1이 팔로우 안 한 사람
```

### Sorted Set (타임라인)

```python
import time

# 타임라인 추가 (timestamp를 score로)
r.zadd('user:1:timeline', {
    'post:100': time.time(),
    'post:101': time.time() + 1,
})

# 최신순 조회
posts = r.zrevrange('user:1:timeline', 0, 19)  # 최근 20개

# 특정 시간 이후 게시물
recent = r.zrangebyscore('user:1:timeline',
    time.time() - 3600,  # 1시간 전
    time.time()
)
```

### Bitmap (출석 체크)

```python
# 출석 체크 (일자별 비트)
user_id = 1
day_of_year = 15  # 1월 15일

r.setbit(f'attendance:2024:{user_id}', day_of_year, 1)

# 출석 확인
attended = r.getbit(f'attendance:2024:{user_id}', day_of_year)

# 이번 달 출석 일수
r.bitcount(f'attendance:2024:{user_id}', 0, 30)
```

### Pub/Sub (실시간 메시징)

```python
# Publisher
r.publish('chat:room:1', json.dumps({
    'user': 'kim',
    'message': '안녕하세요!'
}))

# Subscriber
pubsub = r.pubsub()
pubsub.subscribe('chat:room:1')

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        print(f"{data['user']}: {data['message']}")
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 자료구조 선택

```
단순 값 저장 → String
객체 저장 → Hash
순서 있는 목록 → List
중복 없는 집합 → Set
점수 기반 정렬 → Sorted Set
비트 플래그 → Bitmap
대략적 카운트 → HyperLogLog
```

### 성능 고려

```
O(1): GET, SET, HGET, SADD
O(N): LRANGE, SMEMBERS
O(log N): ZADD, ZRANGE

→ 큰 컬렉션은 페이징 필수!
→ KEYS * 명령 금지 (SCAN 사용)
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

print(f"✅ 07_최적화, 08_NoSQL 섹션 업데이트 완료: {len(db_contents)}개 토픽")
