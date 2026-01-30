# -*- coding: utf-8 -*-
"""
클린코드 콘텐츠 생성 스크립트 - Part 1
01_클린코드 섹션 (11개 토픽)
"""

import json
import sys

# 파일 경로
CLEANCODE_JSON_PATH = "src/data/contents/cleancode.json"

# 01_클린코드 섹션 콘텐츠
CLEANCODE_CONTENTS = {
    "01_클린코드/cleancode-intro": {
        "title": "클린코드 소개",
        "description": "클린코드의 개념과 중요성을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "✨ 클린코드란?",
                "content": """## ✨ 한 줄 요약
> **읽기 쉬운 코드** - 다른 개발자(미래의 나 포함)가 쉽게 이해할 수 있는 코드!

---

## 💡 왜 클린코드가 중요한가?

### 현실 상황:
```
코드 작성 시간: 10%
코드 읽는 시간: 90%

→ 읽기 쉬운 코드 = 생산성 향상!
```

### 클린코드 vs 더티코드:
```python
# ❌ 더티코드
def f(x):
    return x*x if x>0 else -x*x

# ✅ 클린코드
def calculate_squared_value(number):
    if number > 0:
        return number * number
    return -number * number
```

### 클린코드의 특징:
```
1. 읽기 쉬움 (Readable)
   └── 소설 읽듯이 술술 읽힘

2. 단순함 (Simple)
   └── 한 가지 일만 잘 함

3. 명확함 (Clear)
   └── 의도가 드러남

4. 테스트 가능 (Testable)
   └── 검증하기 쉬움
```

---

## 🎯 클린코드 원칙

### 보이스카우트 규칙:
```
"캠핑장을 떠날 때는
 도착했을 때보다 더 깨끗하게"

→ 코드를 수정할 때
   조금이라도 더 깨끗하게 만들어 두기
```

### 핵심 가치:
```
├── 가독성 > 성능 (대부분의 경우)
├── 명확성 > 간결성
├── 일관성 유지
└── 지속적인 개선
```"""
            },
            {
                "type": "code",
                "title": "💻 클린코드 예시",
                "content": """### Before vs After

```python
# ❌ Before: 이해하기 어려움
def calc(d):
    t = 0
    for i in d:
        if i['s'] == 'A':
            t += i['p'] * 0.9
        else:
            t += i['p']
    return t

# ✅ After: 의도가 명확함
def calculate_total_price(products):
    total = 0

    for product in products:
        if product['status'] == 'A':  # A등급 상품
            discounted_price = product['price'] * 0.9
            total += discounted_price
        else:
            total += product['price']

    return total
```

### 함수 개선

```javascript
// ❌ Before: 한 함수가 너무 많은 일
function processUser(user) {
    // 유효성 검사
    if (!user.email) throw new Error('Email required');
    if (!user.name) throw new Error('Name required');

    // 데이터 변환
    user.email = user.email.toLowerCase();
    user.name = user.name.trim();

    // DB 저장
    database.save(user);

    // 이메일 발송
    sendWelcomeEmail(user.email);

    return user;
}

// ✅ After: 역할 분리
function processUser(user) {
    validateUser(user);
    const normalizedUser = normalizeUser(user);
    const savedUser = saveUser(normalizedUser);
    notifyUser(savedUser);
    return savedUser;
}

function validateUser(user) {
    if (!user.email) throw new Error('Email required');
    if (!user.name) throw new Error('Name required');
}

function normalizeUser(user) {
    return {
        ...user,
        email: user.email.toLowerCase(),
        name: user.name.trim()
    };
}
```"""
            },
            {
                "type": "tip",
                "title": "💡 클린코드 시작하기",
                "content": """### 오늘부터 실천할 것

```
1. 의미 있는 이름 짓기
   └── x → userCount

2. 함수는 작게
   └── 한 화면에 다 보이게

3. 주석 대신 코드로 설명
   └── 이름으로 의도 표현

4. 일관성 유지
   └── 같은 개념엔 같은 단어
```

### 추천 학습 순서

```
1단계: 네이밍
├── 변수명, 함수명 제대로 짓기
└── 가장 효과 큼!

2단계: 함수
├── 작게, 한 가지만
└── 파라미터 줄이기

3단계: 리팩토링
├── 기존 코드 개선
└── 조금씩 꾸준히

4단계: 설계 원칙
├── SOLID
└── 디자인 패턴
```

### 명심할 것

```
"동작하는 코드를 작성하는 것은 시작일 뿐,
 클린코드로 만드는 것이 진짜 개발"

"나중은 결코 오지 않는다.
 지금 깨끗하게 작성하자"
```"""
            }
        ]
    },

    "01_클린코드/naming": {
        "title": "네이밍",
        "description": "좋은 이름 짓기의 원칙을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "📝 좋은 이름이란?",
                "content": """## 📝 한 줄 요약
> **이름만 봐도 역할이 보이는 것** - 주석 없이도 코드가 설명되어야 해요!

---

## 💡 이름이 중요한 이유

### 코드의 90%는 이름:
```python
# 이름만으로 구성됨
user_count = get_active_users(start_date, end_date)
if user_count > MAX_USERS:
    send_alert_email(admin_email)
```

### 나쁜 이름의 비용:
```
❌ 나쁜 이름
├── 매번 구현부 확인 필요
├── 잘못된 추측 → 버그
└── 협업 비용 증가

✅ 좋은 이름
├── 바로 이해 가능
├── 주석 불필요
└── 유지보수 쉬움
```

---

## 🎯 네이밍 원칙

### 1. 의도를 드러내라
```python
# ❌ 의도 불명확
d = 30
l = []
def get(id): ...

# ✅ 의도 명확
days_until_expiration = 30
active_user_list = []
def get_user_by_id(user_id): ...
```

### 2. 검색 가능한 이름
```python
# ❌ 검색 불가
if status == 1:  # 1이 뭐지?

# ✅ 검색 가능
STATUS_ACTIVE = 1
if status == STATUS_ACTIVE:
```

### 3. 발음할 수 있는 이름
```python
# ❌ 발음 불가
genymdhms = datetime.now()
cstmr = get_customer()

# ✅ 발음 가능
generation_timestamp = datetime.now()
customer = get_customer()
```

### 4. 맥락을 담아라
```python
# ❌ 맥락 부족
state = "Seoul"
name = "Kim"

# ✅ 맥락 명확
address_state = "Seoul"
customer_name = "Kim"

# 또는 클래스로 맥락 제공
class Address:
    state = "Seoul"
class Customer:
    name = "Kim"
```"""
            },
            {
                "type": "code",
                "title": "💻 네이밍 실전",
                "content": """### 변수명 패턴

```python
# Boolean: is, has, can, should
is_active = True
has_permission = user.check_permission()
can_edit = user.role == 'admin'
should_notify = settings.notifications_enabled

# 컬렉션: 복수형 또는 명시
users = get_all_users()
user_list = []
user_map = {}  # 또는 user_dict
user_set = set()

# 숫자: count, total, max, min
user_count = len(users)
total_price = sum(prices)
max_retry = 3
min_age = 18
```

### 함수명 패턴

```python
# 동사로 시작
def get_user(user_id): ...
def create_order(items): ...
def update_profile(user, data): ...
def delete_comment(comment_id): ...

# Boolean 반환: is, has, can
def is_valid_email(email): ...
def has_admin_role(user): ...
def can_access_resource(user, resource): ...

# 변환: to, from, parse
def to_json(data): ...
def from_dict(dict_data): ...
def parse_date(date_string): ...

# 이벤트 핸들러: on, handle
def on_click(event): ...
def handle_submit(form_data): ...
```

### 클래스명 패턴

```python
# 명사 또는 명사구
class User: ...
class OrderService: ...
class PaymentProcessor: ...
class DatabaseConnection: ...

# 인터페이스: -able, I접두사
class Serializable: ...
class IRepository: ...  # C# 스타일
class Comparable: ...

# 추상 클래스: Base, Abstract
class BaseRepository: ...
class AbstractHandler: ...
```

### 나쁜 이름 피하기

```python
# ❌ 피해야 할 이름
data = ...      # 너무 일반적
info = ...      # 모호함
temp = ...      # 임시? 언제까지?
foo, bar = ...  # 의미 없음
Manager = ...   # 모든 걸 다 하는 느낌
Helper = ...    # 역할 불분명
Util = ...      # 잡동사니 느낌

# ✅ 구체적인 이름
user_profile_data = ...
shipping_address_info = ...
cached_user_session = ...
```"""
            },
            {
                "type": "tip",
                "title": "💡 네이밍 체크리스트",
                "content": """### 이름 검증 질문

```
□ 이 이름만 보고 역할을 알 수 있나?
□ 검색해서 찾을 수 있나?
□ 발음할 수 있나?
□ 오해의 소지가 없나?
□ 일관성 있게 사용하고 있나?
```

### 일관성 규칙

```
같은 개념 = 같은 단어

❌ 혼용하면 혼란
get, fetch, retrieve, find → 하나만!
controller, manager, handler → 하나만!

✅ 프로젝트 내 통일
get_user, get_order, get_product
UserController, OrderController
```

### 길이 가이드

```
변수: 범위에 비례
├── 좁은 범위: 짧아도 OK (i, x)
├── 넓은 범위: 길고 명확하게
└── 전역: 매우 상세하게

함수: 동사 + 목적어
├── 2~4단어가 적당
└── 너무 길면 분리 신호

클래스: 명사구
├── 1~3단어
└── 역할이 명확하게
```

### 피해야 할 패턴

```
❌ 인코딩
strName (헝가리안 표기법)
m_count (멤버 변수 표시)

❌ 약어 남용
usr (user)
msg (message)
btn (button) - 이건 OK

❌ 숫자 접미사
user1, user2 → users[0], users[1]

❌ 과도한 접두사
IUserInterface → UserInterface
```"""
            }
        ]
    },

    "01_클린코드/naming-convention": {
        "title": "네이밍 컨벤션",
        "description": "언어별 네이밍 규칙을 익힙니다",
        "sections": [
            {
                "type": "concept",
                "title": "📏 네이밍 컨벤션이란?",
                "content": """## 📏 한 줄 요약
> **이름 짓는 규칙** - 언어/팀마다 정해진 스타일을 따라요!

---

## 💡 왜 컨벤션을 따라야 하나?

### 일관성의 힘:
```
코드베이스 전체가 한 사람이 쓴 것처럼!

장점:
├── 빠른 이해
├── 예측 가능
├── 협업 용이
└── 실수 감소
```

---

## 🎯 케이스 스타일

### 1. camelCase
```javascript
// 첫 단어 소문자, 이후 단어 첫 글자 대문자
let userName = "Kim";
function getUserById(userId) { ... }

// 사용처: JavaScript, Java 변수/함수
```

### 2. PascalCase (UpperCamelCase)
```javascript
// 모든 단어 첫 글자 대문자
class UserService { ... }
const MyComponent = () => { ... }

// 사용처: 클래스, React 컴포넌트
```

### 3. snake_case
```python
# 모든 소문자, 단어 사이 밑줄
user_name = "Kim"
def get_user_by_id(user_id): ...

# 사용처: Python, Ruby, 데이터베이스
```

### 4. SCREAMING_SNAKE_CASE
```python
# 모든 대문자, 단어 사이 밑줄
MAX_RETRY_COUNT = 3
DATABASE_URL = "localhost"

# 사용처: 상수 (대부분 언어)
```

### 5. kebab-case
```html
<!-- 소문자, 단어 사이 하이픈 -->
<div class="user-profile">
<user-card />

<!-- 사용처: HTML/CSS 클래스, URL -->
```"""
            },
            {
                "type": "code",
                "title": "💻 언어별 컨벤션",
                "content": """### JavaScript / TypeScript

```javascript
// 변수, 함수: camelCase
const userName = "Kim";
function calculateTotal(items) { ... }

// 클래스, 컴포넌트: PascalCase
class UserService { ... }
const MyComponent = () => { ... };

// 상수: SCREAMING_SNAKE_CASE
const MAX_ITEMS = 100;
const API_BASE_URL = "https://api.example.com";

// private: _ 접두사 (관례)
class User {
    _password = "";  // private 의도
}

// 파일명: 컴포넌트는 PascalCase, 나머지는 kebab-case
// UserProfile.tsx, user-service.ts, utils.ts
```

### Python

```python
# 변수, 함수: snake_case
user_name = "Kim"
def get_user_by_id(user_id): ...

# 클래스: PascalCase
class UserService:
    pass

# 상수: SCREAMING_SNAKE_CASE
MAX_RETRY_COUNT = 3
DATABASE_URL = "localhost"

# private: _ 접두사
class User:
    def __init__(self):
        self._password = ""  # protected 의도
        self.__secret = ""   # private (name mangling)

# 모듈/패키지: snake_case
# user_service.py, database_helper.py
```

### Java

```java
// 변수, 메서드: camelCase
String userName = "Kim";
public User getUserById(Long userId) { ... }

// 클래스, 인터페이스: PascalCase
public class UserService { ... }
public interface UserRepository { ... }

// 상수: SCREAMING_SNAKE_CASE
public static final int MAX_RETRY_COUNT = 3;

// 패키지: 소문자
package com.example.userservice;
```

### CSS

```css
/* 클래스: kebab-case */
.user-profile { }
.btn-primary { }
.nav-item-active { }

/* BEM 방법론 */
.block__element--modifier { }
.card__title--highlighted { }

/* CSS-in-JS (camelCase) */
const styles = {
    userProfile: { },
    btnPrimary: { }
};
```"""
            },
            {
                "type": "tip",
                "title": "💡 컨벤션 정리표",
                "content": """### 언어별 요약

```
┌───────────┬───────────┬───────────┬───────────┐
│           │ 변수/함수  │ 클래스    │ 상수      │
├───────────┼───────────┼───────────┼───────────┤
│ JavaScript│ camelCase │ PascalCase│ SCREAMING │
│ Python    │ snake_case│ PascalCase│ SCREAMING │
│ Java      │ camelCase │ PascalCase│ SCREAMING │
│ C#        │ camelCase │ PascalCase│ SCREAMING │
│ Go        │ camelCase │ PascalCase│ camelCase │
│ Ruby      │ snake_case│ PascalCase│ SCREAMING │
└───────────┴───────────┴───────────┴───────────┘
```

### 특수 케이스

```
약어 처리:
❌ HTTPServer, XMLParser
✅ HttpServer, XmlParser
   (2글자 초과 약어는 일반 단어처럼)

Boolean 변수:
✅ isActive, hasPermission, canEdit
❌ active (동사인지 형용사인지 모호)

이벤트 핸들러:
✅ onClick, handleSubmit, onUserCreated
❌ click, submit (동작인지 핸들러인지 모호)
```

### 도구로 강제하기

```javascript
// ESLint 설정
{
  "rules": {
    "camelcase": "error",
    "@typescript-eslint/naming-convention": [
      "error",
      { "selector": "class", "format": ["PascalCase"] },
      { "selector": "function", "format": ["camelCase"] }
    ]
  }
}
```

```python
# pylint 설정 (.pylintrc)
[FORMAT]
variable-naming-style=snake_case
function-naming-style=snake_case
class-naming-style=PascalCase
const-naming-style=UPPER_CASE
```

### 팀 규칙이 우선

```
언어 표준 < 팀 컨벤션

팀에서 정한 규칙이 있다면 그것을 따르세요.
일관성이 가장 중요합니다!

문서화 필수:
├── CONTRIBUTING.md
├── .editorconfig
└── 린터 설정 파일
```"""
            }
        ]
    },

    "01_클린코드/function": {
        "title": "함수",
        "description": "좋은 함수 작성법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "🔧 좋은 함수란?",
                "content": """## 🔧 한 줄 요약
> **한 가지 일만 잘 하는 작은 함수** - 읽기 쉽고 테스트하기 쉬워요!

---

## 💡 함수의 원칙

### 1. 작게 만들어라
```python
# ❌ 너무 긴 함수
def process_order(order):
    # 100줄의 코드...
    # 유효성 검사
    # 재고 확인
    # 결제 처리
    # 배송 등록
    # 이메일 발송
    # ...

# ✅ 작은 함수들로 분리
def process_order(order):
    validate_order(order)
    check_inventory(order.items)
    process_payment(order)
    register_shipping(order)
    send_confirmation_email(order)
```

### 2. 한 가지만 해라
```python
# ❌ 여러 가지 일
def create_user_and_send_email(user_data):
    user = User(**user_data)
    db.save(user)
    email_service.send_welcome(user.email)
    return user

# ✅ 한 가지 일만
def create_user(user_data):
    user = User(**user_data)
    db.save(user)
    return user

def send_welcome_email(user):
    email_service.send_welcome(user.email)
```

### 3. 추상화 수준 통일
```python
# ❌ 추상화 수준 뒤죽박죽
def process_signup(email, password):
    # 고수준
    validate_email(email)
    # 저수준
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    # 고수준
    save_user(email, hashed)

# ✅ 추상화 수준 통일
def process_signup(email, password):
    validate_email(email)
    hashed_password = hash_password(password)
    save_user(email, hashed_password)
```

---

## 🎯 함수 작성 규칙

```
1. 이름: 동사 + 목적어
2. 길이: 20줄 이내 권장
3. 들여쓰기: 2단계 이내
4. 파라미터: 3개 이내
5. 부수 효과: 최소화
```"""
            },
            {
                "type": "code",
                "title": "💻 함수 개선 예시",
                "content": """### 조건문 추출

```javascript
// ❌ 복잡한 조건문
function canAccessResource(user, resource) {
    if (user.role === 'admin' ||
        (user.role === 'editor' && resource.type === 'article') ||
        (user.id === resource.ownerId && resource.status !== 'locked')) {
        return true;
    }
    return false;
}

// ✅ 조건 추출
function canAccessResource(user, resource) {
    if (isAdmin(user)) return true;
    if (isEditorWithArticle(user, resource)) return true;
    if (isOwnerWithUnlockedResource(user, resource)) return true;
    return false;
}

function isAdmin(user) {
    return user.role === 'admin';
}

function isEditorWithArticle(user, resource) {
    return user.role === 'editor' && resource.type === 'article';
}

function isOwnerWithUnlockedResource(user, resource) {
    return user.id === resource.ownerId && resource.status !== 'locked';
}
```

### 반복문 추출

```python
# ❌ 긴 반복문
def calculate_stats(orders):
    total = 0
    count = 0
    max_price = 0

    for order in orders:
        if order.status == 'completed':
            total += order.price
            count += 1
            if order.price > max_price:
                max_price = order.price

    return {
        'total': total,
        'count': count,
        'average': total / count if count > 0 else 0,
        'max': max_price
    }

# ✅ 함수로 분리
def calculate_stats(orders):
    completed_orders = get_completed_orders(orders)
    return {
        'total': calculate_total(completed_orders),
        'count': len(completed_orders),
        'average': calculate_average(completed_orders),
        'max': find_max_price(completed_orders)
    }

def get_completed_orders(orders):
    return [o for o in orders if o.status == 'completed']

def calculate_total(orders):
    return sum(o.price for o in orders)
```

### 플래그 인자 제거

```python
# ❌ Boolean 플래그
def create_user(name, email, send_email=True):
    user = User(name=name, email=email)
    db.save(user)
    if send_email:
        send_welcome_email(user)
    return user

# ✅ 함수 분리
def create_user(name, email):
    user = User(name=name, email=email)
    db.save(user)
    return user

def create_user_and_notify(name, email):
    user = create_user(name, email)
    send_welcome_email(user)
    return user
```"""
            },
            {
                "type": "tip",
                "title": "💡 함수 체크리스트",
                "content": """### 좋은 함수 기준

```
□ 이름만 보고 기능을 알 수 있다
□ 20줄 이내다
□ 들여쓰기 2단계 이내다
□ 파라미터 3개 이내다
□ 한 가지 일만 한다
□ 부수 효과가 없다 (있다면 이름에 표현)
□ 테스트하기 쉽다
```

### 함수 분리 신호

```
분리가 필요할 때:
├── 주석으로 구역을 나눌 때
├── 조건문/반복문이 중첩될 때
├── 재사용 가능한 로직이 보일 때
├── 테스트하기 어려울 때
└── "그리고"가 붙으면 (A하고 B하는 함수)
```

### 네이밍 패턴

```
CRUD:
create_user, get_user, update_user, delete_user

변환:
to_json, from_dict, parse_date, format_currency

검증:
validate_email, is_valid_phone, check_permission

이벤트:
on_click, handle_submit, notify_observers
```

### 순수 함수 지향

```python
# ❌ 부수 효과 있음
total = 0
def add_to_total(value):
    global total
    total += value

# ✅ 순수 함수
def add(a, b):
    return a + b

# 장점:
# - 테스트 쉬움
# - 예측 가능
# - 병렬 처리 안전
```"""
            }
        ]
    },

    "01_클린코드/function-parameter": {
        "title": "함수 파라미터",
        "description": "함수 파라미터 설계를 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "📦 파라미터 설계",
                "content": """## 📦 한 줄 요약
> **적을수록 좋다** - 파라미터가 많으면 이해하기 어렵고 테스트하기 힘들어요!

---

## 💡 파라미터 개수 원칙

### 이상적인 개수:
```
0개 (niladic)  ★★★★★ 최고
1개 (monadic)  ★★★★☆ 좋음
2개 (dyadic)   ★★★☆☆ 괜찮음
3개 (triadic)  ★★☆☆☆ 피하자
4개 이상       ★☆☆☆☆ 리팩토링 필요
```

### 왜 적어야 하나?
```
파라미터가 많으면:
├── 함수 이해 어려움
├── 호출 시 순서 헷갈림
├── 테스트 케이스 폭발
└── 변경 시 영향 범위 큼
```

---

## 🎯 파라미터 줄이기 전략

### 1. 객체로 묶기
```python
# ❌ 파라미터 6개
def create_user(name, email, phone, address, city, country):
    ...

# ✅ 객체로 묶기
def create_user(user_data):
    ...

# 또는 DTO 클래스
@dataclass
class CreateUserRequest:
    name: str
    email: str
    phone: str
    address: str
    city: str
    country: str

def create_user(request: CreateUserRequest):
    ...
```

### 2. 메서드로 변환
```python
# ❌ 객체와 데이터 분리
def calculate_area(shape, width, height):
    if shape == 'rectangle':
        return width * height
    ...

# ✅ 메서드로
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height
```

### 3. Builder 패턴
```python
# ❌ 많은 선택적 파라미터
def send_email(to, subject, body,
               cc=None, bcc=None,
               attachments=None,
               priority='normal',
               template=None):
    ...

# ✅ Builder 패턴
email = EmailBuilder()
    .to("user@example.com")
    .subject("Hello")
    .body("Content")
    .with_attachment("file.pdf")
    .high_priority()
    .build()

email.send()
```"""
            },
            {
                "type": "code",
                "title": "💻 파라미터 개선 예시",
                "content": """### 플래그 파라미터 제거

```javascript
// ❌ Boolean 플래그
function renderPage(isAdmin) {
    if (isAdmin) {
        // 관리자 페이지 렌더링
    } else {
        // 일반 페이지 렌더링
    }
}

// ✅ 함수 분리
function renderAdminPage() { ... }
function renderUserPage() { ... }

// 호출하는 쪽에서 선택
if (user.isAdmin) {
    renderAdminPage();
} else {
    renderUserPage();
}
```

### 출력 파라미터 피하기

```python
# ❌ 출력 파라미터 (result를 수정)
def append_footer(result):
    result.append("==== Footer ====")

report = []
generate_content(report)
append_footer(report)  # report가 변경됨 (예측 어려움)

# ✅ 반환값 사용
def create_footer():
    return "==== Footer ===="

report = generate_content()
report.append(create_footer())
```

### Named Arguments 활용

```python
# ❌ 순서 기억 필요
create_rectangle(100, 200, True, False)
# 100이 뭐지? True가 뭐지?

# ✅ Named arguments
create_rectangle(
    width=100,
    height=200,
    fill=True,
    visible=False
)
```

```javascript
// JavaScript: 객체 구조 분해
// ❌
function createUser(name, email, age, isAdmin) { ... }
createUser('Kim', 'kim@mail.com', 25, true);

// ✅
function createUser({ name, email, age, isAdmin = false }) { ... }
createUser({
    name: 'Kim',
    email: 'kim@mail.com',
    age: 25,
    isAdmin: true
});
```

### 기본값 설정

```python
# Python
def fetch_users(page=1, limit=20, sort_by='created_at'):
    ...

# TypeScript
function fetchUsers(
    page: number = 1,
    limit: number = 20,
    sortBy: string = 'createdAt'
): Promise<User[]> { ... }
```"""
            },
            {
                "type": "tip",
                "title": "💡 파라미터 체크리스트",
                "content": """### 리팩토링 신호

```
파라미터 줄이기가 필요할 때:

□ 파라미터가 4개 이상
□ Boolean 플래그가 있음
□ 출력 파라미터 사용
□ 여러 파라미터가 항상 함께 전달됨
□ 파라미터 순서 자주 헷갈림
□ null 체크가 많음
```

### 해결 전략 요약

```
1. 객체로 묶기
   - 관련 파라미터 그룹화
   - DTO/VO 클래스 생성

2. 함수 분리
   - Boolean 플래그 → 함수 2개로
   - 조건부 로직 분리

3. 메서드 추출
   - 객체의 메서드로 변환
   - this로 암묵적 파라미터

4. Builder 패턴
   - 선택적 파라미터 많을 때
   - 가독성 향상
```

### 언어별 팁

```
Python:
- *args, **kwargs 남용 피하기
- dataclass 활용

JavaScript:
- 객체 구조 분해 활용
- 기본값 설정 활용

TypeScript:
- 인터페이스로 타입 정의
- Optional 파라미터 (?)

Java:
- Builder 패턴
- Lombok @Builder
```

### 테스트 관점

```
파라미터가 적으면:
- 테스트 케이스 줄어듦
- Mock 객체 단순화
- 경계 조건 관리 쉬움

파라미터 3개 = 테스트 케이스 폭발
├── 각 파라미터 정상/비정상
├── 조합 테스트
└── 유지보수 악몽
```"""
            }
        ]
    },

    "01_클린코드/comment": {
        "title": "주석",
        "description": "좋은 주석과 나쁜 주석을 구분합니다",
        "sections": [
            {
                "type": "concept",
                "title": "💬 주석의 진실",
                "content": """## 💬 한 줄 요약
> **주석은 실패의 증거** - 코드로 의도를 표현하지 못했다는 뜻이에요!

---

## 💡 주석이 필요한 이유?

### 주석의 문제점:
```
1. 코드와 동기화 안 됨
   코드 수정 → 주석은 그대로 → 거짓말

2. 주석 없이 이해 못 함 = 나쁜 코드
   코드가 스스로 설명해야 함

3. 주석으로 나쁜 코드 변명
   "복잡해서 주석 달았어요"
   → 복잡하지 않게 리팩토링하세요
```

### 좋은 코드 vs 주석:
```python
# ❌ 주석으로 설명
# 30일 이내 가입하고 구매 이력 있는 활성 사용자 확인
if user.created_at > datetime.now() - timedelta(days=30) and \
   user.status == 'active' and \
   len(user.orders) > 0:

# ✅ 코드로 설명
def is_new_active_buyer(user):
    return (
        is_recently_joined(user) and
        is_active(user) and
        has_purchase_history(user)
    )

if is_new_active_buyer(user):
```

---

## 🎯 좋은 주석 vs 나쁜 주석

### 좋은 주석:
```python
# 법적 주석 (저작권, 라이센스)
# Copyright (c) 2024 Company. All rights reserved.

# 의도 설명 (왜 이렇게 했는지)
# 성능상 이유로 캐시 사용 (DB 조회 비용 절감)
cached_result = cache.get(key)

# 결과 경고
# WARNING: 이 함수는 DB를 초기화합니다!
def reset_database():

# TODO 주석
# TODO: 다음 스프린트에서 비동기로 변경 예정
```

### 나쁜 주석:
```python
# ❌ 당연한 설명
i = 0  # i를 0으로 초기화

# ❌ 코드 반복
# 사용자 이름을 가져온다
user_name = user.get_name()

# ❌ 주석 처리된 코드
# old_function()
# deprecated_call()

# ❌ 이력 주석 (Git 있잖아요)
# 2024-01-15 김개발: 버그 수정
# 2024-01-16 이개발: 기능 추가

# ❌ 위치 표시
# //////////// 유틸리티 함수들 ////////////
```"""
            },
            {
                "type": "code",
                "title": "💻 주석 개선 예시",
                "content": """### 주석을 코드로 변환

```python
# ❌ 주석 필요
# 사용자가 프리미엄이고 구독이 활성 상태인지 확인
if user.plan == 'premium' and user.subscription.status == 'active':
    ...

# ✅ 함수로 추출
def has_active_premium_subscription(user):
    return user.plan == 'premium' and user.subscription.status == 'active'

if has_active_premium_subscription(user):
    ...
```

### 매직 넘버 제거

```javascript
// ❌ 매직 넘버 + 주석
setTimeout(callback, 86400000); // 24시간 (밀리초)

// ✅ 상수로 의미 부여
const ONE_DAY_IN_MS = 24 * 60 * 60 * 1000;
setTimeout(callback, ONE_DAY_IN_MS);
```

### 조건문 명확화

```python
# ❌ 복잡한 조건 + 주석
# 관리자이거나, 소유자이면서 공개 상태일 때
if (user.role == 'admin' or
    (user.id == resource.owner_id and resource.is_public)):

# ✅ 조건 추출
def can_access(user, resource):
    return is_admin(user) or is_owner_of_public_resource(user, resource)

def is_admin(user):
    return user.role == 'admin'

def is_owner_of_public_resource(user, resource):
    return user.id == resource.owner_id and resource.is_public

if can_access(user, resource):
```

### 좋은 주석 예시

```python
# 정규식 설명 (복잡한 패턴)
# 형식: XXX-XXXX-XXXX (한국 전화번호)
PHONE_PATTERN = r'^\\d{3}-\\d{4}-\\d{4}$'

# 외부 요인 설명
# API 제한으로 인해 1초 대기 필요 (Rate limit: 60 req/min)
time.sleep(1)

# 의도 설명
# 빈 배열 반환 (None 대신) - 호출자가 null 체크 불필요
def get_items():
    return items if items else []

# 경고
# 주의: 이 메서드는 스레드 안전하지 않음
def update_cache():
```"""
            },
            {
                "type": "tip",
                "title": "💡 주석 가이드라인",
                "content": """### 주석 작성 전 질문

```
"주석 없이 이해할 수 있게
 코드를 개선할 방법은 없는가?"

대부분 있습니다:
├── 함수 추출
├── 변수/상수 이름 개선
├── 조건문 분리
└── 구조 개선
```

### 허용되는 주석

```
✅ 좋은 주석:
├── 법적 주석 (저작권)
├── 복잡한 정규식 설명
├── API/라이브러리 제약 설명
├── 성능 결정 이유
├── WARNING/TODO
└── 공개 API 문서 (JSDoc, docstring)

❌ 피해야 할 주석:
├── 코드 번역 주석
├── 주석 처리된 코드
├── 변경 이력
├── 위치 표시자
└── 닫는 괄호 주석
```

### 문서화 주석 (DocString)

```python
# Python docstring
def calculate_discount(price: float, rate: float) -> float:
    \"\"\"
    가격에 할인율을 적용합니다.

    Args:
        price: 원래 가격
        rate: 할인율 (0.0 ~ 1.0)

    Returns:
        할인된 가격

    Raises:
        ValueError: 할인율이 0~1 범위 밖일 때
    \"\"\"
    if not 0 <= rate <= 1:
        raise ValueError("할인율은 0~1 사이여야 합니다")
    return price * (1 - rate)
```

### 주석 처리된 코드

```
❌ 절대 남기지 마세요

이유:
├── Git에 이력 있음
├── 코드 오염
├── 언제 지울지 모름
├── 관련 코드인지 혼란

→ 삭제하세요. 필요하면 Git에서 복구.
```"""
            }
        ]
    },

    "01_클린코드/formatting": {
        "title": "포맷팅",
        "description": "코드 포맷팅의 중요성과 규칙을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "📐 코드 포맷팅",
                "content": """## 📐 한 줄 요약
> **일관된 모양** - 팀 전체가 한 사람이 작성한 것처럼 보여야 해요!

---

## 💡 왜 포맷팅이 중요한가?

### 가독성의 핵심:
```
코드는 글이다.
└── 단락, 줄바꿈, 들여쓰기 = 가독성

잘 정돈된 코드:
├── 빠르게 이해
├── 구조 파악 용이
├── 버그 발견 쉬움
└── 협업 효율 상승
```

### 나쁜 포맷팅의 비용:
```
❌ 들쭉날쭉한 포맷
├── 읽는 데 시간 낭비
├── 실수로 인한 버그
├── PR 리뷰 시 불필요한 논쟁
└── 새 팀원 적응 어려움
```

---

## 🎯 포맷팅 원칙

### 1. 세로 포맷팅
```python
# 파일 구조 (위 → 아래로 읽히게)
# 1. imports
# 2. 상수
# 3. 클래스/함수 (고수준 → 저수준)

# 관련 코드는 가깝게
class User:
    def __init__(self, name):
        self.name = name

    def get_name(self):  # name 관련 메서드
        return self.name

    def set_name(self, name):  # name 관련 메서드
        self.name = name

# 다른 개념은 빈 줄로 분리
    def calculate_age(self):  # 다른 기능
        ...
```

### 2. 가로 포맷팅
```python
# ❌ 너무 긴 줄
result = some_function(very_long_parameter_1, very_long_parameter_2, very_long_parameter_3, very_long_parameter_4)

# ✅ 적절히 나누기
result = some_function(
    very_long_parameter_1,
    very_long_parameter_2,
    very_long_parameter_3,
    very_long_parameter_4
)

# 권장 줄 길이: 80~120자
```

### 3. 들여쓰기
```python
# 일관된 들여쓰기 (스페이스 vs 탭 통일)
def outer():
    def inner():
        if condition:
            do_something()
            # 적절한 depth 유지 (3단계 이내 권장)
```"""
            },
            {
                "type": "code",
                "title": "💻 포맷팅 예시",
                "content": """### 수직 정렬

```python
# ❌ 뒤죽박죽
import os
import sys
from datetime import datetime
import json
from collections import defaultdict

# ✅ 그룹화 + 정렬
# 표준 라이브러리
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

# 서드파티
import requests
from flask import Flask

# 로컬
from myapp.models import User
from myapp.utils import helper
```

### 클래스 내부 순서

```python
class UserService:
    # 1. 클래스 변수
    DEFAULT_ROLE = 'user'

    # 2. __init__
    def __init__(self, db):
        self.db = db

    # 3. public 메서드
    def get_user(self, user_id):
        return self._find_user(user_id)

    def create_user(self, data):
        user = self._build_user(data)
        return self._save_user(user)

    # 4. private 메서드 (호출되는 순서대로)
    def _find_user(self, user_id):
        ...

    def _build_user(self, data):
        ...

    def _save_user(self, user):
        ...
```

### 연산자 정렬

```javascript
// ❌ 정렬 없음
const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
    maxRetries: 3,
    enableLogging: true
};

// ✅ 가독성 좋게 (선택적)
const config = {
    apiUrl:        'https://api.example.com',
    timeout:       5000,
    maxRetries:    3,
    enableLogging: true
};

// 또는 그냥 일반 정렬 (더 권장)
const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
    maxRetries: 3,
    enableLogging: true,
};
```

### 빈 줄 사용

```python
class OrderService:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()

    # 빈 줄로 메서드 구분
    def create_order(self, items):
        # 로직 그룹 1: 검증
        self._validate_items(items)
        self._check_stock(items)

        # 빈 줄로 구분
        # 로직 그룹 2: 생성
        order = Order(items)
        self.db.save(order)

        # 빈 줄로 구분
        # 로직 그룹 3: 후처리
        self._send_notification(order)
        return order
```"""
            },
            {
                "type": "tip",
                "title": "💡 포맷팅 도구",
                "content": """### 자동 포맷터 사용하기

```
논쟁하지 말고 도구에 맡기세요!

JavaScript/TypeScript:
├── Prettier (추천!)
└── ESLint --fix

Python:
├── Black (추천!)
├── autopep8
└── yapf

Java:
├── Google Java Format
└── Checkstyle

Go:
└── gofmt (내장)
```

### 설정 파일 예시

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

```toml
# pyproject.toml (Black)
[tool.black]
line-length = 100
target-version = ['py39']
skip-string-normalization = true
```

### 에디터 설정

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### .editorconfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
```

### CI에서 검사

```yaml
# GitHub Actions
- name: Check formatting
  run: |
    npm run lint
    npm run format:check
```"""
            }
        ]
    },

    "01_클린코드/error-handling": {
        "title": "에러 처리",
        "description": "깔끔한 에러 처리 방법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "⚠️ 에러 처리 원칙",
                "content": """## ⚠️ 한 줄 요약
> **에러 처리도 로직이다** - 깔끔하게 분리하고 명확하게 처리하세요!

---

## 💡 에러 처리가 중요한 이유

### 현실:
```
프로덕션에서:
├── 네트워크 끊김
├── DB 연결 실패
├── 잘못된 입력
├── 권한 없음
└── 예상치 못한 상황

→ 에러 처리 = 신뢰성의 핵심
```

---

## 🎯 에러 처리 원칙

### 1. 예외를 사용하라 (에러 코드 대신)
```python
# ❌ 에러 코드 반환
def get_user(user_id):
    user = db.find(user_id)
    if user is None:
        return -1  # 에러 코드
    return user

result = get_user(1)
if result == -1:  # 매번 체크 필요
    print("에러!")

# ✅ 예외 사용
def get_user(user_id):
    user = db.find(user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    return user

try:
    user = get_user(1)
except UserNotFoundError as e:
    handle_error(e)
```

### 2. 예외에 의미를 담아라
```python
# ❌ 일반 예외
raise Exception("Error")

# ✅ 구체적인 예외
raise UserNotFoundError(user_id=1)
raise InvalidEmailError(email="invalid")
raise InsufficientFundsError(balance=100, required=500)
```

### 3. null 반환 피하기
```python
# ❌ null 반환
def find_user(user_id):
    return db.find(user_id)  # None 가능

user = find_user(1)
if user:  # 매번 null 체크
    print(user.name)

# ✅ 예외 또는 Optional
def find_user(user_id) -> Optional[User]:
    user = db.find(user_id)
    if user is None:
        raise UserNotFoundError()
    return user

# 또는 빈 객체/컬렉션 반환
def find_users(query) -> List[User]:
    return db.find_all(query) or []  # 빈 리스트 반환
```"""
            },
            {
                "type": "code",
                "title": "💻 에러 처리 패턴",
                "content": """### 커스텀 예외 클래스

```python
# 기본 예외 클래스
class AppError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

# 도메인별 예외
class UserError(AppError):
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id):
        super().__init__(f"User {user_id} not found", "USER_NOT_FOUND")
        self.user_id = user_id

class InvalidCredentialsError(UserError):
    def __init__(self):
        super().__init__("Invalid credentials", "INVALID_CREDENTIALS")

# 사용
try:
    user = get_user(user_id)
except UserNotFoundError as e:
    logger.error(f"User not found: {e.user_id}")
    return {"error": e.code, "message": str(e)}
```

### try-catch 범위 최소화

```javascript
// ❌ 너무 넓은 범위
try {
    const user = await getUser(id);
    const orders = await getOrders(user.id);
    const total = calculateTotal(orders);
    await sendReport(user.email, total);
} catch (e) {
    console.error('Something failed');  // 뭐가 실패한 거지?
}

// ✅ 구체적인 에러 처리
async function processUserReport(userId) {
    const user = await getUser(userId);  // 여기서 실패하면?

    let orders;
    try {
        orders = await getOrders(user.id);
    } catch (e) {
        logger.warn(`Orders not found for user ${userId}`);
        orders = [];  // 기본값으로 진행
    }

    const total = calculateTotal(orders);

    try {
        await sendReport(user.email, total);
    } catch (e) {
        logger.error(`Failed to send report: ${e.message}`);
        await queueForRetry(user.email, total);  // 재시도 큐에 추가
    }
}
```

### 에러 전파 vs 처리

```python
# 처리할 수 있으면 처리
def get_config(key):
    try:
        return config_store.get(key)
    except ConfigNotFoundError:
        return DEFAULT_CONFIG[key]  # 기본값으로 처리

# 처리할 수 없으면 전파
def save_user(user):
    try:
        db.save(user)
    except DatabaseError as e:
        logger.error(f"Failed to save user: {e}")
        raise  # 상위로 전파 (여기서 처리 불가)
```

### 글로벌 에러 핸들러

```javascript
// Express 에러 핸들러
app.use((err, req, res, next) => {
    logger.error(err.stack);

    if (err instanceof ValidationError) {
        return res.status(400).json({
            error: 'VALIDATION_ERROR',
            message: err.message,
            details: err.details
        });
    }

    if (err instanceof NotFoundError) {
        return res.status(404).json({
            error: 'NOT_FOUND',
            message: err.message
        });
    }

    // 알 수 없는 에러
    return res.status(500).json({
        error: 'INTERNAL_ERROR',
        message: 'Something went wrong'
    });
});
```"""
            },
            {
                "type": "tip",
                "title": "💡 에러 처리 팁",
                "content": """### 에러 처리 체크리스트

```
□ 예외에 충분한 정보가 있는가?
□ 복구 가능한 에러는 처리하고 있는가?
□ 예상치 못한 에러는 로깅하는가?
□ 사용자에게 친절한 메시지인가?
□ 민감 정보가 노출되지 않는가?
```

### 로깅 vs 던지기

```
로깅만: 복구 가능, 무시해도 됨
던지기만: 상위에서 처리 가능
둘 다: 여기서 로깅 + 상위 알림

❌ 피해야 할 것:
- 잡고 무시 (catch 비우기)
- 로깅도 안 하고 삼키기
```

### 방어적 프로그래밍

```python
# 입력 검증
def process_payment(amount):
    if amount is None:
        raise ValueError("Amount is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > MAX_AMOUNT:
        raise ValueError(f"Amount exceeds limit: {MAX_AMOUNT}")

    # 검증 통과 후 로직
    ...
```

### 에러 메시지 작성법

```
❌ 나쁜 메시지:
"Error occurred"
"Invalid input"
"Something went wrong"

✅ 좋은 메시지:
"User with ID 123 not found"
"Email format invalid: missing @ symbol"
"Payment failed: insufficient balance (required: $100, available: $50)"

포함할 것:
├── 무엇이 잘못되었는지
├── 왜 잘못되었는지
└── 어떻게 해결하는지 (가능하면)
```"""
            }
        ]
    },

    "01_클린코드/boundary": {
        "title": "경계",
        "description": "외부 코드와의 경계를 관리하는 방법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "🚧 경계란?",
                "content": """## 🚧 한 줄 요약
> **외부 코드와 우리 코드 사이의 접점** - 잘 관리해야 변경에 강해요!

---

## 💡 왜 경계가 중요한가?

### 외부 코드의 위험:
```
외부 라이브러리/API:
├── 언제든 변경될 수 있음
├── 우리 의도와 다를 수 있음
├── 버전 업데이트 시 영향
└── 테스트하기 어려움
```

### 경계 없이 사용하면:
```python
# ❌ 외부 라이브러리 직접 사용
from third_party_lib import SpecificClass

class MyService:
    def do_something(self):
        # third_party_lib가 변경되면?
        obj = SpecificClass()
        obj.specific_method()  # 전체 코드 수정 필요
```

---

## 🎯 경계 관리 원칙

### 1. Wrapper 사용
```python
# ✅ Wrapper로 감싸기
class MyWrapper:
    def __init__(self):
        self._lib = SpecificClass()

    def do_something(self):
        return self._lib.specific_method()

# 라이브러리 변경 시 Wrapper만 수정
# 나머지 코드는 그대로!
```

### 2. 인터페이스 정의
```python
# ✅ 우리가 원하는 인터페이스 정의
from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def save(self, data): pass

    @abstractmethod
    def load(self, key): pass

# 구현은 외부 라이브러리 사용
class S3Storage(StorageInterface):
    def save(self, data):
        boto3.upload(...)  # AWS SDK 사용

class LocalStorage(StorageInterface):
    def save(self, data):
        with open(...) as f: ...

# 사용하는 쪽은 인터페이스만 알면 됨
```

### 3. 학습 테스트
```python
# 외부 라이브러리 동작 확인용 테스트
class ThirdPartyLibLearningTest(unittest.TestCase):
    def test_basic_usage(self):
        # 라이브러리가 예상대로 동작하는지 확인
        result = third_party_lib.do_something()
        self.assertEqual(result, expected)

    # 버전 업데이트 시 이 테스트로 변경 사항 파악
```"""
            },
            {
                "type": "code",
                "title": "💻 경계 처리 패턴",
                "content": """### Adapter 패턴

```python
# 외부 결제 라이브러리
class StripePayment:
    def charge_card(self, card_number, amount, currency):
        ...

# 우리 인터페이스
class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: int, payment_info: dict) -> bool:
        pass

# Adapter
class StripeAdapter(PaymentGateway):
    def __init__(self):
        self._stripe = StripePayment()

    def process_payment(self, amount: int, payment_info: dict) -> bool:
        try:
            self._stripe.charge_card(
                card_number=payment_info['card'],
                amount=amount / 100,  # 원 → 달러 변환
                currency='USD'
            )
            return True
        except StripeError:
            return False

# 사용
class OrderService:
    def __init__(self, payment: PaymentGateway):  # 인터페이스 의존
        self.payment = payment

    def checkout(self, order):
        return self.payment.process_payment(order.total, order.payment_info)

# 나중에 결제 시스템 변경해도 OrderService는 그대로!
```

### 외부 Map 감싸기

```java
// ❌ 외부 Map 직접 노출
public Map<String, User> getUsers() {
    return users;  // 누구나 수정 가능
}

// ✅ Wrapper로 감싸기
public class UserRepository {
    private Map<String, User> users = new HashMap<>();

    public User findById(String id) {
        return users.get(id);
    }

    public void save(User user) {
        users.put(user.getId(), user);
    }

    public List<User> findAll() {
        return new ArrayList<>(users.values());  // 복사본 반환
    }
}
```

### API 응답 변환

```javascript
// 외부 API 응답
const apiResponse = {
    user_name: 'Kim',
    user_email: 'kim@test.com',
    created_at: '2024-01-15T00:00:00Z'
};

// ✅ 우리 모델로 변환
class UserMapper {
    static fromApiResponse(response) {
        return {
            name: response.user_name,
            email: response.user_email,
            createdAt: new Date(response.created_at)
        };
    }

    static toApiRequest(user) {
        return {
            user_name: user.name,
            user_email: user.email
        };
    }
}

// 사용
const user = UserMapper.fromApiResponse(apiResponse);
```

### 테스트를 위한 경계

```python
# 외부 서비스 추상화
class NotificationService(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str): pass

# 실제 구현
class TwilioNotification(NotificationService):
    def send(self, recipient, message):
        twilio_client.messages.create(...)

# 테스트용 Mock
class MockNotification(NotificationService):
    def __init__(self):
        self.sent_messages = []

    def send(self, recipient, message):
        self.sent_messages.append((recipient, message))

# 테스트
def test_order_notification():
    mock_notifier = MockNotification()
    service = OrderService(notifier=mock_notifier)
    service.complete_order(order)

    assert len(mock_notifier.sent_messages) == 1
```"""
            },
            {
                "type": "tip",
                "title": "💡 경계 관리 팁",
                "content": """### 경계 관리 체크리스트

```
□ 외부 라이브러리를 직접 노출하고 있지 않은가?
□ 변경 시 영향 범위가 한정되어 있는가?
□ 테스트가 용이한가?
□ 학습 테스트가 있는가?
```

### Wrapper 적용 기준

```
Wrapper 필요:
├── 여러 곳에서 사용
├── 복잡한 외부 API
├── 변경 가능성 높음
├── 테스트 필요

Wrapper 불필요:
├── 한 곳에서만 사용
├── 단순한 유틸
├── 표준 라이브러리
```

### Anti-Corruption Layer

```
외부 시스템과 우리 시스템 사이 보호막

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 우리 시스템  │ ←→ │    ACL      │ ←→ │ 외부 시스템  │
│ (깨끗한 모델)│     │ (변환 담당)  │     │ (다른 모델)  │
└─────────────┘     └─────────────┘     └─────────────┘

역할:
├── 모델 변환
├── 에러 처리
├── 데이터 검증
└── 로깅
```

### 버전 업데이트 대응

```
1. 학습 테스트 실행
   └── 기존 동작 확인

2. Wrapper/Adapter만 수정
   └── 내부 코드는 그대로

3. 통합 테스트 실행
   └── 전체 동작 확인

→ 영향 범위 최소화!
```"""
            }
        ]
    },

    "01_클린코드/code-smell": {
        "title": "코드 스멜",
        "description": "나쁜 코드의 징후를 파악합니다",
        "sections": [
            {
                "type": "concept",
                "title": "👃 코드 스멜이란?",
                "content": """## 👃 한 줄 요약
> **코드에서 나는 '냄새'** - 버그는 아니지만 뭔가 잘못됐다는 신호예요!

---

## 💡 왜 코드 스멜을 알아야 하나?

### 코드 스멜의 의미:
```
"지금은 동작하지만..."
├── 유지보수 어려움
├── 버그 발생 가능성 높음
├── 확장하기 힘듦
└── 리팩토링 필요 신호
```

---

## 🎯 주요 코드 스멜

### 1. 긴 메서드 (Long Method)
```python
# ❌ 100줄짜리 메서드
def process_order(order):
    # 검증 로직 30줄
    # 계산 로직 30줄
    # 저장 로직 20줄
    # 알림 로직 20줄
    ...

# 분리 신호: 주석으로 구역 나눔
```

### 2. 긴 파라미터 목록
```python
# ❌ 파라미터 지옥
def create_user(name, email, phone, address,
                city, country, zip_code, age,
                gender, occupation):
    ...
```

### 3. 중복 코드 (Duplicated Code)
```python
# ❌ 복붙 코드
def validate_user_email(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")

def validate_admin_email(email):
    if not email or '@' not in email:  # 똑같은 코드!
        raise ValueError("Invalid email")
```

### 4. 거대한 클래스 (God Class)
```python
# ❌ 모든 걸 다 하는 클래스
class UserManager:
    def create_user(self): ...
    def delete_user(self): ...
    def send_email(self): ...
    def process_payment(self): ...
    def generate_report(self): ...
    def backup_database(self): ...
```

### 5. 기능 편애 (Feature Envy)
```python
# ❌ 다른 객체의 데이터만 사용
class OrderPrinter:
    def print_order(self, order):
        print(f"Name: {order.customer.name}")
        print(f"Address: {order.customer.address}")
        print(f"Total: {order.calculate_total()}")
```"""
            },
            {
                "type": "code",
                "title": "💻 코드 스멜 해결",
                "content": """### 긴 메서드 → 메서드 추출

```python
# ❌ Before
def process_order(order):
    # 검증
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")

    # 가격 계산
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax

    # 저장
    db.save(order)

    # 알림
    send_email(order.customer.email, f"Order total: {total}")

# ✅ After
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order)
    notify_customer(order, total)

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")

def calculate_total(order):
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    return subtotal + tax
```

### 중복 코드 → 메서드/클래스 추출

```python
# ❌ Before: 중복
class UserService:
    def find_active_users(self):
        users = self.db.get_all_users()
        return [u for u in users if u.status == 'active' and not u.deleted]

class AdminService:
    def find_active_admins(self):
        admins = self.db.get_all_admins()
        return [a for a in admins if a.status == 'active' and not a.deleted]

# ✅ After: 공통 로직 추출
def filter_active(items):
    return [item for item in items if item.status == 'active' and not item.deleted]

class UserService:
    def find_active_users(self):
        return filter_active(self.db.get_all_users())

class AdminService:
    def find_active_admins(self):
        return filter_active(self.db.get_all_admins())
```

### 기능 편애 → 메서드 이동

```python
# ❌ Before: 다른 객체 데이터만 사용
class OrderPrinter:
    def get_summary(self, order):
        return f"{order.customer.name}: {order.calculate_total()}"

# ✅ After: 해당 클래스로 이동
class Order:
    def get_summary(self):
        return f"{self.customer.name}: {self.calculate_total()}"
```

### 매직 넘버 → 상수 추출

```python
# ❌ Before
if user.age >= 19:  # 19가 뭐지?
    ...

if retry_count > 3:  # 3이 뭐지?
    ...

# ✅ After
ADULT_AGE = 19
MAX_RETRY_COUNT = 3

if user.age >= ADULT_AGE:
    ...

if retry_count > MAX_RETRY_COUNT:
    ...
```"""
            },
            {
                "type": "tip",
                "title": "💡 코드 스멜 감지",
                "content": """### 주요 코드 스멜 목록

```
📏 크기 관련:
├── Long Method (긴 메서드)
├── Large Class (거대한 클래스)
├── Long Parameter List (긴 파라미터)
└── Data Clumps (데이터 뭉치)

🔄 중복 관련:
├── Duplicated Code (중복 코드)
├── Alternative Classes (유사 클래스)
└── Parallel Inheritance (평행 상속)

🏗️ 구조 관련:
├── Feature Envy (기능 편애)
├── Inappropriate Intimacy (지나친 친밀)
├── Middle Man (중개자)
└── Lazy Class (게으른 클래스)

✏️ 네이밍 관련:
├── Magic Numbers (매직 넘버)
├── Inconsistent Names (일관성 없는 이름)
└── Obscure Intent (불분명한 의도)
```

### 자동 감지 도구

```
JavaScript/TypeScript:
├── ESLint (complexity 규칙)
└── SonarQube

Python:
├── pylint
├── flake8
└── radon (복잡도)

Java:
├── SonarQube
├── PMD
└── FindBugs
```

### 리팩토링 우선순위

```
1순위: 중복 코드
└── 가장 흔하고 해결 효과 큼

2순위: 긴 메서드
└── 가독성 크게 향상

3순위: 거대한 클래스
└── 단일 책임으로 분리

4순위: 매직 넘버
└── 간단하지만 효과적
```"""
            }
        ]
    },

    "01_클린코드/dry-kiss": {
        "title": "DRY & KISS",
        "description": "DRY와 KISS 원칙을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🎯 DRY & KISS",
                "content": """## 🎯 한 줄 요약
> **DRY: 반복하지 마라 / KISS: 단순하게 해라** - 클린코드의 핵심 원칙!

---

## 💡 DRY (Don't Repeat Yourself)

### 의미:
```
"모든 지식은 시스템 내에서
 단일하고 명확하게 표현되어야 한다"

중복의 종류:
├── 코드 중복 (복붙)
├── 로직 중복 (같은 알고리즘)
├── 데이터 중복 (같은 상수)
└── 지식 중복 (같은 비즈니스 규칙)
```

### DRY 위반의 문제:
```
❌ 중복 코드가 있으면:
├── 수정 시 여러 곳 변경 필요
├── 하나 빼먹으면 버그
├── 코드량 증가
└── 유지보수 비용 증가
```

---

## 💡 KISS (Keep It Simple, Stupid)

### 의미:
```
"대부분의 시스템은 복잡하게 만들기보다
 단순하게 유지할 때 가장 잘 작동한다"

단순함:
├── 이해하기 쉬움
├── 버그 적음
├── 수정하기 쉬움
└── 테스트하기 쉬움
```

### KISS 위반의 문제:
```
❌ 과도한 복잡성:
├── 이해하는 데 시간 소요
├── 숨겨진 버그
├── 변경이 두려움
└── 새 팀원 적응 어려움
```

---

## 🎯 관련 원칙

### YAGNI (You Aren't Gonna Need It)
```
"필요할 때까지 만들지 마라"

❌ "나중에 필요할 것 같아서 미리..."
✅ "지금 필요한 것만 만들자"
```

### WET (반대 개념)
```
WET = Write Everything Twice
"모든 것을 두 번 써라" (풍자)

→ DRY의 반대
→ 나쁜 코드의 특징
```"""
            },
            {
                "type": "code",
                "title": "💻 원칙 적용 예시",
                "content": """### DRY 적용

```python
# ❌ DRY 위반: 중복된 검증 로직
def create_user(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    ...

def update_email(user_id, email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    ...

def invite_user(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    ...

# ✅ DRY 적용: 하나로 추출
def validate_email(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")

def create_user(email):
    validate_email(email)
    ...

def update_email(user_id, email):
    validate_email(email)
    ...
```

### KISS 적용

```python
# ❌ KISS 위반: 과도하게 복잡
def is_adult(user):
    age_validator = AgeValidatorFactory.create_validator(
        ValidatorType.ADULT,
        ValidationStrategy.STRICT
    )
    validation_result = age_validator.validate(
        UserAgeWrapper(user.age),
        ValidationContext.default()
    )
    return validation_result.is_valid()

# ✅ KISS 적용: 단순하게
def is_adult(user):
    return user.age >= 18
```

### YAGNI 적용

```python
# ❌ YAGNI 위반: 미래를 위한 과잉 설계
class UserRepository:
    def find_by_id(self, id): ...
    def find_by_email(self, email): ...
    def find_by_phone(self, phone): ...  # 아직 안 쓰는데?
    def find_by_address(self, address): ...  # 이것도?
    def find_by_name_and_age(self, name, age): ...  # 언제 쓸 건데?

# ✅ YAGNI 적용: 필요한 것만
class UserRepository:
    def find_by_id(self, id): ...
    def find_by_email(self, email): ...
    # 나머지는 필요할 때 추가
```

### 균형 잡기

```python
# ⚠️ DRY 과적용 주의
# 비슷해 보이지만 다른 개념

# 결제 금액 계산
def calculate_payment_total(items):
    return sum(item.price for item in items) * 1.1  # 부가세 포함

# 환불 금액 계산 (다른 비즈니스 로직)
def calculate_refund_total(items):
    return sum(item.price for item in items) * 0.9  # 수수료 차감

# 이 둘을 억지로 합치면 오히려 복잡해짐!
# "우연히 비슷한 코드"는 중복이 아님
```"""
            },
            {
                "type": "tip",
                "title": "💡 원칙 적용 가이드",
                "content": """### DRY 적용 기준

```
✅ 추출해야 할 때:
├── 같은 코드가 3번 이상 나타남
├── 비즈니스 규칙 표현
├── 알고리즘 중복
└── 상수 중복

❌ 추출하면 안 될 때:
├── 우연히 비슷한 코드
├── 다른 이유로 변경될 코드
├── 가독성 해치는 추상화
└── 과도한 커플링 발생
```

### KISS 적용 기준

```
✅ 단순하게 해야 할 때:
├── 지금 당장 동작하면 됨
├── 요구사항이 명확함
├── 확장 가능성 낮음
└── 성능 요구 없음

⚠️ 복잡해도 괜찮을 때:
├── 성능이 중요
├── 확실한 확장 요구
├── 복잡한 도메인 로직
└── 검증된 디자인 패턴
```

### Rule of Three

```
1번: 그냥 작성
2번: 일단 복사
3번: 리팩토링!

"두 번까진 봐준다.
 세 번째엔 무조건 추출!"
```

### 균형이 중요

```
DRY 과잉 → 복잡한 추상화
KISS 과잉 → 중복 코드 가득

적정선:
├── 명확한 중복은 제거
├── 불필요한 추상화는 피함
├── 코드의 의도가 명확
└── 변경이 쉬움
```"""
            }
        ]
    }
}

def update_cleancode_json():
    """cleancode.json 파일 업데이트"""
    sys.stdout.reconfigure(encoding='utf-8')

    # 파일 읽기
    with open(CLEANCODE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in CLEANCODE_CONTENTS.items():
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
    with open(CLEANCODE_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Cleancode section 01 updated: {updated_count} topics")

if __name__ == "__main__":
    update_cleancode_json()
