# -*- coding: utf-8 -*-
"""952개 콘텐츠 자동 생성 스크립트"""
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STUDY_DIR = BASE_DIR / "public" / "study"

# 카테고리별 콘텐츠 템플릿
CONTENT_TEMPLATES = {
    "java": {
        "java-intro": ("Java 소개", "Java는 객체지향 프로그래밍 언어로, 'Write Once, Run Anywhere' 철학을 가집니다.", """public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");

        // 변수 선언
        String name = "코드마스터";
        int year = 2024;

        System.out.println("환영합니다, " + name + "!");
    }
}"""),
        "java-basic-syntax": ("Java 기본 문법", "변수, 데이터 타입, 연산자 등 Java의 기본 문법을 학습합니다.", """public class BasicSyntax {
    public static void main(String[] args) {
        // 기본 데이터 타입
        int number = 42;
        double pi = 3.14159;
        boolean isTrue = true;
        char grade = 'A';

        // 참조 타입
        String message = "Hello";
        int[] scores = {90, 85, 88};

        // 연산자
        int sum = 10 + 20;
        boolean result = (10 > 5) && (20 < 30);

        System.out.println("합계: " + sum);
    }
}"""),
        "java-condition": ("조건문", "if-else, switch 등 조건문을 활용한 프로그램 흐름 제어를 학습합니다.", """public class Condition {
    public static void main(String[] args) {
        int score = 85;

        // if-else 문
        if (score >= 90) {
            System.out.println("A등급");
        } else if (score >= 80) {
            System.out.println("B등급");
        } else {
            System.out.println("C등급");
        }

        // switch 문
        String day = "월요일";
        switch (day) {
            case "월요일" -> System.out.println("한 주의 시작!");
            case "금요일" -> System.out.println("불금!");
            default -> System.out.println("평범한 하루");
        }
    }
}"""),
        "java-loop": ("반복문", "for, while, do-while 등 반복문을 활용한 반복 처리를 학습합니다.", """public class Loop {
    public static void main(String[] args) {
        // for 문
        for (int i = 1; i <= 5; i++) {
            System.out.println("반복: " + i);
        }

        // 향상된 for 문
        int[] numbers = {1, 2, 3, 4, 5};
        for (int num : numbers) {
            System.out.println("숫자: " + num);
        }

        // while 문
        int count = 0;
        while (count < 3) {
            System.out.println("카운트: " + count);
            count++;
        }
    }
}"""),
        "java-array": ("배열", "Java 배열의 선언, 초기화, 활용 방법을 학습합니다.", """public class ArrayExample {
    public static void main(String[] args) {
        // 배열 선언 및 초기화
        int[] scores = new int[5];
        scores[0] = 90;
        scores[1] = 85;

        // 리터럴 초기화
        String[] names = {"김철수", "이영희", "박민수"};

        // 배열 순회
        for (int i = 0; i < names.length; i++) {
            System.out.println(names[i]);
        }

        // 2차원 배열
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6}
        };
    }
}"""),
        "java-method": ("메서드", "메서드의 정의, 호출, 매개변수, 반환값을 학습합니다.", """public class MethodExample {
    public static void main(String[] args) {
        // 메서드 호출
        greet("코드마스터");

        int result = add(10, 20);
        System.out.println("합계: " + result);

        int max = findMax(5, 3, 8, 1, 9);
        System.out.println("최대값: " + max);
    }

    // 반환값 없는 메서드
    static void greet(String name) {
        System.out.println("안녕하세요, " + name + "님!");
    }

    // 반환값 있는 메서드
    static int add(int a, int b) {
        return a + b;
    }

    // 가변 인자
    static int findMax(int... numbers) {
        int max = numbers[0];
        for (int num : numbers) {
            if (num > max) max = num;
        }
        return max;
    }
}"""),
        "class-object": ("클래스와 객체", "객체지향의 핵심인 클래스와 객체의 개념을 학습합니다.", """// 클래스 정의
public class Car {
    // 필드 (속성)
    private String brand;
    private int speed;

    // 생성자
    public Car(String brand) {
        this.brand = brand;
        this.speed = 0;
    }

    // 메서드 (행동)
    public void accelerate(int amount) {
        this.speed += amount;
        System.out.println(brand + " 속도: " + speed + "km/h");
    }

    public void brake() {
        this.speed = Math.max(0, speed - 10);
    }
}

// 객체 생성
Car myCar = new Car("Tesla");
myCar.accelerate(50);  // Tesla 속도: 50km/h"""),
        "inheritance": ("상속", "클래스 상속을 통한 코드 재사용과 다형성을 학습합니다.", """// 부모 클래스
public class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + "이(가) 먹습니다.");
    }
}

// 자식 클래스
public class Dog extends Animal {
    public Dog(String name) {
        super(name);  // 부모 생성자 호출
    }

    @Override
    public void eat() {
        System.out.println(name + "이(가) 사료를 먹습니다.");
    }

    public void bark() {
        System.out.println("멍멍!");
    }
}"""),
        "interface": ("인터페이스", "인터페이스를 통한 다형성과 느슨한 결합을 학습합니다.", """// 인터페이스 정의
public interface Flyable {
    void fly();  // 추상 메서드

    default void land() {  // 디폴트 메서드
        System.out.println("착륙합니다.");
    }
}

// 인터페이스 구현
public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("새가 날아갑니다!");
    }
}

public class Airplane implements Flyable {
    @Override
    public void fly() {
        System.out.println("비행기가 이륙합니다!");
    }
}"""),
        "polymorphism": ("다형성", "하나의 타입으로 여러 형태의 객체를 다루는 다형성을 학습합니다.", """public class PolymorphismExample {
    public static void main(String[] args) {
        // 다형성: 부모 타입으로 자식 객체 참조
        Animal dog = new Dog("바둑이");
        Animal cat = new Cat("나비");

        // 동적 바인딩
        dog.speak();  // 멍멍!
        cat.speak();  // 야옹!

        // 배열로 다형성 활용
        Animal[] animals = {new Dog("멍멍이"), new Cat("고양이")};
        for (Animal animal : animals) {
            animal.speak();
        }
    }
}

class Animal {
    void speak() { System.out.println("동물 소리"); }
}
class Dog extends Animal {
    @Override void speak() { System.out.println("멍멍!"); }
}
class Cat extends Animal {
    @Override void speak() { System.out.println("야옹!"); }
}"""),
        "exception": ("예외 처리", "try-catch를 통한 예외 처리와 커스텀 예외를 학습합니다.", """public class ExceptionExample {
    public static void main(String[] args) {
        // try-catch-finally
        try {
            int result = divide(10, 0);
            System.out.println("결과: " + result);
        } catch (ArithmeticException e) {
            System.out.println("0으로 나눌 수 없습니다!");
        } finally {
            System.out.println("항상 실행됩니다.");
        }

        // 다중 catch
        try {
            String str = null;
            System.out.println(str.length());
        } catch (NullPointerException e) {
            System.out.println("null 참조 오류!");
        } catch (Exception e) {
            System.out.println("기타 오류: " + e.getMessage());
        }
    }

    static int divide(int a, int b) throws ArithmeticException {
        return a / b;
    }
}"""),
        "collection": ("컬렉션", "List, Set, Map 등 Java 컬렉션 프레임워크를 학습합니다.", """import java.util.*;

public class CollectionExample {
    public static void main(String[] args) {
        // List - 순서 있음, 중복 허용
        List<String> list = new ArrayList<>();
        list.add("Apple");
        list.add("Banana");
        list.add("Apple");  // 중복 가능

        // Set - 순서 없음, 중복 불가
        Set<String> set = new HashSet<>();
        set.add("Apple");
        set.add("Banana");
        set.add("Apple");  // 무시됨

        // Map - 키-값 쌍
        Map<String, Integer> map = new HashMap<>();
        map.put("Apple", 1000);
        map.put("Banana", 2000);

        // 순회
        for (String item : list) {
            System.out.println(item);
        }

        map.forEach((k, v) -> System.out.println(k + ": " + v));
    }
}"""),
        "stream": ("스트림 API", "Java 8 스트림을 활용한 함수형 데이터 처리를 학습합니다.", """import java.util.*;
import java.util.stream.*;

public class StreamExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // filter + map + collect
        List<Integer> evenDoubled = numbers.stream()
            .filter(n -> n % 2 == 0)     // 짝수만
            .map(n -> n * 2)              // 2배
            .collect(Collectors.toList());

        // reduce
        int sum = numbers.stream()
            .reduce(0, Integer::sum);

        // 정렬 및 제한
        numbers.stream()
            .sorted(Comparator.reverseOrder())
            .limit(3)
            .forEach(System.out::println);

        // 문자열 처리
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
        String result = names.stream()
            .filter(s -> s.length() > 3)
            .map(String::toUpperCase)
            .collect(Collectors.joining(", "));
    }
}"""),
        "lambda": ("람다 표현식", "함수형 프로그래밍의 핵심인 람다 표현식을 학습합니다.", """import java.util.function.*;

public class LambdaExample {
    public static void main(String[] args) {
        // 기본 람다
        Runnable task = () -> System.out.println("Hello Lambda!");
        task.run();

        // 매개변수가 있는 람다
        Consumer<String> printer = msg -> System.out.println(msg);
        printer.accept("코드마스터");

        // 반환값이 있는 람다
        Function<Integer, Integer> square = x -> x * x;
        System.out.println(square.apply(5));  // 25

        // Predicate
        Predicate<Integer> isPositive = n -> n > 0;
        System.out.println(isPositive.test(10));  // true

        // BiFunction
        BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
        System.out.println(add.apply(3, 4));  // 7

        // 메서드 참조
        List<String> names = Arrays.asList("Alice", "Bob");
        names.forEach(System.out::println);
    }
}"""),
        "thread": ("멀티스레딩", "Java에서 멀티스레드 프로그래밍을 학습합니다.", """public class ThreadExample {
    public static void main(String[] args) {
        // 방법 1: Thread 클래스 상속
        Thread t1 = new MyThread();
        t1.start();

        // 방법 2: Runnable 구현
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 2: " + i);
                try { Thread.sleep(100); } catch (Exception e) {}
            }
        });
        t2.start();

        // ExecutorService
        ExecutorService executor = Executors.newFixedThreadPool(2);
        executor.submit(() -> System.out.println("Task 1"));
        executor.submit(() -> System.out.println("Task 2"));
        executor.shutdown();
    }
}

class MyThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Thread 1: " + i);
        }
    }
}"""),
    },
    "python": {
        "01_variables": ("Python 변수", "Python의 동적 타이핑과 변수 선언을 학습합니다.", """# 변수 선언 (타입 자동 추론)
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

# 타입 변환
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)

# f-string (포맷팅)
message = f"이름: {name}, 나이: {age}"
print(message)"""),
        "02_control_flow": ("제어문", "if-else, for, while 등 제어문을 학습합니다.", """# if-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# for 문
for i in range(5):
    print(i)

# 리스트 순회
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# while 문
count = 0
while count < 3:
    print(count)
    count += 1

# 리스트 컴프리헨션
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]"""),
        "03_functions": ("함수", "Python 함수의 정의와 활용을 학습합니다.", """# 기본 함수
def greet(name):
    return f"안녕하세요, {name}님!"

# 기본값 매개변수
def power(base, exp=2):
    return base ** exp

# 가변 인자
def sum_all(*args):
    return sum(args)

# 키워드 인자
def create_user(**kwargs):
    return kwargs

# 람다 함수
square = lambda x: x ** 2

# 사용
print(greet("코드마스터"))
print(power(3))        # 9
print(power(2, 3))     # 8
print(sum_all(1, 2, 3, 4, 5))  # 15
print(create_user(name="Kim", age=25))"""),
        "04_classes": ("클래스", "Python 객체지향 프로그래밍을 학습합니다.", """class Person:
    # 클래스 변수
    species = "Homo sapiens"

    # 생성자
    def __init__(self, name, age):
        self.name = name  # 인스턴스 변수
        self.age = age

    # 인스턴스 메서드
    def greet(self):
        return f"안녕하세요, {self.name}입니다!"

    # 클래스 메서드
    @classmethod
    def get_species(cls):
        return cls.species

    # 정적 메서드
    @staticmethod
    def is_adult(age):
        return age >= 18

# 상속
class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def study(self):
        return f"{self.name}이(가) 공부합니다."

# 사용
person = Person("김철수", 25)
student = Student("이영희", 20, "서울대")"""),
    },
    "os": {
        "kernel": ("커널", "운영체제의 핵심인 커널의 역할과 구조를 학습합니다.", """// 시스템 콜 예시 (C 언어)
#include <unistd.h>
#include <fcntl.h>

int main() {
    // open() 시스템 콜
    int fd = open("test.txt", O_RDONLY);

    // read() 시스템 콜
    char buffer[100];
    ssize_t bytes = read(fd, buffer, sizeof(buffer));

    // write() 시스템 콜
    write(STDOUT_FILENO, buffer, bytes);

    // close() 시스템 콜
    close(fd);

    return 0;
}

/* 커널 모드 vs 사용자 모드
 * - 커널 모드: 모든 하드웨어 접근 가능
 * - 사용자 모드: 제한된 권한
 * - 시스템 콜로 모드 전환
 */"""),
        "process-concept": ("프로세스", "프로세스의 개념, 상태, PCB를 학습합니다.", """// 프로세스 생성 (C 언어)
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();  // 프로세스 복제

    if (pid == 0) {
        // 자식 프로세스
        printf("자식 PID: %d\\n", getpid());
        printf("부모 PID: %d\\n", getppid());
    } else if (pid > 0) {
        // 부모 프로세스
        printf("부모입니다. 자식 PID: %d\\n", pid);
        wait(NULL);  // 자식 종료 대기
    }

    return 0;
}

/* 프로세스 상태
 * New → Ready → Running → Waiting → Terminated
 */"""),
        "thread": ("스레드", "스레드의 개념과 멀티스레딩을 학습합니다.", """// POSIX 스레드 (pthread)
#include <pthread.h>
#include <stdio.h>

void* thread_func(void* arg) {
    int id = *(int*)arg;
    printf("Thread %d 실행 중\\n", id);
    return NULL;
}

int main() {
    pthread_t threads[3];
    int ids[3] = {1, 2, 3};

    // 스레드 생성
    for (int i = 0; i < 3; i++) {
        pthread_create(&threads[i], NULL, thread_func, &ids[i]);
    }

    // 스레드 종료 대기
    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}"""),
        "scheduling": ("CPU 스케줄링", "FCFS, SJF, RR 등 스케줄링 알고리즘을 학습합니다.", """# CPU 스케줄링 시뮬레이션 (Python)
from collections import deque

def fcfs(processes):
    """First Come First Served"""
    time = 0
    for p in processes:
        wait_time = time - p['arrival']
        time += p['burst']
        print(f"프로세스 {p['id']}: 대기시간 {wait_time}")

def round_robin(processes, quantum=2):
    """Round Robin 스케줄링"""
    queue = deque(processes)
    time = 0

    while queue:
        p = queue.popleft()
        exec_time = min(quantum, p['remaining'])
        p['remaining'] -= exec_time
        time += exec_time

        if p['remaining'] > 0:
            queue.append(p)
        else:
            print(f"프로세스 {p['id']} 완료: {time}ms")

# 예시 프로세스
processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 5, 'remaining': 5},
    {'id': 'P2', 'arrival': 1, 'burst': 3, 'remaining': 3},
]"""),
    },
    "algorithm": {
        "binary-search": ("이진 탐색", "정렬된 배열에서 O(log n) 탐색을 학습합니다.", """def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Lower Bound (target 이상인 첫 위치)
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# 사용
numbers = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(numbers, 7))  # 3"""),
        "sorting": ("정렬 알고리즘", "다양한 정렬 알고리즘을 학습합니다.", """# 버블 정렬 O(n²)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# 퀵 정렬 O(n log n)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# 병합 정렬 O(n log n)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result"""),
        "dfs-bfs": ("DFS & BFS", "깊이 우선 탐색과 너비 우선 탐색을 학습합니다.", """from collections import deque

# 그래프 (인접 리스트)
graph = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [], 5: [], 6: []
}

# DFS (깊이 우선 탐색) - 재귀
def dfs(node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node, end=' ')
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

# DFS (스택)
def dfs_stack(start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node, end=' ')
            stack.extend(reversed(graph[node]))

# BFS (너비 우선 탐색) - 큐
def bfs(start):
    visited = set([start])
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

print("DFS:", end=' '); dfs(1)
print("\\nBFS:", end=' '); bfs(1)"""),
        "dynamic-programming": ("동적 프로그래밍", "메모이제이션과 DP를 활용한 최적화를 학습합니다.", """# 피보나치 - 메모이제이션
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# 피보나치 - 타뷸레이션
def fib_tab(n):
    if n <= 2:
        return 1
    dp = [0] * (n + 1)
    dp[1] = dp[2] = 1
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# 0/1 배낭 문제
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]"""),
    },
    "spring": {
        "spring-intro": ("Spring 소개", "Spring Framework의 핵심 개념을 학습합니다.", """// Spring Boot 메인 클래스
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

    @PostMapping
    public User createUser(@RequestBody UserDto dto) {
        return userService.create(dto);
    }
}"""),
        "spring-di": ("의존성 주입", "IoC와 DI의 개념과 활용을 학습합니다.", """// 의존성 주입 3가지 방식

// 1. 생성자 주입 (권장)
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// 2. Setter 주입
@Service
public class OrderService {
    private PaymentService paymentService;

    @Autowired
    public void setPaymentService(PaymentService ps) {
        this.paymentService = ps;
    }
}

// 3. 필드 주입 (권장하지 않음)
@Service
public class ProductService {
    @Autowired
    private ProductRepository productRepository;
}

// 인터페이스 활용
public interface NotificationService {
    void send(String message);
}

@Service
@Primary  // 기본 구현체
public class EmailService implements NotificationService {
    public void send(String message) {
        // 이메일 발송
    }
}

@Service
public class SmsService implements NotificationService {
    public void send(String message) {
        // SMS 발송
    }
}"""),
        "spring-jpa": ("Spring Data JPA", "JPA를 활용한 데이터 접근을 학습합니다.", """// Entity
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(unique = true)
    private String email;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders = new ArrayList<>();
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // 쿼리 메서드
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);

    // JPQL
    @Query("SELECT u FROM User u WHERE u.age > :age")
    List<User> findUsersOlderThan(@Param("age") int age);

    // Native Query
    @Query(value = "SELECT * FROM users WHERE status = 1",
           nativeQuery = true)
    List<User> findActiveUsers();
}

// Service
@Service
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository userRepository;

    @Transactional
    public User create(UserDto dto) {
        User user = new User(dto.getName(), dto.getEmail());
        return userRepository.save(user);
    }
}"""),
    },
    "react": {
        "react-intro": ("React 소개", "React의 핵심 개념과 JSX를 학습합니다.", """// 함수형 컴포넌트
import React from 'react';

function App() {
    return (
        <div className="app">
            <h1>Hello React!</h1>
            <Greeting name="코드마스터" />
        </div>
    );
}

// Props 전달
function Greeting({ name }) {
    return <p>안녕하세요, {name}님!</p>;
}

// JSX 문법
function Example() {
    const items = ['Apple', 'Banana', 'Cherry'];
    const isLoggedIn = true;

    return (
        <div>
            {/* 조건부 렌더링 */}
            {isLoggedIn ? <p>환영합니다!</p> : <p>로그인하세요</p>}

            {/* 리스트 렌더링 */}
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;"""),
        "react-hooks": ("React Hooks", "useState, useEffect 등 Hooks를 학습합니다.", """import React, { useState, useEffect, useCallback, useMemo } from 'react';

function Counter() {
    // useState
    const [count, setCount] = useState(0);
    const [name, setName] = useState('');

    // useEffect (부수 효과)
    useEffect(() => {
        document.title = `Count: ${count}`;

        // cleanup 함수
        return () => {
            console.log('컴포넌트 언마운트');
        };
    }, [count]);  // count 변경 시 실행

    // useCallback (함수 메모이제이션)
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []);

    // useMemo (값 메모이제이션)
    const expensiveValue = useMemo(() => {
        return count * 100;
    }, [count]);

    return (
        <div>
            <p>Count: {count}</p>
            <p>Expensive: {expensiveValue}</p>
            <button onClick={handleClick}>증가</button>
            <input
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
        </div>
    );
}"""),
    },
    "db": {
        "sql-basic": ("SQL 기초", "SELECT, INSERT, UPDATE, DELETE 기본 쿼리를 학습합니다.", """-- SELECT (조회)
SELECT * FROM users;
SELECT name, email FROM users WHERE age >= 20;

-- WHERE 조건
SELECT * FROM users
WHERE age BETWEEN 20 AND 30
  AND city IN ('서울', '부산')
  AND name LIKE '김%';

-- ORDER BY & LIMIT
SELECT * FROM users
ORDER BY age DESC
LIMIT 10 OFFSET 0;

-- GROUP BY & 집계 함수
SELECT city, COUNT(*) as user_count, AVG(age) as avg_age
FROM users
GROUP BY city
HAVING COUNT(*) > 5;

-- JOIN
SELECT u.name, o.order_date, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 10000;

-- INSERT
INSERT INTO users (name, email, age)
VALUES ('김철수', 'kim@example.com', 25);

-- UPDATE
UPDATE users SET age = 26 WHERE name = '김철수';

-- DELETE
DELETE FROM users WHERE id = 1;"""),
        "sql-join": ("SQL JOIN", "INNER, LEFT, RIGHT, FULL JOIN을 학습합니다.", """-- INNER JOIN (교집합)
SELECT u.name, o.product
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN (왼쪽 테이블 기준)
SELECT u.name, COALESCE(o.order_count, 0) as orders
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders GROUP BY user_id
) o ON u.id = o.user_id;

-- RIGHT JOIN (오른쪽 테이블 기준)
SELECT u.name, p.product_name
FROM users u
RIGHT JOIN purchases p ON u.id = p.user_id;

-- FULL OUTER JOIN (합집합)
SELECT *
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.a_id;

-- SELF JOIN
SELECT e.name as employee, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- CROSS JOIN (모든 조합)
SELECT *
FROM colors
CROSS JOIN sizes;"""),
    },
    "network": {
        "osi-model": ("OSI 7계층", "네트워크 통신의 7계층 모델을 학습합니다.", """# OSI 7계층 모델
# L7 응용   - HTTP, FTP, SMTP
# L6 표현   - 암호화, 압축
# L5 세션   - 연결 관리
# L4 전송   - TCP/UDP, 포트
# L3 네트워크 - IP, 라우팅
# L2 데이터링크 - MAC, 스위치
# L1 물리   - 케이블, 허브

# TCP 소켓 프로그래밍
import socket

# 서버
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        data = client.recv(1024)
        client.send(b"Hello from server!")
        client.close()

# 클라이언트
def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    client.send(b"Hello!")
    response = client.recv(1024)
    client.close()"""),
        "tcp-udp": ("TCP vs UDP", "TCP와 UDP의 차이점과 활용을 학습합니다.", """# TCP (Transmission Control Protocol)
# - 연결 지향 (3-way handshake)
# - 신뢰성 보장 (재전송)
# - 순서 보장
# - 흐름 제어, 혼잡 제어
# - HTTP, FTP, SMTP 등

# UDP (User Datagram Protocol)
# - 비연결 지향
# - 신뢰성 없음
# - 순서 보장 없음
# - 빠른 전송
# - DNS, 스트리밍, 게임 등

import socket

# UDP 서버
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        sock.sendto(b"Pong!", addr)

# UDP 클라이언트
def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Ping!", ('127.0.0.1', 8080))
    data, _ = sock.recvfrom(1024)
    print(data.decode())"""),
        "http": ("HTTP 프로토콜", "HTTP 요청/응답과 메서드를 학습합니다.", """# HTTP 메서드
# GET    - 리소스 조회
# POST   - 리소스 생성
# PUT    - 리소스 전체 수정
# PATCH  - 리소스 부분 수정
# DELETE - 리소스 삭제

# HTTP 상태 코드
# 2xx 성공: 200 OK, 201 Created, 204 No Content
# 3xx 리다이렉션: 301 Moved, 304 Not Modified
# 4xx 클라이언트 에러: 400 Bad Request, 401 Unauthorized, 404 Not Found
# 5xx 서버 에러: 500 Internal Server Error, 503 Service Unavailable

import requests

# GET 요청
response = requests.get('https://api.example.com/users')
print(response.status_code)
print(response.json())

# POST 요청
data = {'name': 'Kim', 'email': 'kim@example.com'}
response = requests.post('https://api.example.com/users', json=data)

# 헤더 설정
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/me', headers=headers)"""),
    },
    "devops": {
        "docker-intro": ("Docker 소개", "Docker 컨테이너의 개념과 활용을 학습합니다.", """# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]

# Docker 명령어
# docker build -t my-app .
# docker run -p 3000:3000 my-app
# docker ps
# docker logs <container>
# docker exec -it <container> sh

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
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:"""),
        "git": ("Git 버전 관리", "Git의 기본 명령어와 브랜치 전략을 학습합니다.", """# Git 기본 명령어
git init                    # 저장소 초기화
git clone <url>             # 저장소 복제
git status                  # 상태 확인
git add .                   # 스테이징
git commit -m "message"     # 커밋
git push origin main        # 푸시
git pull origin main        # 풀

# 브랜치 관리
git branch feature          # 브랜치 생성
git checkout feature        # 브랜치 전환
git checkout -b feature     # 생성 + 전환
git merge feature           # 병합
git branch -d feature       # 브랜치 삭제

# 되돌리기
git reset --soft HEAD~1     # 마지막 커밋 취소 (변경 유지)
git reset --hard HEAD~1     # 마지막 커밋 삭제 (변경 삭제)
git revert <commit>         # 커밋 되돌리기 (새 커밋 생성)

# 충돌 해결
git merge feature           # 충돌 발생 시
# 파일 수정 후
git add .
git commit -m "Resolve conflict"

# 원격 저장소
git remote add origin <url>
git remote -v
git fetch origin"""),
    }
}

def get_html_template(title, desc, code, category):
    """HTML 템플릿 생성"""
    # 언어 감지
    lang = "java"
    if "python" in category.lower() or "def " in code or "import " in code:
        lang = "python"
    elif "const " in code or "function " in code or "=>" in code:
        lang = "javascript"
    elif "SELECT" in code or "FROM" in code:
        lang = "sql"
    elif "FROM " in code and "RUN " in code:
        lang = "dockerfile"
    elif "git " in code:
        lang = "bash"
    elif "#include" in code:
        lang = "c"

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 코드마스터</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: #e2e8f0;
      line-height: 1.8;
      min-height: 100vh;
    }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    .header {{
      background: linear-gradient(135deg, #6366F122 0%, #6366F111 100%);
      border: 1px solid #6366F144;
      border-radius: 20px;
      padding: 40px;
      margin-bottom: 32px;
    }}
    .category-badge {{
      display: inline-block;
      background: #6366F1;
      color: white;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 16px;
    }}
    .title {{ font-size: 32px; font-weight: 800; margin-bottom: 16px; color: #fff; }}
    .meta {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .meta-item {{ color: #94a3b8; font-size: 14px; }}
    .section {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 24px;
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 20px;
      color: #fff;
    }}
    .desc {{ color: #94a3b8; margin-bottom: 20px; font-size: 16px; }}
    .code-block {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      overflow: hidden;
    }}
    .code-header {{
      background: #1e293b;
      padding: 12px 20px;
      font-size: 14px;
      color: #94a3b8;
      border-bottom: 1px solid #334155;
    }}
    .code-content {{ padding: 20px; overflow-x: auto; }}
    pre {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 14px; line-height: 1.6; }}
    code {{ color: #e2e8f0; }}
    .tip-box {{
      background: linear-gradient(135deg, #3b82f622 0%, #3b82f611 100%);
      border: 1px solid #3b82f644;
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
    }}
    .tip-title {{ font-weight: 600; margin-bottom: 8px; color: #3b82f6; }}
    .practice-box {{
      background: linear-gradient(135deg, #6366F122 0%, #6366F111 100%);
      border: 1px solid #6366F144;
      border-radius: 12px;
      padding: 24px;
    }}
    .practice-title {{ font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #fff; }}
    .practice-list {{ list-style: decimal; padding-left: 24px; }}
    .practice-list li {{ margin-bottom: 12px; color: #cbd5e1; }}
    @media (max-width: 640px) {{
      .container {{ padding: 20px 16px; }}
      .header {{ padding: 24px; }}
      .title {{ font-size: 24px; }}
      .section {{ padding: 20px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="category-badge">{category}</span>
      <h1 class="title">{title}</h1>
      <div class="meta">
        <span class="meta-item">⏱️ 30분</span>
        <span class="meta-item">🌿 입문~초급</span>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">📚 핵심 개념</h2>
      <p class="desc">{desc}</p>
    </div>

    <div class="section">
      <h2 class="section-title">💻 코드 예제</h2>
      <div class="code-block">
        <div class="code-header">{lang.upper()}</div>
        <div class="code-content">
          <pre><code>{code}</code></pre>
        </div>
      </div>

      <div class="tip-box">
        <div class="tip-title">💡 핵심 포인트</div>
        <p style="color: #94a3b8;">코드를 직접 실행해보며 동작 원리를 이해하세요.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">✏️ 실습 문제</h2>
      <div class="practice-box">
        <h4 class="practice-title">🚀 직접 해보기</h4>
        <ol class="practice-list">
          <li>위 예제 코드를 직접 실행해보세요.</li>
          <li>코드를 수정하여 다른 결과를 만들어보세요.</li>
          <li>관련 개념을 자신의 프로젝트에 적용해보세요.</li>
        </ol>
      </div>
    </div>
  </div>
</body>
</html>'''

def find_content(filename, category_name):
    """파일명으로 콘텐츠 찾기"""
    stem = Path(filename).stem

    # 카테고리별 검색
    for cat_key, templates in CONTENT_TEMPLATES.items():
        if cat_key in category_name.lower():
            for key, value in templates.items():
                if key in stem or stem in key:
                    return value

    # 전체 검색
    for cat_key, templates in CONTENT_TEMPLATES.items():
        for key, value in templates.items():
            if key == stem or key in stem or stem in key:
                return value

    return None

def process_file(html_file):
    """파일 처리"""
    category = html_file.parent.parent.name if html_file.parent.name.startswith(('0', '1')) else html_file.parent.name
    content = find_content(html_file.name, category)

    if content:
        title, desc, code = content
        new_html = get_html_template(title, desc, code, category.upper())

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False

def main():
    updated = 0
    total = 0

    for html_file in STUDY_DIR.rglob("*.html"):
        if "index.html" in str(html_file):
            continue
        total += 1

        if process_file(html_file):
            print(f"✓ {html_file.relative_to(STUDY_DIR)}")
            updated += 1

    print(f"\n완료: {updated}/{total} 파일 업데이트")

if __name__ == "__main__":
    main()
