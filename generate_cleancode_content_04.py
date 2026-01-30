# -*- coding: utf-8 -*-
# 클린코드 콘텐츠 생성 스크립트 - Part 4
# 04_테스트 섹션 (3개 토픽) + 04_면접 섹션 (1개 토픽)

import json
import sys

CLEANCODE_JSON_PATH = "src/data/contents/cleancode.json"

TEST_CONTENTS = {
    "04_테스트/test-code": {
        "title": "테스트 코드",
        "description": "테스트 코드 작성법을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "테스트 코드란?",
                "content": "## 한 줄 요약\n> **내 코드가 제대로 동작하는지 자동으로 확인하는 코드** - 수동 테스트는 이제 그만!\n\n---\n\n## 왜 테스트 코드가 필요할까?\n\n### 테스트 없이 개발하면:\n```\n코드 수정할 때마다:\n1. 수동으로 이것저것 클릭\n2. \"이거 괜찮겠지?\" 배포\n3. 새벽에 장애 전화\n4. \"어디가 문제지?\" 디버깅 지옥\n```\n\n### 테스트 코드가 있으면:\n```\n코드 수정할 때:\n1. 테스트 실행 (1초)\n2. 초록불 = 안전, 빨간불 = 문제 있음\n3. 자신감 있게 배포\n4. 편안한 밤잠\n```\n\n---\n\n## 테스트의 종류\n\n```\n단위 테스트 (Unit Test)\n├── 함수 하나하나 테스트\n├── 가장 작은 단위\n└── 실행 속도 빠름 (밀리초)\n\n통합 테스트 (Integration Test)\n├── 여러 모듈 함께 테스트\n├── DB, API 연동 테스트\n└── 실행 속도 중간 (초)\n\nE2E 테스트 (End-to-End)\n├── 사용자 시나리오 전체 테스트\n├── 브라우저 자동화\n└── 실행 속도 느림 (분)\n```\n\n### 테스트 피라미드\n\n```\n        /\\\n       /E2E\\      <- 적게 (느림, 비쌈)\n      /------\\\n     /통합테스트\\   <- 중간\n    /------------\\\n   /   단위 테스트  \\  <- 많이 (빠름, 저렴)\n  /________________\\\n```"
            },
            {
                "type": "code",
                "title": "첫 번째 테스트 작성",
                "content": "### Python - pytest 사용\n\n```python\n# calculator.py - 테스트할 코드\ndef add(a, b):\n    return a + b\n\ndef divide(a, b):\n    if b == 0:\n        raise ValueError(\"0으로 나눌 수 없습니다\")\n    return a / b\n```\n\n```python\n# test_calculator.py - 테스트 코드\nimport pytest\nfrom calculator import add, divide\n\n# 테스트 함수는 test_로 시작\ndef test_add_positive_numbers():\n    # Given: 두 양수\n    a, b = 2, 3\n    \n    # When: 더하기 실행\n    result = add(a, b)\n    \n    # Then: 결과 확인\n    assert result == 5\n\ndef test_add_negative_numbers():\n    assert add(-1, -2) == -3\n\ndef test_divide_normal():\n    assert divide(10, 2) == 5\n\ndef test_divide_by_zero():\n    # 예외가 발생하는지 확인\n    with pytest.raises(ValueError):\n        divide(10, 0)\n```\n\n### 테스트 실행\n\n```bash\n# 모든 테스트 실행\npytest\n\n# 특정 파일만 실행\npytest test_calculator.py\n\n# 상세 출력\npytest -v\n\n# 결과 예시:\n# test_calculator.py::test_add_positive_numbers PASSED\n# test_calculator.py::test_add_negative_numbers PASSED\n# test_calculator.py::test_divide_normal PASSED\n# test_calculator.py::test_divide_by_zero PASSED\n```"
            },
            {
                "type": "code",
                "title": "JavaScript 테스트 (Jest)",
                "content": "### Jest 기본 사용법\n\n```javascript\n// calculator.js\nfunction add(a, b) {\n    return a + b;\n}\n\nfunction divide(a, b) {\n    if (b === 0) {\n        throw new Error('0으로 나눌 수 없습니다');\n    }\n    return a / b;\n}\n\nmodule.exports = { add, divide };\n```\n\n```javascript\n// calculator.test.js\nconst { add, divide } = require('./calculator');\n\ndescribe('Calculator', () => {\n    describe('add', () => {\n        test('두 양수를 더한다', () => {\n            expect(add(2, 3)).toBe(5);\n        });\n\n        test('음수도 더할 수 있다', () => {\n            expect(add(-1, -2)).toBe(-3);\n        });\n    });\n\n    describe('divide', () => {\n        test('정상적인 나눗셈', () => {\n            expect(divide(10, 2)).toBe(5);\n        });\n\n        test('0으로 나누면 에러 발생', () => {\n            expect(() => divide(10, 0)).toThrow('0으로 나눌 수 없습니다');\n        });\n    });\n});\n```\n\n```bash\n# 테스트 실행\nnpm test\n\n# watch 모드 (파일 변경 시 자동 실행)\nnpm test -- --watch\n```"
            },
            {
                "type": "tip",
                "title": "좋은 테스트 작성 팁",
                "content": "### 테스트 이름 짓기\n\n```\n좋은 테스트 이름 = 문서화\n\n나쁜 이름:\ntest_add()          # 뭘 테스트하는지 모름\ntest_1()            # 의미 없음\n\n좋은 이름:\ntest_add_returns_sum_of_two_positive_numbers()\ntest_divide_by_zero_raises_value_error()\ntest_user_can_login_with_valid_credentials()\n\n패턴: test_[테스트대상]_[상황]_[기대결과]\n```\n\n### Given-When-Then 패턴\n\n```python\ndef test_user_registration():\n    # Given: 준비 (테스트 데이터 설정)\n    user_data = {\"email\": \"test@test.com\", \"password\": \"1234\"}\n    \n    # When: 실행 (테스트할 동작)\n    result = register_user(user_data)\n    \n    # Then: 검증 (결과 확인)\n    assert result.success == True\n    assert result.user.email == \"test@test.com\"\n```\n\n### 테스트 코드도 코드다!\n\n```\n테스트 코드 관리:\n- 중복 코드 제거 (fixture 활용)\n- 가독성 좋게 작성\n- 하나의 테스트 = 하나의 검증\n- 테스트 간 독립성 유지\n```"
            }
        ]
    },

    "04_테스트/tdd": {
        "title": "TDD",
        "description": "Test Driven Development를 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "TDD란?",
                "content": "## 한 줄 요약\n> **테스트를 먼저 작성하고, 그 다음 코드를 작성** - 거꾸로 개발하기!\n\n---\n\n## TDD의 핵심\n\n### 일반적인 개발:\n```\n1. 코드 작성 (열심히 구현)\n2. 테스트 작성 (귀찮아서 스킵)\n3. 버그 발견 (나중에 고통)\n```\n\n### TDD 개발:\n```\n1. 테스트 먼저 작성 (실패하는 테스트)\n2. 코드 작성 (테스트 통과할 만큼만)\n3. 리팩토링 (깔끔하게 정리)\n```\n\n---\n\n## TDD 사이클: Red-Green-Refactor\n\n```\n    RED (빨간불)\n   실패하는 테스트 작성\n        |\n        v\n   GREEN (초록불)\n   테스트 통과하는 코드 작성\n        |\n        v\n   REFACTOR (정리)\n   코드 개선 (테스트는 계속 통과)\n        |\n        +----> 다시 RED로...\n```\n\n### 왜 이렇게 할까?\n\n```\nRED: \"뭘 만들어야 하는지\" 명확해짐\nGREEN: \"일단 동작하게\" 빠르게 구현\nREFACTOR: \"깔끔하게\" 안전하게 개선\n\n장점:\n- 설계를 먼저 생각하게 됨\n- 테스트가 항상 있음 (스킵 불가)\n- 과도한 코드 작성 방지\n- 자신감 있는 리팩토링\n```"
            },
            {
                "type": "code",
                "title": "TDD 실습: 문자열 계산기",
                "content": "### 요구사항\n```\n\"1,2,3\" -> 6\n\"\" -> 0\n\"5\" -> 5\n```\n\n### 1단계: RED - 실패하는 테스트\n\n```python\n# test_string_calculator.py\nfrom string_calculator import calculate\n\ndef test_empty_string_returns_zero():\n    assert calculate(\"\") == 0\n```\n\n```bash\n# 실행하면 실패! (calculate 함수가 없음)\npytest  # FAILED\n```\n\n### 2단계: GREEN - 테스트 통과\n\n```python\n# string_calculator.py\ndef calculate(text):\n    return 0  # 최소한의 코드로 테스트 통과\n```\n\n```bash\npytest  # PASSED\n```\n\n### 3단계: 다음 테스트 추가 (RED)\n\n```python\ndef test_single_number_returns_itself():\n    assert calculate(\"5\") == 5\n```\n\n```bash\npytest  # FAILED (0이 리턴됨)\n```\n\n### 4단계: 코드 수정 (GREEN)\n\n```python\ndef calculate(text):\n    if text == \"\":\n        return 0\n    return int(text)\n```\n\n### 5단계: 쉼표 구분 테스트 (RED)\n\n```python\ndef test_comma_separated_numbers():\n    assert calculate(\"1,2,3\") == 6\n```\n\n### 6단계: 구현 완성 (GREEN)\n\n```python\ndef calculate(text):\n    if text == \"\":\n        return 0\n    numbers = text.split(\",\")\n    return sum(int(n) for n in numbers)\n```\n\n### 7단계: REFACTOR\n\n```python\ndef calculate(text: str) -> int:\n    \"\"\"쉼표로 구분된 숫자들의 합을 반환\"\"\"\n    if not text:\n        return 0\n    return sum(int(n) for n in text.split(\",\"))\n```"
            },
            {
                "type": "code",
                "title": "TDD로 회원가입 기능 만들기",
                "content": "### 요구사항\n```\n- 이메일 형식 검증\n- 비밀번호 8자 이상\n- 중복 이메일 체크\n```\n\n### RED: 실패하는 테스트들\n\n```python\nimport pytest\nfrom user_service import UserService, InvalidEmailError, WeakPasswordError\n\nclass TestUserRegistration:\n    def test_valid_email_format(self):\n        service = UserService()\n        # 유효한 이메일은 통과\n        service.validate_email(\"user@test.com\")  # 예외 없음\n\n    def test_invalid_email_raises_error(self):\n        service = UserService()\n        with pytest.raises(InvalidEmailError):\n            service.validate_email(\"invalid-email\")\n\n    def test_password_must_be_8_chars(self):\n        service = UserService()\n        with pytest.raises(WeakPasswordError):\n            service.validate_password(\"1234567\")  # 7자\n\n    def test_valid_password_passes(self):\n        service = UserService()\n        service.validate_password(\"12345678\")  # 8자 - 예외 없음\n```\n\n### GREEN: 구현\n\n```python\nimport re\n\nclass InvalidEmailError(Exception):\n    pass\n\nclass WeakPasswordError(Exception):\n    pass\n\nclass UserService:\n    def validate_email(self, email: str):\n        pattern = r'^[\\w.-]+@[\\w.-]+\\.\\w+$'\n        if not re.match(pattern, email):\n            raise InvalidEmailError(\"유효하지 않은 이메일 형식\")\n\n    def validate_password(self, password: str):\n        if len(password) < 8:\n            raise WeakPasswordError(\"비밀번호는 8자 이상이어야 합니다\")\n```"
            },
            {
                "type": "tip",
                "title": "TDD 실전 팁",
                "content": "### TDD 마인드셋\n\n```\n처음엔 어색함:\n\"테스트 먼저? 뭘 테스트해?\"\n\n익숙해지면:\n\"테스트가 설계 문서가 되네!\"\n\n핵심:\n- 작은 단계로 나누기\n- 한 번에 하나씩만 테스트\n- 테스트가 통과하면 바로 커밋\n```\n\n### TDD가 어려운 경우\n\n```\nTDD 적합:\n- 비즈니스 로직\n- 알고리즘\n- 유틸리티 함수\n- API 엔드포인트\n\nTDD 어려움:\n- UI/UX 개발\n- 프로토타입\n- 탐색적 개발\n- 외부 API 연동 (Mock 필요)\n```\n\n### Baby Steps\n\n```\nTDD의 핵심은 \"작은 걸음\"\n\n나쁜 예:\n1. 100줄 테스트 작성\n2. 500줄 코드 작성\n3. 뭔가 안 됨...\n\n좋은 예:\n1. 테스트 1개\n2. 코드 5줄\n3. 통과!\n4. 테스트 1개 추가\n5. 코드 5줄...\n```"
            }
        ]
    },

    "04_테스트/test-pattern": {
        "title": "테스트 패턴",
        "description": "테스트 코드 작성 패턴을 배웁니다",
        "sections": [
            {
                "type": "concept",
                "title": "테스트 패턴이란?",
                "content": "## 한 줄 요약\n> **테스트 코드를 잘 작성하는 방법들** - 테스트도 패턴이 있어요!\n\n---\n\n## 왜 테스트 패턴이 필요할까?\n\n### 나쁜 테스트의 문제\n```\n나쁜 테스트:\n- 실행 시간이 너무 길다\n- 뭘 테스트하는지 모르겠다\n- 가끔 실패한다 (Flaky)\n- 수정하기 무섭다\n```\n\n### 좋은 테스트의 특징: FIRST\n```\nF - Fast (빠르게)\n    단위 테스트는 밀리초 단위\n\nI - Independent (독립적)\n    테스트 간 영향 없음\n\nR - Repeatable (반복 가능)\n    언제 실행해도 같은 결과\n\nS - Self-validating (자가 검증)\n    성공/실패가 명확\n\nT - Timely (적시에)\n    코드와 함께 작성\n```"
            },
            {
                "type": "code",
                "title": "테스트 더블 (Mock, Stub, Fake)",
                "content": "### 테스트 더블이란?\n```\n실제 객체를 대신하는 가짜 객체\n\n종류:\n- Mock: 호출 여부 검증\n- Stub: 미리 정해진 값 반환\n- Fake: 간단한 구현 (인메모리 DB)\n```\n\n### Mock 사용 예시\n\n```python\nfrom unittest.mock import Mock, patch\n\n# 이메일 발송 서비스 테스트\nclass EmailService:\n    def send(self, to, subject, body):\n        # 실제로는 SMTP 서버 호출\n        pass\n\nclass UserService:\n    def __init__(self, email_service):\n        self.email_service = email_service\n\n    def register(self, email, password):\n        # 회원가입 로직...\n        self.email_service.send(\n            to=email,\n            subject=\"환영합니다\",\n            body=\"가입을 축하합니다\"\n        )\n        return True\n\n# 테스트\ndef test_register_sends_welcome_email():\n    # Mock 객체 생성\n    mock_email = Mock()\n    service = UserService(mock_email)\n\n    # 회원가입 실행\n    service.register(\"user@test.com\", \"password123\")\n\n    # 이메일 발송이 호출되었는지 검증\n    mock_email.send.assert_called_once_with(\n        to=\"user@test.com\",\n        subject=\"환영합니다\",\n        body=\"가입을 축하합니다\"\n    )\n```\n\n### Stub 사용 예시\n\n```python\n# 외부 API 응답을 가짜로 만들기\ndef test_get_weather():\n    # Stub: 항상 같은 값 반환\n    mock_api = Mock()\n    mock_api.get_weather.return_value = {\"temp\": 25, \"status\": \"sunny\"}\n\n    service = WeatherService(mock_api)\n    result = service.get_today_weather(\"seoul\")\n\n    assert result[\"temp\"] == 25\n```"
            },
            {
                "type": "code",
                "title": "테스트 Fixture 패턴",
                "content": "### Fixture란?\n```\n테스트에 필요한 데이터나 객체를 준비하는 것\n매 테스트마다 반복되는 준비 작업을 재사용\n```\n\n### pytest fixture\n\n```python\nimport pytest\n\n# Fixture 정의\n@pytest.fixture\ndef user():\n    return User(name=\"테스트유저\", email=\"test@test.com\")\n\n@pytest.fixture\ndef user_service():\n    return UserService(\n        db=InMemoryDatabase(),\n        email=MockEmailService()\n    )\n\n# Fixture 사용\ndef test_user_can_change_name(user):\n    user.change_name(\"새이름\")\n    assert user.name == \"새이름\"\n\ndef test_register_user(user_service, user):\n    result = user_service.register(user)\n    assert result.success == True\n```\n\n### Factory 패턴\n\n```python\n# 다양한 테스트 데이터 생성\nclass UserFactory:\n    @staticmethod\n    def create(**kwargs):\n        defaults = {\n            \"name\": \"기본이름\",\n            \"email\": \"default@test.com\",\n            \"age\": 25\n        }\n        defaults.update(kwargs)\n        return User(**defaults)\n\n# 테스트에서 사용\ndef test_adult_user():\n    user = UserFactory.create(age=20)\n    assert user.is_adult() == True\n\ndef test_minor_user():\n    user = UserFactory.create(age=15)\n    assert user.is_adult() == False\n```\n\n### Setup/Teardown\n\n```python\nclass TestDatabase:\n    def setup_method(self):\n        # 각 테스트 전에 실행\n        self.db = create_test_database()\n        self.db.connect()\n\n    def teardown_method(self):\n        # 각 테스트 후에 실행\n        self.db.clear_all()\n        self.db.disconnect()\n\n    def test_insert(self):\n        self.db.insert({\"name\": \"test\"})\n        assert self.db.count() == 1\n```"
            },
            {
                "type": "tip",
                "title": "테스트 안티 패턴",
                "content": "### 피해야 할 패턴들\n\n```\n1. Flaky Test (가끔 실패)\n   - 원인: 시간 의존, 랜덤값, 외부 서비스\n   - 해결: Mock 사용, 시간 고정\n\n2. Slow Test (느린 테스트)\n   - 원인: 실제 DB, 네트워크 호출\n   - 해결: 인메모리 DB, Mock\n\n3. Test Interdependence (테스트 간 의존)\n   - 원인: 전역 상태 공유\n   - 해결: 각 테스트 후 cleanup\n\n4. Testing Implementation (구현 테스트)\n   - 원인: private 메서드 테스트\n   - 해결: public 인터페이스만 테스트\n```\n\n### 좋은 테스트 구조\n\n```python\n# Arrange-Act-Assert (AAA) 패턴\ndef test_user_full_name():\n    # Arrange (준비)\n    user = User(first_name=\"길동\", last_name=\"홍\")\n\n    # Act (실행)\n    full_name = user.get_full_name()\n\n    # Assert (검증)\n    assert full_name == \"홍길동\"\n```\n\n### 테스트 커버리지\n\n```\n커버리지 100%가 목표?\n- 커버리지는 지표일 뿐\n- 중요한 건 \"의미 있는 테스트\"\n- 핵심 비즈니스 로직 80% 이상 권장\n- getter/setter 테스트는 불필요\n```"
            }
        ]
    },

    "04_면접/interview-cleancode": {
        "title": "클린코드 면접",
        "description": "면접에서 자주 나오는 클린코드 질문을 준비합니다",
        "sections": [
            {
                "type": "concept",
                "title": "면접 빈출 질문",
                "content": "## 클린코드 면접 준비\n\n### Q1: 클린코드란 무엇인가요?\n\n```\n모범 답안:\n\"클린코드는 읽기 쉽고, 유지보수하기 좋은 코드입니다.\n다른 개발자(또는 미래의 나)가 코드를 봤을 때\n쉽게 이해하고 수정할 수 있어야 합니다.\n\n핵심 원칙:\n1. 의미 있는 이름 사용\n2. 함수는 한 가지 일만\n3. 중복 제거\n4. 적절한 주석\n5. 일관된 포매팅\"\n```\n\n### Q2: SOLID 원칙을 설명해주세요\n\n```\n모범 답안:\n\"SOLID는 객체지향 설계의 5대 원칙입니다.\n\nS - 단일 책임: 클래스는 하나의 책임만\nO - 개방/폐쇄: 확장엔 열려있고, 수정엔 닫혀있게\nL - 리스코프 치환: 자식은 부모를 대체 가능해야\nI - 인터페이스 분리: 사용하지 않는 인터페이스에 의존 금지\nD - 의존성 역전: 추상화에 의존\n\n실제 프로젝트에서는 DIP를 적용해서\n테스트하기 쉬운 구조를 만들었습니다.\"\n```\n\n### Q3: 리팩토링이란?\n\n```\n모범 답안:\n\"리팩토링은 외부 동작을 유지하면서\n내부 구조를 개선하는 것입니다.\n\n주요 기법:\n- 메서드 추출\n- 변수 이름 변경\n- 중복 코드 제거\n- 조건문 간소화\n\n리팩토링 시 테스트 코드가 있으면\n안전하게 진행할 수 있습니다.\"\n```"
            },
            {
                "type": "code",
                "title": "코드 리뷰 면접 준비",
                "content": "### 면접에서 코드 개선하기\n\n```python\n# 면접관: \"이 코드를 개선해보세요\"\n\n# Before (나쁜 코드)\ndef f(l):\n    r = []\n    for i in l:\n        if i > 0:\n            r.append(i * 2)\n    return r\n```\n\n```python\n# After (개선된 코드)\ndef double_positive_numbers(numbers: list[int]) -> list[int]:\n    \"\"\"양수만 2배로 만들어 반환합니다.\"\"\"\n    return [num * 2 for num in numbers if num > 0]\n\n# 설명:\n# 1. 의미 있는 함수명 (f -> double_positive_numbers)\n# 2. 명확한 매개변수명 (l -> numbers)\n# 3. 타입 힌트 추가\n# 4. docstring 추가\n# 5. 리스트 컴프리헨션으로 간결하게\n```\n\n### 또 다른 예시\n\n```javascript\n// Before\nfunction process(data) {\n    if (data != null) {\n        if (data.type == 'user') {\n            if (data.age >= 18) {\n                return true;\n            }\n        }\n    }\n    return false;\n}\n```\n\n```javascript\n// After\nfunction isAdultUser(data) {\n    if (!data) return false;\n    if (data.type !== 'user') return false;\n    \n    const ADULT_AGE = 18;\n    return data.age >= ADULT_AGE;\n}\n\n// 개선 포인트:\n// 1. 함수명이 의도를 설명 (process -> isAdultUser)\n// 2. 빠른 반환으로 중첩 제거\n// 3. 매직 넘버를 상수로 (18 -> ADULT_AGE)\n// 4. == 대신 === 사용\n```"
            },
            {
                "type": "tip",
                "title": "면접 팁",
                "content": "### 자주 나오는 추가 질문\n\n```\nQ: 테스트 코드를 작성하시나요?\nA: \"네, 단위 테스트를 작성합니다.\n   Jest/pytest를 사용하고,\n   핵심 비즈니스 로직은 반드시 테스트합니다.\n   TDD도 상황에 따라 적용합니다.\"\n\nQ: 코드 리뷰를 어떻게 하시나요?\nA: \"기능보다 가독성, 유지보수성을 봅니다.\n   네이밍, 함수 크기, 중복 여부,\n   테스트 존재 여부를 확인합니다.\n   피드백은 구체적으로, 대안을 제시합니다.\"\n\nQ: 레거시 코드를 어떻게 개선하시나요?\nA: \"먼저 테스트 코드를 작성하고,\n   작은 단위로 점진적으로 리팩토링합니다.\n   한 번에 큰 변경은 위험합니다.\"\n```\n\n### 면접 꿀팁\n\n```\n1. 경험 기반 답변\n   \"제가 진행한 프로젝트에서는...\"\n   \"실제로 이런 문제가 있었는데...\"\n\n2. 트레이드오프 언급\n   \"이 방법의 장점은... 단점은...\"\n   \"상황에 따라 다르게 적용합니다\"\n\n3. 과도한 원칙 적용 경계\n   \"SOLID를 모든 곳에 적용하진 않습니다\"\n   \"필요한 곳에 적절히 적용합니다\"\n```\n\n### 핵심 키워드 암기\n\n```\n클린코드: 가독성, 유지보수성\nSOLID: 단일책임, 개방폐쇄, 리스코프, 인터페이스분리, 의존성역전\n리팩토링: 외부동작 유지, 내부구조 개선\nTDD: Red-Green-Refactor\n테스트: 단위테스트, 통합테스트, Mock\n```"
            }
        ]
    }
}

def update_cleancode_json():
    sys.stdout.reconfigure(encoding='utf-8')

    with open(CLEANCODE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in TEST_CONTENTS.items():
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

    print(f"\n[DONE] Test & Interview sections updated: {updated_count} topics")

if __name__ == "__main__":
    update_cleancode_json()
