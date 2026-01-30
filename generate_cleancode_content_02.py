# -*- coding: utf-8 -*-
# 클린코드 콘텐츠 생성 스크립트 - Part 2
# 02_SOLID 섹션 (7개 토픽)

import json
import sys

CLEANCODE_JSON_PATH = "src/data/contents/cleancode.json"

SOLID_CONTENTS = {
    "02_SOLID/solid-intro": {
        "title": "SOLID 소개",
        "description": "SOLID 원칙의 개요를 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🏛️ SOLID란?",
                "content": "## 🏛️ 한 줄 요약\n> **객체지향 설계의 5대 원칙** - 유지보수하기 좋은 코드를 위한 가이드라인!\n\n---\n\n## 💡 왜 SOLID를 배워야 하나?\n\n### SOLID 없이 코딩하면:\n```\n시간이 지날수록:\n├── 코드 수정이 두려움\n├── 한 곳 고치면 다른 곳 터짐\n├── 새 기능 추가가 어려움\n└── 테스트 작성 불가능\n```\n\n### SOLID를 적용하면:\n```\n├── 변경에 유연함\n├── 코드 재사용 쉬움\n├── 테스트 작성 쉬움\n├── 유지보수 비용 감소\n└── 확장성 확보\n```\n\n---\n\n## 🎯 SOLID 5가지 원칙\n\n### 암기법: \"솔리드\"\n```\nS - Single Responsibility (단일 책임)\n    \"한 클래스는 하나의 책임만\"\n\nO - Open/Closed (개방/폐쇄)\n    \"확장에는 열려있고, 수정에는 닫혀있게\"\n\nL - Liskov Substitution (리스코프 치환)\n    \"자식은 부모를 대체할 수 있어야\"\n\nI - Interface Segregation (인터페이스 분리)\n    \"클라이언트별로 인터페이스 분리\"\n\nD - Dependency Inversion (의존성 역전)\n    \"추상화에 의존하라\"\n```"
            },
            {
                "type": "code",
                "title": "💻 SOLID 미리보기",
                "content": "### S - 단일 책임\n\n```python\n# ❌ 여러 책임\nclass User:\n    def save_to_db(self): ...\n    def send_email(self): ...\n    def generate_report(self): ...\n\n# ✅ 단일 책임\nclass User: ...\nclass UserRepository:\n    def save(self, user): ...\nclass EmailService:\n    def send(self, to, msg): ...\n```\n\n### O - 개방/폐쇄\n\n```python\n# ❌ 수정 필요\ndef calculate_discount(product_type):\n    if product_type == \"book\":\n        return 0.1\n    elif product_type == \"electronics\":\n        return 0.2\n\n# ✅ 확장만 하면 됨\nclass DiscountPolicy(ABC):\n    @abstractmethod\n    def calculate(self): pass\n\nclass BookDiscount(DiscountPolicy):\n    def calculate(self): return 0.1\n```\n\n### L - 리스코프 치환\n\n```python\n# ❌ 위반: 자식이 부모 역할 못함\nclass Bird:\n    def fly(self): ...\n\nclass Penguin(Bird):\n    def fly(self):\n        raise Exception(\"Can't fly!\")\n\n# ✅ 올바른 설계\nclass Bird: ...\nclass FlyingBird(Bird):\n    def fly(self): ...\nclass Penguin(Bird): ...\n```"
            },
            {
                "type": "tip",
                "title": "💡 SOLID 학습 팁",
                "content": "### 학습 순서 추천\n\n```\n1단계: SRP (단일 책임)\n└── 가장 기본, 바로 적용 가능\n\n2단계: OCP (개방/폐쇄)\n└── 확장성 있는 설계 이해\n\n3단계: DIP (의존성 역전)\n└── 테스트 용이성 확보\n\n4단계: LSP, ISP\n└── 상속과 인터페이스 설계\n```\n\n### 적용 가이드\n\n```\n모든 코드에 SOLID를?\n├── ❌ 과도한 적용은 오버엔지니어링\n├── ✅ 변경 가능성 높은 부분에 적용\n└── ✅ 점진적으로 적용\n```"
            }
        ]
    },

    "02_SOLID/srp": {
        "title": "단일 책임 원칙 (SRP)",
        "description": "Single Responsibility Principle을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "1️⃣ 단일 책임 원칙",
                "content": "## 1️⃣ 한 줄 요약\n> **한 클래스는 하나의 책임만** - 변경 이유가 하나뿐이어야 해요!\n\n---\n\n## 💡 책임이란?\n\n### 책임 = 변경 이유\n```\n\"클래스를 변경해야 하는 이유가\n 단 하나뿐이어야 한다\"\n\n예시:\nUser 클래스를 변경하는 이유가 3가지?\n├── 사용자 정보 변경\n├── DB 스키마 변경\n└── 이메일 형식 변경\n\n→ 책임이 3개! SRP 위반!\n```\n\n---\n\n## 🎯 SRP 적용\n\n### 위반 사례:\n```python\nclass User:\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email\n\n    # 책임 1: 사용자 데이터\n    def change_name(self, name):\n        self.name = name\n\n    # 책임 2: DB 저장\n    def save_to_database(self):\n        db.execute(f\"INSERT INTO users...\")\n\n    # 책임 3: 이메일 발송\n    def send_welcome_email(self):\n        smtp.send(self.email, \"Welcome!\")\n```\n\n### 적용 사례:\n```python\n# 책임 1: 사용자 데이터만\nclass User:\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email\n\n# 책임 2: DB 저장\nclass UserRepository:\n    def save(self, user):\n        db.execute(f\"INSERT INTO users...\")\n\n# 책임 3: 이메일 발송\nclass EmailService:\n    def send_welcome_email(self, user):\n        smtp.send(user.email, \"Welcome!\")\n```"
            },
            {
                "type": "code",
                "title": "💻 SRP 실전 예시",
                "content": "### 컨트롤러 분리\n\n```javascript\n// ❌ SRP 위반: 컨트롤러가 너무 많은 일\nclass UserController {\n    async createUser(req, res) {\n        // 검증\n        if (!req.body.email.includes('@')) {\n            return res.status(400).json({error: 'Invalid email'});\n        }\n        // 비즈니스 로직 + DB 저장 + 이메일...\n    }\n}\n\n// ✅ SRP 적용: 책임 분리\nclass UserController {\n    constructor(userService) {\n        this.userService = userService;\n    }\n\n    async createUser(req, res) {\n        const user = await this.userService.createUser(req.body);\n        res.json(user);\n    }\n}\n\nclass UserService {\n    constructor(userRepo, emailService, validator) {\n        this.userRepo = userRepo;\n        this.emailService = emailService;\n        this.validator = validator;\n    }\n\n    async createUser(data) {\n        this.validator.validate(data);\n        const user = await this.userRepo.create(data);\n        await this.emailService.sendWelcome(user);\n        return user;\n    }\n}\n```"
            },
            {
                "type": "tip",
                "title": "💡 SRP 적용 팁",
                "content": "### 책임 분리 신호\n\n```\n분리가 필요할 때:\n├── \"그리고\"가 들어갈 때\n│   └── \"주문을 처리하고 이메일을 보낸다\"\n├── 변경 이유가 여러 개\n├── 테스트가 어려울 때\n└── 클래스가 500줄 이상\n```\n\n### 주의사항\n\n```\n❌ 과도한 분리\n├── 클래스가 너무 작음\n├── 클래스 수 폭발\n\n✅ 적절한 분리\n├── 응집도 높음\n├── 변경 영향 최소\n```"
            }
        ]
    },

    "02_SOLID/ocp": {
        "title": "개방/폐쇄 원칙 (OCP)",
        "description": "Open/Closed Principle을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "2️⃣ 개방/폐쇄 원칙",
                "content": "## 2️⃣ 한 줄 요약\n> **확장에는 열려있고, 수정에는 닫혀있게** - 기존 코드 안 건드리고 새 기능 추가!\n\n---\n\n## 💡 OCP의 의미\n\n### 개방 (Open): 새로운 기능을 추가할 수 있다\n### 폐쇄 (Closed): 기존 코드를 수정하지 않는다\n\n### 비유:\n```\n🔌 콘센트와 플러그\n\n콘센트 (기존 코드): 수정 없이 그대로\n플러그 (새 기능): 새로운 가전제품 연결 가능\n\n→ 콘센트 규격만 맞추면 뭐든 연결!\n```\n\n---\n\n## 🎯 OCP 위반 사례\n\n```python\n# ❌ OCP 위반: 새 타입마다 코드 수정 필요\nclass DiscountCalculator:\n    def calculate(self, product):\n        if product.type == \"book\":\n            return product.price * 0.1\n        elif product.type == \"electronics\":\n            return product.price * 0.2\n        # 새 타입 추가할 때마다 elif 추가...\n```"
            },
            {
                "type": "code",
                "title": "💻 OCP 적용",
                "content": "### 전략 패턴으로 해결\n\n```python\nfrom abc import ABC, abstractmethod\n\n# 추상 클래스\nclass DiscountPolicy(ABC):\n    @abstractmethod\n    def calculate_discount(self, price: float) -> float:\n        pass\n\n# 구체 클래스들 (확장)\nclass BookDiscount(DiscountPolicy):\n    def calculate_discount(self, price):\n        return price * 0.1\n\nclass ElectronicsDiscount(DiscountPolicy):\n    def calculate_discount(self, price):\n        return price * 0.2\n\n# 새 타입 추가: 기존 코드 수정 없이 새 클래스만 추가!\nclass ClothingDiscount(DiscountPolicy):\n    def calculate_discount(self, price):\n        return price * 0.15\n\n# 사용\nclass Product:\n    def __init__(self, price: float, discount_policy: DiscountPolicy):\n        self.price = price\n        self.discount_policy = discount_policy\n\n    def get_discounted_price(self):\n        discount = self.discount_policy.calculate_discount(self.price)\n        return self.price - discount\n```"
            },
            {
                "type": "tip",
                "title": "💡 OCP 적용 팁",
                "content": "### OCP 적용 패턴\n\n```\n1. 전략 패턴 (Strategy)\n   └── 알고리즘 교체\n\n2. 템플릿 메서드 패턴\n   └── 공통 흐름 + 세부 구현 분리\n\n3. 팩토리 패턴\n   └── 객체 생성 분리\n```\n\n### 적용 시점\n\n```\nOCP 적용하면 좋을 때:\n├── if-else가 계속 늘어날 때\n├── 새 타입 추가가 빈번할 때\n├── 변경 시 여러 곳 수정 필요할 때\n\n과적용 주의:\n├── 변경 가능성 낮은 코드\n├── 단순한 조건문\n├── 타입이 2-3개로 고정\n```"
            }
        ]
    },

    "02_SOLID/lsp": {
        "title": "리스코프 치환 원칙 (LSP)",
        "description": "Liskov Substitution Principle을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "3️⃣ 리스코프 치환 원칙",
                "content": "## 3️⃣ 한 줄 요약\n> **자식은 부모를 대체할 수 있어야 한다** - 부모 타입 자리에 자식을 넣어도 OK!\n\n---\n\n## 💡 LSP의 의미\n\n### 정의:\n```\n\"서브타입은 언제나 자신의 기반 타입으로\n 교체할 수 있어야 한다\"\n```\n\n### 비유:\n```\n🚗 운전 대행 서비스\n\n\"운전할 줄 아는 사람\" 요청\n├── 일반 운전자 → OK\n├── 버스 기사 → OK\n├── 택시 기사 → OK\n└── 면허 없는 사람 → ❌ (대체 불가!)\n```\n\n---\n\n## 🎯 LSP 위반 사례\n\n### 고전적인 예: 직사각형과 정사각형\n\n```python\nclass Rectangle:\n    def set_width(self, width):\n        self._width = width\n\n    def set_height(self, height):\n        self._height = height\n\n# ❌ LSP 위반!\nclass Square(Rectangle):\n    def set_width(self, width):\n        self._width = width\n        self._height = width  # 정사각형이니까!\n\n    def set_height(self, height):\n        self._width = height\n        self._height = height\n\n# Rectangle 대신 Square를 사용하면 예상과 다르게 동작!\n```"
            },
            {
                "type": "code",
                "title": "💻 LSP 올바른 적용",
                "content": "### 상속 대신 구성\n\n```python\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def get_area(self) -> float:\n        pass\n\nclass Rectangle(Shape):\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def get_area(self):\n        return self.width * self.height\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def get_area(self):\n        return self.side * self.side\n\n# 이제 둘 다 Shape로 사용 가능\ndef print_area(shape: Shape):\n    print(f\"Area: {shape.get_area()}\")\n\nprint_area(Rectangle(5, 4))  # Area: 20\nprint_area(Square(5))        # Area: 25\n```"
            },
            {
                "type": "tip",
                "title": "💡 LSP 체크리스트",
                "content": "### LSP 위반 신호\n\n```\n❌ 위반 징후:\n├── 자식 클래스에서 예외 발생\n├── 자식 클래스에서 빈 구현\n├── instanceof / type 체크 필요\n└── 부모 메서드 오버라이드 시 동작 변경\n```\n\n### 설계 가이드\n\n```\n상속 전 질문:\n\"자식이 진짜 부모의 일종인가?\"\n\n├── 정사각형 IS-A 직사각형? → 수학적으론 yes\n│   └── 하지만 동작은 다름!\n├── 펭귄 IS-A 새? → yes\n│   └── 하지만 fly()는 못함!\n\n해결책:\n├── 상속 대신 구성 (Composition)\n├── 인터페이스 분리\n└── 공통 추상 클래스 추출\n```"
            }
        ]
    },

    "02_SOLID/isp": {
        "title": "인터페이스 분리 원칙 (ISP)",
        "description": "Interface Segregation Principle을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "4️⃣ 인터페이스 분리 원칙",
                "content": "## 4️⃣ 한 줄 요약\n> **클라이언트별로 인터페이스 분리** - 사용하지 않는 메서드에 의존하지 마세요!\n\n---\n\n## 💡 ISP의 의미\n\n### 핵심:\n```\n\"자신이 사용하지 않는 인터페이스는\n 구현하지 않아야 한다\"\n\n뚱뚱한 인터페이스 → 날씬한 인터페이스들로!\n```\n\n---\n\n## 🎯 ISP 위반 사례\n\n```python\n# ❌ 뚱뚱한 인터페이스\nclass Worker(ABC):\n    @abstractmethod\n    def work(self): pass\n\n    @abstractmethod\n    def eat(self): pass\n\n    @abstractmethod\n    def sleep(self): pass\n\n# 로봇은 eat(), sleep() 필요 없음!\nclass Robot(Worker):\n    def work(self):\n        print(\"Working...\")\n\n    def eat(self):\n        pass  # 구현할 게 없음\n\n    def sleep(self):\n        pass  # 구현할 게 없음\n```"
            },
            {
                "type": "code",
                "title": "💻 ISP 적용",
                "content": "### 인터페이스 분리\n\n```python\nclass Workable(ABC):\n    @abstractmethod\n    def work(self): pass\n\nclass Eatable(ABC):\n    @abstractmethod\n    def eat(self): pass\n\nclass Sleepable(ABC):\n    @abstractmethod\n    def sleep(self): pass\n\n# 로봇: 필요한 것만 구현\nclass Robot(Workable):\n    def work(self):\n        print(\"Working efficiently...\")\n\n# 인간: 필요한 것 모두 구현\nclass Human(Workable, Eatable, Sleepable):\n    def work(self):\n        print(\"Working...\")\n\n    def eat(self):\n        print(\"Eating...\")\n\n    def sleep(self):\n        print(\"Sleeping...\")\n\n# 사용\ndef do_work(worker: Workable):\n    worker.work()\n\ndo_work(Robot())  # OK\ndo_work(Human())  # OK\n```"
            },
            {
                "type": "tip",
                "title": "💡 ISP 적용 팁",
                "content": "### 분리 기준\n\n```\n인터페이스 분리 시점:\n├── 구현체가 빈 메서드를 가질 때\n├── 클라이언트가 일부만 사용할 때\n├── 변경 시 영향 범위가 너무 클 때\n└── 역할이 명확히 구분될 때\n```\n\n### 인터페이스 크기 가이드\n\n```\n작은 인터페이스 선호:\n├── 3-5개 메서드 권장\n├── 하나의 역할만\n├── 역할별로 분리\n```"
            }
        ]
    },

    "02_SOLID/dip": {
        "title": "의존성 역전 원칙 (DIP)",
        "description": "Dependency Inversion Principle을 이해합니다",
        "sections": [
            {
                "type": "concept",
                "title": "5️⃣ 의존성 역전 원칙",
                "content": "## 5️⃣ 한 줄 요약\n> **추상화에 의존하라** - 구체적인 것이 아닌 추상적인 것에 의존하세요!\n\n---\n\n## 💡 DIP의 의미\n\n### 핵심 규칙:\n```\n1. 고수준 모듈이 저수준 모듈에 의존하면 안 됨\n2. 둘 다 추상화에 의존해야 함\n```\n\n### 비유:\n```\n🔌 USB 포트\n\n❌ DIP 없이:\n컴퓨터 ─── 특정 마우스 (직접 연결)\n└── 마우스 바꾸려면 컴퓨터 수정!\n\n✅ DIP 적용:\n컴퓨터 ─── USB 인터페이스 ─── 마우스, 키보드 등\n└── 인터페이스만 맞으면 뭐든 연결!\n```\n\n---\n\n## 🎯 DIP 위반 사례\n\n```python\n# ❌ 고수준이 저수준에 의존\nclass OrderService:\n    def __init__(self):\n        self.db = MySQLDatabase()  # 구체 클래스에 의존!\n        self.mailer = GmailMailer()  # 구체 클래스에 의존!\n```"
            },
            {
                "type": "code",
                "title": "💻 DIP 적용",
                "content": "### 인터페이스 도입\n\n```python\nfrom abc import ABC, abstractmethod\n\n# 추상화 (인터페이스)\nclass Database(ABC):\n    @abstractmethod\n    def save(self, entity): pass\n\nclass Mailer(ABC):\n    @abstractmethod\n    def send(self, to, message): pass\n\n# 저수준 모듈 (구현체)\nclass MySQLDatabase(Database):\n    def save(self, entity):\n        pass\n\nclass GmailMailer(Mailer):\n    def send(self, to, message):\n        pass\n\n# 고수준 모듈 (비즈니스 로직)\nclass OrderService:\n    def __init__(self, db: Database, mailer: Mailer):  # 추상화에 의존!\n        self.db = db\n        self.mailer = mailer\n\n    def create_order(self, order_data):\n        order = Order(**order_data)\n        self.db.save(order)\n        self.mailer.send(order.email, \"주문 완료\")\n\n# 조립 (의존성 주입)\nservice = OrderService(\n    db=MySQLDatabase(),\n    mailer=GmailMailer()\n)\n\n# 테스트 시 Mock 사용 가능!\ntest_service = OrderService(\n    db=InMemoryDatabase(),\n    mailer=MockMailer()\n)\n```"
            },
            {
                "type": "tip",
                "title": "💡 DIP 실전 팁",
                "content": "### 의존성 주입 방법\n\n```\n1. 생성자 주입 (권장)\n   def __init__(self, db: Database):\n       self.db = db\n\n2. 세터 주입\n   def set_database(self, db: Database):\n       self.db = db\n```\n\n### DIP 적용 기준\n\n```\nDIP 적용하면 좋을 때:\n├── 외부 서비스 연동 (DB, API, 메일)\n├── 테스트 필요한 비즈니스 로직\n├── 변경 가능성 높은 구현체\n\n과적용 주의:\n├── 단순한 유틸리티\n├── 변경 가능성 없는 코드\n```\n\n### 계층 구조\n\n```\n고수준 모듈 (비즈니스 로직)\n     │ 의존\n     ▼\n   추상화 (인터페이스)\n     │ 구현\n     ▼\n저수준 모듈 (MySQL, Gmail 등)\n\n→ 화살표 방향이 \"역전\"됨!\n```"
            }
        ]
    },

    "02_SOLID/solid-example": {
        "title": "SOLID 종합 예제",
        "description": "SOLID 원칙을 종합적으로 적용합니다",
        "sections": [
            {
                "type": "concept",
                "title": "🏗️ SOLID 종합 예제",
                "content": "## 🏗️ 한 줄 요약\n> **5가지 원칙을 함께 적용** - 실제 프로젝트에서 SOLID를 어떻게 쓰는지 봐요!\n\n---\n\n## 💡 시나리오: 결제 시스템\n\n### 요구사항:\n```\n1. 여러 결제 수단 지원 (카드, 카카오페이)\n2. 결제 후 알림 발송\n3. 결제 내역 저장\n4. 할인 정책 적용\n```\n\n### SOLID 관점 분석:\n```\nS (SRP): 결제, 알림, 저장, 할인 분리\nO (OCP): 새 결제 수단 추가 쉽게\nL (LSP): 모든 결제 수단이 동일 인터페이스\nI (ISP): 결제, 환불 인터페이스 분리\nD (DIP): 추상화에 의존하여 테스트 용이\n```"
            },
            {
                "type": "code",
                "title": "💻 종합 구현",
                "content": "### 인터페이스 정의\n\n```python\nfrom abc import ABC, abstractmethod\n\n# 결제 인터페이스\nclass Payable(ABC):\n    @abstractmethod\n    def process(self, amount: float) -> bool:\n        pass\n\n# 알림 인터페이스\nclass Notifier(ABC):\n    @abstractmethod\n    def send(self, recipient: str, message: str) -> bool:\n        pass\n\n# 할인 인터페이스\nclass DiscountPolicy(ABC):\n    @abstractmethod\n    def calculate(self, amount: float) -> float:\n        pass\n```\n\n### 구현체들\n\n```python\n# 결제 수단\nclass CreditCardPayment(Payable):\n    def process(self, amount):\n        print(f\"카드 결제: {amount}원\")\n        return True\n\nclass KakaoPayPayment(Payable):\n    def process(self, amount):\n        print(f\"카카오페이 결제: {amount}원\")\n        return True\n\n# 알림\nclass EmailNotifier(Notifier):\n    def send(self, recipient, message):\n        print(f\"이메일: {recipient} - {message}\")\n        return True\n\n# 할인 정책\nclass PercentageDiscount(DiscountPolicy):\n    def __init__(self, percent: float):\n        self.percent = percent\n\n    def calculate(self, amount):\n        return amount * self.percent\n```\n\n### 서비스 계층\n\n```python\nclass PaymentService:\n    def __init__(self, payment: Payable, notifier: Notifier, discount: DiscountPolicy):\n        self.payment = payment\n        self.notifier = notifier\n        self.discount = discount\n\n    def process_payment(self, amount: float, email: str):\n        discount_amount = self.discount.calculate(amount)\n        final_amount = amount - discount_amount\n        \n        if self.payment.process(final_amount):\n            self.notifier.send(email, f\"결제 완료: {final_amount}원\")\n            return True\n        return False\n\n# 사용\nservice = PaymentService(\n    payment=KakaoPayPayment(),\n    notifier=EmailNotifier(),\n    discount=PercentageDiscount(0.1)\n)\n\nservice.process_payment(10000, \"user@test.com\")\n```"
            },
            {
                "type": "tip",
                "title": "💡 SOLID 적용 정리",
                "content": "### 예제에서 적용된 원칙\n\n```\nS (SRP):\n├── PaymentService: 결제 흐름만\n├── Notifier: 알림만\n└── DiscountPolicy: 할인 계산만\n\nO (OCP):\n├── 새 결제 수단: 새 클래스 추가\n├── 새 알림 방식: 새 클래스 추가\n└── 새 할인 정책: 새 클래스 추가\n\nL (LSP):\n├── 모든 Payable 구현체 교체 가능\n└── 테스트에서 Mock 사용 가능\n\nI (ISP):\n├── Payable: 결제만\n├── Notifier: 알림만\n└── 필요한 인터페이스만 구현\n\nD (DIP):\n├── 추상화에 의존\n├── 생성자 주입\n└── 테스트 용이\n```\n\n### 점진적 적용\n\n```\n1단계: 동작하는 코드 작성\n2단계: 테스트 필요한 부분 DIP 적용\n3단계: 중복 발견 시 OCP 적용\n4단계: 클래스 비대 시 SRP 적용\n\n→ 한 번에 완벽하게 X\n→ 필요할 때 점진적으로 O\n```"
            }
        ]
    }
}

def update_cleancode_json():
    sys.stdout.reconfigure(encoding='utf-8')

    with open(CLEANCODE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for key, content in SOLID_CONTENTS.items():
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

    print(f"\n[DONE] SOLID section updated: {updated_count} topics")

if __name__ == "__main__":
    update_cleancode_json()
