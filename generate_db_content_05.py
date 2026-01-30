# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load existing data
with open('src/data/contents/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 09_실무, 10_면접, index 섹션
db_contents = {
    "09_실무/connection-pool": {
        "title": "커넥션 풀",
        "description": "데이터베이스 커넥션 풀 관리를 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 커넥션 풀이란?",
                "content": """## 🔥 한 줄 요약
> **미리 만들어둔 DB 연결 재사용** - 연결 비용 절약!

---

## 💡 왜 필요한가?

```
❌ 커넥션 풀 없이
1. 요청마다 새 연결 생성 (50~100ms)
2. 쿼리 실행 (5ms)
3. 연결 종료
→ 연결 비용이 쿼리보다 큼!
→ 동시 요청 시 DB 연결 폭주

✅ 커넥션 풀 사용
1. 미리 연결 10개 생성
2. 요청 시 기존 연결 빌려줌 (1ms)
3. 쿼리 실행 후 반환
→ 연결 재사용으로 성능 향상
```

---

## 🎯 풀 설정

```
최소 연결 수 (min): 기본 유지 연결
최대 연결 수 (max): 동시 최대 연결
대기 타임아웃: 연결 기다리는 시간
유휴 타임아웃: 안 쓰는 연결 정리
```"""
            },
            {
                "type": "code",
                "title": "💻 커넥션 풀 설정",
                "content": """### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://user:pass@localhost/db",
    pool_size=10,          # 기본 풀 크기
    max_overflow=20,       # 추가 허용 연결
    pool_timeout=30,       # 연결 대기 시간 (초)
    pool_recycle=3600,     # 1시간마다 재연결
    pool_pre_ping=True,    # 연결 유효성 체크
)

# 사용
with engine.connect() as conn:
    result = conn.execute("SELECT * FROM users")
    # 자동으로 연결 반환
```

### Java (HikariCP)

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost/db");
config.setUsername("user");
config.setPassword("pass");

// 풀 설정
config.setMinimumIdle(5);       // 최소 유휴 연결
config.setMaximumPoolSize(20);  // 최대 연결
config.setConnectionTimeout(30000);  // 30초
config.setIdleTimeout(600000);  // 10분
config.setMaxLifetime(1800000); // 30분

HikariDataSource ds = new HikariDataSource(config);
```

### Node.js (mysql2)

```javascript
const mysql = require('mysql2');

const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    database: 'mydb',
    waitForConnections: true,
    connectionLimit: 10,      // 최대 연결
    queueLimit: 0,            // 대기열 제한 없음
    enableKeepAlive: true,
    keepAliveInitialDelay: 0
});

// 사용
pool.query('SELECT * FROM users', (err, results) => {
    // 자동 반환
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 커넥션 풀 튜닝",
                "content": """### 적정 풀 크기

```
공식: 연결 수 = (코어 수 * 2) + 유효 디스크 수

예시:
├── 4코어 서버
├── SSD 1개
└── 권장: (4 * 2) + 1 = 9~10개

주의:
├── 너무 많으면: DB 부하 증가
├── 너무 적으면: 대기 발생
└── 모니터링으로 조정
```

### 모니터링 포인트

```
□ 활성 연결 수 (active)
□ 유휴 연결 수 (idle)
□ 대기 요청 수 (pending)
□ 타임아웃 발생 횟수
□ 연결 생성/해제 빈도
```"""
            }
        ]
    },

    "09_실무/n-plus-1": {
        "title": "N+1 문제",
        "description": "ORM의 N+1 쿼리 문제와 해결법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 N+1 문제란?",
                "content": """## 🔥 한 줄 요약
> **1개 조회 후 N개 추가 쿼리** - ORM의 대표적 성능 문제!

---

## 💡 문제 상황

```python
# 유저 10명 조회
users = User.query.all()  # 쿼리 1개

for user in users:
    print(user.orders)  # 쿼리 10개 추가!

# 총 11개 쿼리 (1 + N)
```

```sql
-- 실제 실행되는 쿼리
SELECT * FROM users;                    -- 1번
SELECT * FROM orders WHERE user_id = 1; -- 2번
SELECT * FROM orders WHERE user_id = 2; -- 3번
...
SELECT * FROM orders WHERE user_id = 10; -- 11번
```

---

## 🎯 해결 방법

### 1. Eager Loading (즉시 로딩)
```python
# 처음부터 관계 데이터 함께 로드
users = User.query.options(joinedload(User.orders)).all()
```

### 2. Batch Loading (배치 로딩)
```python
# ID 목록으로 한 번에 로드
user_ids = [u.id for u in users]
orders = Order.query.filter(Order.user_id.in_(user_ids)).all()
```

### 3. JOIN으로 직접 조회
```sql
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```"""
            },
            {
                "type": "code",
                "title": "💻 N+1 해결",
                "content": """### SQLAlchemy 해결

```python
from sqlalchemy.orm import joinedload, subqueryload

# ❌ N+1 발생
users = session.query(User).all()
for user in users:
    print(user.orders)  # 매번 쿼리!

# ✅ Joined Load (1개 쿼리, JOIN)
users = session.query(User).options(
    joinedload(User.orders)
).all()

# ✅ Subquery Load (2개 쿼리)
users = session.query(User).options(
    subqueryload(User.orders)
).all()
```

### Django ORM 해결

```python
# ❌ N+1 발생
users = User.objects.all()
for user in users:
    print(user.order_set.all())  # 매번 쿼리!

# ✅ select_related (1:1, FK - JOIN)
users = User.objects.select_related('profile').all()

# ✅ prefetch_related (1:N, M:N - IN 쿼리)
users = User.objects.prefetch_related('order_set').all()

# ✅ 복합 사용
users = User.objects.select_related('profile').prefetch_related('order_set', 'order_set__items').all()
```

### JPA 해결

```java
// ❌ N+1 발생
List<User> users = userRepository.findAll();
users.forEach(u -> u.getOrders().size());  // Lazy loading

// ✅ Fetch Join
@Query("SELECT u FROM User u JOIN FETCH u.orders")
List<User> findAllWithOrders();

// ✅ EntityGraph
@EntityGraph(attributePaths = {"orders"})
List<User> findAll();

// ✅ Batch Size 설정
@BatchSize(size = 100)
@OneToMany(mappedBy = "user")
private List<Order> orders;
```"""
            },
            {
                "type": "tip",
                "title": "💡 N+1 예방",
                "content": """### 탐지 방법

```python
# 쿼리 로깅 활성화
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Django
LOGGING = {
    'loggers': {
        'django.db.backends': {'level': 'DEBUG'}
    }
}
```

### 예방 체크리스트

```
□ 루프 내 관계 접근 확인
□ ORM 쿼리 로그 확인
□ Eager Loading 적용
□ 필요한 관계만 로드
□ API 응답에 관계 데이터 포함 시 주의
```"""
            }
        ]
    },

    "09_실무/caching-strategy": {
        "title": "캐싱 전략",
        "description": "데이터베이스 캐싱 전략을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 캐싱 전략",
                "content": """## 🔥 한 줄 요약
> **자주 쓰는 데이터를 빠른 저장소에** - DB 부하 90% 감소!

---

## 🎯 캐싱 패턴

### 1. Cache-Aside (Look-Aside)
```
가장 일반적인 패턴

1. 캐시 확인
2. 없으면 DB 조회
3. 캐시에 저장
4. 반환
```

### 2. Write-Through
```
쓰기 시 캐시도 함께 갱신

1. 데이터 쓰기
2. 캐시 + DB 동시 저장
3. 일관성 보장
```

### 3. Write-Behind (Write-Back)
```
캐시에만 쓰고 나중에 DB 반영

1. 캐시에 쓰기
2. 비동기로 DB 저장
3. 빠르지만 데이터 손실 위험
```

### 4. Read-Through
```
캐시가 DB 조회 담당

1. 캐시에 요청
2. 캐시가 없으면 DB 조회
3. 캐시가 저장 후 반환
```"""
            },
            {
                "type": "code",
                "title": "💻 캐싱 구현",
                "content": """### Cache-Aside 패턴

```python
import redis
import json

r = redis.Redis()
CACHE_TTL = 3600  # 1시간

def get_user(user_id):
    cache_key = f"user:{user_id}"

    # 1. 캐시 확인
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. DB 조회
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)

    # 3. 캐시 저장
    r.setex(cache_key, CACHE_TTL, json.dumps(user))

    return user

def update_user(user_id, data):
    # 1. DB 업데이트
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)

    # 2. 캐시 무효화
    r.delete(f"user:{user_id}")
```

### 캐시 무효화 전략

```python
# 1. Time-based (TTL)
r.setex(key, 3600, value)  # 1시간 후 만료

# 2. Event-based
def on_user_update(user_id):
    r.delete(f"user:{user_id}")
    r.delete(f"user_profile:{user_id}")

# 3. Version-based
def get_cached(key, version):
    cached = r.hgetall(key)
    if cached.get('version') == version:
        return cached['data']
    return None
```

### 캐시 Warming

```python
# 자주 조회되는 데이터 미리 캐싱
def warm_cache():
    query = 'SELECT * FROM products ORDER BY view_count DESC LIMIT 100'
    popular_products = db.query(query)

    for product in popular_products:
        cache_key = f"product:{product['id']}"
        r.setex(cache_key, 3600, json.dumps(product))
```"""
            },
            {
                "type": "tip",
                "title": "💡 캐싱 주의사항",
                "content": """### 캐싱 대상

```
✅ 캐싱 적합
├── 읽기 빈번, 쓰기 적음
├── 계산 비용 큰 데이터
├── 동일 요청 반복
└── 잠시 오래된 데이터 허용

❌ 캐싱 부적합
├── 실시간 정확성 필요
├── 자주 변경되는 데이터
├── 개인화된 데이터
```

### 캐시 문제

```
Cache Stampede:
├── 캐시 만료 시 동시 DB 요청
├── 해결: Lock, 미리 갱신

Cache Penetration:
├── 없는 데이터 반복 조회
├── 해결: Null 캐싱, Bloom Filter

Cache Avalanche:
├── 동시에 대량 캐시 만료
├── 해결: TTL 분산, 배치 갱신
```"""
            }
        ]
    },

    "09_실무/replication": {
        "title": "복제 (Replication)",
        "description": "데이터베이스 복제 전략을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 Replication이란?",
                "content": """## 🔥 한 줄 요약
> **DB를 여러 대로 복제** - 읽기 성능 향상 + 장애 대비!

---

## 💡 왜 필요한가?

```
단일 DB 한계:
├── 읽기 부하 집중
├── 장애 시 서비스 중단
├── 백업 중 성능 저하

Replication으로:
├── Master: 쓰기 담당
├── Slave: 읽기 담당 (여러 대)
├── 장애 시 Slave → Master 승격
└── 읽기 성능 N배 향상
```

---

## 🎯 복제 방식

### 비동기 복제 (Async)
```
Master 쓰기 완료 → 응답 → Slave 복제

장점: 빠름
단점: 복제 지연 (lag)
```

### 동기 복제 (Sync)
```
Master 쓰기 → Slave 복제 완료 → 응답

장점: 데이터 일관성
단점: 느림
```

### 반동기 복제 (Semi-Sync)
```
최소 1대 Slave 복제 완료 → 응답

장점: 균형잡힌 선택
```"""
            },
            {
                "type": "code",
                "title": "💻 복제 설정",
                "content": """### 읽기/쓰기 분리 (Python)

```python
from sqlalchemy import create_engine

# Master (쓰기)
master_engine = create_engine("mysql://master-host/db")

# Slave (읽기) - 여러 대 가능
slave_engines = [
    create_engine("mysql://slave1-host/db"),
    create_engine("mysql://slave2-host/db"),
]

class DatabaseRouter:
    def __init__(self):
        self.slave_index = 0

    def get_read_engine(self):
        # Round-robin
        engine = slave_engines[self.slave_index]
        self.slave_index = (self.slave_index + 1) % len(slave_engines)
        return engine

    def get_write_engine(self):
        return master_engine

router = DatabaseRouter()

# 사용
def get_user(user_id):
    engine = router.get_read_engine()  # Slave에서 읽기
    return engine.execute("SELECT * FROM users WHERE id = %s", user_id)

def create_user(data):
    engine = router.get_write_engine()  # Master에 쓰기
    engine.execute("INSERT INTO users ...", data)
```

### Django 설정

```python
# settings.py
DATABASES = {
    'default': {  # Master
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'master-host',
    },
    'replica': {  # Slave
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'slave-host',
    }
}

# Router
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'replica'

    def db_for_write(self, model, **hints):
        return 'default'

DATABASE_ROUTERS = ['path.to.PrimaryReplicaRouter']
```"""
            },
            {
                "type": "tip",
                "title": "💡 복제 주의사항",
                "content": """### 복제 지연 (Lag) 문제

```python
# 문제: 쓰기 직후 읽기
create_user(data)
user = get_user(user_id)  # Slave에서 아직 없을 수 있음!

# 해결: 쓰기 직후는 Master에서 읽기
def get_user(user_id, from_master=False):
    if from_master:
        engine = router.get_write_engine()
    else:
        engine = router.get_read_engine()
    ...

# 사용
create_user(data)
user = get_user(user_id, from_master=True)
```

### 모니터링

```sql
-- MySQL Slave 상태 확인
SHOW SLAVE STATUS;

-- 복제 지연 확인
Seconds_Behind_Master: 0  -- 0이면 정상
```"""
            }
        ]
    },

    "09_실무/backup-restore": {
        "title": "백업과 복구",
        "description": "데이터베이스 백업 전략을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 백업의 중요성",
                "content": """## 🔥 한 줄 요약
> **데이터 손실 대비 안전장치** - 백업 없으면 복구 불가!

---

## 💡 백업이 필요한 상황

```
데이터 손실 원인:
├── 하드웨어 장애
├── 사람 실수 (DELETE 잘못)
├── 소프트웨어 버그
├── 해킹/랜섬웨어
├── 자연재해
└── 데이터 센터 장애

백업 없으면:
└── 복구 불가능! 사업 종료 가능
```

---

## 🎯 백업 종류

### Full Backup (전체)
```
모든 데이터 백업
├── 장점: 복구 간단
├── 단점: 시간/용량 큼
└── 주기: 주 1회
```

### Incremental (증분)
```
마지막 백업 이후 변경분만
├── 장점: 빠름, 용량 적음
├── 단점: 복구 복잡
└── 주기: 매일
```

### Differential (차등)
```
마지막 Full 이후 변경분
├── 장점: 복구 비교적 간단
├── 단점: 점점 커짐
└── 주기: 매일
```"""
            },
            {
                "type": "code",
                "title": "💻 백업 실전",
                "content": """### MySQL 백업

```bash
# mysqldump (논리적 백업)
mysqldump -u root -p --single-transaction --routines --triggers --events mydb > backup_$(date +%Y%m%d).sql

# 압축
mysqldump mydb | gzip > backup_$(date +%Y%m%d).sql.gz

# 특정 테이블만
mysqldump mydb users orders > partial_backup.sql
```

### MySQL 복구

```bash
# 복구
mysql -u root -p mydb < backup_20240115.sql

# 압축 파일 복구
gunzip < backup_20240115.sql.gz | mysql -u root -p mydb
```

### 자동 백업 스크립트

```bash
#!/bin/bash
# /etc/cron.daily/mysql-backup

BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# 백업 실행
mysqldump --single-transaction --all-databases | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# 오래된 백업 삭제
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# S3 업로드 (선택)
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://my-backups/
```

### Point-in-Time Recovery

```bash
# binlog 활성화 (my.cnf)
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
expire_logs_days = 7

# 특정 시점 복구
mysqlbinlog --stop-datetime="2024-01-15 14:00:00" mysql-bin.000001 | mysql -u root -p
```"""
            },
            {
                "type": "tip",
                "title": "💡 백업 체크리스트",
                "content": """### 3-2-1 백업 규칙

```
3: 3개의 백업 복사본
2: 2개의 다른 미디어 (디스크, 테이프)
1: 1개는 오프사이트 (클라우드)
```

### 백업 검증

```
□ 정기적으로 복구 테스트
□ 백업 파일 무결성 확인
□ 복구 시간 측정 (RTO)
□ 데이터 손실 범위 확인 (RPO)
□ 백업 성공 알림 설정
```

### RTO/RPO

```
RTO (Recovery Time Objective):
└── 복구까지 허용 시간 (예: 1시간)

RPO (Recovery Point Objective):
└── 손실 허용 데이터량 (예: 1시간치)

백업 주기 = RPO
복구 목표 시간 = RTO
```"""
            }
        ]
    },

    "10_면접/interview-db": {
        "title": "DB 면접 질문",
        "description": "데이터베이스 면접 대비 핵심 질문을 정리합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 필수 면접 질문",
                "content": """## 🎯 기초 질문

### Q: RDBMS와 NoSQL의 차이?
```
RDBMS:
├── 정형화된 스키마
├── ACID 트랜잭션
├── SQL 표준
├── 수직 확장

NoSQL:
├── 유연한 스키마
├── BASE (최종 일관성)
├── 다양한 쿼리
├── 수평 확장
```

### Q: 인덱스란? 왜 필요한가?
```
인덱스 = 데이터 검색 속도 향상 자료구조
├── B-Tree 구조로 O(log N) 검색
├── WHERE, JOIN, ORDER BY 성능 향상
├── 단점: 쓰기 성능 저하, 저장공간 필요
```

### Q: 정규화란?
```
데이터 중복 제거 + 무결성 보장
├── 1NF: 원자값
├── 2NF: 부분 함수 종속 제거
├── 3NF: 이행 함수 종속 제거
└── 실무: 3NF까지, 필요시 역정규화
```"""
            },
            {
                "type": "code",
                "title": "💻 심화 질문",
                "content": """### Q: 트랜잭션 격리 수준 설명

```
READ UNCOMMITTED: 커밋 안 된 데이터 읽음 (Dirty Read)
READ COMMITTED: 커밋된 것만 읽음
REPEATABLE READ: 트랜잭션 내 일관된 읽기 (MySQL 기본)
SERIALIZABLE: 완전 격리 (가장 느림)

→ 높을수록 안전하지만 성능 저하
```

### Q: 인덱스가 안 타는 경우?

```sql
-- 1. 함수 사용
WHERE YEAR(created_at) = 2024  -- ❌

-- 2. LIKE '%keyword'
WHERE name LIKE '%철수'  -- ❌

-- 3. 타입 불일치
WHERE string_column = 123  -- ❌

-- 4. OR 조건
WHERE col1 = 'A' OR col2 = 'B'  -- ❌

-- 5. 부정 조건
WHERE status != 'deleted'  -- ❌
```

### Q: N+1 문제란?

```python
# 문제: 1 + N개 쿼리
users = User.query.all()  # 1개
for user in users:
    print(user.orders)  # N개

# 해결: Eager Loading
users = User.query.options(
    joinedload(User.orders)
).all()  # 1개로 해결
```

### Q: 데드락이란? 해결법?

```
데드락 = 서로가 서로의 락 대기

해결:
1. 항상 같은 순서로 락 획득
2. 락 타임아웃 설정
3. 재시도 로직 구현
4. 트랜잭션 짧게 유지
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 질문",
                "content": """### Q: 슬로우 쿼리 대응?

```
1. 슬로우 쿼리 로그로 식별
2. EXPLAIN으로 실행계획 분석
3. 인덱스 추가/수정
4. 쿼리 리팩토링
5. 필요시 캐싱/샤딩
```

### Q: DB 확장 전략?

```
1단계: 쿼리 최적화, 인덱스
2단계: 읽기 복제본 (Read Replica)
3단계: 캐싱 (Redis)
4단계: 파티셔닝
5단계: 샤딩 (최후의 수단)
```

### Q: 경험한 DB 장애와 해결?

```
(준비해야 할 답변 예시)
"피크 시간에 슬로우 쿼리로 커넥션 풀 고갈
→ SHOW PROCESSLIST로 문제 쿼리 확인
→ 인덱스 추가로 즉시 해결
→ 이후 슬로우 쿼리 모니터링 도입"
```"""
            }
        ]
    },

    "index": {
        "title": "Database",
        "description": "데이터베이스 학습 로드맵입니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 데이터베이스 학습 로드맵",
                "content": """## 🎯 학습 순서

### 1단계: 기초 (1-2주)
```
├── DB 개념, RDBMS
├── SQL 기초 (SELECT, INSERT, UPDATE, DELETE)
├── WHERE, ORDER BY, LIMIT
└── 기본 자료형
```

### 2단계: SQL 심화 (2-3주)
```
├── JOIN (INNER, LEFT, RIGHT)
├── GROUP BY, HAVING
├── 서브쿼리
├── 집계 함수
└── 날짜/문자열 함수
```

### 3단계: 설계 (1-2주)
```
├── 정규화 (1NF~3NF)
├── ERD 설계
├── PK, FK, 관계
└── 제약조건
```

### 4단계: 성능 (2-3주)
```
├── 인덱스 원리와 설계
├── EXPLAIN 분석
├── 쿼리 최적화
└── 슬로우 쿼리 해결
```

### 5단계: 트랜잭션 (1-2주)
```
├── ACID
├── 격리 수준
├── 락 (Lock)
└── MVCC
```

### 6단계: 실무/심화 (2-3주)
```
├── 커넥션 풀
├── 복제 (Replication)
├── 파티셔닝/샤딩
├── NoSQL (Redis, MongoDB)
└── 백업/복구
```"""
            },
            {
                "type": "tip",
                "title": "💡 학습 팁",
                "content": """### 실습 권장

```
1. 로컬에 MySQL 설치
2. 쇼핑몰 DB 직접 설계
3. 100만건 데이터로 최적화 실습
4. ORM과 함께 사용해보기
```

### 추천 리소스

```
무료:
├── MySQL 공식 문서
├── SQLZoo (온라인 실습)
├── LeetCode SQL 문제
└── 프로그래머스 SQL

도서:
├── Real MySQL (한국어)
├── SQL 첫걸음
├── 데이터베이스 개론
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

print(f"✅ 09_실무, 10_면접, index 섹션 업데이트 완료: {len(db_contents)}개 토픽")
