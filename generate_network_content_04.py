# -*- coding: utf-8 -*-
"""
네트워크 콘텐츠 생성 스크립트 - Part 4
07_실시간, 08_고급/기타, 09_면접, index 섹션 (11개 토픽)
"""

import json
import os
import sys

# 파일 경로
NETWORK_JSON_PATH = "src/data/contents/network.json"

# 07_실시간 섹션 콘텐츠
REALTIME_CONTENTS = {
    "07_실시간/websocket": {
        "title": "WebSocket",
        "description": "WebSocket 양방향 실시간 통신을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔌 WebSocket이란?",
                "content": """## 🔌 한 줄 요약
> **전화 통화처럼 연결 유지** - 서버와 클라이언트가 실시간으로 대화해요!

---

## 💡 왜 WebSocket이 필요한가?

### HTTP의 한계:
```
HTTP = 편지 주고받기 📬

클라이언트: "새 메시지 있어?" → 서버: "없어"
클라이언트: "새 메시지 있어?" → 서버: "없어"
클라이언트: "새 메시지 있어?" → 서버: "있어!"

→ 계속 물어봐야 함 (폴링)
→ 비효율적! 😩
```

### WebSocket으로 해결:
```
WebSocket = 전화 통화 📞

1. 연결 (핸드셰이크)
2. 서버: "새 메시지 왔어!" (즉시 알림)
3. 클라이언트: "답장 보낼게!" (즉시 전송)
4. 연결 유지...

→ 물어볼 필요 없이 바로 알림!
→ 실시간! ⚡
```

---

## 🎯 WebSocket 동작 방식

### 연결 과정:
```
클라이언트                    서버
    │                         │
    │ GET /chat HTTP/1.1      │
    │ Upgrade: websocket      │
    │ Connection: Upgrade     │
    │────────────────────────►│
    │                         │
    │ HTTP/1.1 101 Switching  │
    │ Upgrade: websocket      │
    │◄────────────────────────│
    │                         │
    │════ WebSocket 연결 ═════│
    │                         │
    │◄───── 메시지 ──────────►│
    │◄───── 메시지 ──────────►│
```

### HTTP vs WebSocket:
```
┌─────────────┬──────────────┬──────────────┐
│             │ HTTP         │ WebSocket    │
├─────────────┼──────────────┼──────────────┤
│ 연결        │ 요청마다 새로 │ 한 번 연결   │
│ 방향        │ 단방향       │ 양방향       │
│ 오버헤드    │ 큼 (헤더)    │ 작음         │
│ 실시간성    │ 낮음         │ 높음         │
│ 용도        │ 일반 웹      │ 채팅, 게임   │
└─────────────┴──────────────┴──────────────┘
```"""
            },
            {
                "type": "code",
                "title": "💻 WebSocket 구현",
                "content": """### 클라이언트 (브라우저)

```javascript
// WebSocket 연결
const socket = new WebSocket('wss://example.com/chat');

// 연결 성공
socket.onopen = () => {
  console.log('연결됨!');
  socket.send('안녕하세요!');
};

// 메시지 수신
socket.onmessage = (event) => {
  console.log('받은 메시지:', event.data);

  // JSON 메시지인 경우
  const data = JSON.parse(event.data);
  console.log(data);
};

// 연결 종료
socket.onclose = (event) => {
  console.log('연결 종료:', event.code, event.reason);
};

// 에러 발생
socket.onerror = (error) => {
  console.error('에러:', error);
};

// 메시지 보내기
function sendMessage(message) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'chat', text: message }));
  }
}

// 연결 종료
function disconnect() {
  socket.close(1000, '정상 종료');
}
```

### 서버 (Node.js + ws)

```javascript
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

// 연결된 클라이언트 목록
const clients = new Set();

wss.on('connection', (ws) => {
  console.log('새 클라이언트 연결');
  clients.add(ws);

  // 메시지 수신
  ws.on('message', (message) => {
    console.log('받은 메시지:', message.toString());

    // 모든 클라이언트에게 브로드캐스트
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message.toString());
      }
    });
  });

  // 연결 종료
  ws.on('close', () => {
    console.log('클라이언트 연결 종료');
    clients.delete(ws);
  });

  // 에러
  ws.on('error', (error) => {
    console.error('에러:', error);
  });

  // 환영 메시지
  ws.send(JSON.stringify({ type: 'welcome', message: '연결 성공!' }));
});

console.log('WebSocket 서버 시작: ws://localhost:8080');
```

### Socket.IO (더 편리한 라이브러리)

```javascript
// 서버
const io = require('socket.io')(3000);

io.on('connection', (socket) => {
  console.log('연결:', socket.id);

  // 방 입장
  socket.join('room1');

  // 이벤트 수신
  socket.on('chat', (data) => {
    // 특정 방에만 전송
    io.to('room1').emit('chat', data);
  });

  socket.on('disconnect', () => {
    console.log('연결 종료');
  });
});

// 클라이언트
const socket = io('http://localhost:3000');

socket.on('connect', () => {
  console.log('연결됨!');
});

socket.emit('chat', { message: '안녕!' });

socket.on('chat', (data) => {
  console.log('메시지:', data);
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 WebSocket 실전 팁",
                "content": """### 사용 사례

```
1. 채팅 앱 💬
2. 실시간 알림 🔔
3. 온라인 게임 🎮
4. 주식/코인 시세 📈
5. 협업 도구 (Google Docs) 📝
6. IoT 대시보드 📊
```

### 연결 유지 (Heartbeat)

```javascript
// 클라이언트
setInterval(() => {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'ping' }));
  }
}, 30000); // 30초마다

// 서버
ws.on('message', (message) => {
  const data = JSON.parse(message);
  if (data.type === 'ping') {
    ws.send(JSON.stringify({ type: 'pong' }));
  }
});
```

### 재연결 로직

```javascript
function connect() {
  const socket = new WebSocket('wss://example.com');

  socket.onclose = () => {
    console.log('연결 끊김, 3초 후 재연결...');
    setTimeout(connect, 3000);
  };

  socket.onerror = () => {
    socket.close();
  };
}

connect();
```

### 보안 고려사항

```
1. wss:// 사용 (TLS 암호화)
2. 인증 토큰 전송
   ├── URL 파라미터
   └── 첫 메시지로 전송
3. 메시지 검증
4. Rate limiting
5. 연결 수 제한
```"""
            }
        ]
    },

    "07_실시간/sse": {
        "title": "SSE",
        "description": "Server-Sent Events로 서버 푸시를 구현합니다",
        "sections": [
            {
                "type": "concept",
                "title": "📡 SSE란?",
                "content": """## 📡 한 줄 요약
> **서버가 일방적으로 알려주기** - 뉴스 속보처럼 서버가 클라이언트에게 푸시해요!

---

## 💡 SSE vs WebSocket

### SSE (Server-Sent Events):
```
📺 TV 뉴스처럼
├── 방송국(서버) → 시청자(클라이언트)
├── 단방향 (서버 → 클라이언트만)
├── HTTP 사용 (간단!)
└── 자동 재연결
```

### WebSocket:
```
📞 전화 통화처럼
├── 양방향 (서버 ↔ 클라이언트)
├── 전용 프로토콜
├── 더 복잡
└── 수동 재연결
```

### 선택 기준:
```
SSE 적합:
├── 서버 → 클라이언트 단방향
├── 실시간 알림
├── 뉴스 피드
├── 주식 시세
└── 간단한 구현 원할 때

WebSocket 적합:
├── 양방향 필요
├── 채팅
├── 게임
├── 협업 도구
└── 복잡한 실시간 기능
```

---

## 🎯 SSE 동작 방식

```
클라이언트                    서버
    │                         │
    │ GET /events             │
    │ Accept: text/           │
    │   event-stream          │
    │────────────────────────►│
    │                         │
    │◄──────── 연결 유지 ──────│
    │                         │
    │◄──── event: update ─────│
    │◄──── data: {...} ───────│
    │                         │
    │◄──── event: alert ──────│
    │◄──── data: {...} ───────│
    │          ...            │
```

### SSE 메시지 형식:
```
event: update
data: {"price": 50000}

event: alert
data: {"message": "급등!"}
id: 123
retry: 3000
```"""
            },
            {
                "type": "code",
                "title": "💻 SSE 구현",
                "content": """### 클라이언트 (브라우저)

```javascript
// SSE 연결
const eventSource = new EventSource('/events');

// 기본 메시지 수신
eventSource.onmessage = (event) => {
  console.log('메시지:', event.data);
};

// 특정 이벤트 수신
eventSource.addEventListener('update', (event) => {
  const data = JSON.parse(event.data);
  console.log('업데이트:', data);
});

eventSource.addEventListener('alert', (event) => {
  const data = JSON.parse(event.data);
  alert(data.message);
});

// 연결 상태
eventSource.onopen = () => {
  console.log('연결됨!');
};

eventSource.onerror = (error) => {
  console.error('에러:', error);
  // 자동 재연결됨!
};

// 연결 종료
function disconnect() {
  eventSource.close();
}
```

### 서버 (Express)

```javascript
const express = require('express');
const app = express();

app.get('/events', (req, res) => {
  // SSE 헤더 설정
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // 클라이언트에게 이벤트 전송 함수
  const sendEvent = (event, data) => {
    res.write(`event: ${event}\\n`);
    res.write(`data: ${JSON.stringify(data)}\\n\\n`);
  };

  // 환영 메시지
  sendEvent('welcome', { message: '연결 성공!' });

  // 주기적으로 데이터 전송
  const interval = setInterval(() => {
    sendEvent('update', {
      time: new Date().toISOString(),
      price: Math.random() * 100
    });
  }, 1000);

  // 연결 종료 시 정리
  req.on('close', () => {
    clearInterval(interval);
    console.log('클라이언트 연결 종료');
  });
});

app.listen(3000);
```

### Python Flask

```python
from flask import Flask, Response
import json
import time

app = Flask(__name__)

@app.route('/events')
def events():
    def generate():
        while True:
            data = {
                'time': time.strftime('%H:%M:%S'),
                'value': 123
            }
            yield f"event: update\\n"
            yield f"data: {json.dumps(data)}\\n\\n"
            time.sleep(1)

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )
```

### 인증 포함 (JWT)

```javascript
// URL 파라미터로 토큰 전달
const token = localStorage.getItem('token');
const eventSource = new EventSource(`/events?token=${token}`);

// 서버에서 검증
app.get('/events', (req, res) => {
  const token = req.query.token;
  const user = verifyToken(token);

  if (!user) {
    return res.status(401).send('Unauthorized');
  }

  // SSE 설정...
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 SSE 실전 팁",
                "content": """### 장단점

```
장점:
├── 간단한 구현 (HTTP 사용)
├── 자동 재연결 내장
├── 브라우저 기본 지원
├── 방화벽 통과 쉬움
└── 적은 오버헤드

단점:
├── 단방향 (서버→클라이언트)
├── 브라우저당 6개 연결 제한
├── 바이너리 전송 불가
└── IE 미지원 (폴리필 필요)
```

### 사용 사례

```
1. 실시간 알림 🔔
2. 주식/코인 시세 📈
3. 스포츠 경기 점수 ⚽
4. 뉴스 피드 📰
5. 진행률 표시 📊
6. 로그 스트리밍 📝
```

### Last-Event-ID (재연결 시)

```javascript
// 서버: ID 포함하여 전송
res.write(`id: 123\\n`);
res.write(`data: {...}\\n\\n`);

// 클라이언트가 재연결하면
// Last-Event-ID: 123 헤더 자동 전송

// 서버에서 확인
app.get('/events', (req, res) => {
  const lastId = req.headers['last-event-id'];
  if (lastId) {
    // 해당 ID 이후의 이벤트부터 전송
  }
});
```

### 재연결 간격 조정

```javascript
// 서버에서 지정
res.write(`retry: 5000\\n\\n`); // 5초 후 재연결
```

### SSE vs 폴링 vs WebSocket

```
📊 비교표

폴링: 10초마다 요청 → 10초 지연
SSE: 즉시 푸시 → 0초 지연
WebSocket: 즉시 푸시 → 0초 지연

연결 수 (1000명 기준):
폴링: 1000 req/10sec = 6000 req/min
SSE: 1000 연결 유지
WebSocket: 1000 연결 유지

선택:
├── 단방향 + 간단 → SSE ⭐
├── 양방향 필요 → WebSocket
└── 호환성 최우선 → 폴링
```"""
            }
        ]
    },

    "07_실시간/long-polling": {
        "title": "Long Polling",
        "description": "Long Polling 기법의 원리를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "⏳ Long Polling이란?",
                "content": """## ⏳ 한 줄 요약
> **기다렸다가 응답하기** - 새 소식 있을 때까지 서버가 응답을 보류해요!

---

## 💡 폴링 vs Long Polling

### 일반 폴링 (Short Polling):
```
클라이언트: "새 메시지?" → 서버: "없어" (즉시 응답)
(1초 대기)
클라이언트: "새 메시지?" → 서버: "없어" (즉시 응답)
(1초 대기)
클라이언트: "새 메시지?" → 서버: "있어!" (즉시 응답)

문제점:
├── 불필요한 요청 많음
├── 서버 부하
└── 실시간성 낮음
```

### Long Polling:
```
클라이언트: "새 메시지?"
서버: (대기중... 30초)
서버: "있어!" (새 메시지 오면 응답)

클라이언트: "새 메시지?" (바로 다시 요청)
서버: (대기중...)

장점:
├── 불필요한 요청 감소
├── 즉시 응답 가능
└── 호환성 좋음
```

---

## 🎯 Long Polling 동작

```
클라이언트                    서버
    │                         │
    │─── GET /updates ───────►│
    │                         │ (대기...)
    │                         │ (새 데이터 발생!)
    │◄─── 응답: 새 데이터 ────│
    │                         │
    │─── GET /updates ───────►│ (바로 다시 요청)
    │                         │ (대기...)
    │         ...             │
```

### 비교표:
```
┌────────────┬────────────┬────────────┐
│            │ Short Poll │ Long Poll  │
├────────────┼────────────┼────────────┤
│ 요청 빈도   │ 많음      │ 적음       │
│ 지연 시간   │ 폴링 주기  │ 거의 즉시  │
│ 서버 부하   │ 높음      │ 중간       │
│ 구현 복잡도 │ 쉬움      │ 중간       │
│ 연결 유지   │ 짧음      │ 김 (30초)  │
└────────────┴────────────┴────────────┘
```"""
            },
            {
                "type": "code",
                "title": "💻 Long Polling 구현",
                "content": """### 클라이언트 (JavaScript)

```javascript
async function longPoll() {
  try {
    const response = await fetch('/updates', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (response.ok) {
      const data = await response.json();
      console.log('새 데이터:', data);

      // 데이터 처리
      handleUpdate(data);
    }
  } catch (error) {
    console.error('에러:', error);
    // 잠시 대기 후 재시도
    await new Promise(r => setTimeout(r, 1000));
  }

  // 즉시 다시 요청 (재귀)
  longPoll();
}

// 시작
longPoll();

// 타임아웃 설정 버전
async function longPollWithTimeout() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch('/updates', {
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      handleUpdate(data);
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('타임아웃, 재연결...');
    }
  }

  longPollWithTimeout();
}
```

### 서버 (Express)

```javascript
const express = require('express');
const app = express();

// 대기 중인 클라이언트들
const waitingClients = [];

// Long Polling 엔드포인트
app.get('/updates', (req, res) => {
  // 타임아웃 설정 (30초)
  const timeout = setTimeout(() => {
    // 타임아웃 시 빈 응답
    res.json({ data: null, timeout: true });
  }, 30000);

  // 대기 목록에 추가
  const client = { res, timeout };
  waitingClients.push(client);

  // 연결 종료 시 정리
  req.on('close', () => {
    clearTimeout(timeout);
    const index = waitingClients.indexOf(client);
    if (index > -1) {
      waitingClients.splice(index, 1);
    }
  });
});

// 새 데이터 발생 시 모든 클라이언트에게 응답
function notifyAll(data) {
  while (waitingClients.length > 0) {
    const client = waitingClients.shift();
    clearTimeout(client.timeout);
    client.res.json({ data, timeout: false });
  }
}

// 예: 새 메시지 도착
app.post('/message', (req, res) => {
  const message = req.body;
  notifyAll(message);  // 대기 중인 모든 클라이언트에게 전송
  res.json({ success: true });
});
```

### Python Flask

```python
from flask import Flask, jsonify, request
import time
import threading

app = Flask(__name__)
waiting_clients = []
lock = threading.Lock()

@app.route('/updates')
def updates():
    event = threading.Event()
    data = {'result': None}

    with lock:
        waiting_clients.append((event, data))

    # 30초 대기
    has_data = event.wait(timeout=30)

    with lock:
        if (event, data) in waiting_clients:
            waiting_clients.remove((event, data))

    if has_data:
        return jsonify(data['result'])
    else:
        return jsonify({'timeout': True})

def notify_all(new_data):
    with lock:
        for event, data in waiting_clients:
            data['result'] = new_data
            event.set()
```"""
            },
            {
                "type": "tip",
                "title": "💡 Long Polling 팁",
                "content": """### 사용 사례

```
1. 채팅 (WebSocket 못 쓸 때)
2. 알림 시스템
3. 레거시 시스템
4. 방화벽 제약 환경
5. 브라우저 호환성 필요
```

### 장단점

```
장점:
├── 모든 브라우저 지원
├── 기존 HTTP 인프라 사용
├── 프록시/방화벽 통과 쉬움
├── 구현 비교적 간단
└── WebSocket 폴백용

단점:
├── WebSocket보다 오버헤드 큼
├── 서버 연결 유지 부담
├── 타임아웃 관리 필요
├── 단방향 (클라이언트→서버는 별도)
└── 확장성 제한
```

### 타임아웃 설정

```
클라이언트 타임아웃:
├── 보통 30초
├── 프록시 타임아웃 고려 (60초 일반적)
└── 너무 짧으면 요청 많아짐

서버 타임아웃:
├── 클라이언트보다 약간 짧게
├── 빈 응답 또는 keepalive 응답
└── 연결 정리 필수
```

### 실시간 기술 선택 가이드

```
1순위: WebSocket
├── 양방향, 효율적
└── 대부분의 현대 앱

2순위: SSE (Server-Sent Events)
├── 단방향이면 충분할 때
└── 간단한 구현

3순위: Long Polling
├── 레거시 환경
├── WebSocket 차단 시
└── 폴백 용도

4순위: Short Polling
├── 실시간성 낮아도 될 때
└── 가장 간단한 구현
```"""
            }
        ]
    },

    "07_실시간/realtime-compare": {
        "title": "실시간 통신 비교",
        "description": "다양한 실시간 통신 기술을 비교합니다",
        "sections": [
            {
                "type": "concept",
                "title": "⚡ 실시간 통신 총정리",
                "content": """## ⚡ 한 줄 요약
> **목적에 맞는 기술 선택** - 채팅엔 WebSocket, 알림엔 SSE, 호환성엔 Polling!

---

## 🎯 4가지 방식 비교

### 한눈에 보기:
```
┌────────────┬─────────────┬──────────┬─────────┐
│            │ Polling     │ Long     │ SSE     │ WebSocket
│            │             │ Polling  │         │
├────────────┼─────────────┼──────────┼─────────┤
│ 방향       │ 단방향      │ 단방향    │ 단방향  │ 양방향
│ 연결       │ 매번 새로   │ 유지     │ 유지    │ 유지
│ 실시간성   │ 낮음        │ 중간     │ 높음    │ 높음
│ 효율성     │ 낮음        │ 중간     │ 높음    │ 높음
│ 복잡도     │ 쉬움        │ 중간     │ 쉬움    │ 중간
│ 호환성     │ 최고        │ 좋음     │ 좋음    │ 좋음
└────────────┴─────────────┴──────────┴─────────┘
```

### 비유로 이해하기:
```
📬 Polling
└── 5분마다 우체통 확인하러 감

📬 Long Polling
└── 우체통 앞에서 편지 올 때까지 대기

📺 SSE
└── TV처럼 방송국에서 일방적으로 송출

📞 WebSocket
└── 전화처럼 양방향 실시간 대화
```

---

## 🎯 상세 비교

### 지연 시간:
```
Polling (10초 간격)
├── 최대 10초 지연
└── 평균 5초 지연

Long Polling
├── 거의 즉시 (< 100ms)
└── 새 데이터 발생 시 바로 응답

SSE
├── 거의 즉시 (< 50ms)
└── 연결 유지로 즉각 푸시

WebSocket
├── 거의 즉시 (< 50ms)
└── 양방향 모두 즉각 전달
```

### 서버 부하:
```
Polling (1000명, 10초 간격)
├── 6000 req/min
└── 매번 연결/해제

Long Polling (1000명)
├── 1000 연결 유지
├── 데이터 있을 때만 응답
└── 타임아웃마다 재연결

SSE/WebSocket (1000명)
├── 1000 연결 유지
└── 오버헤드 최소
```"""
            },
            {
                "type": "code",
                "title": "💻 상황별 코드 예시",
                "content": """### 상황 1: 간단한 알림 → SSE

```javascript
// 서버
app.get('/notifications', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');

  // 새 알림 발생 시 전송
  const sendNotification = (data) => {
    res.write(`data: ${JSON.stringify(data)}\\n\\n`);
  };

  // 알림 이벤트 리스너 등록
  notificationEmitter.on('new', sendNotification);

  req.on('close', () => {
    notificationEmitter.off('new', sendNotification);
  });
});

// 클라이언트
const events = new EventSource('/notifications');
events.onmessage = (e) => showNotification(JSON.parse(e.data));
```

### 상황 2: 채팅 → WebSocket

```javascript
// 서버 (Socket.IO)
io.on('connection', (socket) => {
  socket.on('chat', (msg) => {
    io.emit('chat', msg);  // 모두에게 전송
  });
});

// 클라이언트
const socket = io();
socket.emit('chat', { text: '안녕!' });
socket.on('chat', (msg) => addMessage(msg));
```

### 상황 3: 레거시 호환 → Long Polling

```javascript
// 폴백 패턴
class RealtimeClient {
  constructor() {
    if (typeof WebSocket !== 'undefined') {
      this.useWebSocket();
    } else if (typeof EventSource !== 'undefined') {
      this.useSSE();
    } else {
      this.useLongPolling();
    }
  }

  useWebSocket() {
    this.socket = new WebSocket('wss://example.com');
    this.socket.onmessage = (e) => this.onMessage(e.data);
  }

  useSSE() {
    this.eventSource = new EventSource('/events');
    this.eventSource.onmessage = (e) => this.onMessage(e.data);
  }

  useLongPolling() {
    const poll = async () => {
      const res = await fetch('/poll');
      const data = await res.json();
      this.onMessage(data);
      poll();
    };
    poll();
  }

  onMessage(data) {
    console.log('받음:', data);
  }
}
```

### 상황 4: 고빈도 데이터 → WebSocket + 스로틀링

```javascript
// 주식 시세처럼 빠른 업데이트
// 서버
const throttle = require('lodash/throttle');

// 100ms마다 최대 1번만 전송
const sendPrice = throttle((price) => {
  io.emit('price', price);
}, 100);

priceStream.on('update', sendPrice);

// 클라이언트
socket.on('price', (price) => {
  updateChart(price);  // UI 업데이트
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 기술 선택 가이드",
                "content": """### 결정 트리

```
양방향 필요한가?
├── Yes → WebSocket
└── No → 서버→클라이언트만?
         ├── Yes → SSE (현대 브라우저)
         │         Long Polling (레거시)
         └── No → REST API로 충분
```

### 서비스별 추천

```
💬 채팅
└── WebSocket (Socket.IO)

🔔 알림
└── SSE 또는 WebSocket

📈 주식/코인 시세
└── WebSocket (빈번한 업데이트)

📊 대시보드
└── SSE (서버에서 푸시)

🎮 게임
└── WebSocket (양방향, 저지연)

📝 협업 도구
└── WebSocket (실시간 동기화)

🛒 이커머스 재고
└── SSE 또는 Polling
```

### 확장성 고려

```
1000명 이하:
└── 어떤 기술이든 OK

1만명 이상:
├── WebSocket: 연결 관리 복잡
├── Redis Pub/Sub 사용
└── 로드밸런서 sticky session

10만명 이상:
├── 전용 실시간 서비스 분리
├── Kafka/RabbitMQ 사용
└── 클러스터링 필수
```

### 비용 비교

```
개발 비용: Polling < SSE < WebSocket
운영 비용: WebSocket < SSE < Polling
확장 비용: SSE ≈ Polling < WebSocket

결론:
├── 간단 + 서버푸시만 → SSE
├── 양방향 + 실시간 → WebSocket
└── 호환성 최우선 → Long Polling
```"""
            }
        ]
    }
}

# 08_고급/기타 섹션 콘텐츠
ADVANCED_CONTENTS = {
    "08_고급/browser-rendering": {
        "title": "브라우저 렌더링",
        "description": "브라우저의 렌더링 과정을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🖼️ 브라우저 렌더링이란?",
                "content": """## 🖼️ 한 줄 요약
> **HTML을 화면에 그리는 과정** - 코드가 예쁜 웹페이지가 되기까지!

---

## 💡 왜 알아야 하나?

### 프론트엔드 최적화의 핵심:
```
"왜 페이지가 느려요?"
└── 렌더링 과정을 알면 답이 보임!

"어떻게 빠르게 만들어요?"
└── 렌더링 최적화 방법 적용!
```

---

## 🎯 렌더링 과정 (Critical Rendering Path)

### 전체 흐름:
```
1. HTML 파싱 → DOM 트리
2. CSS 파싱 → CSSOM 트리
3. DOM + CSSOM → 렌더 트리
4. Layout (위치/크기 계산)
5. Paint (픽셀로 그리기)
6. Composite (레이어 합성)
```

### 상세 과정:

```
┌─────────────────────────────────────────┐
│ 1. HTML 파싱 → DOM 트리                  │
├─────────────────────────────────────────┤
│ <html>                    Document       │
│   <head>                     │           │
│   <body>               ┌────┴────┐      │
│     <div>             head     body      │
│       <p>              │         │       │
│                      title     div       │
│                                 │        │
│                                 p        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 2. CSS 파싱 → CSSOM 트리                 │
├─────────────────────────────────────────┤
│ body { color: black }     CSSOM          │
│ div { margin: 10px }        │            │
│ p { font-size: 16px }   ┌───┴───┐       │
│                        body    div       │
│                         │       │        │
│                    color:black margin    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 3. 렌더 트리 (Render Tree)               │
├─────────────────────────────────────────┤
│ DOM + CSSOM = 화면에 보이는 것만!         │
│                                          │
│ display: none → 렌더 트리에서 제외!       │
│ visibility: hidden → 포함 (공간 차지)     │
└─────────────────────────────────────────┘
```"""
            },
            {
                "type": "code",
                "title": "💻 렌더링 최적화",
                "content": """### 렌더링 차단 리소스

```html
<!-- 렌더링 차단: CSS -->
<link rel="stylesheet" href="style.css">
<!-- 파싱 중단, CSS 로드 대기 -->

<!-- 렌더링 차단: 동기 JS -->
<script src="app.js"></script>
<!-- 파싱 중단, JS 실행 대기 -->

<!-- 해결책: async/defer -->
<script async src="analytics.js"></script>
<!-- 비동기 로드, 즉시 실행 -->

<script defer src="app.js"></script>
<!-- 비동기 로드, DOM 완성 후 실행 -->
```

### Reflow vs Repaint

```javascript
// Reflow (레이아웃 다시 계산) - 비용 높음
element.style.width = '100px';   // 레이아웃 변경
element.style.height = '200px';  // 레이아웃 변경
element.style.margin = '10px';   // 레이아웃 변경

// Repaint (다시 그리기) - 비용 중간
element.style.color = 'red';     // 색상만 변경
element.style.background = 'blue'; // 배경만 변경

// 최적화: 일괄 변경
element.style.cssText = 'width:100px; height:200px; margin:10px';
// 또는
element.classList.add('new-style');
```

### Layout Thrashing 방지

```javascript
// 나쁜 예: 읽기/쓰기 반복
for (let i = 0; i < items.length; i++) {
  items[i].style.width = container.offsetWidth + 'px';
  // offsetWidth 읽기 → 강제 reflow
}

// 좋은 예: 읽기 먼저, 쓰기 나중
const width = container.offsetWidth; // 읽기
for (let i = 0; i < items.length; i++) {
  items[i].style.width = width + 'px'; // 쓰기만
}
```

### requestAnimationFrame

```javascript
// 나쁜 예: 즉시 실행
function animate() {
  element.style.left = x + 'px';
  x += 1;
  setTimeout(animate, 16); // 불규칙
}

// 좋은 예: 다음 프레임에 실행
function animate() {
  element.style.left = x + 'px';
  x += 1;
  requestAnimationFrame(animate); // 60fps 동기화
}

requestAnimationFrame(animate);
```

### 레이어 분리 (Composite)

```css
/* GPU 가속 활성화 */
.animated {
  /* 별도 레이어로 분리 */
  will-change: transform;
  /* 또는 */
  transform: translateZ(0);
}

/* transform, opacity만 변경 → reflow 없음! */
.animated:hover {
  transform: scale(1.1);
  opacity: 0.8;
}
```"""
            },
            {
                "type": "tip",
                "title": "💡 성능 최적화 팁",
                "content": """### Critical Rendering Path 최적화

```
1. CSS를 <head>에
   └── 빠른 CSSOM 생성

2. JS를 </body> 앞에 또는 defer
   └── DOM 파싱 차단 방지

3. 중요 CSS 인라인
   └── 외부 파일 로드 대기 없음

4. 불필요한 CSS 제거
   └── CSSOM 생성 시간 단축
```

### 성능 측정 도구

```
Chrome DevTools:
├── Performance 탭: 렌더링 분석
├── Lighthouse: 전체 성능 점수
└── Rendering 탭: Paint 영역 표시

핵심 지표:
├── FCP (First Contentful Paint)
├── LCP (Largest Contentful Paint)
├── CLS (Cumulative Layout Shift)
└── FID (First Input Delay)
```

### Reflow 유발 속성

```
피해야 할 속성:
├── width, height
├── margin, padding
├── top, left, right, bottom
├── font-size, font-family
└── display

선호할 속성:
├── transform
├── opacity
└── GPU 가속 속성
```

### 최적화 체크리스트

```
□ CSS는 head에
□ JS는 defer 또는 body 끝에
□ 이미지 lazy loading
□ CSS 애니메이션은 transform 사용
□ Layout Thrashing 방지
□ will-change 적절히 사용
□ 불필요한 DOM 조작 최소화
```"""
            }
        ]
    },

    "08_고급/load-balancing": {
        "title": "로드 밸런싱",
        "description": "로드 밸런싱의 개념과 알고리즘을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "⚖️ 로드 밸런싱이란?",
                "content": """## ⚖️ 한 줄 요약
> **트래픽 분산 담당** - 요청을 여러 서버에 골고루 나눠줘요!

---

## 💡 왜 필요한가?

### 문제 상황:
```
서버 1대에 10만 명 접속
├── 서버 과부하
├── 응답 느림
└── 서버 다운! 😱
```

### 로드 밸런서로 해결:
```
        ┌─────────────┐
        │로드 밸런서   │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│서버 1  │ │서버 2  │ │서버 3  │
└───────┘ └───────┘ └───────┘

10만 명 ÷ 3 = 서버당 3.3만 명
→ 안정적인 서비스! ✅
```

---

## 🎯 로드 밸런싱 알고리즘

### 1. Round Robin (라운드 로빈)
```
순서대로 돌아가며 배분

요청1 → 서버1
요청2 → 서버2
요청3 → 서버3
요청4 → 서버1 (다시)
...

장점: 간단
단점: 서버 성능 차이 무시
```

### 2. Weighted Round Robin
```
가중치에 따라 배분

서버1 (가중치 3): ●●●
서버2 (가중치 2): ●●
서버3 (가중치 1): ●

→ 성능 좋은 서버에 더 많이!
```

### 3. Least Connections
```
현재 연결이 가장 적은 서버로

서버1: 100개 연결
서버2: 50개 연결  ← 여기로!
서버3: 80개 연결
```

### 4. IP Hash
```
클라이언트 IP로 서버 결정

hash(192.168.0.1) % 3 = 1
→ 항상 서버1로!

장점: 같은 사용자 = 같은 서버
     (세션 유지)
```"""
            },
            {
                "type": "code",
                "title": "💻 로드 밸런서 설정",
                "content": """### Nginx 로드 밸런서

```nginx
# nginx.conf
http {
    # 서버 그룹 정의
    upstream backend {
        # Round Robin (기본)
        server 192.168.0.1:3000;
        server 192.168.0.2:3000;
        server 192.168.0.3:3000;
    }

    # Weighted
    upstream backend_weighted {
        server 192.168.0.1:3000 weight=3;
        server 192.168.0.2:3000 weight=2;
        server 192.168.0.3:3000 weight=1;
    }

    # Least Connections
    upstream backend_least {
        least_conn;
        server 192.168.0.1:3000;
        server 192.168.0.2:3000;
    }

    # IP Hash (세션 유지)
    upstream backend_hash {
        ip_hash;
        server 192.168.0.1:3000;
        server 192.168.0.2:3000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 헬스 체크

```nginx
upstream backend {
    server 192.168.0.1:3000 max_fails=3 fail_timeout=30s;
    server 192.168.0.2:3000 max_fails=3 fail_timeout=30s;
    server 192.168.0.3:3000 backup;  # 백업 서버
}

# 3번 실패하면 30초간 제외
# backup 서버는 다른 서버 다운 시에만 사용
```

### AWS ALB (Application Load Balancer)

```javascript
// AWS CDK 예시
const alb = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
  vpc,
  internetFacing: true
});

const listener = alb.addListener('Listener', {
  port: 80
});

const targetGroup = listener.addTargets('Targets', {
  port: 3000,
  targets: [
    new targets.InstanceTarget(instance1),
    new targets.InstanceTarget(instance2)
  ],
  healthCheck: {
    path: '/health',
    interval: Duration.seconds(30)
  }
});
```

### Docker Compose + Nginx

```yaml
# docker-compose.yml
version: '3'
services:
  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2
      - app3

  app1:
    build: .
    expose:
      - "3000"

  app2:
    build: .
    expose:
      - "3000"

  app3:
    build: .
    expose:
      - "3000"
```"""
            },
            {
                "type": "tip",
                "title": "💡 로드 밸런싱 팁",
                "content": """### L4 vs L7 로드 밸런서

```
L4 (Transport Layer)
├── IP/Port 기반
├── 빠름
├── 간단한 분산
└── TCP/UDP 지원

L7 (Application Layer)
├── HTTP 헤더/URL 기반
├── 스마트한 분산
├── SSL 종료
├── 캐싱 가능
└── 더 많은 기능

선택:
├── 단순 분산 → L4
└── HTTP 기능 필요 → L7
```

### 세션 유지 전략

```
1. Sticky Session (IP Hash)
   └── 같은 사용자 = 같은 서버

2. Session 중앙화 (Redis)
   └── 어느 서버든 세션 접근 가능

3. Stateless (JWT)
   └── 세션 서버 불필요

추천: Session 중앙화 또는 JWT
```

### 헬스 체크 설정

```
체크 주기: 5~30초
타임아웃: 2~5초
임계값: 2~3회 실패 시 제외
복구 조건: 2~3회 성공 시 복구

엔드포인트 예시:
GET /health → 200 OK
└── DB 연결, 캐시 연결 확인
```

### 클라우드 서비스 비교

```
AWS:
├── ALB (L7, HTTP)
├── NLB (L4, TCP/UDP)
└── CLB (Classic, 레거시)

GCP:
├── HTTP(S) Load Balancer
└── TCP/UDP Load Balancer

Azure:
├── Application Gateway
└── Load Balancer
```"""
            }
        ]
    },

    "08_고급/proxy": {
        "title": "프록시",
        "description": "프록시 서버의 개념과 종류를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔀 프록시란?",
                "content": """## 🔀 한 줄 요약
> **대리인 서버** - 클라이언트와 서버 사이에서 대신 요청/응답해줘요!

---

## 💡 프록시의 종류

### 1. Forward Proxy (정방향)
```
클라이언트를 대신하여 요청

┌────────┐     ┌────────┐     ┌────────┐
│클라이언트│ ──► │ 프록시  │ ──► │ 서버   │
└────────┘     └────────┘     └────────┘

사용 사례:
├── 회사/학교 인터넷 필터링
├── IP 숨기기
├── 지역 제한 우회
└── 캐싱
```

### 2. Reverse Proxy (역방향)
```
서버를 대신하여 응답

┌────────┐     ┌────────┐     ┌────────┐
│클라이언트│ ──► │ 프록시  │ ──► │ 서버   │
└────────┘     └────────┘     └────────┘

사용 사례:
├── 로드 밸런싱
├── SSL 종료
├── 캐싱
├── 보안 (서버 숨기기)
└── 압축
```

---

## 🎯 프록시 역할

### Forward Proxy:
```
회사 내부 직원 → 프록시 → 인터넷

1. 접근 제어
   └── "유튜브 차단"

2. 캐싱
   └── 자주 요청되는 콘텐츠 저장

3. 익명성
   └── 실제 IP 숨김

4. 로깅
   └── 누가 뭘 접속했는지 기록
```

### Reverse Proxy:
```
인터넷 사용자 → 프록시 → 내부 서버

1. 로드 밸런싱
   └── 여러 서버로 분산

2. SSL 종료
   └── HTTPS 처리 후 HTTP로 전달

3. 캐싱
   └── 정적 파일 캐싱

4. 보안
   └── WAF, DDoS 방어
   └── 실제 서버 IP 숨김

5. 압축
   └── gzip 등 응답 압축
```"""
            },
            {
                "type": "code",
                "title": "💻 프록시 설정",
                "content": """### Nginx Reverse Proxy

```nginx
# 기본 리버스 프록시
server {
    listen 80;
    server_name myapp.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# SSL 종료 + 프록시
server {
    listen 443 ssl;
    server_name myapp.com;

    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://localhost:3000;  # 내부는 HTTP
    }
}

# 캐싱 설정
location ~* \\.(jpg|css|js)$ {
    proxy_pass http://localhost:3000;
    proxy_cache my_cache;
    proxy_cache_valid 200 1d;
    add_header X-Cache-Status $upstream_cache_status;
}
```

### Node.js 프록시 (http-proxy-middleware)

```javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

// API 요청을 백엔드로 프록시
app.use('/api', createProxyMiddleware({
  target: 'http://backend:5000',
  changeOrigin: true,
  pathRewrite: { '^/api': '' }
}));

// WebSocket 프록시
app.use('/socket.io', createProxyMiddleware({
  target: 'http://backend:5000',
  ws: true
}));
```

### 개발 환경 프록시 (Vite)

```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/socket.io': {
        target: 'ws://localhost:5000',
        ws: true
      }
    }
  }
}
```

### CORS 프록시 (Express)

```javascript
// CORS 문제 우회용 프록시
app.get('/proxy', async (req, res) => {
  const { url } = req.query;

  const response = await fetch(url);
  const data = await response.text();

  res.send(data);
});

// 클라이언트
fetch('/proxy?url=https://api.example.com/data')
```"""
            },
            {
                "type": "tip",
                "title": "💡 프록시 활용 팁",
                "content": """### 프록시 vs 로드 밸런서 vs CDN

```
프록시:
├── 요청 중개
├── 캐싱, 필터링, 변환
└── 단일 목적지도 OK

로드 밸런서:
├── 트래픽 분산 특화
├── 여러 서버로 분배
└── 헬스 체크

CDN:
├── 콘텐츠 배포 특화
├── 전세계 엣지 서버
└── 정적 파일 캐싱

조합:
사용자 → CDN → 로드밸런서 → 서버
```

### X-Forwarded-* 헤더

```
프록시 뒤에서 원본 정보 얻기:

X-Forwarded-For: 클라이언트 IP
X-Forwarded-Proto: 원본 프로토콜 (http/https)
X-Forwarded-Host: 원본 호스트

서버에서 확인:
const clientIP = req.headers['x-forwarded-for']
  || req.connection.remoteAddress;
```

### 보안 고려사항

```
1. 프록시 헤더 신뢰 설정
   └── 믿을 수 있는 프록시만 허용

2. 숨김 헤더 제거
   └── Server, X-Powered-By 등

3. 접근 제어
   └── 내부 서비스 노출 방지

4. Rate Limiting
   └── DDoS 방어
```

### 디버깅 팁

```
1. curl로 테스트
curl -v https://myapp.com

2. 헤더 확인
X-Cache-Status: HIT/MISS
X-Proxy-Cache: 캐시 상태

3. 로그 확인
tail -f /var/log/nginx/access.log
```"""
            }
        ]
    },

    "08_기타/cdn": {
        "title": "CDN",
        "description": "Content Delivery Network의 개념을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🌍 CDN이란?",
                "content": """## 🌍 한 줄 요약
> **전세계 콘텐츠 배달부** - 가까운 곳에서 빠르게 콘텐츠를 전달해요!

---

## 💡 왜 CDN이 필요한가?

### 문제 상황:
```
서버: 미국
사용자: 한국

한국 ────── 태평양 ────── 미국
         왕복 200ms 😢

이미지 10개 로드 = 2초 지연!
```

### CDN으로 해결:
```
원본 서버: 미국
CDN 엣지: 한국

한국 ── CDN 서울 ── 원본(미국)
       왕복 20ms 😊

이미지가 한국 CDN에 캐시됨!
```

---

## 🎯 CDN 동작 방식

```
1. 첫 요청 (Cache MISS)
┌────────┐     ┌────────┐     ┌────────┐
│ 한국    │ ──► │CDN 서울│ ──► │원본 미국│
│ 사용자  │ ◄── │        │ ◄── │        │
└────────┘     └────────┘     └────────┘
               (캐시 저장)

2. 이후 요청 (Cache HIT)
┌────────┐     ┌────────┐
│ 한국    │ ──► │CDN 서울│
│ 사용자  │ ◄── │(캐시)  │
└────────┘     └────────┘
원본 서버 접근 불필요! ⚡
```

### CDN 장점:
```
1. 속도 향상 ⚡
   └── 가까운 서버에서 응답

2. 부하 분산 📊
   └── 원본 서버 트래픽 감소

3. 가용성 📈
   └── 원본 다운 시에도 캐시 제공

4. 보안 🔒
   └── DDoS 방어, WAF
```"""
            },
            {
                "type": "code",
                "title": "💻 CDN 설정하기",
                "content": """### Cloudflare 설정

```
1. DNS 설정
   example.com → Cloudflare 네임서버

2. 캐시 규칙
   ├── 정적 파일: 캐시 (이미지, CSS, JS)
   ├── API: 캐시 안 함
   └── HTML: 상황에 따라

3. 페이지 규칙 예시
   example.com/static/* → 캐시 1달
   example.com/api/* → 캐시 우회
```

### 캐시 제어 헤더

```javascript
// Express에서 캐시 헤더 설정
app.use('/static', express.static('public', {
  maxAge: '1y',  // 1년 캐시
  immutable: true
}));

// 동적 콘텐츠: 캐시 안 함
app.get('/api/*', (req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

// 조건부 캐시 (ETag)
app.get('/posts/:id', (req, res) => {
  const post = getPost(req.params.id);
  const etag = generateETag(post);

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }

  res.set('ETag', etag);
  res.json(post);
});
```

### 캐시 무효화 (Cache Invalidation)

```javascript
// 파일명에 해시 포함 (권장)
// main.abc123.js
// → 파일 변경 시 새 URL = 새 캐시

// Webpack 설정
output: {
  filename: '[name].[contenthash].js'
}

// Vite 기본 지원
// dist/assets/index.a1b2c3d4.js

// API로 캐시 삭제 (Cloudflare)
fetch('https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    files: ['https://example.com/style.css']
  })
});
```

### HTML에서 CDN 사용

```html
<!-- 직접 호스팅 대신 CDN -->
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>

<!-- 자체 CDN -->
<img src="https://cdn.myapp.com/images/logo.png">
<link href="https://cdn.myapp.com/css/style.css">
<script src="https://cdn.myapp.com/js/app.js"></script>
```"""
            },
            {
                "type": "tip",
                "title": "💡 CDN 활용 팁",
                "content": """### CDN 서비스 비교

```
Cloudflare
├── 무료 플랜 있음
├── DDoS 방어 강력
└── 설정 쉬움

AWS CloudFront
├── AWS 서비스 연동
├── 세밀한 제어
└── 종량제

Vercel Edge Network
├── Next.js 최적화
├── 자동 배포
└── 무료 tier

Fastly
├── 실시간 캐시 삭제
├── 엣지 컴퓨팅
└── 고성능
```

### 캐시 전략

```
정적 파일 (이미지, CSS, JS):
├── 긴 캐시 (1년)
├── 파일명에 해시 포함
└── immutable 설정

HTML:
├── 짧은 캐시 또는 no-cache
├── stale-while-revalidate
└── 동적 콘텐츠는 캐시 안 함

API 응답:
├── 대부분 캐시 안 함
├── 공개 데이터만 짧게 캐시
└── 사용자별 데이터 절대 캐시 X
```

### Cache-Control 헤더

```
public: CDN 캐시 가능
private: 브라우저만 캐시
no-store: 캐시 금지
no-cache: 매번 검증
max-age=3600: 1시간 캐시
s-maxage=3600: CDN용 (별도 설정)
immutable: 변경 안 됨
stale-while-revalidate: 백그라운드 갱신

예시:
Cache-Control: public, max-age=31536000, immutable
```

### 측정 도구

```
1. WebPageTest
   └── 전세계 위치에서 속도 측정

2. Chrome DevTools
   └── Network 탭에서 Cache 상태

3. curl
   curl -I https://example.com/image.jpg
   └── 헤더 확인

4. CDN 대시보드
   └── 히트율, 대역폭 확인
```"""
            }
        ]
    },

    "08_기타/load-balancer": {
        "title": "로드 밸런서 심화",
        "description": "로드 밸런서 구성과 고가용성을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔄 로드 밸런서 심화",
                "content": """## 🔄 한 줄 요약
> **고가용성의 핵심** - 서버가 죽어도 서비스는 살아있게!

---

## 💡 고가용성 (High Availability)

### 단일 장애점 제거:
```
문제: 로드 밸런서 1대
├── 로드 밸런서 다운 = 전체 서비스 다운
└── 단일 장애점 (SPOF)

해결: 로드 밸런서 이중화
        ┌─────────────────┐
        │  Virtual IP     │
        └────────┬────────┘
            Active│Standby
        ┌────────┴────────┐
    ┌───▼───┐        ┌───▼───┐
    │ LB 1  │◄──────►│ LB 2  │
    │(Active)│Heartbeat│(Standby)│
    └───┬───┘        └───┬───┘
        │                │
    ┌───▼───┬───┬───▼───┐
    │서버1   │서버2│서버3   │
    └───────┴───┴───────┘
```

### Failover 과정:
```
1. LB1이 다운됨
2. LB2가 감지 (Heartbeat 없음)
3. LB2가 VIP를 인계받음
4. 트래픽이 LB2로 전환
5. 서비스 중단 최소화 (수 초)
```

---

## 🎯 L4 vs L7 상세 비교

```
┌──────────────┬───────────────┬───────────────┐
│              │ L4 (TCP/UDP)  │ L7 (HTTP)     │
├──────────────┼───────────────┼───────────────┤
│ 처리 속도     │ 빠름          │ 느림 (파싱)   │
│ 분산 기준     │ IP, Port      │ URL, 헤더    │
│ SSL 종료     │ 불가          │ 가능          │
│ 세션 유지     │ 제한적        │ 쿠키 기반     │
│ 캐싱         │ 불가          │ 가능          │
│ 압축         │ 불가          │ 가능          │
│ 가격         │ 저렴          │ 비쌈          │
└──────────────┴───────────────┴───────────────┘
```

### 언제 무엇을 선택?

```
L4 선택:
├── 고성능 필요
├── 비 HTTP 트래픽 (DB, 게임)
├── 단순 분산
└── 비용 절감

L7 선택:
├── URL 기반 라우팅
├── SSL 종료
├── A/B 테스트
├── 인증, 캐싱
└── 세밀한 제어
```"""
            },
            {
                "type": "code",
                "title": "💻 고급 로드 밸런싱",
                "content": """### URL 기반 라우팅 (Nginx)

```nginx
upstream api_servers {
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
}

upstream web_servers {
    server 10.0.0.3:3000;
    server 10.0.0.4:3000;
}

server {
    listen 80;

    # /api/* → API 서버
    location /api/ {
        proxy_pass http://api_servers;
    }

    # /static/* → 웹 서버
    location /static/ {
        proxy_pass http://web_servers;
    }

    # 나머지 → 웹 서버
    location / {
        proxy_pass http://web_servers;
    }
}
```

### 세션 유지 (Sticky Session)

```nginx
upstream backend {
    ip_hash;  # IP 기반 고정
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
}

# 또는 쿠키 기반 (Plus 버전)
upstream backend {
    sticky cookie srv_id expires=1h;
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
}
```

### 헬스 체크 고급 설정

```nginx
upstream backend {
    server 10.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:3000 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:3000 backup;  # 백업
    server 10.0.0.4:3000 down;    # 수동으로 제외

    keepalive 32;  # 연결 유지
}

# 능동적 헬스 체크 (Plus 버전)
upstream backend {
    zone backend 64k;
    server 10.0.0.1:3000;

    health_check interval=5s
                 fails=3
                 passes=2
                 uri=/health
                 match=healthy;
}

match healthy {
    status 200;
    body ~ "OK";
}
```

### AWS ALB + Target Group

```javascript
// AWS CDK
const alb = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
  vpc,
  internetFacing: true
});

const apiTarget = new elbv2.ApplicationTargetGroup(this, 'APITarget', {
  vpc,
  port: 3000,
  protocol: elbv2.ApplicationProtocol.HTTP,
  healthCheck: {
    path: '/health',
    healthyThresholdCount: 2,
    unhealthyThresholdCount: 3
  }
});

const webTarget = new elbv2.ApplicationTargetGroup(this, 'WebTarget', {
  vpc,
  port: 3000
});

const listener = alb.addListener('Listener', { port: 443 });

listener.addAction('Route', {
  action: elbv2.ListenerAction.forward([
    {
      targetGroup: apiTarget,
      conditions: [elbv2.ListenerCondition.pathPatterns(['/api/*'])]
    },
    {
      targetGroup: webTarget  // 기본
    }
  ])
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 운영 팁",
                "content": """### 무중단 배포 전략

```
1. Rolling Update
   ├── 서버 하나씩 순차 배포
   ├── 배포 중 일부 서버만 새 버전
   └── 간단하지만 롤백 느림

2. Blue-Green
   ├── 새 환경 전체 배포
   ├── LB에서 트래픽 전환
   └── 빠른 롤백 가능

3. Canary
   ├── 일부 트래픽만 새 버전으로
   ├── 점진적 확대
   └── 위험 최소화
```

### Connection Draining

```
서버 제거 시:
1. 새 연결 차단
2. 기존 연결 완료 대기 (30초)
3. 타임아웃 후 강제 종료
4. 서버 제거

설정:
├── AWS: Deregistration delay
├── Nginx: upstream 설정
└── 권장: 30~60초
```

### 모니터링 지표

```
필수 지표:
├── 요청 수 (RPS)
├── 응답 시간 (Latency)
├── 에러율 (5xx 비율)
├── 활성 연결 수
└── 서버별 부하

알람 설정:
├── 에러율 > 1%
├── 응답 시간 > 500ms
├── 서버 다운
└── CPU/메모리 임계치
```

### 보안 설정

```
1. SSL/TLS
   └── 인증서 관리, 최신 프로토콜

2. WAF (Web Application Firewall)
   └── SQL Injection, XSS 방어

3. Rate Limiting
   └── DDoS, 브루트포스 방어

4. 접근 제어
   └── IP 화이트리스트/블랙리스트

5. 로깅
   └── 접근 로그, 에러 로그
```"""
            }
        ]
    }
}

# 09_면접, index 콘텐츠
INTERVIEW_CONTENTS = {
    "09_면접/interview-network": {
        "title": "네트워크 면접",
        "description": "네트워크 관련 기술 면접을 준비합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🎯 네트워크 면접 총정리",
                "content": """## 🎯 빈출 주제

### 필수 암기 TOP 10:
```
1. HTTP vs HTTPS
2. TCP vs UDP
3. REST API란?
4. 쿠키 vs 세션
5. JWT란?
6. CORS란?
7. WebSocket이란?
8. OSI 7계층
9. 3-way / 4-way handshake
10. DNS 동작 원리
```

---

## 💬 자주 나오는 질문과 답변

### Q1: HTTP와 HTTPS의 차이?
```
A: HTTPS는 HTTP에 SSL/TLS 암호화를 추가한 것입니다.

차이점:
├── 보안: HTTPS는 데이터 암호화
├── 포트: HTTP(80), HTTPS(443)
├── 인증: HTTPS는 SSL 인증서 필요
└── 성능: HTTPS가 약간 느림 (암호화 비용)

왜 중요한가:
├── 개인정보 보호
├── 데이터 무결성
├── 서버 인증
└── SEO 가점 (구글)
```

### Q2: TCP와 UDP의 차이?
```
A: TCP는 신뢰성, UDP는 속도 중심입니다.

TCP:
├── 연결형 (3-way handshake)
├── 순서 보장
├── 재전송 (손실 복구)
└── 웹, 이메일, 파일 전송

UDP:
├── 비연결형
├── 순서 미보장
├── 재전송 없음
└── 스트리밍, 게임, DNS

비유:
├── TCP = 등기우편 (확인, 추적)
└── UDP = 일반우편 (빠름, 확인X)
```

### Q3: REST API란?
```
A: HTTP를 활용한 웹 API 설계 원칙입니다.

핵심 원칙:
├── 자원 중심 URL (/users, /posts)
├── HTTP 메서드로 행위 표현
│   ├── GET: 조회
│   ├── POST: 생성
│   ├── PUT/PATCH: 수정
│   └── DELETE: 삭제
├── 무상태 (Stateless)
└── 표준 상태 코드 사용

예시:
GET /users/1     → 사용자 1 조회
POST /users      → 사용자 생성
PUT /users/1     → 사용자 1 수정
DELETE /users/1  → 사용자 1 삭제
```"""
            },
            {
                "type": "code",
                "title": "💻 핵심 개념 코드",
                "content": """### Q4: 쿠키 vs 세션 차이? (코드로)

```javascript
// 쿠키: 클라이언트 저장
res.cookie('theme', 'dark', {
  maxAge: 86400000,
  httpOnly: true
});
// → 브라우저에 저장, 매 요청 자동 전송

// 세션: 서버 저장
req.session.userId = 123;
// → 서버에 저장, 클라이언트는 세션 ID만 보유

// 비교:
// 쿠키: 노출 위험, 4KB 제한, 클라이언트 부담
// 세션: 안전, 용량 무제한, 서버 부담
```

### Q5: JWT 구조 설명

```javascript
// JWT = Header.Payload.Signature

// Header
{ "alg": "HS256", "typ": "JWT" }

// Payload (데이터)
{ "userId": 1, "exp": 1735689600 }

// Signature (위조 방지)
HMACSHA256(base64(header) + "." + base64(payload), secret)

// 특징:
// - 서버 저장 불필요 (Stateless)
// - 암호화 X, 인코딩 O (내용 볼 수 있음)
// - 서명으로 위변조 검증
```

### Q6: CORS 해결 방법

```javascript
// 1. 서버에서 헤더 추가
app.use(cors({
  origin: 'https://frontend.com',
  methods: ['GET', 'POST'],
  credentials: true
}));

// 2. 응답 헤더
Access-Control-Allow-Origin: https://frontend.com

// CORS가 필요한 이유:
// - 브라우저 보안 정책 (SOP)
// - 다른 출처 요청 차단
// - 서버가 명시적으로 허용해야 함
```

### Q7: TCP 3-way Handshake

```
클라이언트              서버
    │                    │
    │──── SYN ──────────►│  1. 연결 요청
    │                    │
    │◄─── SYN + ACK ─────│  2. 요청 수락 + 확인
    │                    │
    │──── ACK ──────────►│  3. 확인
    │                    │
    │═══ 연결 완료 ═══════│

왜 3번?
├── 양방향 통신 확인
├── 초기 순서 번호 교환
└── 서로의 수신 능력 확인
```"""
            },
            {
                "type": "tip",
                "title": "💡 면접 팁",
                "content": """### 답변 구조 (STAR)

```
S(상황): 개념 설명
T(과제): 왜 필요한지
A(행동): 어떻게 동작하는지
R(결과): 실제 사용 사례

예시:
"HTTPS는... (개념)
보안이 필요해서... (이유)
SSL/TLS로 암호화... (동작)
로그인 페이지 등에 사용... (사례)"
```

### 꼬리 질문 대비

```
Q: "HTTPS가 느리다고 했는데, 왜 느린가요?"
A: "암호화/복호화 연산 때문입니다.
    하지만 HTTP/2와 함께 사용하면
    멀티플렉싱으로 오히려 빨라질 수 있습니다."

Q: "JWT의 단점은?"
A: "토큰 탈취 시 만료까지 유효합니다.
    해결책으로 Access+Refresh 토큰 조합과
    짧은 만료 시간을 사용합니다."
```

### 모르는 질문 대처

```
"정확히는 모르지만,
제가 이해한 바로는..."

"실무에서 사용해본 적은 없지만,
개념적으로는..."

"관련된 OOO는 알고 있는데,
그 부분은 더 공부가 필요할 것 같습니다."
```

### 실무 경험 연결

```
"이전 프로젝트에서 CORS 문제를 겪었는데,
Nginx 프록시로 해결했습니다."

"채팅 기능 구현 시 WebSocket을 사용했고,
재연결 로직도 구현했습니다."

"성능 개선을 위해 CDN을 도입하여
응답 시간을 70% 단축했습니다."
```

### 최신 트렌드 언급

```
"HTTP/3와 QUIC 프로토콜"
"gRPC의 장점"
"Edge Computing / CDN"
"Zero Trust 보안 모델"
```"""
            }
        ]
    },

    "index": {
        "title": "네트워크 학습 가이드",
        "description": "네트워크 과목 전체 로드맵입니다",
        "sections": [
            {
                "type": "concept",
                "title": "🗺️ 네트워크 학습 로드맵",
                "content": """## 🗺️ 전체 커리큘럼

### 1주차: 기초 다지기
```
Day 1-2: 네트워크 기초
├── 네트워크란?
├── IP 주소
├── 포트
└── DNS

Day 3-4: 프로토콜 이해
├── OSI 7계층
├── TCP/IP
└── TCP vs UDP

Day 5: 실습
└── ping, traceroute, nslookup 사용
```

### 2주차: 웹 통신
```
Day 1-2: HTTP
├── HTTP 메서드
├── 상태 코드
├── 헤더
└── HTTPS

Day 3-4: REST API
├── REST 개념
├── RESTful 설계
└── GraphQL 비교

Day 5: 실습
└── Postman으로 API 테스트
```

### 3주차: 인증과 보안
```
Day 1-2: 인증
├── 쿠키 vs 세션
├── JWT
└── OAuth

Day 3-4: 보안
├── CORS
├── Same-Origin Policy
└── 보안 헤더

Day 5: 실습
└── 로그인 시스템 구현
```

### 4주차: 실시간과 심화
```
Day 1-2: 실시간 통신
├── WebSocket
├── SSE
└── Long Polling

Day 3-4: 인프라
├── 로드 밸런싱
├── CDN
├── 프록시

Day 5: 종합 실습
└── 채팅 앱 만들기
```"""
            },
            {
                "type": "code",
                "title": "💻 핵심 명령어 모음",
                "content": """### 네트워크 진단

```bash
# 연결 테스트
ping google.com

# 경로 추적
traceroute google.com  # Mac/Linux
tracert google.com     # Windows

# DNS 조회
nslookup naver.com

# 내 IP 확인
curl ifconfig.me

# 포트 확인
netstat -an | grep LISTEN
```

### HTTP 테스트

```bash
# GET 요청
curl https://api.example.com/users

# POST 요청 (JSON)
curl -X POST https://api.example.com/users \\
  -H "Content-Type: application/json" \\
  -d '{"name": "홍길동"}'

# 헤더 포함
curl -H "Authorization: Bearer token123" \\
  https://api.example.com/profile

# 응답 헤더 확인
curl -I https://example.com
```

### 자주 쓰는 코드

```javascript
// fetch API
const response = await fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({ name: '홍길동' })
});

const data = await response.json();

// WebSocket
const socket = new WebSocket('wss://example.com');
socket.onmessage = (e) => console.log(e.data);
socket.send('Hello!');

// SSE
const events = new EventSource('/events');
events.onmessage = (e) => console.log(e.data);
```"""
            },
            {
                "type": "tip",
                "title": "💡 학습 팁",
                "content": """### 효과적인 학습법

```
1. 개념 → 실습 → 프로젝트
   └── 이론만으론 부족해요!

2. 브라우저 개발자 도구 활용
   └── Network 탭에서 실시간 확인

3. 작은 프로젝트로 적용
   ├── 간단한 API 서버
   ├── 채팅 앱
   └── 로그인 시스템
```

### 추천 도구

```
Postman: API 테스트
Wireshark: 패킷 분석
curl: 터미널 HTTP 테스트
ngrok: 로컬 서버 외부 노출
```

### 면접 준비

```
1. 핵심 개념 암기
   └── TCP/UDP, HTTP/HTTPS, REST

2. 동작 원리 이해
   └── 3-way handshake, DNS 조회

3. 실제 사용 경험
   └── CORS 해결, JWT 구현

4. 장단점 비교
   └── 쿠키 vs 세션 vs JWT
```

### 다음 단계

```
네트워크 마스터 후:
├── 시스템 설계
├── 보안 심화
├── 클라우드 인프라
└── DevOps
```"""
            }
        ]
    }
}

def update_network_json():
    """network.json 파일 업데이트"""
    sys.stdout.reconfigure(encoding='utf-8')

    # 파일 읽기
    with open(NETWORK_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 모든 콘텐츠 통합
    all_contents = {}
    all_contents.update(REALTIME_CONTENTS)
    all_contents.update(ADVANCED_CONTENTS)
    all_contents.update(INTERVIEW_CONTENTS)

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

    print(f"\n[DONE] Realtime, Advanced, Interview sections updated: {updated_count} topics")

if __name__ == "__main__":
    update_network_json()
