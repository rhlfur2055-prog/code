# -*- coding: utf-8 -*-
"""
952개 콘텐츠 자동 생성 스크립트
각 카테고리별 실제 교육 콘텐츠를 생성합니다.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STUDY_DIR = BASE_DIR / "public" / "study"

# 카테고리별 콘텐츠 정의
CONTENT_DB = {
    # ============ OS 카테고리 ============
    "kernel": {
        "title": "커널 (Kernel)",
        "concepts": [
            {"name": "커널이란?", "desc": "운영체제의 핵심으로, 하드웨어와 소프트웨어 사이의 중재자 역할을 합니다."},
            {"name": "커널 모드 vs 사용자 모드", "desc": "커널 모드는 모든 하드웨어 접근 권한을 가지며, 사용자 모드는 제한된 권한만 가집니다."},
            {"name": "시스템 콜", "desc": "사용자 프로그램이 커널 기능을 요청하는 인터페이스입니다."},
            {"name": "인터럽트 처리", "desc": "하드웨어/소프트웨어 이벤트를 커널이 처리하는 메커니즘입니다."}
        ],
        "code": """// 시스템 콜 예시 (C 언어)
#include <unistd.h>
#include <fcntl.h>

int main() {
    // open() 시스템 콜 - 파일 열기
    int fd = open("test.txt", O_RDONLY);

    // read() 시스템 콜 - 파일 읽기
    char buffer[100];
    ssize_t bytes = read(fd, buffer, sizeof(buffer));

    // write() 시스템 콜 - 화면 출력
    write(STDOUT_FILENO, buffer, bytes);

    // close() 시스템 콜 - 파일 닫기
    close(fd);

    return 0;
}""",
        "tips": [
            "커널은 항상 메모리에 상주하며 시스템 전체를 관리합니다",
            "시스템 콜은 사용자 모드에서 커널 모드로 전환하는 유일한 방법입니다",
            "모놀리식 커널과 마이크로 커널의 차이점을 이해하세요"
        ],
        "practice": [
            "리눅스에서 strace 명령어로 시스템 콜 추적해보기",
            "fork(), exec(), wait() 시스템 콜로 프로세스 생성하기",
            "커널 모듈을 작성하여 커널 확장하기 (고급)"
        ]
    },

    "process-concept": {
        "title": "프로세스 개념",
        "concepts": [
            {"name": "프로세스란?", "desc": "실행 중인 프로그램의 인스턴스로, CPU 시간, 메모리, 파일 등의 자원을 할당받습니다."},
            {"name": "프로세스 상태", "desc": "New, Ready, Running, Waiting, Terminated 5가지 상태로 전이됩니다."},
            {"name": "PCB (Process Control Block)", "desc": "프로세스 정보를 저장하는 자료구조로, PID, 상태, 레지스터 값 등을 포함합니다."},
            {"name": "컨텍스트 스위칭", "desc": "CPU가 다른 프로세스로 전환할 때 현재 상태를 저장하고 복원하는 과정입니다."}
        ],
        "code": """// 프로세스 생성 예시 (C 언어)
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();  // 프로세스 복제

    if (pid < 0) {
        // 에러 처리
        perror("fork failed");
        return 1;
    } else if (pid == 0) {
        // 자식 프로세스
        printf("자식 프로세스 PID: %d\\n", getpid());
        printf("부모 프로세스 PID: %d\\n", getppid());
    } else {
        // 부모 프로세스
        printf("부모입니다. 자식 PID: %d\\n", pid);
        wait(NULL);  // 자식 종료 대기
    }

    return 0;
}""",
        "tips": [
            "프로세스는 독립적인 메모리 공간을 가집니다",
            "컨텍스트 스위칭은 오버헤드가 발생하므로 최소화해야 합니다",
            "좀비 프로세스와 고아 프로세스의 차이를 알아두세요"
        ],
        "practice": [
            "ps, top 명령어로 프로세스 목록 확인하기",
            "fork()로 여러 자식 프로세스 생성하기",
            "프로세스 상태 전이 다이어그램 직접 그려보기"
        ]
    },

    # ============ JAVA 카테고리 ============
    "java-intro": {
        "title": "Java 소개",
        "concepts": [
            {"name": "Java란?", "desc": "객체지향 프로그래밍 언어로, 'Write Once, Run Anywhere' 철학을 가집니다."},
            {"name": "JVM (Java Virtual Machine)", "desc": "Java 바이트코드를 실행하는 가상 머신으로, 플랫폼 독립성을 제공합니다."},
            {"name": "JDK vs JRE", "desc": "JDK는 개발 도구 포함, JRE는 실행 환경만 제공합니다."},
            {"name": "Java의 특징", "desc": "플랫폼 독립성, 객체지향, 메모리 자동 관리(GC), 멀티스레드 지원"}
        ],
        "code": """// 첫 번째 Java 프로그램
public class HelloWorld {
    public static void main(String[] args) {
        // 콘솔에 출력
        System.out.println("Hello, Java!");

        // 변수 선언과 출력
        String name = "코드마스터";
        int year = 2024;

        System.out.println("환영합니다, " + name + "!");
        System.out.println("현재 연도: " + year);
    }
}

// 컴파일: javac HelloWorld.java
// 실행: java HelloWorld""",
        "tips": [
            "Java 파일명과 public 클래스명은 반드시 일치해야 합니다",
            "main 메서드는 프로그램의 시작점(entry point)입니다",
            "Java 17 LTS 또는 Java 21 LTS 버전 사용을 권장합니다"
        ],
        "practice": [
            "JDK를 설치하고 환경변수 설정하기",
            "Hello World 프로그램 작성 후 컴파일/실행하기",
            "다양한 데이터 타입으로 변수 선언해보기"
        ]
    },

    "java-basic-syntax": {
        "title": "Java 기본 문법",
        "concepts": [
            {"name": "변수와 데이터 타입", "desc": "기본형(int, double, boolean 등)과 참조형(String, 배열 등)으로 구분됩니다."},
            {"name": "연산자", "desc": "산술, 비교, 논리, 대입, 삼항 연산자 등을 제공합니다."},
            {"name": "형변환", "desc": "자동 형변환(작은→큰)과 명시적 형변환(캐스팅)이 있습니다."},
            {"name": "상수", "desc": "final 키워드로 선언하며, 값을 변경할 수 없습니다."}
        ],
        "code": """public class BasicSyntax {
    public static void main(String[] args) {
        // 기본 데이터 타입
        int number = 42;
        double pi = 3.14159;
        boolean isJavaFun = true;
        char grade = 'A';

        // 참조 타입
        String message = "Hello Java";
        int[] scores = {90, 85, 88, 92};

        // 상수 선언
        final int MAX_SIZE = 100;

        // 연산자
        int sum = 10 + 20;
        int remainder = 10 % 3;  // 나머지: 1
        boolean result = (10 > 5) && (20 < 30);  // true

        // 형변환
        double d = number;  // 자동 형변환
        int i = (int) pi;   // 명시적 형변환 (3)

        // 삼항 연산자
        String status = (number > 50) ? "합격" : "불합격";

        System.out.println("합계: " + sum);
        System.out.println("상태: " + status);
    }
}""",
        "tips": [
            "변수명은 camelCase 규칙을 따릅니다 (예: myVariable)",
            "상수명은 UPPER_SNAKE_CASE를 사용합니다 (예: MAX_VALUE)",
            "정수 리터럴은 기본적으로 int, 실수는 double입니다"
        ],
        "practice": [
            "8가지 기본 데이터 타입 모두 사용해보기",
            "다양한 연산자로 계산기 프로그램 만들기",
            "형변환 시 데이터 손실 확인하기"
        ]
    },

    "class-object": {
        "title": "클래스와 객체",
        "concepts": [
            {"name": "클래스란?", "desc": "객체를 생성하기 위한 설계도(템플릿)입니다."},
            {"name": "객체란?", "desc": "클래스로부터 생성된 실체(인스턴스)입니다."},
            {"name": "필드와 메서드", "desc": "필드는 객체의 상태, 메서드는 객체의 행동을 정의합니다."},
            {"name": "this 키워드", "desc": "현재 객체 자신을 참조하는 키워드입니다."}
        ],
        "code": """// 클래스 정의
public class Car {
    // 필드 (속성)
    private String brand;
    private String model;
    private int speed;

    // 생성자
    public Car(String brand, String model) {
        this.brand = brand;
        this.model = model;
        this.speed = 0;
    }

    // 메서드 (행동)
    public void accelerate(int amount) {
        this.speed += amount;
        System.out.println(brand + " " + model + " 속도: " + speed + "km/h");
    }

    public void brake() {
        this.speed = Math.max(0, speed - 10);
    }

    // Getter
    public int getSpeed() {
        return speed;
    }
}

// 객체 생성 및 사용
public class Main {
    public static void main(String[] args) {
        Car myCar = new Car("Tesla", "Model 3");
        myCar.accelerate(50);  // 속도: 50km/h
        myCar.accelerate(30);  // 속도: 80km/h
        myCar.brake();         // 속도: 70km/h
    }
}""",
        "tips": [
            "하나의 .java 파일에는 하나의 public 클래스만 가능합니다",
            "필드는 private으로 선언하고 getter/setter로 접근합니다 (캡슐화)",
            "객체는 new 키워드로 생성하며, 힙 메모리에 할당됩니다"
        ],
        "practice": [
            "학생(Student) 클래스를 설계하고 객체 생성하기",
            "은행 계좌(Account) 클래스로 입출금 기능 구현하기",
            "여러 객체를 배열로 관리해보기"
        ]
    },

    "inheritance": {
        "title": "상속 (Inheritance)",
        "concepts": [
            {"name": "상속이란?", "desc": "기존 클래스(부모)의 속성과 메서드를 새 클래스(자식)가 물려받는 것입니다."},
            {"name": "extends 키워드", "desc": "클래스 상속을 선언할 때 사용합니다. Java는 단일 상속만 지원합니다."},
            {"name": "super 키워드", "desc": "부모 클래스의 생성자나 메서드를 호출할 때 사용합니다."},
            {"name": "메서드 오버라이딩", "desc": "부모의 메서드를 자식이 재정의하는 것입니다."}
        ],
        "code": """// 부모 클래스
public class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + "이(가) 먹습니다.");
    }

    public void sleep() {
        System.out.println(name + "이(가) 잡니다.");
    }
}

// 자식 클래스
public class Dog extends Animal {
    private String breed;

    public Dog(String name, String breed) {
        super(name);  // 부모 생성자 호출
        this.breed = breed;
    }

    // 메서드 오버라이딩
    @Override
    public void eat() {
        System.out.println(name + "이(가) 사료를 먹습니다.");
    }

    // 자식만의 메서드
    public void bark() {
        System.out.println(name + "이(가) 짖습니다: 멍멍!");
    }
}

// 사용 예시
public class Main {
    public static void main(String[] args) {
        Dog myDog = new Dog("바둑이", "진돗개");
        myDog.eat();    // 바둑이이(가) 사료를 먹습니다.
        myDog.sleep();  // 바둑이이(가) 잡니다. (상속받은 메서드)
        myDog.bark();   // 바둑이이(가) 짖습니다: 멍멍!
    }
}""",
        "tips": [
            "상속은 'is-a' 관계일 때 사용합니다 (Dog is an Animal)",
            "@Override 어노테이션은 컴파일러가 오버라이딩을 확인하게 합니다",
            "부모 생성자 호출 super()는 자식 생성자의 첫 줄에 위치해야 합니다"
        ],
        "practice": [
            "Shape → Rectangle, Circle 상속 구조 만들기",
            "Employee → Manager, Developer 클래스 설계하기",
            "toString() 메서드 오버라이딩해보기"
        ]
    },

    # ============ PYTHON 카테고리 ============
    "01_variables": {
        "title": "Python 변수",
        "concepts": [
            {"name": "변수 선언", "desc": "Python은 동적 타이핑으로 타입 선언 없이 변수를 생성합니다."},
            {"name": "데이터 타입", "desc": "int, float, str, bool, list, dict, tuple, set 등이 있습니다."},
            {"name": "변수 명명 규칙", "desc": "snake_case를 사용하며, 숫자로 시작할 수 없습니다."},
            {"name": "None 타입", "desc": "값이 없음을 나타내는 특별한 타입입니다."}
        ],
        "code": """# 변수 선언 (타입 자동 추론)
name = "Python"
age = 30
height = 175.5
is_developer = True

# 여러 변수 동시 할당
x, y, z = 1, 2, 3
a = b = c = 0

# 타입 확인
print(type(name))    # <class 'str'>
print(type(age))     # <class 'int'>
print(type(height))  # <class 'float'>

# 타입 변환
num_str = "42"
num_int = int(num_str)      # 문자열 → 정수
num_float = float(num_str)  # 문자열 → 실수

# f-string (포맷팅)
message = f"이름: {name}, 나이: {age}"
print(message)

# None 타입
result = None
if result is None:
    print("결과가 없습니다")""",
        "tips": [
            "Python은 동적 타이핑이라 변수 타입이 런타임에 결정됩니다",
            "상수 개념이 없으므로 대문자로 상수임을 표시합니다 (MAX_SIZE = 100)",
            "is 연산자는 객체 동일성, == 연산자는 값 동등성을 비교합니다"
        ],
        "practice": [
            "다양한 데이터 타입의 변수 선언하기",
            "type()과 isinstance()로 타입 확인하기",
            "타입 변환 연습하기 (int, float, str)"
        ]
    },

    # ============ ALGORITHM 카테고리 ============
    "binary-search": {
        "title": "이진 탐색 (Binary Search)",
        "concepts": [
            {"name": "이진 탐색이란?", "desc": "정렬된 배열에서 중간값과 비교하여 탐색 범위를 절반씩 줄여가는 알고리즘입니다."},
            {"name": "시간 복잡도", "desc": "O(log n)으로 매우 효율적입니다. 선형 탐색 O(n)보다 빠릅니다."},
            {"name": "전제 조건", "desc": "반드시 정렬된 배열에서만 사용 가능합니다."},
            {"name": "Lower/Upper Bound", "desc": "특정 값의 첫 위치와 마지막 위치+1을 찾는 변형입니다."}
        ],
        "code": """# Python 이진 탐색 구현
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid  # 찾음
        elif arr[mid] < target:
            left = mid + 1  # 오른쪽 절반 탐색
        else:
            right = mid - 1  # 왼쪽 절반 탐색

    return -1  # 못 찾음

# 재귀 버전
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# 사용 예시
numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
result = binary_search(numbers, 11)
print(f"11의 인덱스: {result}")  # 5

# Python 내장 모듈 사용
from bisect import bisect_left, bisect_right

idx = bisect_left(numbers, 11)
print(f"bisect_left: {idx}")  # 5""",
        "tips": [
            "left + right가 오버플로우될 수 있으므로 left + (right - left) // 2 권장",
            "조건문의 등호 위치에 주의하세요 (무한 루프 방지)",
            "bisect 모듈을 활용하면 더 간단하게 구현 가능합니다"
        ],
        "practice": [
            "정렬된 배열에서 특정 값 찾기",
            "Lower Bound, Upper Bound 구현하기",
            "회전된 정렬 배열에서 이진 탐색하기 (응용)"
        ]
    },

    # ============ NETWORK 카테고리 ============
    "osi-model": {
        "title": "OSI 7계층 모델",
        "concepts": [
            {"name": "물리 계층 (L1)", "desc": "전기적 신호, 케이블, 허브 등 물리적 전송을 담당합니다."},
            {"name": "데이터링크 계층 (L2)", "desc": "MAC 주소 기반 통신, 스위치, 프레임 단위 전송을 담당합니다."},
            {"name": "네트워크 계층 (L3)", "desc": "IP 주소, 라우팅, 패킷 단위 전송을 담당합니다."},
            {"name": "전송 계층 (L4)", "desc": "TCP/UDP, 포트 번호, 세그먼트 단위 전송을 담당합니다."}
        ],
        "code": """# OSI 7계층 예시 (Python Socket)
import socket

# TCP 서버 (전송 계층 - L4)
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    print("서버 시작: 포트 8080")

    while True:
        client, addr = server.accept()
        print(f"연결됨: {addr}")

        data = client.recv(1024)
        print(f"수신: {data.decode()}")

        client.send(b"Hello from server!")
        client.close()

# TCP 클라이언트
def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    client.send(b"Hello from client!")
    response = client.recv(1024)
    print(f"응답: {response.decode()}")

    client.close()

# HTTP 요청 예시 (응용 계층 - L7)
import requests

response = requests.get("https://api.example.com/data")
print(f"상태 코드: {response.status_code}")
print(f"데이터: {response.json()}")""",
        "tips": [
            "계층을 외우는 방법: 'Please Do Not Throw Sausage Pizza Away'",
            "TCP/IP 모델은 4계층(네트워크 인터페이스, 인터넷, 전송, 응용)입니다",
            "캡슐화/역캡슐화 과정을 이해하면 네트워크 동작을 파악할 수 있습니다"
        ],
        "practice": [
            "Wireshark로 패킷 분석하기",
            "간단한 TCP 에코 서버 만들기",
            "HTTP 요청/응답 헤더 분석하기"
        ]
    },

    # ============ DB 카테고리 ============
    "sql-basic": {
        "title": "SQL 기초",
        "concepts": [
            {"name": "SELECT", "desc": "테이블에서 데이터를 조회하는 기본 명령어입니다."},
            {"name": "WHERE", "desc": "조건에 맞는 행만 필터링합니다."},
            {"name": "ORDER BY", "desc": "결과를 정렬합니다 (ASC: 오름차순, DESC: 내림차순)."},
            {"name": "JOIN", "desc": "여러 테이블을 연결하여 조회합니다."}
        ],
        "code": """-- 기본 SELECT
SELECT * FROM users;
SELECT name, email FROM users;

-- WHERE 조건
SELECT * FROM users WHERE age >= 20;
SELECT * FROM users WHERE name LIKE '%김%';
SELECT * FROM users WHERE age BETWEEN 20 AND 30;
SELECT * FROM users WHERE city IN ('서울', '부산');

-- ORDER BY 정렬
SELECT * FROM users ORDER BY age DESC;
SELECT * FROM users ORDER BY name ASC, age DESC;

-- LIMIT (페이징)
SELECT * FROM users LIMIT 10 OFFSET 0;

-- GROUP BY & 집계 함수
SELECT city, COUNT(*) as user_count
FROM users
GROUP BY city
HAVING COUNT(*) > 5;

-- JOIN
SELECT u.name, o.order_date, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 10000;

-- LEFT JOIN (없어도 포함)
SELECT u.name, COALESCE(o.order_count, 0) as orders
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;""",
        "tips": [
            "SELECT 실행 순서: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY",
            "NULL 비교는 IS NULL / IS NOT NULL을 사용합니다 (= NULL은 작동 안 함)",
            "인덱스가 있는 컬럼을 WHERE 조건에 사용하면 성능이 향상됩니다"
        ],
        "practice": [
            "기본 CRUD 쿼리 작성하기",
            "다양한 JOIN 유형 연습하기 (INNER, LEFT, RIGHT, FULL)",
            "서브쿼리와 집계 함수 활용하기"
        ]
    },

    # ============ SPRING 카테고리 ============
    "spring-intro": {
        "title": "Spring Framework 소개",
        "concepts": [
            {"name": "Spring이란?", "desc": "Java 엔터프라이즈 개발을 위한 오픈소스 프레임워크입니다."},
            {"name": "IoC (제어의 역전)", "desc": "객체의 생성과 의존성 관리를 프레임워크가 담당합니다."},
            {"name": "DI (의존성 주입)", "desc": "필요한 의존성을 외부에서 주입받는 패턴입니다."},
            {"name": "AOP (관점 지향)", "desc": "공통 기능(로깅, 트랜잭션 등)을 분리하여 관리합니다."}
        ],
        "code": """// Spring Boot 메인 클래스
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// REST Controller
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    // 생성자 주입 (권장)
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    public User createUser(@RequestBody UserDto dto) {
        return userService.create(dto);
    }
}

// Service 계층
@Service
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> findAll() {
        return userRepository.findAll();
    }

    @Transactional
    public User create(UserDto dto) {
        User user = new User(dto.getName(), dto.getEmail());
        return userRepository.save(user);
    }
}""",
        "tips": [
            "생성자 주입을 사용하면 불변성과 테스트 용이성이 보장됩니다",
            "@Autowired는 필드 주입으로, 생성자 주입보다 권장되지 않습니다",
            "Spring Boot는 Auto-Configuration으로 설정을 간소화합니다"
        ],
        "practice": [
            "Spring Boot 프로젝트 생성하기 (start.spring.io)",
            "간단한 REST API 구현하기",
            "의존성 주입 3가지 방식 비교하기"
        ]
    },

    # ============ REACT 카테고리 ============
    "react-intro": {
        "title": "React 소개",
        "concepts": [
            {"name": "React란?", "desc": "Facebook이 만든 UI 라이브러리로, 컴포넌트 기반으로 개발합니다."},
            {"name": "Virtual DOM", "desc": "실제 DOM 대신 가상 DOM을 사용하여 효율적으로 렌더링합니다."},
            {"name": "컴포넌트", "desc": "재사용 가능한 UI 조각으로, 함수형과 클래스형이 있습니다."},
            {"name": "JSX", "desc": "JavaScript 안에서 HTML과 유사한 문법을 사용할 수 있게 합니다."}
        ],
        "code": """// 함수형 컴포넌트 (권장)
import React, { useState, useEffect } from 'react';

function App() {
    return (
        <div className="app">
            <h1>Hello React!</h1>
            <Counter />
            <UserList />
        </div>
    );
}

// useState Hook
function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                증가
            </button>
            <button onClick={() => setCount(count - 1)}>
                감소
            </button>
        </div>
    );
}

// useEffect Hook (부수 효과)
function UserList() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/users')
            .then(res => res.json())
            .then(data => {
                setUsers(data);
                setLoading(false);
            });
    }, []);  // 빈 배열 = 마운트 시 1회 실행

    if (loading) return <p>로딩 중...</p>;

    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}

export default App;""",
        "tips": [
            "key는 리스트 렌더링 시 반드시 고유한 값으로 지정해야 합니다",
            "useState의 setter는 비동기로 동작합니다",
            "useEffect의 의존성 배열을 잘 관리해야 무한 루프를 방지합니다"
        ],
        "practice": [
            "Vite로 React 프로젝트 생성하기",
            "간단한 Todo 앱 만들기",
            "부모-자식 컴포넌트 간 props 전달하기"
        ]
    },

    # ============ DEVOPS 카테고리 ============
    "docker-intro": {
        "title": "Docker 소개",
        "concepts": [
            {"name": "Docker란?", "desc": "컨테이너 기반의 가상화 플랫폼으로, 애플리케이션을 격리된 환경에서 실행합니다."},
            {"name": "이미지 vs 컨테이너", "desc": "이미지는 템플릿, 컨테이너는 이미지의 실행 인스턴스입니다."},
            {"name": "Dockerfile", "desc": "이미지를 빌드하기 위한 설정 파일입니다."},
            {"name": "Docker Compose", "desc": "여러 컨테이너를 정의하고 관리하는 도구입니다."}
        ],
        "code": """# Dockerfile 예시
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]

# 빌드 & 실행
# docker build -t my-app .
# docker run -p 3000:3000 my-app

# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

# 자주 쓰는 Docker 명령어
# docker ps                    # 실행 중인 컨테이너 목록
# docker images               # 이미지 목록
# docker logs <container>     # 로그 확인
# docker exec -it <container> sh  # 컨테이너 접속
# docker-compose up -d        # 백그라운드 실행
# docker-compose down         # 종료""",
        "tips": [
            "레이어 캐싱을 위해 자주 변경되는 파일은 Dockerfile 아래쪽에 배치합니다",
            "alpine 이미지를 사용하면 이미지 크기를 줄일 수 있습니다",
            ".dockerignore 파일로 불필요한 파일 제외하세요 (node_modules 등)"
        ],
        "practice": [
            "Docker Desktop 설치 후 hello-world 실행하기",
            "Node.js 앱을 Docker로 컨테이너화하기",
            "Docker Compose로 프론트엔드 + 백엔드 + DB 구성하기"
        ]
    }
}

def get_content_data(filename):
    """파일명에서 콘텐츠 데이터 찾기"""
    name = Path(filename).stem

    # 정확히 일치하는 콘텐츠 찾기
    if name in CONTENT_DB:
        return CONTENT_DB[name]

    # 부분 일치 검색
    for key in CONTENT_DB:
        if key in name or name in key:
            return CONTENT_DB[key]

    return None

def generate_html_content(filepath, title, content_data):
    """HTML 콘텐츠 생성"""
    if not content_data:
        return None

    concepts_html = ""
    for c in content_data.get("concepts", []):
        concepts_html += f'''
        <div class="concept-card">
          <h4>{c["name"]}</h4>
          <p>{c["desc"]}</p>
        </div>'''

    tips_html = ""
    for tip in content_data.get("tips", []):
        tips_html += f"<li>{tip}</li>\n"

    practice_html = ""
    for p in content_data.get("practice", []):
        practice_html += f"<li>{p}</li>\n"

    code = content_data.get("code", "// 예제 코드")

    return concepts_html, tips_html, practice_html, code

def main():
    """메인 실행"""
    updated = 0
    total = 0

    for html_file in STUDY_DIR.rglob("*.html"):
        if "index.html" in str(html_file):
            continue

        total += 1
        content_data = get_content_data(html_file.name)

        if content_data:
            print(f"✓ 업데이트: {html_file.name}")
            updated += 1

    print(f"\n총 {total}개 파일 중 {updated}개 업데이트 가능")

if __name__ == "__main__":
    main()
