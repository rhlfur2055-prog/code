# -*- coding: utf-8 -*-
# 클린코드 콘텐츠 생성 스크립트 - Part 3
# 03_리팩토링 섹션 (8개 토픽)

import json
import sys

CLEANCODE_JSON_PATH = "src/data/contents/cleancode.json"

REFACTORING_CONTENTS = {
    "03_리팩토링/refactoring-intro": {
        "title": "리팩토링 소개",
        "description": "리팩토링의 기본 개념을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "리팩토링이란?",
                "content": "## 한 줄 요약\n> **동작은 그대로, 구조만 개선** - 코드를 더 깨끗하게 만드는 작업이에요!\n\n---\n\n## 리팩토링 정의\n\n### 공식 정의:\n```\n\"외부 동작을 바꾸지 않으면서\n 내부 구조를 개선하는 것\"\n\n핵심: 기능은 같음 + 코드만 좋아짐\n```\n\n### 비유:\n```\n집 리모델링\n\n리팩토링:\n├── 거실 크기 그대로\n├── 가구 배치만 변경\n├── 동선 개선\n└── 사는 사람은 같은 생활\n\n코드 리팩토링:\n├── 기능은 그대로\n├── 코드 구조만 변경\n├── 가독성 개선\n└── 사용자는 변화 모름\n```\n\n---\n\n## 왜 리팩토링하나?\n\n### 리팩토링 안 하면:\n```\n시간이 지날수록:\n├── 코드 이해하기 어려움\n├── 버그 고치기 두려움\n├── 새 기능 추가 시간 증가\n├── 개발 속도 점점 느려짐\n└── 결국 \"다시 짜자\" 선언\n```\n\n### 리팩토링 하면:\n```\n├── 코드 쉽게 이해\n├── 버그 빨리 발견\n├── 새 기능 쉽게 추가\n├── 개발 속도 유지\n└── 기술 부채 감소\n```"
            },
            {
                "type": "code",
                "title": "리팩토링 예시",
                "content": "### 리팩토링 전\n\n```python\n# 읽기 어려운 코드\ndef calc(l):\n    t = 0\n    for i in l:\n        if i['type'] == 'food':\n            t += i['price'] * 0.9\n        elif i['type'] == 'book':\n            t += i['price'] * 0.85\n        else:\n            t += i['price']\n    return t\n```\n\n### 리팩토링 후\n\n```python\n# 읽기 쉬운 코드\ndef calculate_total_price(items):\n    total = 0\n    for item in items:\n        discounted_price = apply_discount(item)\n        total += discounted_price\n    return total\n\ndef apply_discount(item):\n    discount_rates = {\n        'food': 0.9,\n        'book': 0.85\n    }\n    rate = discount_rates.get(item['type'], 1.0)\n    return item['price'] * rate\n```\n\n### 무엇이 바뀌었나?\n\n```\n변경 사항:\n├── 의미 있는 이름 사용\n├── 함수 분리 (extract method)\n├── 매직 넘버 제거\n└── 가독성 향상\n\n변하지 않은 것:\n└── 계산 결과 (동작 동일)\n```"
            },
            {
                "type": "tip",
                "title": "리팩토링 기본 원칙",
                "content": "### 리팩토링 3대 원칙\n\n```\n1. 작은 단계로 진행\n   ├── 한 번에 하나만 변경\n   ├── 변경 후 테스트\n   └── 문제 시 바로 롤백\n\n2. 테스트 필수\n   ├── 테스트 없이 리팩토링 금지\n   ├── 변경 전후 동작 확인\n   └── 자동화된 테스트 권장\n\n3. 동작 변경 금지\n   ├── 기능 추가 X\n   ├── 버그 수정 X (별도로)\n   └── 구조 개선만\n```\n\n### 리팩토링 vs 리라이팅\n\n```\n리팩토링:\n├── 점진적 개선\n├── 기존 코드 유지\n├── 위험도 낮음\n└── 작은 단위로 진행\n\n리라이팅 (다시 작성):\n├── 처음부터 새로\n├── 기존 코드 버림\n├── 위험도 높음\n└── 오래 걸림\n\n권장: 리팩토링 먼저 시도!\n```"
            }
        ]
    },

    "03_리팩토링/refactoring-when": {
        "title": "리팩토링 시점",
        "description": "언제 리팩토링해야 하는지 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "언제 리팩토링하나?",
                "content": "## 한 줄 요약\n> **냄새가 날 때 청소하자** - 코드 냄새(Code Smell)가 리팩토링 신호예요!\n\n---\n\n## 3의 법칙 (Rule of Three)\n\n```\n마틴 파울러의 법칙:\n\n1번째: 그냥 한다\n2번째: 중복이 생겨도 일단 한다\n3번째: 이제 리팩토링한다!\n\n\"처음엔 그냥 하고,\n 두 번째는 눈 감고,\n 세 번째면 리팩토링\"\n```\n\n---\n\n## 리팩토링 타이밍\n\n### 1. 기능 추가 전\n```\n새 기능 추가하려는데...\n├── 기존 코드가 복잡함\n├── 어디를 수정해야 할지 모름\n└── 먼저 정리하고 추가하자!\n```\n\n### 2. 버그 수정 전\n```\n버그를 고치려는데...\n├── 코드가 이해 안 됨\n├── 버그 원인 찾기 어려움\n└── 먼저 정리하고 수정하자!\n```\n\n### 3. 코드 리뷰 시\n```\nPR 리뷰하는데...\n├── \"이거 무슨 뜻이죠?\"\n├── \"여기 중복 아닌가요?\"\n└── 리뷰 후 리팩토링!\n```"
            },
            {
                "type": "code",
                "title": "코드 냄새 (Code Smells)",
                "content": "### 대표적인 코드 냄새\n\n```python\n# 1. 중복 코드 (Duplicated Code)\ndef get_user_summary(user):\n    name = user['name'].strip().title()\n    return f\"Name: {name}\"\n\ndef get_admin_summary(admin):\n    name = admin['name'].strip().title()  # 중복!\n    return f\"Admin: {name}\"\n\n# 2. 긴 함수 (Long Method)\ndef process_order(order):\n    # 100줄 이상의 코드...\n    # 여러 가지 일을 한 함수에서\n    pass\n\n# 3. 긴 매개변수 목록 (Long Parameter List)\ndef create_user(name, email, phone, address, city, \n                country, zip_code, birth_date):\n    pass\n\n# 4. 매직 넘버 (Magic Numbers)\ndef calculate_shipping(weight):\n    if weight < 5:\n        return weight * 2.5  # 2.5가 뭔지?\n    return 12.5  # 12.5는 또 뭔지?\n```\n\n### 냄새 제거 예시\n\n```python\n# 중복 제거\ndef format_name(name):\n    return name.strip().title()\n\ndef get_user_summary(user):\n    return f\"Name: {format_name(user['name'])}\"\n\ndef get_admin_summary(admin):\n    return f\"Admin: {format_name(admin['name'])}\"\n\n# 매직 넘버 제거\nSHIPPING_RATE_PER_KG = 2.5\nMAX_SHIPPING_FEE = 12.5\nFREE_SHIPPING_THRESHOLD = 5\n\ndef calculate_shipping(weight):\n    if weight < FREE_SHIPPING_THRESHOLD:\n        return weight * SHIPPING_RATE_PER_KG\n    return MAX_SHIPPING_FEE\n```"
            },
            {
                "type": "tip",
                "title": "리팩토링 하지 말아야 할 때",
                "content": "### 리팩토링 금지 상황\n\n```\n1. 데드라인 직전\n   ├── 리팩토링은 시간 필요\n   ├── 급할 땐 일단 동작하게\n   └── 나중에 시간 확보 후 진행\n\n2. 코드가 동작하지 않을 때\n   ├── 먼저 동작하게 만들기\n   ├── 테스트 통과 후 리팩토링\n   └── 깨진 코드 리팩토링 X\n\n3. 완전히 새로 짜야 할 때\n   ├── 구조가 완전히 잘못됨\n   ├── 리팩토링 비용 > 재작성 비용\n   └── 차라리 새로 작성\n```\n\n### 리팩토링 우선순위\n\n```\n높음:\n├── 자주 수정되는 코드\n├── 버그가 자주 발생하는 곳\n└── 새 기능 추가 예정인 곳\n\n낮음:\n├── 거의 수정 안 되는 코드\n├── 곧 삭제될 코드\n└── 레거시 시스템 (건드리면 위험)\n```\n\n### 보이스카우트 규칙\n\n```\n\"캠프장은 왔을 때보다\n 깨끗하게 떠나라\"\n\n코드도 마찬가지:\n├── 작업한 부분만 조금씩 개선\n├── 한 번에 완벽하게 X\n├── 매일 조금씩 O\n└── 점진적 개선이 핵심\n```"
            }
        ]
    },

    "03_리팩토링/extract-method": {
        "title": "메서드 추출",
        "description": "코드를 함수로 분리하는 기법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "메서드 추출이란?",
                "content": "## 한 줄 요약\n> **코드 덩어리를 함수로 분리** - 가장 많이 쓰이는 리팩토링 기법이에요!\n\n---\n\n## 왜 메서드를 추출하나?\n\n### 문제 상황:\n```\n긴 함수의 문제점:\n├── 이해하기 어려움\n├── 테스트하기 어려움\n├── 재사용 불가능\n├── 수정 시 영향 범위 큼\n└── 코드 중복 발생\n```\n\n### 해결책:\n```\n작은 함수로 분리하면:\n├── 이름으로 의도 표현\n├── 각각 테스트 가능\n├── 재사용 가능\n├── 수정 영향 최소화\n└── 중복 제거 쉬움\n```\n\n---\n\n## 추출 기준\n\n### 언제 추출하나?\n\n```\n추출 신호:\n├── 주석이 필요한 코드 블록\n├── 반복되는 코드 패턴\n├── 조건문 내부 코드\n├── 루프 내부 복잡한 로직\n└── \"그리고\"가 들어가는 함수\n```\n\n### 이름 짓기:\n```\n좋은 함수 이름 = 무엇을 하는가\n\n예시:\n├── calculate_discount (할인 계산)\n├── validate_email (이메일 검증)\n├── format_currency (통화 포맷)\n└── is_valid_user (유저 유효성)\n```"
            },
            {
                "type": "code",
                "title": "메서드 추출 예시",
                "content": "### 추출 전: 긴 함수\n\n```python\ndef print_invoice(invoice):\n    # 헤더 출력\n    print(\"=\" * 50)\n    print(f\"Invoice #{invoice['id']}\")\n    print(f\"Date: {invoice['date']}\")\n    print(\"=\" * 50)\n    \n    # 상품 목록 출력\n    total = 0\n    for item in invoice['items']:\n        price = item['price'] * item['quantity']\n        total += price\n        print(f\"{item['name']}: {price}원\")\n    \n    # 할인 계산\n    if total > 100000:\n        discount = total * 0.1\n    elif total > 50000:\n        discount = total * 0.05\n    else:\n        discount = 0\n    \n    # 최종 금액 출력\n    final = total - discount\n    print(\"-\" * 50)\n    print(f\"소계: {total}원\")\n    print(f\"할인: {discount}원\")\n    print(f\"합계: {final}원\")\n```\n\n### 추출 후: 작은 함수들\n\n```python\ndef print_invoice(invoice):\n    print_header(invoice)\n    total = print_items(invoice['items'])\n    discount = calculate_discount(total)\n    print_summary(total, discount)\n\ndef print_header(invoice):\n    print(\"=\" * 50)\n    print(f\"Invoice #{invoice['id']}\")\n    print(f\"Date: {invoice['date']}\")\n    print(\"=\" * 50)\n\ndef print_items(items):\n    total = 0\n    for item in items:\n        price = calculate_item_price(item)\n        total += price\n        print(f\"{item['name']}: {price}원\")\n    return total\n\ndef calculate_item_price(item):\n    return item['price'] * item['quantity']\n\ndef calculate_discount(total):\n    if total > 100000:\n        return total * 0.1\n    elif total > 50000:\n        return total * 0.05\n    return 0\n\ndef print_summary(total, discount):\n    final = total - discount\n    print(\"-\" * 50)\n    print(f\"소계: {total}원\")\n    print(f\"할인: {discount}원\")\n    print(f\"합계: {final}원\")\n```"
            },
            {
                "type": "tip",
                "title": "메서드 추출 팁",
                "content": "### 추출 단계\n\n```\n1. 추출할 코드 선택\n2. 새 함수 생성\n3. 코드 복사\n4. 필요한 매개변수 추가\n5. 반환값 결정\n6. 원래 위치에서 함수 호출\n7. 테스트\n```\n\n### IDE 활용\n\n```\nVS Code:\n├── 코드 선택\n├── 우클릭 > Refactor\n└── Extract Method\n\nPyCharm:\n├── 코드 선택\n├── Ctrl+Alt+M (Mac: Cmd+Opt+M)\n└── 함수 이름 입력\n\n자동으로:\n├── 매개변수 분석\n├── 반환값 결정\n└── 호출 코드 생성\n```\n\n### 주의사항\n\n```\n적절한 크기:\n├── 너무 작은 함수: 오버킬\n├── 너무 큰 함수: 리팩토링 안 됨\n└── 3-15줄 정도가 적당\n\n매개변수 개수:\n├── 3개 이하 권장\n├── 4개 이상이면 객체로 묶기\n└── 너무 많으면 설계 재검토\n```"
            }
        ]
    },

    "03_리팩토링/extract-variable": {
        "title": "변수 추출",
        "description": "표현식을 변수로 분리하는 기법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "변수 추출이란?",
                "content": "## 한 줄 요약\n> **복잡한 표현식에 이름 붙이기** - 읽기 어려운 식을 변수로 분리해요!\n\n---\n\n## 왜 변수를 추출하나?\n\n### 문제 상황:\n```python\n# 이게 무슨 뜻인지 모르겠음\nif (user.age >= 18 and user.country == 'KR' and \n    user.balance > 0 and not user.is_banned):\n    process_payment()\n```\n\n### 해결:\n```python\n# 의도가 명확함\nis_adult = user.age >= 18\nis_korean = user.country == 'KR'\nhas_balance = user.balance > 0\nis_active = not user.is_banned\n\ncan_make_payment = is_adult and is_korean and has_balance and is_active\n\nif can_make_payment:\n    process_payment()\n```\n\n---\n\n## 추출 기준\n\n### 언제 추출하나?\n\n```\n추출 신호:\n├── 표현식이 길고 복잡함\n├── 같은 표현식이 반복됨\n├── 주석이 필요한 계산\n├── 중첩된 함수 호출\n└── 조건문이 복잡함\n```"
            },
            {
                "type": "code",
                "title": "변수 추출 예시",
                "content": "### 예시 1: 복잡한 계산\n\n```python\n# 추출 전\nprice = base_price * (1 - discount_rate) * (1 + tax_rate) + shipping_fee\n\n# 추출 후\ndiscounted_price = base_price * (1 - discount_rate)\nprice_with_tax = discounted_price * (1 + tax_rate)\nfinal_price = price_with_tax + shipping_fee\n```\n\n### 예시 2: 복잡한 조건문\n\n```javascript\n// 추출 전\nif (order.status === 'confirmed' && \n    order.items.length > 0 && \n    Date.now() - order.createdAt < 24 * 60 * 60 * 1000) {\n    cancelOrder(order);\n}\n\n// 추출 후\nconst isConfirmed = order.status === 'confirmed';\nconst hasItems = order.items.length > 0;\nconst ONE_DAY_MS = 24 * 60 * 60 * 1000;\nconst isWithin24Hours = Date.now() - order.createdAt < ONE_DAY_MS;\n\nconst canCancel = isConfirmed && hasItems && isWithin24Hours;\n\nif (canCancel) {\n    cancelOrder(order);\n}\n```\n\n### 예시 3: 중첩 함수 호출\n\n```python\n# 추출 전\nresult = format_currency(calculate_discount(get_base_price(product), rate))\n\n# 추출 후\nbase_price = get_base_price(product)\ndiscounted_price = calculate_discount(base_price, rate)\nresult = format_currency(discounted_price)\n```"
            },
            {
                "type": "tip",
                "title": "변수 추출 팁",
                "content": "### 좋은 변수 이름\n\n```\n의도를 표현하는 이름:\n├── is_valid (불리언)\n├── total_count (숫자)\n├── user_name (문자열)\n├── selected_items (컬렉션)\n└── can_proceed (권한/조건)\n\n피해야 할 이름:\n├── temp, tmp\n├── data, info\n├── flag\n└── x, y, i (루프 제외)\n```\n\n### 추출하지 말아야 할 때\n\n```\n추출 불필요:\n├── 이미 명확한 표현식\n├── 한 번만 사용되는 단순 값\n├── 자명한 계산\n\n예시:\nfull_name = first_name + ' ' + last_name  # OK\nconcatenated = first + second  # 불필요\n```\n\n### 변수 추출 vs 메서드 추출\n\n```\n변수 추출 선택:\n├── 현재 함수 내에서만 사용\n├── 단순한 표현식\n├── 한 번만 사용\n\n메서드 추출 선택:\n├── 여러 곳에서 재사용\n├── 복잡한 로직 포함\n├── 테스트 필요\n```"
            }
        ]
    },

    "03_리팩토링/rename": {
        "title": "이름 변경",
        "description": "의미있는 이름으로 변경하는 기법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "이름 변경이란?",
                "content": "## 한 줄 요약\n> **좋은 이름이 좋은 코드를 만든다** - 이름만 바꿔도 코드가 달라져요!\n\n---\n\n## 왜 이름이 중요한가?\n\n### 코드는 읽는 시간이 더 많다\n```\n개발자의 시간 분배:\n├── 코드 읽기: 70%\n├── 코드 쓰기: 30%\n\n좋은 이름 = 읽기 쉬운 코드\n         = 개발 속도 향상\n```\n\n### 나쁜 이름의 비용\n```\n나쁜 이름이 있으면:\n├── 매번 코드 해석 필요\n├── 주석 의존도 증가\n├── 버그 발생 가능성 증가\n├── 온보딩 시간 증가\n└── 유지보수 비용 증가\n```\n\n---\n\n## 좋은 이름의 기준\n\n```\n좋은 이름 체크리스트:\n├── 의도가 드러나는가?\n├── 잘못 해석될 여지가 없는가?\n├── 발음할 수 있는가?\n├── 검색 가능한가?\n└── 일관성이 있는가?\n```"
            },
            {
                "type": "code",
                "title": "이름 변경 예시",
                "content": "### 변수 이름 개선\n\n```python\n# 나쁜 이름 -> 좋은 이름\n\nd = 5                    # days_until_deadline = 5\ntemp = get_user()        # current_user = get_user()\nflag = True              # is_active = True\nlist1 = []               # pending_orders = []\ndata = fetch()           # user_profiles = fetch()\n```\n\n### 함수 이름 개선\n\n```javascript\n// 나쁜 이름 -> 좋은 이름\n\nfunction proc(u) { }     // function processUser(user) { }\nfunction getData() { }   // function fetchUserOrders() { }\nfunction check(x) { }    // function isValidEmail(email) { }\nfunction doIt() { }      // function sendNotification() { }\nfunction handle() { }    // function handlePaymentError() { }\n```\n\n### 클래스 이름 개선\n\n```python\n# 나쁜 이름 -> 좋은 이름\n\nclass Data:              # class UserProfile:\nclass Manager:           # class OrderProcessor:\nclass Helper:            # class PriceCalculator:\nclass Info:              # class ShippingAddress:\n```\n\n### 불리언 이름 개선\n\n```python\n# 불리언은 is, has, can, should로 시작\n\nstatus = True            # is_active = True\nflag = False             # has_permission = False\ncheck = True             # can_edit = True\nok = False               # should_notify = False\n```"
            },
            {
                "type": "tip",
                "title": "이름 변경 팁",
                "content": "### 이름 짓기 규칙\n\n```\n함수: 동사로 시작\n├── get_user()\n├── calculate_total()\n├── validate_input()\n└── send_email()\n\n변수: 명사 또는 형용사+명사\n├── user_name\n├── total_price\n├── active_users\n└── max_retry_count\n\n불리언: is/has/can/should\n├── is_valid\n├── has_children\n├── can_delete\n└── should_update\n\n상수: 대문자+언더스코어\n├── MAX_CONNECTIONS\n├── DEFAULT_TIMEOUT\n└── API_BASE_URL\n```\n\n### IDE 리네임 기능\n\n```\nVS Code:\n├── F2 키 또는\n├── 우클릭 > Rename Symbol\n└── 모든 참조 자동 변경!\n\nPyCharm:\n├── Shift+F6\n└── 모든 참조 자동 변경!\n\n장점:\n├── 오타 방지\n├── 누락 방지\n└── 안전한 변경\n```\n\n### 주의사항\n\n```\n리네임 시 체크:\n├── public API 변경 시 호환성\n├── 테스트 코드도 함께 변경\n├── 문서/주석 업데이트\n└── 팀 컨벤션 확인\n```"
            }
        ]
    },

    "03_리팩토링/replace-conditional": {
        "title": "조건문 대체",
        "description": "다형성으로 조건문을 제거하는 기법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "조건문 대체란?",
                "content": "## 한 줄 요약\n> **if-else 지옥 탈출** - 조건문 대신 다형성이나 전략 패턴을 사용해요!\n\n---\n\n## 왜 조건문을 대체하나?\n\n### 조건문의 문제\n```python\n# 새 타입 추가할 때마다 모든 조건문 수정 필요\ndef calculate_pay(employee_type, hours):\n    if employee_type == 'regular':\n        return hours * 20\n    elif employee_type == 'manager':\n        return hours * 30 + 500\n    elif employee_type == 'intern':\n        return hours * 10\n    # 새 타입 추가? elif 추가...\n    # 다른 함수에도 같은 패턴 반복...\n```\n\n### 문제점\n```\n조건문 남발의 문제:\n├── 새 타입 추가 시 여러 곳 수정\n├── 수정 누락 가능성\n├── 코드 중복\n├── 테스트 복잡도 증가\n└── OCP 위반 (수정에 열려있음)\n```"
            },
            {
                "type": "code",
                "title": "다형성으로 대체",
                "content": "### 전략 패턴 사용\n\n```python\nfrom abc import ABC, abstractmethod\n\n# 추상 클래스\nclass Employee(ABC):\n    @abstractmethod\n    def calculate_pay(self, hours: int) -> int:\n        pass\n\n# 구체 클래스들\nclass RegularEmployee(Employee):\n    def calculate_pay(self, hours):\n        return hours * 20\n\nclass Manager(Employee):\n    def calculate_pay(self, hours):\n        return hours * 30 + 500\n\nclass Intern(Employee):\n    def calculate_pay(self, hours):\n        return hours * 10\n\n# 새 타입 추가: 클래스만 추가하면 됨!\nclass Contractor(Employee):\n    def calculate_pay(self, hours):\n        return hours * 40\n\n# 사용\ndef process_payroll(employee: Employee, hours: int):\n    return employee.calculate_pay(hours)\n\n# 조건문 없이 동작!\nmanager = Manager()\nprint(process_payroll(manager, 40))  # 1700\n```\n\n### 딕셔너리 매핑 (간단한 경우)\n\n```python\n# 조건문 대신 딕셔너리\nPAY_RATES = {\n    'regular': lambda h: h * 20,\n    'manager': lambda h: h * 30 + 500,\n    'intern': lambda h: h * 10,\n}\n\ndef calculate_pay(employee_type, hours):\n    calculator = PAY_RATES.get(employee_type)\n    if calculator:\n        return calculator(hours)\n    raise ValueError(f\"Unknown type: {employee_type}\")\n```"
            },
            {
                "type": "tip",
                "title": "조건문 대체 팁",
                "content": "### 언제 대체하나?\n\n```\n대체 권장:\n├── 같은 조건이 여러 곳에 반복\n├── 타입별 동작이 다른 경우\n├── 새 타입 추가가 예상될 때\n├── 조건문이 3개 이상\n└── 각 분기가 복잡한 로직일 때\n\n그대로 유지:\n├── 단순한 null 체크\n├── 예외 처리\n├── 2개 이하의 분기\n├── 타입 추가 가능성 없음\n└── 각 분기가 단순할 때\n```\n\n### 대체 패턴 선택\n\n```\n1. 전략 패턴 (Strategy)\n   └── 알고리즘이 다를 때\n\n2. 상태 패턴 (State)\n   └── 상태에 따라 동작이 다를 때\n\n3. 딕셔너리 매핑\n   └── 단순한 값 매핑일 때\n\n4. 다형성\n   └── 타입별 동작이 다를 때\n```\n\n### 리팩토링 단계\n\n```\n1. 인터페이스/추상 클래스 정의\n2. 각 조건에 대한 클래스 생성\n3. 조건문 로직을 클래스로 이동\n4. 팩토리로 객체 생성\n5. 원래 조건문 제거\n6. 테스트\n```"
            }
        ]
    },

    "03_리팩토링/encapsulate-collection": {
        "title": "컬렉션 캡슐화",
        "description": "컬렉션을 보호하는 기법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "컬렉션 캡슐화란?",
                "content": "## 한 줄 요약\n> **컬렉션을 직접 노출하지 마세요** - 수정 권한을 통제해서 예기치 않은 변경을 막아요!\n\n---\n\n## 왜 컬렉션을 캡슐화하나?\n\n### 문제 상황\n```python\nclass Team:\n    def __init__(self):\n        self.members = []  # 직접 노출!\n\nteam = Team()\nteam.members.append('Alice')  # 외부에서 마음대로 수정\nteam.members.clear()  # 모든 멤버 삭제!\n```\n\n### 위험성\n```\n컬렉션 직접 노출 시:\n├── 외부에서 무제한 수정 가능\n├── 불변 조건 깨질 수 있음\n├── 변경 추적 불가능\n├── 유효성 검사 우회\n└── 버그 원인 찾기 어려움\n```\n\n---\n\n## 캡슐화 원칙\n\n```\n캡슐화 방법:\n├── getter는 복사본 반환\n├── setter 대신 add/remove 메서드\n├── 유효성 검사 추가\n├── 변경 시 이벤트 발생 가능\n└── 불변 컬렉션 사용 고려\n```"
            },
            {
                "type": "code",
                "title": "컬렉션 캡슐화 예시",
                "content": "### 캡슐화 전\n\n```python\nclass ShoppingCart:\n    def __init__(self):\n        self.items = []\n\ncart = ShoppingCart()\ncart.items.append({'name': 'Book', 'price': -100})  # 음수 가격!\ncart.items = None  # 리스트 자체를 변경!\n```\n\n### 캡슐화 후\n\n```python\nclass ShoppingCart:\n    def __init__(self):\n        self._items = []  # private\n    \n    @property\n    def items(self):\n        return self._items.copy()  # 복사본 반환\n    \n    def add_item(self, name, price):\n        if price <= 0:\n            raise ValueError(\"Price must be positive\")\n        self._items.append({'name': name, 'price': price})\n    \n    def remove_item(self, name):\n        self._items = [item for item in self._items if item['name'] != name]\n    \n    def get_total(self):\n        return sum(item['price'] for item in self._items)\n    \n    def clear(self):\n        self._items.clear()\n\n# 사용\ncart = ShoppingCart()\ncart.add_item('Book', 15000)      # OK\ncart.add_item('Pen', -100)        # ValueError!\n\nexternal_list = cart.items        # 복사본 받음\nexternal_list.append({'x': 'y'}) # 원본 영향 없음\n```\n\n### JavaScript 예시\n\n```javascript\nclass Team {\n    #members = [];  // private field\n    \n    get members() {\n        return [...this.#members];  // spread로 복사\n    }\n    \n    addMember(member) {\n        if (!member.name) {\n            throw new Error('Member must have a name');\n        }\n        this.#members.push(member);\n    }\n    \n    removeMember(name) {\n        this.#members = this.#members.filter(m => m.name !== name);\n    }\n}\n```"
            },
            {
                "type": "tip",
                "title": "컬렉션 캡슐화 팁",
                "content": "### 캡슐화 체크리스트\n\n```\n1. 필드는 private으로\n   ├── Python: _items (convention)\n   └── JS: #items (private field)\n\n2. getter는 복사본 반환\n   ├── Python: return list.copy()\n   └── JS: return [...array]\n\n3. 수정 메서드 제공\n   ├── add_item() / addItem()\n   ├── remove_item() / removeItem()\n   └── clear()\n\n4. 유효성 검사 추가\n   └── 메서드 내에서 검증\n```\n\n### 불변 컬렉션 활용\n\n```python\nfrom typing import Tuple\n\nclass Config:\n    def __init__(self):\n        self._settings: Tuple = ()  # 불변 튜플\n    \n    @property\n    def settings(self):\n        return self._settings  # 튜플은 수정 불가\n    \n    def add_setting(self, key, value):\n        self._settings = (*self._settings, (key, value))\n```\n\n### 주의사항\n\n```\n성능 고려:\n├── 매번 복사는 비용 발생\n├── 큰 컬렉션은 주의\n├── 필요시 iterator 제공\n└── 읽기 전용 뷰 고려\n\n깊은 복사 vs 얕은 복사:\n├── 객체 컬렉션은 깊은 복사 고려\n├── 단순 값은 얕은 복사로 충분\n└── 상황에 맞게 선택\n```"
            }
        ]
    },

    "03_리팩토링/practice-refactoring": {
        "title": "리팩토링 실습",
        "description": "실제 코드를 리팩토링하는 예제를 실습합니다",
        "sections": [
            {
                "type": "concept",
                "title": "리팩토링 실습 가이드",
                "content": "## 한 줄 요약\n> **실제 코드로 연습하기** - 배운 기법들을 종합적으로 적용해봐요!\n\n---\n\n## 실습 접근법\n\n### 리팩토링 순서\n```\n1. 코드 읽고 이해하기\n2. 테스트 작성 (없다면)\n3. 코드 냄새 찾기\n4. 작은 단계로 개선\n5. 테스트 실행\n6. 반복\n```\n\n### 코드 냄새 체크리스트\n```\n확인할 항목:\n├── 중복 코드가 있나?\n├── 함수가 너무 긴가? (15줄 초과)\n├── 매개변수가 많은가? (3개 초과)\n├── 조건문이 복잡한가?\n├── 이름이 불명확한가?\n├── 매직 넘버가 있나?\n├── 주석이 많이 필요한가?\n└── 컬렉션이 노출되어 있나?\n```"
            },
            {
                "type": "code",
                "title": "종합 리팩토링 예제",
                "content": "### 리팩토링 전\n\n```python\ndef calc(o):\n    t = 0\n    for i in o['items']:\n        if i['t'] == 'book':\n            t += i['p'] * i['q'] * 0.9\n        elif i['t'] == 'food':\n            t += i['p'] * i['q'] * 0.95\n        elif i['t'] == 'electronics':\n            t += i['p'] * i['q']\n        else:\n            t += i['p'] * i['q']\n    if t > 100000:\n        t = t * 0.9\n    elif t > 50000:\n        t = t * 0.95\n    if o['m'] == 'vip':\n        t = t * 0.9\n    return t\n```\n\n### 리팩토링 후\n\n```python\nfrom abc import ABC, abstractmethod\nfrom dataclasses import dataclass\nfrom typing import List\n\n# 상수 정의\nBULK_DISCOUNT_THRESHOLD_HIGH = 100000\nBULK_DISCOUNT_THRESHOLD_LOW = 50000\nBULK_DISCOUNT_RATE_HIGH = 0.9\nBULK_DISCOUNT_RATE_LOW = 0.95\nVIP_DISCOUNT_RATE = 0.9\n\n# 데이터 클래스\n@dataclass\nclass OrderItem:\n    item_type: str\n    price: int\n    quantity: int\n\n@dataclass\nclass Order:\n    items: List[OrderItem]\n    membership: str\n\n# 카테고리별 할인 정책\nCATEGORY_DISCOUNT_RATES = {\n    'book': 0.9,\n    'food': 0.95,\n    'electronics': 1.0,\n}\n\ndef calculate_item_price(item: OrderItem) -> float:\n    base_price = item.price * item.quantity\n    discount_rate = CATEGORY_DISCOUNT_RATES.get(item.item_type, 1.0)\n    return base_price * discount_rate\n\ndef calculate_subtotal(items: List[OrderItem]) -> float:\n    return sum(calculate_item_price(item) for item in items)\n\ndef apply_bulk_discount(subtotal: float) -> float:\n    if subtotal > BULK_DISCOUNT_THRESHOLD_HIGH:\n        return subtotal * BULK_DISCOUNT_RATE_HIGH\n    elif subtotal > BULK_DISCOUNT_THRESHOLD_LOW:\n        return subtotal * BULK_DISCOUNT_RATE_LOW\n    return subtotal\n\ndef apply_membership_discount(total: float, membership: str) -> float:\n    if membership == 'vip':\n        return total * VIP_DISCOUNT_RATE\n    return total\n\ndef calculate_order_total(order: Order) -> float:\n    subtotal = calculate_subtotal(order.items)\n    after_bulk = apply_bulk_discount(subtotal)\n    final_total = apply_membership_discount(after_bulk, order.membership)\n    return final_total\n```"
            },
            {
                "type": "tip",
                "title": "리팩토링 정리",
                "content": "### 적용된 기법 정리\n\n```\n1. 이름 변경 (Rename)\n   ├── calc -> calculate_order_total\n   ├── t -> subtotal, total\n   ├── i -> item\n   └── o -> order\n\n2. 변수 추출 (Extract Variable)\n   ├── 매직 넘버 -> 상수\n   └── 중간 계산 결과 -> 변수\n\n3. 메서드 추출 (Extract Method)\n   ├── calculate_item_price()\n   ├── calculate_subtotal()\n   ├── apply_bulk_discount()\n   └── apply_membership_discount()\n\n4. 조건문 대체\n   └── 딕셔너리 매핑 사용\n\n5. 데이터 구조화\n   └── dataclass 사용\n```\n\n### 리팩토링 효과\n\n```\n개선된 점:\n├── 코드 가독성 향상\n├── 각 함수 단일 책임\n├── 테스트 용이성\n├── 새 할인 타입 추가 쉬움\n├── 버그 발견 용이\n└── 유지보수 비용 감소\n```\n\n### 실습 팁\n\n```\n효과적인 연습 방법:\n├── 실제 프로젝트 코드로 연습\n├── 작은 것부터 시작\n├── 한 번에 한 기법만\n├── 테스트 먼저 작성\n├── 커밋 자주 하기\n└── 코드 리뷰 받기\n```"
            }
        ]
    }
}

def update_cleancode_json():
    sys.stdout.reconfigure(encoding='utf-8')

    with open(CLEANCODE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in REFACTORING_CONTENTS.items():
        if key in data:
            data[key]['title'] = content['title']
            data[key]['description'] = content['description']
            data[key]['sections'] = content['sections']
            data[key]['isPlaceholder'] = False
            updated_count += 1
            print(f"[OK] {key} updated")
        else:
            print(f"[WARN] {key} key not found")

    with open(CLEANCODE_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Refactoring section updated: {updated_count} topics")

if __name__ == "__main__":
    update_cleancode_json()
