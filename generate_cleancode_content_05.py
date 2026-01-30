# -*- coding: utf-8 -*-
# 클린코드 콘텐츠 생성 스크립트 - Part 5
# 05_설계 섹션 (2개 토픽) + index

import json
import sys

CLEANCODE_JSON_PATH = "src/data/contents/cleancode.json"

DESIGN_CONTENTS = {
    "05_설계/class-design": {
        "title": "클래스 설계",
        "description": "좋은 클래스 설계 원칙을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "1. 클래스 설계란?",
                "content": "## 1. 한 줄 요약\n> **좋은 클래스 = 명확한 책임 + 높은 응집도 + 낮은 결합도** - 유지보수하기 좋은 코드의 핵심!\n\n---\n\n## 왜 클래스 설계가 중요한가?\n\n### 나쁜 클래스 설계의 결과:\n```\n시간이 지나면:\n- 하나 고치면 다른 곳이 터짐\n- 클래스가 점점 비대해짐\n- 어디서 뭘 하는지 파악 불가\n- 테스트 작성 불가능\n```\n\n### 좋은 클래스 설계의 결과:\n```\n- 변경 영향 범위 최소화\n- 코드 재사용 용이\n- 테스트하기 쉬움\n- 새 개발자도 빠르게 이해\n```\n\n---\n\n## 좋은 클래스의 특징\n\n### 3가지 핵심 원칙:\n```\n1. 단일 책임 (Single Responsibility)\n   - 한 클래스는 하나의 일만\n   - 변경 이유가 하나뿐\n\n2. 높은 응집도 (High Cohesion)\n   - 관련된 것들끼리 모임\n   - 메서드들이 같은 데이터 사용\n\n3. 낮은 결합도 (Low Coupling)\n   - 다른 클래스와 최소한으로 연결\n   - 인터페이스로 소통\n```"
            },
            {
                "type": "code",
                "title": "2. 클래스 크기와 책임",
                "content": "### 나쁜 예: 신(God) 클래스\n\n```python\n# X 나쁜 예: 모든 것을 하는 클래스\nclass UserManager:\n    def __init__(self):\n        self.db = Database()\n        self.mailer = Mailer()\n        self.logger = Logger()\n    \n    # 사용자 CRUD\n    def create_user(self, data): ...\n    def get_user(self, id): ...\n    def update_user(self, id, data): ...\n    def delete_user(self, id): ...\n    \n    # 인증\n    def login(self, email, password): ...\n    def logout(self, user_id): ...\n    def reset_password(self, email): ...\n    \n    # 이메일\n    def send_welcome_email(self, user): ...\n    def send_password_reset_email(self, user): ...\n    \n    # 검증\n    def validate_email(self, email): ...\n    def validate_password(self, password): ...\n    \n    # 통계\n    def get_user_statistics(self): ...\n    def generate_report(self): ...\n\n# 문제점:\n# - 500줄이 넘는 클래스\n# - 여러 책임이 섞여 있음\n# - 테스트하기 어려움\n# - 변경 시 영향 범위가 큼\n```\n\n### 좋은 예: 책임 분리\n\n```python\n# O 좋은 예: 책임별로 분리된 클래스들\n\n# 사용자 엔티티 (데이터만)\nclass User:\n    def __init__(self, id, email, name):\n        self.id = id\n        self.email = email\n        self.name = name\n\n# 저장소 (DB 접근만)\nclass UserRepository:\n    def __init__(self, db):\n        self.db = db\n    \n    def save(self, user): ...\n    def find_by_id(self, id): ...\n    def find_by_email(self, email): ...\n    def delete(self, id): ...\n\n# 인증 서비스 (로그인/로그아웃만)\nclass AuthService:\n    def __init__(self, user_repo, password_hasher):\n        self.user_repo = user_repo\n        self.hasher = password_hasher\n    \n    def login(self, email, password): ...\n    def logout(self, user_id): ...\n\n# 이메일 서비스 (이메일 발송만)\nclass UserEmailService:\n    def __init__(self, mailer):\n        self.mailer = mailer\n    \n    def send_welcome(self, user): ...\n    def send_password_reset(self, user): ...\n\n# 검증기 (검증만)\nclass UserValidator:\n    def validate_email(self, email): ...\n    def validate_password(self, password): ...\n```"
            },
            {
                "type": "code",
                "title": "3. 응집도 높이기",
                "content": "### 응집도란?\n\n```\n응집도 = 클래스 내부 요소들이 얼마나 관련되어 있는가\n\n높은 응집도: 모든 메서드가 모든 필드를 사용\n낮은 응집도: 메서드들이 서로 다른 필드만 사용\n```\n\n### 낮은 응집도 예시\n\n```python\n# X 낮은 응집도: 메서드들이 서로 다른 필드 사용\nclass Employee:\n    def __init__(self):\n        # 그룹 1: 개인정보\n        self.name = None\n        self.email = None\n        \n        # 그룹 2: 급여정보\n        self.salary = None\n        self.bonus = None\n        \n        # 그룹 3: 출퇴근정보\n        self.check_in_time = None\n        self.check_out_time = None\n    \n    # 그룹 1 메서드들\n    def get_name(self): return self.name\n    def update_email(self, email): ...\n    \n    # 그룹 2 메서드들\n    def calculate_salary(self): ...  # salary, bonus만 사용\n    def apply_bonus(self): ...       # salary, bonus만 사용\n    \n    # 그룹 3 메서드들\n    def check_in(self): ...          # 시간만 사용\n    def check_out(self): ...         # 시간만 사용\n```\n\n### 높은 응집도로 분리\n\n```python\n# O 높은 응집도: 관련된 것끼리 분리\nclass EmployeeProfile:\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email\n    \n    def get_name(self): return self.name\n    def update_email(self, email): self.email = email\n\nclass Payroll:\n    def __init__(self, salary, bonus_rate=0.1):\n        self.salary = salary\n        self.bonus_rate = bonus_rate\n    \n    def calculate_total(self):\n        return self.salary * (1 + self.bonus_rate)\n    \n    def apply_raise(self, percent):\n        self.salary *= (1 + percent)\n\nclass Attendance:\n    def __init__(self):\n        self.check_in_time = None\n        self.check_out_time = None\n    \n    def check_in(self):\n        self.check_in_time = datetime.now()\n    \n    def check_out(self):\n        self.check_out_time = datetime.now()\n    \n    def get_work_hours(self):\n        return (self.check_out_time - self.check_in_time).hours\n\n# 필요시 조합\nclass Employee:\n    def __init__(self, profile, payroll, attendance):\n        self.profile = profile\n        self.payroll = payroll\n        self.attendance = attendance\n```"
            },
            {
                "type": "code",
                "title": "4. 결합도 낮추기",
                "content": "### 결합도란?\n\n```\n결합도 = 클래스 간의 의존 정도\n\n높은 결합도: A가 B의 내부를 직접 사용\n낮은 결합도: A가 B의 인터페이스만 사용\n```\n\n### 높은 결합도 (나쁜 예)\n\n```python\n# X 높은 결합도: 구체적인 구현에 의존\nclass OrderService:\n    def __init__(self):\n        # 구체 클래스에 직접 의존\n        self.db = MySQLDatabase()\n        self.payment = StripePayment()\n        self.notifier = KakaoNotifier()\n    \n    def create_order(self, order_data):\n        # MySQL 고유 메서드 사용\n        self.db.mysql_insert(\"orders\", order_data)\n        \n        # Stripe 고유 메서드 사용\n        self.payment.stripe_charge(order_data.amount)\n        \n        # 카카오 고유 메서드 사용\n        self.notifier.send_kakao_message(\"주문완료\")\n\n# 문제점:\n# - DB 변경시 OrderService 수정 필요\n# - 결제사 변경시 OrderService 수정 필요\n# - 테스트시 실제 DB/결제 필요\n```\n\n### 낮은 결합도 (좋은 예)\n\n```python\n# O 낮은 결합도: 추상화에 의존\nfrom abc import ABC, abstractmethod\n\n# 인터페이스 정의\nclass Database(ABC):\n    @abstractmethod\n    def save(self, table, data): pass\n\nclass PaymentGateway(ABC):\n    @abstractmethod\n    def charge(self, amount): pass\n\nclass Notifier(ABC):\n    @abstractmethod\n    def send(self, message): pass\n\n# 서비스는 인터페이스에만 의존\nclass OrderService:\n    def __init__(self, db: Database, payment: PaymentGateway, notifier: Notifier):\n        self.db = db\n        self.payment = payment\n        self.notifier = notifier\n    \n    def create_order(self, order_data):\n        self.db.save(\"orders\", order_data)\n        self.payment.charge(order_data.amount)\n        self.notifier.send(\"주문완료\")\n\n# 구현체는 별도로\nclass MySQLDatabase(Database):\n    def save(self, table, data):\n        # MySQL 저장 로직\n        pass\n\nclass PostgreSQLDatabase(Database):\n    def save(self, table, data):\n        # PostgreSQL 저장 로직\n        pass\n\n# 사용: 원하는 구현체 주입\nservice = OrderService(\n    db=MySQLDatabase(),\n    payment=StripePayment(),\n    notifier=KakaoNotifier()\n)\n\n# 테스트: Mock 주입\ntest_service = OrderService(\n    db=MockDatabase(),\n    payment=MockPayment(),\n    notifier=MockNotifier()\n)\n```"
            },
            {
                "type": "tip",
                "title": "5. 클래스 설계 체크리스트",
                "content": "### 클래스 이름 짓기\n\n```\n좋은 이름의 특징:\n- 명사 또는 명사구 사용\n- 클래스의 책임을 명확히 표현\n- Manager, Handler, Processor 남용 금지\n\n예시:\n- UserManager -> UserService, UserRepository\n- DataHandler -> OrderProcessor, PaymentGateway\n- InfoUtils -> AddressFormatter, PriceCalculator\n```\n\n### 클래스 크기 가이드\n\n```\n경고 신호:\n- 200줄 이상 -> 분리 고려\n- 메서드 20개 이상 -> 책임 검토\n- 필드 10개 이상 -> 그룹화 고려\n- 주입받는 의존성 5개 이상 -> 책임 분리\n```\n\n### 설계 체크리스트\n\n```\n[ ] 클래스 이름이 책임을 명확히 표현하는가?\n[ ] 변경 이유가 하나뿐인가? (SRP)\n[ ] 모든 메서드가 대부분의 필드를 사용하는가? (응집도)\n[ ] 구체 클래스가 아닌 인터페이스에 의존하는가? (결합도)\n[ ] 테스트하기 쉬운가?\n[ ] 새 기능 추가시 기존 코드 수정이 최소화되는가?\n```\n\n### 리팩토링 시점\n\n```\n지금 당장 분리:\n- 같은 코드 복붙이 3번 이상\n- 버그 수정시 여러 곳 수정 필요\n- 테스트 작성이 불가능\n\n천천히 분리:\n- 클래스가 점점 커지는 중\n- \"나중에 분리해야지\" 생각이 들 때\n- 코드 리뷰에서 지적받았을 때\n```"
            }
        ]
    },

    "05_설계/composition-over-inheritance": {
        "title": "상속보다 구성",
        "description": "상속보다 구성(Composition)을 우선하는 원칙을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "1. 상속보다 구성이란?",
                "content": "## 1. 한 줄 요약\n> **\"is-a\" 보다 \"has-a\"** - 상속으로 기능을 물려받기보다, 필요한 기능을 가진 객체를 포함하세요!\n\n---\n\n## 왜 상속보다 구성인가?\n\n### 상속의 문제점:\n```\n1. 강한 결합\n   - 부모 변경 = 자식 모두 영향\n   - 부모 내부 구현에 의존\n\n2. 유연성 부족\n   - 런타임에 행동 변경 불가\n   - 다중 상속 불가 (대부분 언어)\n\n3. 캡슐화 깨짐\n   - 부모의 내부를 알아야 함\n   - 부모 메서드 오버라이드 위험\n```\n\n### 구성의 장점:\n```\n1. 느슨한 결합\n   - 인터페이스로만 소통\n   - 내부 구현 변경 자유로움\n\n2. 높은 유연성\n   - 런타임에 행동 변경 가능\n   - 여러 기능 조합 가능\n\n3. 캡슐화 유지\n   - 내부 구현 숨김\n   - 변경 영향 최소화\n```\n\n---\n\n## 비유로 이해하기\n\n### 상속 = 유전\n```\n부모에게 물려받은 특성\n- 바꿀 수 없음\n- 부모가 바뀌면 나도 바뀜\n- 선택할 수 없음\n```\n\n### 구성 = 도구 사용\n```\n필요한 도구를 선택해서 사용\n- 언제든 교체 가능\n- 도구 내부가 바뀌어도 사용법만 같으면 OK\n- 상황에 맞게 선택\n```"
            },
            {
                "type": "code",
                "title": "2. 상속의 문제점",
                "content": "### 문제 1: 깨지기 쉬운 기반 클래스\n\n```python\n# X 상속: 부모 변경이 자식을 망침\n\nclass Stack(list):  # list를 상속\n    def push(self, item):\n        self.append(item)\n    \n    def pop_item(self):\n        return self.pop()\n\n# 문제: list의 모든 메서드가 노출됨!\nstack = Stack()\nstack.push(1)\nstack.push(2)\nstack.insert(0, 100)  # 스택인데 중간 삽입 가능!\nstack[0] = 999        # 직접 수정 가능!\n\n# 스택의 LIFO 원칙이 깨짐\n```\n\n### 문제 2: 다이아몬드 문제\n\n```python\n# X 상속: 다중 상속의 복잡성\n\nclass A:\n    def greet(self):\n        return \"A\"\n\nclass B(A):\n    def greet(self):\n        return \"B\"\n\nclass C(A):\n    def greet(self):\n        return \"C\"\n\nclass D(B, C):  # B와 C 모두 상속\n    pass\n\nd = D()\nd.greet()  # \"B\"? \"C\"? 헷갈림!\n# MRO(Method Resolution Order)를 알아야 예측 가능\n```\n\n### 문제 3: 부적절한 상속\n\n```python\n# X 나쁜 상속: 정사각형은 직사각형인가?\n\nclass Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n    \n    def set_width(self, width):\n        self.width = width\n    \n    def set_height(self, height):\n        self.height = height\n    \n    def area(self):\n        return self.width * self.height\n\nclass Square(Rectangle):\n    def __init__(self, side):\n        super().__init__(side, side)\n    \n    def set_width(self, width):\n        # 정사각형이니까 높이도 바꿔야 함\n        self.width = width\n        self.height = width\n    \n    def set_height(self, height):\n        self.width = height\n        self.height = height\n\n# 문제: Rectangle을 기대하는 코드에서 오작동\ndef double_width(rect: Rectangle):\n    rect.set_width(rect.width * 2)\n    return rect.area()\n\nr = Rectangle(5, 10)\nprint(double_width(r))  # 100 (10*10)\n\ns = Square(5)\nprint(double_width(s))  # 100이 아닌 100! (10*10)\n# 리스코프 치환 원칙 위반\n```"
            },
            {
                "type": "code",
                "title": "3. 구성으로 해결하기",
                "content": "### 해결 1: 위임 사용\n\n```python\n# O 구성: 내부에 list를 가지고 필요한 것만 노출\n\nclass Stack:\n    def __init__(self):\n        self._items = []  # list를 포함 (has-a)\n    \n    def push(self, item):\n        self._items.append(item)\n    \n    def pop(self):\n        if not self.is_empty():\n            return self._items.pop()\n        raise IndexError(\"Stack is empty\")\n    \n    def peek(self):\n        if not self.is_empty():\n            return self._items[-1]\n        raise IndexError(\"Stack is empty\")\n    \n    def is_empty(self):\n        return len(self._items) == 0\n\n# 이제 스택답게만 사용 가능\nstack = Stack()\nstack.push(1)\nstack.push(2)\n# stack.insert(0, 100)  # 불가능!\n# stack[0] = 999        # 불가능!\n```\n\n### 해결 2: 전략 패턴\n\n```python\n# O 구성: 행동을 객체로 분리\nfrom abc import ABC, abstractmethod\n\n# 전략 인터페이스\nclass FlyBehavior(ABC):\n    @abstractmethod\n    def fly(self): pass\n\nclass QuackBehavior(ABC):\n    @abstractmethod\n    def quack(self): pass\n\n# 구체 전략들\nclass FlyWithWings(FlyBehavior):\n    def fly(self):\n        return \"날개로 날아갑니다\"\n\nclass FlyNoWay(FlyBehavior):\n    def fly(self):\n        return \"날 수 없습니다\"\n\nclass Quack(QuackBehavior):\n    def quack(self):\n        return \"꽥꽥!\"\n\nclass Squeak(QuackBehavior):\n    def quack(self):\n        return \"삑삑!\"\n\n# 오리 클래스: 행동을 구성으로 가짐\nclass Duck:\n    def __init__(self, fly_behavior: FlyBehavior, quack_behavior: QuackBehavior):\n        self.fly_behavior = fly_behavior\n        self.quack_behavior = quack_behavior\n    \n    def fly(self):\n        return self.fly_behavior.fly()\n    \n    def quack(self):\n        return self.quack_behavior.quack()\n    \n    # 런타임에 행동 변경 가능!\n    def set_fly_behavior(self, fb: FlyBehavior):\n        self.fly_behavior = fb\n\n# 사용\nmallard = Duck(FlyWithWings(), Quack())\nprint(mallard.fly())    # 날개로 날아갑니다\nprint(mallard.quack())  # 꽥꽥!\n\nrubber_duck = Duck(FlyNoWay(), Squeak())\nprint(rubber_duck.fly())    # 날 수 없습니다\nprint(rubber_duck.quack())  # 삑삑!\n\n# 런타임에 행동 변경\nmallard.set_fly_behavior(FlyNoWay())\nprint(mallard.fly())  # 날 수 없습니다\n```"
            },
            {
                "type": "code",
                "title": "4. 실전 예제: 로깅 시스템",
                "content": "### 상속 방식 (비권장)\n\n```python\n# X 상속: 유연성 없음\n\nclass Logger:\n    def log(self, message):\n        pass\n\nclass FileLogger(Logger):\n    def log(self, message):\n        with open(\"log.txt\", \"a\") as f:\n            f.write(message + \"\\n\")\n\nclass ConsoleLogger(Logger):\n    def log(self, message):\n        print(message)\n\n# 파일과 콘솔 둘 다 하고 싶으면?\nclass FileAndConsoleLogger(FileLogger, ConsoleLogger):\n    def log(self, message):\n        FileLogger.log(self, message)\n        ConsoleLogger.log(self, message)\n\n# 문제:\n# - 새 조합마다 클래스 필요\n# - DB, Email 추가하면 조합 폭발\n# - 런타임에 변경 불가\n```\n\n### 구성 방식 (권장)\n\n```python\n# O 구성: 유연하고 확장 가능\n\nfrom abc import ABC, abstractmethod\n\n# 로그 핸들러 인터페이스\nclass LogHandler(ABC):\n    @abstractmethod\n    def handle(self, message): pass\n\n# 핸들러 구현체들\nclass FileHandler(LogHandler):\n    def __init__(self, filename):\n        self.filename = filename\n    \n    def handle(self, message):\n        with open(self.filename, \"a\") as f:\n            f.write(message + \"\\n\")\n\nclass ConsoleHandler(LogHandler):\n    def handle(self, message):\n        print(message)\n\nclass DatabaseHandler(LogHandler):\n    def __init__(self, db):\n        self.db = db\n    \n    def handle(self, message):\n        self.db.insert(\"logs\", {\"message\": message})\n\n# 로거: 핸들러들을 구성으로 가짐\nclass Logger:\n    def __init__(self):\n        self.handlers = []\n    \n    def add_handler(self, handler: LogHandler):\n        self.handlers.append(handler)\n        return self  # 메서드 체이닝\n    \n    def remove_handler(self, handler: LogHandler):\n        self.handlers.remove(handler)\n    \n    def log(self, message):\n        for handler in self.handlers:\n            handler.handle(message)\n\n# 사용: 자유롭게 조합\nlogger = Logger()\nlogger.add_handler(FileHandler(\"app.log\"))\nlogger.add_handler(ConsoleHandler())\nlogger.add_handler(DatabaseHandler(db))\n\nlogger.log(\"Hello\")  # 파일 + 콘솔 + DB 동시에!\n\n# 런타임에 핸들러 추가/제거 가능\nif DEBUG_MODE:\n    logger.add_handler(ConsoleHandler())\n```"
            },
            {
                "type": "tip",
                "title": "5. 언제 무엇을 사용할까?",
                "content": "### 상속이 적절한 경우\n\n```\n상속을 써도 되는 경우:\n- 진짜 \"is-a\" 관계일 때\n  - Dog is-a Animal (O)\n  - Button is-a Component (O)\n\n- 프레임워크에서 요구할 때\n  - Django View 상속\n  - React Component 상속\n\n- 템플릿 메서드 패턴\n  - 알고리즘 골격 정의\n  - 세부 구현만 자식에서\n```\n\n### 구성이 적절한 경우\n\n```\n구성을 써야 하는 경우:\n- \"has-a\" 관계일 때\n  - Car has-a Engine (O)\n  - User has-a Address (O)\n\n- 행동을 동적으로 바꿀 때\n  - 전략 패턴\n  - 데코레이터 패턴\n\n- 여러 기능을 조합할 때\n  - 로깅 + 캐싱 + 검증\n```\n\n### 판단 기준\n\n```\n질문 1: \"B는 A의 일종이다\"가 자연스러운가?\n- 자연스럽다 -> 상속 고려\n- 어색하다 -> 구성 사용\n\n질문 2: B가 A의 모든 메서드를 지원하는가?\n- Yes -> 상속 가능\n- No -> 구성 사용\n\n질문 3: 런타임에 행동이 바뀔 수 있는가?\n- Yes -> 구성 사용\n- No -> 상속 가능\n\n질문 4: A의 내부 구현이 바뀌면 B도 바뀌어야 하는가?\n- Yes -> 구성 사용 (느슨한 결합)\n- No -> 상속 가능\n```\n\n### 격언\n\n```\n\"Favor object composition over class inheritance\"\n- GoF 디자인 패턴\n\n\"상속은 코드 재사용을 위한 것이 아니다.\n 타입 관계를 표현하기 위한 것이다.\"\n\n경험 법칙:\n- 상속 깊이 2-3단계 이하 유지\n- 상속보다 인터페이스 구현 선호\n- 코드 재사용은 구성으로\n```"
            }
        ]
    },

    "index": {
        "title": "클린코드 학습 가이드",
        "description": "전체 커리큘럼 및 학습 로드맵",
        "sections": [
            {
                "type": "concept",
                "title": "클린코드 학습 가이드",
                "content": "## 클린코드란?\n\n> **읽기 쉽고, 이해하기 쉽고, 수정하기 쉬운 코드**\n\n### 클린코드가 중요한 이유:\n```\n코드는 작성하는 시간보다 읽는 시간이 10배 더 많습니다.\n\n- 내가 쓴 코드를 3개월 후 다시 봐야 할 때\n- 팀원이 내 코드를 이해해야 할 때\n- 버그를 찾아서 수정해야 할 때\n- 새 기능을 추가해야 할 때\n\n클린코드는 이 모든 상황에서 시간을 절약해줍니다.\n```\n\n### 이 가이드에서 배우는 것:\n```\n1. 코드 기초     - 이름짓기, 함수, 주석\n2. SOLID 원칙   - 객체지향 설계의 핵심\n3. 코드 스멜    - 나쁜 코드 감지하기\n4. 리팩토링     - 코드 개선 기법\n5. 설계 원칙    - 클래스 설계, 구성\n```"
            },
            {
                "type": "concept",
                "title": "학습 로드맵",
                "content": "## 추천 학습 순서\n\n### 1단계: 기초 다지기 (01_코드기초)\n```\n순서: naming -> functions -> comments\n\n1. 이름짓기 (naming)\n   - 변수, 함수, 클래스 이름 잘 짓기\n   - 가장 기본이면서 가장 중요!\n   - 예상 학습 시간: 1시간\n\n2. 함수 (functions)\n   - 작고 한 가지 일만 하는 함수\n   - 파라미터와 반환값 설계\n   - 예상 학습 시간: 2시간\n\n3. 주석 (comments)\n   - 좋은 주석 vs 나쁜 주석\n   - 코드로 의도를 표현하기\n   - 예상 학습 시간: 1시간\n```\n\n### 2단계: SOLID 원칙 (02_SOLID)\n```\n순서: solid-intro -> srp -> ocp -> lsp -> isp -> dip -> solid-example\n\n1. SOLID 소개 (solid-intro)\n   - 5가지 원칙 개요\n   - 예상 학습 시간: 30분\n\n2. 단일 책임 원칙 (srp)\n   - 한 클래스, 한 책임\n   - 예상 학습 시간: 1시간\n\n3. 개방/폐쇄 원칙 (ocp)\n   - 확장에 열려있고 수정에 닫혀있게\n   - 예상 학습 시간: 1시간\n\n4. 리스코프 치환 원칙 (lsp)\n   - 자식은 부모를 대체할 수 있어야\n   - 예상 학습 시간: 1시간\n\n5. 인터페이스 분리 원칙 (isp)\n   - 클라이언트별 인터페이스 분리\n   - 예상 학습 시간: 45분\n\n6. 의존성 역전 원칙 (dip)\n   - 추상화에 의존하라\n   - 예상 학습 시간: 1시간\n\n7. SOLID 종합 예제 (solid-example)\n   - 실제 프로젝트에 적용하기\n   - 예상 학습 시간: 1시간\n```"
            },
            {
                "type": "concept",
                "title": "학습 로드맵 (계속)",
                "content": "### 3단계: 코드 스멜 감지 (03_코드스멜)\n```\n순서: code-smell-intro -> bloaters -> oo-abusers -> change-preventers -> dispensables -> couplers\n\n1. 코드 스멜 소개 (code-smell-intro)\n   - 나쁜 코드의 징후 알기\n   - 예상 학습 시간: 30분\n\n2. 비대한 코드 (bloaters)\n   - 긴 메서드, 큰 클래스\n   - 예상 학습 시간: 1시간\n\n3. 객체지향 남용 (oo-abusers)\n   - 스위치문, 임시 필드\n   - 예상 학습 시간: 1시간\n\n4. 변경 방해 (change-preventers)\n   - 산탄총 수술, 병렬 상속\n   - 예상 학습 시간: 1시간\n\n5. 불필요한 것들 (dispensables)\n   - 죽은 코드, 중복 코드\n   - 예상 학습 시간: 45분\n\n6. 결합 문제 (couplers)\n   - 과도한 친밀도, 메시지 체인\n   - 예상 학습 시간: 1시간\n```\n\n### 4단계: 리팩토링 기법 (04_리팩토링)\n```\n순서: refactoring-intro -> extract-method -> move-method -> replace-conditional\n\n1. 리팩토링 소개 (refactoring-intro)\n   - 리팩토링이란? 언제 해야 하나?\n   - 예상 학습 시간: 30분\n\n2. 메서드 추출 (extract-method)\n   - 긴 함수 쪼개기\n   - 예상 학습 시간: 1시간\n\n3. 메서드 이동 (move-method)\n   - 적절한 클래스로 옮기기\n   - 예상 학습 시간: 45분\n\n4. 조건문 리팩토링 (replace-conditional)\n   - if-else를 다형성으로\n   - 예상 학습 시간: 1시간\n```\n\n### 5단계: 설계 원칙 (05_설계)\n```\n순서: class-design -> composition-over-inheritance\n\n1. 클래스 설계 (class-design)\n   - 응집도, 결합도, 책임\n   - 예상 학습 시간: 1.5시간\n\n2. 상속보다 구성 (composition-over-inheritance)\n   - 유연한 설계를 위한 구성 원칙\n   - 예상 학습 시간: 1.5시간\n```"
            },
            {
                "type": "tip",
                "title": "학습 팁",
                "content": "### 효과적인 학습 방법\n\n```\n1. 이론 + 실습 병행\n   - 예제 코드 직접 타이핑\n   - 본인 프로젝트에 적용해보기\n   - 리팩토링 연습하기\n\n2. 작은 것부터 시작\n   - 오늘 쓴 코드에서 변수명 하나 개선\n   - 긴 함수 하나 분리해보기\n   - 중복 코드 하나 제거하기\n\n3. 코드 리뷰 활용\n   - 동료 코드 읽어보기\n   - 피드백 주고받기\n   - 다른 사람의 관점 배우기\n\n4. 반복 학습\n   - 한 번에 완벽히 이해 X\n   - 여러 번 읽고 적용하기\n   - 경험이 쌓이면 이해도 UP\n```\n\n### 주의사항\n\n```\n1. 과도한 적용 금지\n   - 모든 코드에 패턴 적용 X\n   - 간단한 문제는 간단하게\n   - YAGNI: 필요할 때 적용\n\n2. 맹목적 규칙 따르기 금지\n   - 상황에 따라 판단\n   - 규칙의 \"이유\"를 이해\n   - 트레이드오프 고려\n\n3. 완벽주의 금지\n   - 처음부터 완벽한 코드 없음\n   - 점진적으로 개선\n   - 동작하는 코드 먼저, 개선은 나중\n```\n\n### 총 예상 학습 시간\n\n```\n1단계: 4시간\n2단계: 6시간 15분\n3단계: 5시간 15분\n4단계: 3시간 15분\n5단계: 3시간\n------------------------\n총합: 약 22시간\n\n추천: 하루 1-2시간씩 2-3주\n```"
            },
            {
                "type": "concept",
                "title": "다음 단계",
                "content": "## 클린코드 마스터 후 다음 단계\n\n### 추천 학습 경로\n\n```\n1. 디자인 패턴\n   - 생성 패턴: Factory, Singleton, Builder\n   - 구조 패턴: Adapter, Decorator, Facade\n   - 행동 패턴: Strategy, Observer, Command\n\n2. 테스트 주도 개발 (TDD)\n   - 단위 테스트 작성법\n   - 테스트 가능한 코드 설계\n   - Red-Green-Refactor 사이클\n\n3. 도메인 주도 설계 (DDD)\n   - 유비쿼터스 언어\n   - 바운디드 컨텍스트\n   - 애그리게이트 설계\n\n4. 클린 아키텍처\n   - 계층형 아키텍처\n   - 의존성 규칙\n   - 프레임워크 독립성\n```\n\n### 추천 도서\n\n```\n입문:\n- 클린 코드 (로버트 마틴)\n- 리팩터링 (마틴 파울러)\n\n중급:\n- 클린 아키텍처 (로버트 마틴)\n- 테스트 주도 개발 (켄트 벡)\n\n고급:\n- 도메인 주도 설계 (에릭 에반스)\n- 패턴 지향 소프트웨어 아키텍처\n```\n\n### 마무리\n\n```\n클린코드는 목적지가 아니라 여정입니다.\n\n매일 조금씩 더 나은 코드를 작성하려고 노력하세요.\n완벽한 코드는 없지만, 더 나은 코드는 있습니다.\n\n\"프로그래밍은 예술이다. 코드는 시다.\"\n- 작성하는 순간뿐 아니라\n- 읽히는 모든 순간을 위해 쓰세요.\n\n행운을 빕니다! Happy Coding!\n```"
            }
        ]
    }
}

def update_cleancode_json():
    sys.stdout.reconfigure(encoding='utf-8')

    with open(CLEANCODE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in DESIGN_CONTENTS.items():
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

    print(f"\n[DONE] Design section + index updated: {updated_count} topics")

if __name__ == "__main__":
    update_cleancode_json()
