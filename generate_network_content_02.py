# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/contents/network.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

network_contents = {
    "03_HTTP/http-intro": {
        "title": "HTTP 소개",
        "description": "HTTP 프로토콜의 기본을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 HTTP란?",
                "content": """## 🔥 한 줄 요약
> **웹에서 데이터 주고받는 규칙** - 브라우저와 서버의 대화법!

---

## 💡 왜 배워야 하나?

### 웹 개발 = HTTP 이해
```
🌐 모든 웹 통신 = HTTP
├── 웹사이트 접속
├── API 호출
├── 이미지 로딩
├── 로그인 처리
└── 다 HTTP!
```

### 실제 예시
```
브라우저에서 네이버 접속:

1. 브라우저: "GET /index.html 줘!" (요청)
2. 네이버 서버: "여기 있어!" (응답)
3. 브라우저: 화면에 표시

→ 이게 HTTP 통신!
```

---

## 🎯 HTTP 특징

### 1. 요청-응답 구조
```
클라이언트 ──요청──▶ 서버
          ◀──응답──
```

### 2. 무상태 (Stateless)
```
서버: "너 누구야? 처음 보는데?"
클라이언트: "아까 로그인했잖아!"
서버: "기억 안 나..."

→ 매 요청이 독립적
→ 상태 유지하려면 쿠키/세션 필요
```

### 3. 텍스트 기반
```
HTTP/1.1 200 OK
Content-Type: text/html

<html>...</html>

→ 사람이 읽을 수 있음!
```"""
            },
            {
                "type": "code",
                "title": "💻 HTTP 요청/응답",
                "content": """### HTTP 요청 구조

```http
GET /users/1 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer token123

(본문 - GET은 보통 없음)
```

### HTTP 응답 구조

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 45

{"id": 1, "name": "김철수"}
```

### Python으로 HTTP 요청

```python
import requests

# GET 요청
response = requests.get('https://api.example.com/users')
print(response.status_code)  # 200
print(response.json())       # 응답 데이터

# POST 요청
response = requests.post(
    'https://api.example.com/users',
    json={'name': '김철수', 'email': 'kim@test.com'}
)
```

### JavaScript (fetch)

```javascript
// GET
const response = await fetch('https://api.example.com/users');
const data = await response.json();

// POST
const response = await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: '김철수' })
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 개발자 도구",
                "content": """### 브라우저에서 HTTP 확인

```
Chrome 개발자 도구 (F12)
└── Network 탭
    ├── 모든 HTTP 요청 확인
    ├── 헤더, 응답 내용 확인
    └── 시간 측정
```

### HTTP 학습 순서

```
1. 요청/응답 구조
2. HTTP 메서드 (GET, POST...)
3. 상태 코드 (200, 404...)
4. 헤더 (Content-Type, Authorization...)
5. HTTPS (보안)
```"""
            }
        ]
    },

    "03_HTTP/http-method": {
        "title": "HTTP 메서드",
        "description": "GET, POST, PUT, DELETE 등 HTTP 메서드를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 HTTP 메서드란?",
                "content": """## 🔥 한 줄 요약
> **서버에게 원하는 작업을 알려주는 동사** - "조회해줘", "생성해줘"

---

## 🎯 주요 메서드

### CRUD와 매핑

```
Create  → POST   (생성)
Read    → GET    (조회)
Update  → PUT/PATCH (수정)
Delete  → DELETE (삭제)
```

### 메서드별 특징

```
📖 GET (조회)
├── 데이터 가져오기
├── 본문(body) 없음
├── URL에 파라미터 (?name=kim)
└── 브라우저 주소창 = GET

📝 POST (생성)
├── 새 데이터 만들기
├── 본문에 데이터 포함
├── 여러 번 호출 = 여러 개 생성
└── 폼 제출 = POST

✏️ PUT (전체 수정)
├── 데이터 전체 교체
├── 같은 요청 여러 번 = 결과 동일
└── 없으면 생성도 가능

🩹 PATCH (부분 수정)
├── 일부만 수정
└── 변경할 필드만 전송

🗑️ DELETE (삭제)
├── 데이터 삭제
└── 같은 요청 여러 번 = 결과 동일
```"""
            },
            {
                "type": "code",
                "title": "💻 메서드 사용 예시",
                "content": """### REST API 예시

```http
# 유저 목록 조회
GET /users HTTP/1.1

# 특정 유저 조회
GET /users/1 HTTP/1.1

# 유저 생성
POST /users HTTP/1.1
Content-Type: application/json

{"name": "김철수", "email": "kim@test.com"}

# 유저 전체 수정
PUT /users/1 HTTP/1.1
Content-Type: application/json

{"name": "김철수", "email": "kim2@test.com", "age": 30}

# 유저 부분 수정
PATCH /users/1 HTTP/1.1
Content-Type: application/json

{"email": "newemail@test.com"}

# 유저 삭제
DELETE /users/1 HTTP/1.1
```

### Python 예시

```python
import requests

# GET
users = requests.get('/users').json()

# POST
new_user = requests.post('/users', json={
    'name': '김철수'
}).json()

# PUT
requests.put('/users/1', json={
    'name': '김철수',
    'email': 'new@test.com'
})

# PATCH
requests.patch('/users/1', json={
    'email': 'new@test.com'
})

# DELETE
requests.delete('/users/1')
```"""
            },
            {
                "type": "tip",
                "title": "💡 안전성과 멱등성",
                "content": """### 개념 정리

```
안전(Safe): 서버 데이터 안 바뀜
멱등(Idempotent): 여러 번 해도 결과 같음

GET: 안전 O, 멱등 O
POST: 안전 X, 멱등 X (호출할 때마다 새로 생성)
PUT: 안전 X, 멱등 O (덮어쓰기)
PATCH: 안전 X, 멱등 X (상황에 따라 다름)
DELETE: 안전 X, 멱등 O (이미 삭제돼도 결과 같음)
```

### PUT vs PATCH

```
PUT: 전체 교체
├── 보내지 않은 필드 = 삭제/초기화
└── 전체 데이터 필요

PATCH: 부분 수정
├── 보낸 필드만 수정
└── 변경할 것만 전송
```"""
            }
        ]
    },

    "03_HTTP/http-status-code": {
        "title": "HTTP 상태 코드",
        "description": "HTTP 응답 상태 코드의 의미를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 상태 코드란?",
                "content": """## 🔥 한 줄 요약
> **서버 응답의 결과를 숫자로** - "성공!", "못 찾음!", "서버 에러!"

---

## 🎯 상태 코드 분류

```
1xx: 정보 (거의 안 씀)
2xx: 성공 ✅
3xx: 리다이렉션 ↪️
4xx: 클라이언트 에러 ❌ (너 잘못)
5xx: 서버 에러 💥 (내 잘못)
```

---

## 🎯 자주 쓰는 코드

### 2xx 성공

```
200 OK
└── 성공! (가장 흔함)

201 Created
└── 생성 성공! (POST 후)

204 No Content
└── 성공인데 보낼 데이터 없음 (DELETE 후)
```

### 3xx 리다이렉션

```
301 Moved Permanently
└── 영구 이동 (북마크 변경됨)

302 Found
└── 임시 이동

304 Not Modified
└── 캐시 사용해 (변경 없음)
```

### 4xx 클라이언트 에러

```
400 Bad Request
└── 잘못된 요청 (파라미터 오류)

401 Unauthorized
└── 인증 필요 (로그인 해!)

403 Forbidden
└── 권한 없음 (로그인 했지만 접근 불가)

404 Not Found
└── 못 찾음 (URL 오류)

409 Conflict
└── 충돌 (이미 존재)

429 Too Many Requests
└── 요청 너무 많음 (rate limit)
```

### 5xx 서버 에러

```
500 Internal Server Error
└── 서버 에러 (코드 버그!)

502 Bad Gateway
└── 게이트웨이 에러 (프록시 문제)

503 Service Unavailable
└── 서버 과부하/점검 중

504 Gateway Timeout
└── 타임아웃
```"""
            },
            {
                "type": "code",
                "title": "💻 상태 코드 처리",
                "content": """### 프론트엔드에서 처리

```javascript
try {
    const response = await fetch('/api/users');

    if (response.ok) {  // 200-299
        const data = await response.json();
    } else if (response.status === 401) {
        // 로그인 페이지로
        window.location.href = '/login';
    } else if (response.status === 404) {
        alert('데이터를 찾을 수 없습니다');
    } else if (response.status >= 500) {
        alert('서버 에러가 발생했습니다');
    }
} catch (error) {
    alert('네트워크 에러');
}
```

### 백엔드에서 반환

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users/<int:id>')
def get_user(id):
    user = find_user(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    # 유효성 검사 실패
    if not valid:
        return jsonify({'error': 'Invalid data'}), 400

    user = create(data)
    return jsonify(user), 201  # Created
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 자주 실수하는 것

```
❌ 모든 에러에 500 반환
✅ 상황에 맞는 코드 사용

❌ 에러인데 200 반환
✅ 실패하면 4xx/5xx

❌ 401과 403 혼동
401: 인증 안 됨 (로그인 필요)
403: 인증 됐지만 권한 없음
```

### API 설계 시

```
GET 성공: 200 + 데이터
POST 성공: 201 + 생성된 데이터
PUT/PATCH 성공: 200 + 수정된 데이터
DELETE 성공: 204 (No Content)
```"""
            }
        ]
    },

    "03_HTTP/http-header": {
        "title": "HTTP 헤더",
        "description": "HTTP 헤더의 종류와 역할을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 HTTP 헤더란?",
                "content": """## 🔥 한 줄 요약
> **요청/응답의 부가 정보** - 편지의 봉투 정보!

---

## 🎯 헤더 분류

### 요청 헤더

```
Host: api.example.com
└── 요청할 서버

Accept: application/json
└── 원하는 응답 형식

Authorization: Bearer token
└── 인증 정보

Content-Type: application/json
└── 보내는 데이터 형식

User-Agent: Chrome/91.0
└── 브라우저/클라이언트 정보

Cookie: session=abc123
└── 쿠키 전송
```

### 응답 헤더

```
Content-Type: text/html
└── 응답 데이터 형식

Content-Length: 1234
└── 응답 크기 (바이트)

Set-Cookie: session=abc123
└── 쿠키 설정

Cache-Control: max-age=3600
└── 캐시 설정

Location: /new-page
└── 리다이렉트 위치

Access-Control-Allow-Origin: *
└── CORS 설정
```"""
            },
            {
                "type": "code",
                "title": "💻 헤더 사용 예시",
                "content": """### 요청에 헤더 추가

```python
import requests

response = requests.get(
    'https://api.example.com/users',
    headers={
        'Authorization': 'Bearer my-token',
        'Accept': 'application/json',
        'X-Custom-Header': 'custom-value'
    }
)

# 응답 헤더 확인
print(response.headers['Content-Type'])
```

### JavaScript (fetch)

```javascript
const response = await fetch('/api/data', {
    headers: {
        'Authorization': 'Bearer token',
        'Content-Type': 'application/json',
    }
});

// 응답 헤더 확인
console.log(response.headers.get('Content-Type'));
```

### 서버에서 헤더 설정

```python
from flask import Flask, jsonify, make_response

@app.route('/data')
def get_data():
    response = make_response(jsonify({'data': 'value'}))
    response.headers['X-Custom-Header'] = 'value'
    response.headers['Cache-Control'] = 'no-cache'
    return response
```"""
            },
            {
                "type": "tip",
                "title": "💡 중요한 헤더",
                "content": """### Content-Type 종류

```
text/html              - HTML
text/plain             - 일반 텍스트
application/json       - JSON
application/xml        - XML
multipart/form-data    - 파일 업로드
application/x-www-form-urlencoded - 폼 데이터
```

### 캐시 관련 헤더

```
Cache-Control: no-cache
└── 캐시 안 함

Cache-Control: max-age=3600
└── 1시간 캐시

ETag: "abc123"
└── 버전 태그 (변경 감지)

If-None-Match: "abc123"
└── 변경됐으면 보내줘
```"""
            }
        ]
    },

    "03_HTTP/http-version": {
        "title": "HTTP 버전",
        "description": "HTTP/1.1, HTTP/2, HTTP/3의 차이를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 HTTP 버전 비교",
                "content": """## 🎯 버전 역사

```
HTTP/0.9 (1991): HTML만 전송
HTTP/1.0 (1996): 헤더, 상태코드 추가
HTTP/1.1 (1997): 지속 연결 (현재 대부분)
HTTP/2 (2015): 멀티플렉싱, 헤더 압축
HTTP/3 (2022): UDP 기반 (QUIC)
```

---

## 🎯 버전별 특징

### HTTP/1.1

```
한 번에 하나씩:
요청1 → 응답1 → 요청2 → 응답2

문제:
├── 순서대로 처리 (Head-of-line blocking)
├── 매 요청마다 헤더 반복
└── 연결 여러 개로 해결 (최대 6개)
```

### HTTP/2

```
동시에 여러 개:
요청1, 요청2, 요청3 → 응답들이 뒤섞여 도착

장점:
├── 멀티플렉싱 (하나의 연결로 동시 요청)
├── 헤더 압축 (HPACK)
├── 서버 푸시 (요청 전에 미리 전송)
└── 바이너리 프레임
```

### HTTP/3

```
QUIC 프로토콜 (UDP 기반):

장점:
├── 연결 설정 빠름 (0-RTT)
├── 패킷 손실에 강함
├── 모바일 환경 최적화
└── 내장 암호화 (TLS 1.3)
```"""
            },
            {
                "type": "code",
                "title": "💻 버전 확인",
                "content": """### 브라우저에서 확인

```
Chrome 개발자 도구 (F12)
└── Network 탭
    └── Protocol 열 확인
        ├── h2 = HTTP/2
        ├── h3 = HTTP/3
        └── http/1.1 = HTTP/1.1
```

### curl로 확인

```bash
# HTTP 버전 지정
curl --http1.1 https://example.com
curl --http2 https://example.com
curl --http3 https://example.com

# 사용된 프로토콜 확인
curl -I -s https://google.com | grep -i 'http/'
```

### 서버에서 HTTP/2 활성화

```nginx
# Nginx
server {
    listen 443 ssl http2;
    # ...
}
```

```python
# Python (hypercorn)
# hypercorn --bind 0.0.0.0:443 app:app
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 언제 어떤 버전?

```
HTTP/1.1:
├── 레거시 시스템
├── 간단한 API

HTTP/2:
├── 대부분의 웹사이트 (권장)
├── 많은 리소스 로딩

HTTP/3:
├── 모바일 앱
├── 불안정한 네트워크
├── 실시간 스트리밍
```

### 현재 지원 현황

```
대부분의 브라우저: HTTP/2 기본
최신 브라우저: HTTP/3 지원
서버: Nginx, Cloudflare 등 지원
```"""
            }
        ]
    },

    "03_HTTP/https": {
        "title": "HTTPS",
        "description": "HTTPS의 원리와 중요성을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 HTTPS란?",
                "content": """## 🔥 한 줄 요약
> **HTTP + 암호화** - 도청 방지 보안 통신!

---

## 💡 왜 필요한가?

### HTTP의 문제

```
📱 카페 와이파이에서 HTTP 사용 시:

나 ──────────── 해커 ──────────── 서버
      "비밀번호: 1234"
           ↓
      해커: "야호! 비밀번호 1234!"

→ 중간에서 훔쳐볼 수 있음 (스니핑)
→ 내용 변조 가능
```

### HTTPS 사용 시

```
나 ────🔒──── 해커 ────🔒──── 서버
   "Xk3#@!9z..."
        ↓
   해커: "뭔 소리야?"

→ 암호화되어 해독 불가
→ 변조 감지 가능
```

---

## 🎯 HTTPS가 제공하는 것

```
1. 기밀성 (Confidentiality)
   └── 내용 암호화 (도청 방지)

2. 무결성 (Integrity)
   └── 변조 감지 (중간에 수정 불가)

3. 인증 (Authentication)
   └── 서버 신원 확인 (피싱 방지)
```"""
            },
            {
                "type": "code",
                "title": "💻 HTTPS 적용",
                "content": """### 인증서 발급 (Let's Encrypt 무료)

```bash
# certbot 설치 (Ubuntu)
sudo apt install certbot python3-certbot-nginx

# 인증서 발급 + Nginx 자동 설정
sudo certbot --nginx -d example.com -d www.example.com

# 인증서 갱신 (자동)
sudo certbot renew --dry-run
```

### Nginx HTTPS 설정

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # 보안 설정
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
}

# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### 브라우저에서 확인

```
🔒 자물쇠 아이콘 클릭
└── 인증서 정보 확인
    ├── 발급 대상
    ├── 발급 기관
    └── 유효 기간
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### 필수 적용

```
✅ HTTPS 필수인 경우
├── 로그인/회원가입
├── 결제
├── 개인정보 입력
├── PWA
└── HTTP/2 (HTTPS 필수)

실제로: 모든 사이트에 HTTPS 권장
Chrome: HTTP 사이트에 "안전하지 않음" 표시
```

### 주의사항

```
Mixed Content:
├── HTTPS 페이지에서 HTTP 리소스 로드
├── 브라우저가 차단!
└── 모든 리소스 HTTPS로

인증서 갱신:
├── Let's Encrypt: 90일
├── 자동 갱신 설정 필수
└── 만료되면 사이트 접속 불가
```"""
            }
        ]
    },

    "03_HTTP/tls-handshake": {
        "title": "TLS Handshake",
        "description": "HTTPS 연결의 TLS 핸드셰이크를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 TLS Handshake란?",
                "content": """## 🔥 한 줄 요약
> **HTTPS 연결 전 암호화 협상** - "어떤 암호 쓸까?"

---

## 🎯 TLS 1.2 Handshake

```
클라이언트                     서버
    │                           │
    │─── ClientHello ──────────▶│
    │   "나 TLS 쓸 수 있어,     │
    │    이런 암호들 가능해"      │
    │                           │
    │◀── ServerHello ───────────│
    │   "이 암호 쓰자,          │
    │    내 인증서야"            │
    │                           │
    │◀── Certificate ───────────│
    │   (서버 인증서)            │
    │                           │
    │─── 키 교환 ──────────────▶│
    │   (비밀키 생성 재료)        │
    │                           │
    │◀── Finished ──────────────│
    │                           │
    │─── Finished ─────────────▶│
    │                           │
    │◀═══ 암호화 통신 시작 ═════▶│
```

---

## 🎯 TLS 1.3 (더 빠름!)

```
1-RTT Handshake:

클라이언트 → 서버: ClientHello + 키 공유
서버 → 클라이언트: ServerHello + 키 공유 + 인증서

끝! 바로 암호화 통신 시작

→ TLS 1.2보다 1 왕복 절약
→ 더 빠른 연결
```"""
            },
            {
                "type": "code",
                "title": "💻 TLS 확인",
                "content": """### OpenSSL로 확인

```bash
# TLS 연결 테스트
openssl s_client -connect google.com:443

# 출력:
# Protocol  : TLSv1.3
# Cipher    : TLS_AES_256_GCM_SHA384
# Certificate chain
#  0 s:CN = www.google.com
#    i:C = US, O = Google Trust Services
```

### 인증서 정보 확인

```bash
# 인증서 상세 정보
openssl s_client -connect google.com:443 | openssl x509 -text

# 만료일만 확인
echo | openssl s_client -connect google.com:443 2>/dev/null | openssl x509 -noout -dates
```

### curl로 TLS 버전 확인

```bash
curl -v https://google.com 2>&1 | grep "SSL connection"
# SSL connection using TLSv1.3
```"""
            },
            {
                "type": "tip",
                "title": "💡 보안 설정",
                "content": """### 권장 TLS 설정

```
✅ 사용
├── TLS 1.3 (최신)
├── TLS 1.2 (호환성)

❌ 사용 금지
├── TLS 1.1 이하
├── SSL 3.0
└── 취약한 암호 스위트
```

### HSTS (HTTP Strict Transport Security)

```
브라우저에게 "항상 HTTPS로 접속해" 지시

Strict-Transport-Security: max-age=31536000; includeSubDomains

→ 1년간 HTTPS만 사용
→ HTTP로 접속 시도 시 자동으로 HTTPS로 변환
```"""
            }
        ]
    },

    "04_REST/rest-concept": {
        "title": "REST 개념",
        "description": "REST 아키텍처의 원칙을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 REST란?",
                "content": """## 🔥 한 줄 요약
> **URL로 자원을 나타내고, HTTP 메서드로 행위를 표현** - API 설계 규칙!

---

## 💡 왜 배워야 하나?

```
🌐 현대 웹 API의 90% = REST

프론트엔드: "유저 정보 어떻게 받아요?"
백엔드: "GET /users/1 호출하세요"

→ REST를 알면 API가 직관적!
```

---

## 🎯 REST 원칙

### 1. 자원(Resource) 중심

```
모든 것은 자원(명사)!

❌ /getUsers        (동사)
❌ /createUser      (동사)
✅ /users           (명사, 복수형)
✅ /users/1         (특정 자원)
```

### 2. HTTP 메서드로 행위 표현

```
자원 + 메서드 = 행위

GET    /users     = 유저 목록 조회
GET    /users/1   = 유저 1번 조회
POST   /users     = 유저 생성
PUT    /users/1   = 유저 1번 수정
DELETE /users/1   = 유저 1번 삭제
```

### 3. 무상태(Stateless)

```
서버가 클라이언트 상태 저장 X
모든 요청은 독립적

→ 매 요청에 필요한 정보 모두 포함
→ 토큰으로 인증
```"""
            },
            {
                "type": "code",
                "title": "💻 REST API 예시",
                "content": """### 게시판 API 설계

```
# 게시글 목록
GET /posts

# 게시글 상세
GET /posts/1

# 게시글 작성
POST /posts
Body: {"title": "제목", "content": "내용"}

# 게시글 수정
PUT /posts/1
Body: {"title": "새 제목", "content": "새 내용"}

# 게시글 삭제
DELETE /posts/1

# 게시글의 댓글 목록
GET /posts/1/comments

# 댓글 작성
POST /posts/1/comments
Body: {"content": "댓글 내용"}
```

### 쿼리 파라미터 활용

```
# 페이지네이션
GET /posts?page=1&limit=10

# 정렬
GET /posts?sort=created_at&order=desc

# 필터링
GET /posts?category=tech&author=kim

# 검색
GET /posts?q=키워드
```

### 응답 예시

```json
// GET /posts/1
{
    "id": 1,
    "title": "REST API란?",
    "content": "...",
    "author": {
        "id": 100,
        "name": "김철수"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "_links": {
        "self": "/posts/1",
        "comments": "/posts/1/comments"
    }
}
```"""
            },
            {
                "type": "tip",
                "title": "💡 REST 팁",
                "content": """### URL 설계 규칙

```
✅ 좋은 예
/users
/users/123
/users/123/orders
/products?category=electronics

❌ 나쁜 예
/getUsers
/user_list
/users/123/get
/UsersOrders
```

### 상태 코드 활용

```
200: 조회 성공
201: 생성 성공
204: 삭제 성공 (No Content)
400: 잘못된 요청
401: 인증 필요
403: 권한 없음
404: 자원 없음
500: 서버 에러
```"""
            }
        ]
    },

    "04_REST/restful-api": {
        "title": "RESTful API",
        "description": "RESTful API 설계 원칙을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 RESTful이란?",
                "content": """## 🔥 한 줄 요약
> **REST 원칙을 잘 지킨 API** - "제대로 된 REST"

---

## 🎯 RESTful 체크리스트

```
✅ URL은 자원(명사) 표현
✅ 행위는 HTTP 메서드로
✅ 복수형 명사 사용 (/users)
✅ 계층 구조 표현 (/users/1/posts)
✅ 적절한 상태 코드 반환
✅ 버전 관리 (/v1/users)
```

---

## 🎯 안티패턴 vs 좋은 예

```
❌ GET /getUser?id=1
✅ GET /users/1

❌ POST /users/delete/1
✅ DELETE /users/1

❌ GET /users/1/posts/create
✅ POST /users/1/posts

❌ POST /search/users
✅ GET /users?q=keyword
```"""
            },
            {
                "type": "code",
                "title": "💻 RESTful API 구현",
                "content": """### Flask로 구현

```python
from flask import Flask, jsonify, request

app = Flask(__name__)
users = {}

# GET /users - 목록 조회
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

# GET /users/:id - 상세 조회
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    if id not in users:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(users[id]), 200

# POST /users - 생성
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    id = len(users) + 1
    users[id] = {'id': id, **data}
    return jsonify(users[id]), 201

# PUT /users/:id - 수정
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    if id not in users:
        return jsonify({'error': 'Not found'}), 404
    users[id].update(request.json)
    return jsonify(users[id]), 200

# DELETE /users/:id - 삭제
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    if id not in users:
        return jsonify({'error': 'Not found'}), 404
    del users[id]
    return '', 204
```"""
            },
            {
                "type": "tip",
                "title": "💡 실무 팁",
                "content": """### API 버전 관리

```
방법 1: URL에 버전
/v1/users
/v2/users

방법 2: 헤더에 버전
Accept: application/vnd.api+json;version=1

→ URL 방식이 직관적 (많이 사용)
```

### 에러 응답 형식

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "유저를 찾을 수 없습니다",
        "details": {
            "user_id": 123
        }
    }
}
```"""
            }
        ]
    },

    "04_REST/rest-design": {
        "title": "REST API 설계",
        "description": "실무 REST API 설계 방법을 학습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 API 설계 패턴",
                "content": """## 🎯 URL 설계

### 계층 구조

```
/users                    # 유저 목록
/users/{id}               # 특정 유저
/users/{id}/orders        # 유저의 주문 목록
/users/{id}/orders/{id}   # 특정 주문
```

### 쿼리 파라미터

```
페이지네이션:
?page=1&per_page=20
?offset=0&limit=20
?cursor=abc123 (커서 기반)

필터링:
?status=active
?created_after=2024-01-01

정렬:
?sort=created_at
?sort=-created_at (역순, - 접두사)
?sort=name,asc
```

---

## 🎯 응답 설계

### 단일 자원

```json
{
    "id": 1,
    "name": "김철수",
    "email": "kim@test.com",
    "created_at": "2024-01-15T10:00:00Z"
}
```

### 목록 (페이지네이션)

```json
{
    "data": [
        {"id": 1, "name": "김철수"},
        {"id": 2, "name": "이영희"}
    ],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "total_pages": 5
    }
}
```"""
            },
            {
                "type": "code",
                "title": "💻 설계 예시",
                "content": """### 쇼핑몰 API 설계

```
# 상품
GET    /products              # 상품 목록
GET    /products/:id          # 상품 상세
POST   /products              # 상품 등록 (관리자)
PUT    /products/:id          # 상품 수정
DELETE /products/:id          # 상품 삭제

# 장바구니
GET    /cart                  # 내 장바구니
POST   /cart/items            # 장바구니 추가
PATCH  /cart/items/:id        # 수량 변경
DELETE /cart/items/:id        # 항목 삭제

# 주문
GET    /orders                # 내 주문 목록
GET    /orders/:id            # 주문 상세
POST   /orders                # 주문 생성
PATCH  /orders/:id/cancel     # 주문 취소

# 리뷰
GET    /products/:id/reviews  # 상품 리뷰 목록
POST   /products/:id/reviews  # 리뷰 작성
```

### 복잡한 검색

```
# 방법 1: GET + 쿼리 파라미터
GET /products?category=electronics&min_price=100&max_price=500

# 방법 2: POST + Body (복잡한 검색)
POST /products/search
{
    "filters": {
        "category": ["electronics", "fashion"],
        "price": {"min": 100, "max": 500},
        "rating": {"gte": 4}
    },
    "sort": {"field": "price", "order": "asc"}
}
```"""
            },
            {
                "type": "tip",
                "title": "💡 설계 원칙",
                "content": """### 일관성 유지

```
✅ 모든 API에서 동일한 패턴

응답 형식 통일
에러 형식 통일
인증 방식 통일
네이밍 컨벤션 통일
```

### 문서화

```
Swagger/OpenAPI로 문서 자동 생성
→ 프론트엔드 개발자가 쉽게 이해
→ API 테스트도 가능
```"""
            }
        ]
    },

    "04_REST/rest-vs-graphql": {
        "title": "REST vs GraphQL",
        "description": "REST와 GraphQL의 차이점을 비교합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔥 REST vs GraphQL",
                "content": """## 🎯 비교

### REST
```
여러 엔드포인트, 고정된 응답

GET /users/1
GET /users/1/posts
GET /users/1/followers

→ 3번의 요청
→ 불필요한 데이터도 받음 (Over-fetching)
→ 필요한 데이터 부족할 수 있음 (Under-fetching)
```

### GraphQL
```
하나의 엔드포인트, 원하는 데이터만

POST /graphql
{
    user(id: 1) {
        name
        posts { title }
        followers { name }
    }
}

→ 1번의 요청
→ 필요한 것만 정확히 받음
```

---

## 🎯 언제 뭘 쓸까?

```
REST:
├── 간단한 CRUD
├── 캐싱 중요
├── 파일 업로드
└── 팀이 익숙함

GraphQL:
├── 복잡한 관계 데이터
├── 모바일 앱 (대역폭 절약)
├── 프론트엔드 주도 개발
└── 빠른 프로토타이핑
```"""
            },
            {
                "type": "code",
                "title": "💻 비교 예시",
                "content": """### 같은 기능, 다른 방식

```
# REST: 유저 + 게시글 + 팔로워 조회

GET /users/1
GET /users/1/posts
GET /users/1/followers

# 응답 3개, 불필요한 필드 포함
```

```graphql
# GraphQL: 한 번에

query {
    user(id: 1) {
        name
        email
        posts(limit: 5) {
            title
            createdAt
        }
        followers {
            name
        }
    }
}

# 응답 1개, 필요한 필드만
```

### Python GraphQL (Strawberry)

```python
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return get_user(id)

schema = strawberry.Schema(query=Query)
app = FastAPI()
app.add_route("/graphql", GraphQL(schema))
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 결정 기준

```
데이터 구조 복잡? → GraphQL
캐싱 중요? → REST
팀 경험? → 익숙한 것
마이크로서비스? → REST (API Gateway)
```

### 하이브리드 접근

```
많은 회사들:
├── 외부 API: REST
├── 내부 BFF: GraphQL
└── 상황에 맞게 선택
```"""
            }
        ]
    }
}

for key, content in network_contents.items():
    if key in data:
        data[key].update({
            "title": content["title"],
            "description": content["description"],
            "sections": content["sections"],
            "isPlaceholder": False
        })

with open('src/data/contents/network.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 03_HTTP, 04_REST 섹션 업데이트 완료: {len(network_contents)}개 토픽")
