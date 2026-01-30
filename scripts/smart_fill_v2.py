#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Content Generator v2 - More topic mappings
"""
import os
import re
from pathlib import Path

# Extended topic to code mapping
TOPIC_CODES = {
    # === JAVA BASICS ===
    "array": ("Java", '''// 배열 선언과 초기화
int[] numbers = {1, 2, 3, 4, 5};
String[] names = new String[3];

// 배열 순회
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}

// 향상된 for문
for (int num : numbers) {
    System.out.println(num);
}

// Arrays 유틸리티
Arrays.sort(numbers);
int index = Arrays.binarySearch(numbers, 3);
int[] copy = Arrays.copyOf(numbers, 10);'''),

    "loop": ("Java", '''// for 반복문
for (int i = 0; i < 5; i++) {
    System.out.println("반복: " + i);
}

// while 반복문
int count = 0;
while (count < 3) {
    System.out.println("카운트: " + count);
    count++;
}

// do-while 반복문
do {
    System.out.println("최소 1번 실행");
} while (false);

// 중첩 반복문과 레이블
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break outer;
        System.out.println(i + ", " + j);
    }
}'''),

    "condition": ("Java", '''// if-else 조건문
int score = 85;
if (score >= 90) {
    System.out.println("A등급");
} else if (score >= 80) {
    System.out.println("B등급");
} else {
    System.out.println("F등급");
}

// switch 표현식 (Java 14+)
String grade = switch (score / 10) {
    case 10, 9 -> "A";
    case 8 -> "B";
    case 7 -> "C";
    default -> "F";
};

// 삼항 연산자
String result = (score >= 60) ? "합격" : "불합격";'''),

    "exception": ("Java", '''// 예외 처리 기본
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("0으로 나눌 수 없습니다");
} finally {
    System.out.println("항상 실행");
}

// 다중 catch
try {
    // 위험한 코드
} catch (IOException | SQLException e) {
    e.printStackTrace();
}

// try-with-resources
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
}

// 커스텀 예외
class MyException extends RuntimeException {
    public MyException(String msg) { super(msg); }
}'''),

    "inheritance": ("Java", '''// 상속
class Animal {
    protected String name;
    public void eat() { System.out.println("먹습니다"); }
}

class Dog extends Animal {
    public Dog(String name) { this.name = name; }

    @Override
    public void eat() { System.out.println(name + " 사료를 먹습니다"); }

    public void bark() { System.out.println("멍멍!"); }
}

// 추상 클래스
abstract class Shape {
    abstract double area();
    void display() { System.out.println("Area: " + area()); }
}

class Circle extends Shape {
    private double radius;
    Circle(double r) { this.radius = r; }
    double area() { return Math.PI * radius * radius; }
}'''),

    "interface": ("Java", '''// 인터페이스
interface Drawable {
    void draw();
    default void log() { System.out.println("Drawing..."); }
    static void info() { System.out.println("Drawable interface"); }
}

interface Movable {
    void move(int x, int y);
}

// 다중 구현
class Circle implements Drawable, Movable {
    private int x, y;

    @Override
    public void draw() { System.out.println("원 그리기"); }

    @Override
    public void move(int x, int y) { this.x = x; this.y = y; }
}

// 함수형 인터페이스
@FunctionalInterface
interface Calculator {
    int calc(int a, int b);
}
Calculator add = (a, b) -> a + b;'''),

    "generic": ("Java", '''// 제네릭 클래스
class Box<T> {
    private T item;
    public void set(T item) { this.item = item; }
    public T get() { return item; }
}

// 제네릭 메서드
public static <T> void printArray(T[] arr) {
    for (T item : arr) System.out.println(item);
}

// 와일드카드
void printList(List<?> list) { }           // 모든 타입
void addNumbers(List<? extends Number> list) { }  // Number 하위
void addIntegers(List<? super Integer> list) { }  // Integer 상위

// 타입 제한
class NumBox<T extends Number> {
    private T num;
    double getDouble() { return num.doubleValue(); }
}'''),

    "stream": ("Java", '''// Stream API
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// filter & map
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * 2)
    .collect(Collectors.toList());

// reduce
int sum = numbers.stream().reduce(0, Integer::sum);

// groupingBy
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity));

// flatMap
List<String> words = lines.stream()
    .flatMap(line -> Arrays.stream(line.split(" ")))
    .collect(Collectors.toList());

// parallel stream
long count = numbers.parallelStream()
    .filter(n -> n > 2)
    .count();'''),

    "thread": ("Java", '''// 스레드 생성
Thread t1 = new Thread(() -> {
    System.out.println("Thread: " + Thread.currentThread().getName());
});
t1.start();

// 동기화
class Counter {
    private int count = 0;
    public synchronized void increment() { count++; }
}

// ReentrantLock
private final Lock lock = new ReentrantLock();
lock.lock();
try {
    // 임계 영역
} finally {
    lock.unlock();
}

// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(4);
Future<String> future = executor.submit(() -> "Result");
String result = future.get();
executor.shutdown();'''),

    "lambda": ("Java", '''// 람다 표현식
Runnable r = () -> System.out.println("Hello");

// 함수형 인터페이스
Function<String, Integer> length = s -> s.length();
Predicate<Integer> isPositive = n -> n > 0;
Consumer<String> printer = System.out::println;
Supplier<Double> random = Math::random;
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// 메서드 참조
list.forEach(System.out::println);        // 인스턴스 메서드
list.stream().map(String::toUpperCase);   // 파라미터 메서드
list.stream().map(Person::new);           // 생성자

// Comparator
list.sort(Comparator.comparing(Person::getName)
    .thenComparing(Person::getAge));'''),

    "optional": ("Java", '''// Optional 생성
Optional<String> opt = Optional.of("value");
Optional<String> empty = Optional.empty();
Optional<String> nullable = Optional.ofNullable(null);

// 값 추출
String value = opt.orElse("default");
String value2 = opt.orElseGet(() -> expensive());
String value3 = opt.orElseThrow(() -> new RuntimeException());

// 변환
Optional<Integer> len = opt.map(String::length);
Optional<String> upper = opt.flatMap(s -> Optional.of(s.toUpperCase()));

// 조건부 실행
opt.ifPresent(System.out::println);
opt.ifPresentOrElse(
    System.out::println,
    () -> System.out.println("Empty")
);

// 필터
opt.filter(s -> s.length() > 3).ifPresent(System.out::println);'''),

    "collection": ("Java", '''// List
List<String> list = new ArrayList<>();
list.add("A"); list.add("B");
list.get(0); list.remove(0);

// Set
Set<String> set = new HashSet<>();
set.add("A"); set.add("A"); // 중복 무시
set.contains("A");

// Map
Map<String, Integer> map = new HashMap<>();
map.put("key", 100);
map.getOrDefault("key2", 0);
map.computeIfAbsent("key3", k -> compute(k));

// Queue
Queue<String> queue = new LinkedList<>();
queue.offer("A"); queue.poll();

// Stack
Deque<String> stack = new ArrayDeque<>();
stack.push("A"); stack.pop();'''),

    # === SPRING ===
    "ioc": ("Java", '''// IoC (Inversion of Control)
// 기존: 직접 생성
UserService service = new UserService(new UserRepository());

// IoC: 컨테이너가 관리
@Service
public class UserService {
    private final UserRepository repository;

    // 생성자 주입 - 컨테이너가 자동 주입
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// Bean 등록
@Configuration
public class AppConfig {
    @Bean
    public UserRepository userRepository() {
        return new JpaUserRepository();
    }
}'''),

    "di": ("Java", '''// 의존성 주입 방법

// 1. 생성자 주입 (권장)
@Service
public class UserService {
    private final UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }
}

// 2. Setter 주입
@Service
public class UserService {
    private UserRepository repo;

    @Autowired
    public void setRepo(UserRepository repo) {
        this.repo = repo;
    }
}

// 3. 필드 주입 (권장하지 않음)
@Service
public class UserService {
    @Autowired
    private UserRepository repo;
}'''),

    "aop": ("Java", '''// AOP (Aspect Oriented Programming)
@Aspect
@Component
public class LoggingAspect {

    // Before
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint jp) {
        log.info("Method: {}", jp.getSignature().getName());
    }

    // Around
    @Around("@annotation(Timed)")
    public Object measureTime(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = pjp.proceed();
        log.info("Time: {}ms", System.currentTimeMillis() - start);
        return result;
    }

    // AfterReturning
    @AfterReturning(pointcut = "execution(* *..find*(..))", returning = "result")
    public void logResult(Object result) {
        log.info("Result: {}", result);
    }
}'''),

    "controller": ("Java", '''@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public List<UserDto> getUsers() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public UserDto getUser(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto createUser(@RequestBody @Valid CreateUserRequest req) {
        return userService.create(req);
    }

    @PutMapping("/{id}")
    public UserDto updateUser(@PathVariable Long id, @RequestBody UpdateUserRequest req) {
        return userService.update(id, req);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}'''),

    "jpa": ("Java", '''// Entity
@Entity
@Table(name = "users")
@Getter @Setter
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders = new ArrayList<>();
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);
}

// Service
@Service @Transactional(readOnly = true)
public class UserService {
    @Transactional
    public User save(User user) { return repo.save(user); }
}'''),

    "transaction": ("Java", '''// 트랜잭션 관리
@Service
@Transactional(readOnly = true)  // 클래스 레벨 기본값
public class OrderService {

    @Transactional  // 쓰기 작업은 readOnly = false
    public Order createOrder(OrderDto dto) {
        Order order = new Order(dto);
        paymentService.process(order);
        inventoryService.decrease(dto.getItems());
        return orderRepository.save(order);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logActivity(String action) {
        // 별도 트랜잭션
    }

    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void criticalOperation() {
        // 격리 수준 최고
    }
}'''),

    "security": ("Java", '''// Spring Security 설정
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}'''),

    "validation": ("Java", '''// Bean Validation
public class UserDto {
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50)
    private String name;

    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;

    @Pattern(regexp = "^01[0-9]-\\\\d{4}-\\\\d{4}$")
    private String phone;

    @Min(0) @Max(150)
    private Integer age;
}

// Controller에서 검증
@PostMapping
public User create(@RequestBody @Valid UserDto dto, BindingResult result) {
    if (result.hasErrors()) {
        throw new ValidationException(result);
    }
    return userService.create(dto);
}'''),

    # === PYTHON ===
    "list": ("Python", '''# 리스트 기본
fruits = ["사과", "바나나", "오렌지"]
fruits.append("포도")
fruits.insert(1, "딸기")
fruits.remove("바나나")
last = fruits.pop()

# 슬라이싱
nums = [0, 1, 2, 3, 4, 5]
print(nums[1:4])    # [1, 2, 3]
print(nums[::2])    # [0, 2, 4]
print(nums[::-1])   # [5, 4, 3, 2, 1, 0]

# 리스트 컴프리헨션
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix = [[i*j for j in range(3)] for i in range(3)]

# 유용한 함수
sorted_list = sorted(fruits, key=len)
total = sum([1, 2, 3, 4, 5])'''),

    "dict": ("Python", '''# 딕셔너리 기본
person = {"name": "홍길동", "age": 25}
person["city"] = "서울"
age = person.get("age", 0)
person.pop("city")

# 순회
for key, value in person.items():
    print(f"{key}: {value}")

# 딕셔너리 컴프리헨션
squares = {x: x**2 for x in range(5)}
filtered = {k: v for k, v in person.items() if v}

# 고급 기능
from collections import defaultdict, Counter
dd = defaultdict(list)
dd["key"].append(1)

counter = Counter(["a", "b", "a", "c", "a"])
print(counter.most_common(2))  # [('a', 3), ('b', 1)]'''),

    "function": ("Python", '''# 함수 정의
def greet(name: str, greeting: str = "안녕하세요") -> str:
    """인사 함수"""
    return f"{greeting}, {name}님!"

# 가변 인자
def sum_all(*args, **kwargs):
    total = sum(args)
    for value in kwargs.values():
        total += value
    return total

# 람다
square = lambda x: x ** 2
add = lambda a, b: a + b

# 클로저
def multiplier(n):
    def multiply(x):
        return x * n
    return multiply
double = multiplier(2)
print(double(5))  # 10'''),

    "class": ("Python", '''# 클래스 정의
class Person:
    species = "인간"  # 클래스 변수

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"안녕하세요, {self.name}입니다."

    @classmethod
    def from_birth_year(cls, name: str, year: int):
        return cls(name, 2024 - year)

    @staticmethod
    def is_adult(age: int) -> bool:
        return age >= 18

# 상속
class Student(Person):
    def __init__(self, name: str, age: int, school: str):
        super().__init__(name, age)
        self.school = school'''),

    "decorator": ("Python", '''# 데코레이터 기본
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

# 매개변수 있는 데코레이터
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")'''),

    "async": ("Python", '''import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    # 동시 실행
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    # 타임아웃
    try:
        result = await asyncio.wait_for(fetch_data("url"), timeout=5.0)
    except asyncio.TimeoutError:
        print("Timeout!")

# 실행
asyncio.run(main())'''),

    "file": ("Python", '''# 파일 읽기/쓰기
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
    # 또는 라인별
    lines = f.readlines()

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\\n")
    f.writelines(["Line 1\\n", "Line 2\\n"])

# JSON
import json
with open("data.json", "r") as f:
    data = json.load(f)

with open("output.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# CSV
import csv
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)'''),

    # === REACT ===
    "useState": ("JavaScript", '''import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    const [user, setUser] = useState({ name: '', age: 0 });

    // 단순 업데이트
    const increment = () => setCount(count + 1);

    // 함수형 업데이트 (이전 상태 기반)
    const decrement = () => setCount(prev => prev - 1);

    // 객체 상태 업데이트
    const updateName = (name) => {
        setUser(prev => ({ ...prev, name }));
    };

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    );
}'''),

    "useEffect": ("JavaScript", '''import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 마운트 시 1회 실행
    useEffect(() => {
        console.log('Component mounted');
        return () => console.log('Cleanup on unmount');
    }, []);

    // userId 변경 시 실행
    useEffect(() => {
        const fetchUser = async () => {
            setLoading(true);
            const res = await fetch(\`/api/users/\${userId}\`);
            setUser(await res.json());
            setLoading(false);
        };
        fetchUser();
    }, [userId]);

    if (loading) return <p>Loading...</p>;
    return <div>{user?.name}</div>;
}'''),

    "props": ("JavaScript", '''// Props 전달
function Greeting({ name, age, onButtonClick }) {
    return (
        <div>
            <h1>Hello, {name}!</h1>
            <p>Age: {age}</p>
            <button onClick={onButtonClick}>Click</button>
        </div>
    );
}

// children props
function Card({ title, children }) {
    return (
        <div className="card">
            <h2>{title}</h2>
            <div className="card-body">{children}</div>
        </div>
    );
}

// 사용
function App() {
    return (
        <Card title="User Info">
            <Greeting
                name="홍길동"
                age={25}
                onButtonClick={() => alert('Clicked!')}
            />
        </Card>
    );
}'''),

    "context": ("JavaScript", '''import { createContext, useContext, useState } from 'react';

// Context 생성
const ThemeContext = createContext();

// Provider
function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light');

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

// 커스텀 훅
function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) throw new Error('useTheme must be used within ThemeProvider');
    return context;
}

// 사용
function Header() {
    const { theme, toggleTheme } = useTheme();
    return <button onClick={toggleTheme}>Current: {theme}</button>;
}'''),

    "useMemo": ("JavaScript", '''import { useMemo, useCallback, memo } from 'react';

function ExpensiveComponent({ data, onItemClick }) {
    // useMemo: 값 메모이제이션
    const processedData = useMemo(() => {
        console.log('Processing data...');
        return data.map(item => ({
            ...item,
            processed: true
        }));
    }, [data]);

    // useCallback: 함수 메모이제이션
    const handleClick = useCallback((id) => {
        onItemClick(id);
    }, [onItemClick]);

    return (
        <ul>
            {processedData.map(item => (
                <li key={item.id} onClick={() => handleClick(item.id)}>
                    {item.name}
                </li>
            ))}
        </ul>
    );
}

// memo: 컴포넌트 메모이제이션
const MemoizedComponent = memo(ExpensiveComponent);'''),

    "useReducer": ("JavaScript", '''import { useReducer } from 'react';

// Reducer 함수
function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        case 'reset':
            return { count: 0 };
        default:
            throw new Error('Unknown action');
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0 });

    return (
        <div>
            <p>Count: {state.count}</p>
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
        </div>
    );
}'''),

    # === SQL ===
    "select": ("SQL", '''-- 기본 SELECT
SELECT * FROM users;
SELECT name, email FROM users WHERE active = true;

-- 조건절
SELECT * FROM users
WHERE age BETWEEN 20 AND 30
  AND city IN ('서울', '부산')
  AND name LIKE '김%';

-- 정렬과 페이징
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;

-- 집계
SELECT city, COUNT(*) as cnt, AVG(age) as avg_age
FROM users
GROUP BY city
HAVING COUNT(*) >= 5;

-- 서브쿼리
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE amount > 10000);'''),

    "join": ("SQL", '''-- INNER JOIN
SELECT u.name, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- 다중 JOIN
SELECT u.name, o.order_date, p.product_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id;

-- SELF JOIN
SELECT e.name as employee, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;'''),

    "index": ("SQL", '''-- 인덱스 생성
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_phone ON users(phone);

-- 복합 인덱스
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date DESC);

-- 실행 계획
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- 인덱스가 효과적인 경우
-- WHERE, JOIN, ORDER BY에 사용되는 컬럼
-- 카디널리티가 높은 컬럼

-- 인덱스 삭제
DROP INDEX idx_users_email ON users;'''),

    "subquery": ("SQL", '''-- 스칼라 서브쿼리 (SELECT)
SELECT name,
    (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count
FROM users u;

-- 인라인 뷰 (FROM)
SELECT avg_amount
FROM (
    SELECT user_id, AVG(amount) as avg_amount
    FROM orders
    GROUP BY user_id
) as user_avg
WHERE avg_amount > 10000;

-- 중첩 서브쿼리 (WHERE)
SELECT * FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE amount > (SELECT AVG(amount) FROM orders)
);

-- EXISTS
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id);'''),

    # === ALGORITHM ===
    "bfs": ("Python", '''from collections import deque

def bfs(graph, start):
    """너비 우선 탐색"""
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result

# 최단 경로 (가중치 없는 그래프)
def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []'''),

    "dfs": ("Python", '''def dfs_recursive(graph, node, visited=None):
    """DFS 재귀"""
    if visited is None:
        visited = set()

    visited.add(node)
    result = [node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))

    return result

def dfs_iterative(graph, start):
    """DFS 스택"""
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            stack.extend(reversed(graph[node]))

    return result'''),

    "binary_search": ("Python", '''def binary_search(arr, target):
    """이진 탐색 - O(log n)"""
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

def lower_bound(arr, target):
    """target 이상인 첫 위치"""
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

def upper_bound(arr, target):
    """target 초과인 첫 위치"""
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left'''),

    "dp": ("Python", '''# 동적 프로그래밍

# 피보나치 - Bottom-up
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# 0-1 배낭 문제
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w-weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]

# LCS (최장 공통 부분 수열)
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]'''),

    "sort": ("Python", '''# 퀵 정렬
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# 병합 정렬
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
    return result'''),

    "graph": ("Python", '''# 그래프 표현
# 인접 리스트
graph = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [], 5: [], 6: []
}

# 인접 행렬
n = 6
matrix = [[0] * n for _ in range(n)]
matrix[0][1] = 1  # 1->2 연결

# 가중치 그래프 (딕셔너리)
weighted = {
    'A': [('B', 5), ('C', 3)],
    'B': [('D', 2)],
    'C': [('D', 4)],
    'D': []
}

# 다익스트라
import heapq
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    return distances'''),

    "heap": ("Python", '''import heapq

# 최소 힙
min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 2)
smallest = heapq.heappop(min_heap)  # 1

# 최대 힙 (음수 활용)
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
largest = -heapq.heappop(max_heap)  # 3

# 힙 정렬
def heap_sort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]

# K번째 큰 요소
def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]

# 우선순위 큐
pq = []
heapq.heappush(pq, (priority, item))
_, item = heapq.heappop(pq)'''),

    "tree": ("Python", '''class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

# 전위 순회 (Pre-order)
def preorder(node):
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)

# 중위 순회 (In-order)
def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

# 후위 순회 (Post-order)
def postorder(node):
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]

# 레벨 순회 (Level-order)
from collections import deque
def levelorder(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result'''),

    # === NETWORK ===
    "tcp": ("Python", '''import socket

# TCP 서버
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        data = client.recv(1024).decode()
        client.send(f"Echo: {data}".encode())
        client.close()

# TCP 클라이언트
def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8080))
    client.send("Hello".encode())
    response = client.recv(1024).decode()
    client.close()
    return response'''),

    "http": ("Python", '''import requests

# GET 요청
response = requests.get('https://api.example.com/users')
data = response.json()

# POST 요청
response = requests.post(
    'https://api.example.com/users',
    json={'name': '홍길동', 'email': 'hong@example.com'},
    headers={'Authorization': 'Bearer token123'}
)

# 에러 처리
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")

# 세션 사용
with requests.Session() as session:
    session.headers.update({'Authorization': 'Bearer token'})
    response = session.get('/api/data')'''),

    # === OS ===
    "process": ("C", '''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 자식 프로세스
        printf("Child PID: %d\\n", getpid());
        printf("Parent PID: %d\\n", getppid());
        execl("/bin/ls", "ls", "-l", NULL);
    } else if (pid > 0) {
        // 부모 프로세스
        int status;
        waitpid(pid, &status, 0);
        printf("Child exited with status: %d\\n", WEXITSTATUS(status));
    }

    return 0;
}

/* 프로세스 상태
 * New -> Ready -> Running -> Waiting -> Terminated
 */'''),

    "memory": ("C", '''#include <stdlib.h>

// 동적 메모리 할당
int *arr = (int *)malloc(10 * sizeof(int));
if (arr == NULL) return -1;

// 초기화된 메모리
int *arr2 = (int *)calloc(10, sizeof(int));

// 크기 변경
arr = (int *)realloc(arr, 20 * sizeof(int));

// 메모리 해제
free(arr);
arr = NULL;

/* 메모리 구조
 * Stack: 지역 변수, 함수 호출
 * Heap: 동적 할당
 * Data: 전역/정적 변수
 * Code: 실행 코드
 */

/* 페이지 교체 알고리즘
 * FIFO, LRU, LFU, Optimal
 */'''),

    "thread": ("C", '''#include <pthread.h>
#include <stdio.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int counter = 0;

void* increment(void* arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&mutex);
        counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;

    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Counter: %d\\n", counter);
    return 0;
}'''),

    "deadlock": ("Python", '''# 데드락 조건 (4가지 모두 충족 시 발생)
# 1. 상호 배제 (Mutual Exclusion)
# 2. 점유 대기 (Hold and Wait)
# 3. 비선점 (No Preemption)
# 4. 순환 대기 (Circular Wait)

import threading

# 데드락 예방 - 락 순서 지정
lock_a = threading.Lock()
lock_b = threading.Lock()

def safe_function():
    # 항상 같은 순서로 락 획득
    with lock_a:
        with lock_b:
            # 작업 수행
            pass

# 데드락 회피 - 타임아웃 사용
def with_timeout():
    acquired_a = lock_a.acquire(timeout=1.0)
    if acquired_a:
        try:
            acquired_b = lock_b.acquire(timeout=1.0)
            if acquired_b:
                try:
                    # 작업 수행
                    pass
                finally:
                    lock_b.release()
        finally:
            lock_a.release()'''),

    # === SECURITY ===
    "xss": ("JavaScript", '''// XSS 방어

// 취약한 코드
element.innerHTML = userInput;  // 위험!

// 안전한 코드
element.textContent = userInput;

// HTML 이스케이프
function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// React는 자동 이스케이프
function Safe({ userInput }) {
    return <div>{userInput}</div>;
}

// DOMPurify 사용
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);'''),

    "csrf": ("Java", '''// CSRF 방어 - Spring Security
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        return http
            .csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            )
            .build();
    }
}

// HTML 폼
<form method="POST">
    <input type="hidden" name="_csrf" th:value="${_csrf.token}"/>
</form>

// JavaScript 요청
const csrfToken = document.querySelector('meta[name="_csrf"]').content;
fetch('/api/data', {
    method: 'POST',
    headers: { 'X-CSRF-TOKEN': csrfToken },
    body: JSON.stringify(data)
});'''),

    "sql_injection": ("Java", '''// SQL Injection 방어

// 취약한 코드
String query = "SELECT * FROM users WHERE id = " + userId;

// 안전한 코드 - PreparedStatement
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.setLong(1, userId);
ResultSet rs = stmt.executeQuery();

// JPA 사용
@Query("SELECT u FROM User u WHERE u.id = :id")
User findById(@Param("id") Long id);

// 입력 검증
if (!userId.matches("\\\\d+")) {
    throw new IllegalArgumentException("Invalid ID");
}'''),

    "encryption": ("Python", '''from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

# 대칭키 암호화 (Fernet)
key = Fernet.generate_key()
fernet = Fernet(key)

encrypted = fernet.encrypt(b"secret message")
decrypted = fernet.decrypt(encrypted)

# 비밀번호 기반 키 생성
password = b"my_password"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# 해시 (bcrypt)
import bcrypt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
bcrypt.checkpw(password, hashed)  # True'''),

    "hash": ("Python", '''import hashlib
import bcrypt
import secrets

# SHA-256 해시
def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# 비밀번호 해시 (bcrypt 권장)
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

# 보안 토큰 생성
token = secrets.token_urlsafe(32)

# HMAC
import hmac
def create_signature(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()'''),

    "jwt": ("JavaScript", '''// JWT 생성 (Node.js)
const jwt = require('jsonwebtoken');

const payload = { userId: 123, role: 'admin' };
const secret = process.env.JWT_SECRET;

// 토큰 생성
const token = jwt.sign(payload, secret, { expiresIn: '1h' });

// 토큰 검증
try {
    const decoded = jwt.verify(token, secret);
    console.log(decoded.userId);
} catch (err) {
    console.log('Invalid token');
}

// 미들웨어
function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });

    try {
        req.user = jwt.verify(token, secret);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
}'''),

    # === DOCKER/DEVOPS ===
    "docker": ("YAML", '''# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]

# docker-compose.yml
version: '3.8'
services:
  app:
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
      POSTGRES_DB: mydb
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:'''),

    "kubernetes": ("YAML", '''# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 3000
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer'''),

    "cicd": ("YAML", '''# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: npm ci
    - run: npm test
    - run: npm run build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        echo "Deploying..."'''),

    # === AI/ML ===
    "neural": ("Python", '''import numpy as np

# 간단한 뉴런
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# 단층 퍼셉트론
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()

    def forward(self, x):
        return sigmoid(np.dot(x, self.weights) + self.bias)

    def train(self, X, y, lr=0.1, epochs=1000):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.forward(xi)
                error = yi - pred
                self.weights += lr * error * xi
                self.bias += lr * error'''),

    "cnn": ("Python", '''import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x'''),

    "transformer": ("Python", '''import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_k = d_model // num_heads
        self.num_heads = num_heads
        self.q_linear = nn.Linear(d_model, d_model)
        self.k_linear = nn.Linear(d_model, d_model)
        self.v_linear = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, q, k, v, mask=None):
        bs = q.size(0)
        q = self.q_linear(q).view(bs, -1, self.num_heads, self.d_k).transpose(1,2)
        k = self.k_linear(k).view(bs, -1, self.num_heads, self.d_k).transpose(1,2)
        v = self.v_linear(v).view(bs, -1, self.num_heads, self.d_k).transpose(1,2)

        scores = torch.matmul(q, k.transpose(-2,-1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = torch.softmax(scores, dim=-1)

        output = torch.matmul(attn, v)
        return self.out(output.transpose(1,2).contiguous().view(bs, -1, self.num_heads * self.d_k))'''),
}

# Default codes by category
DEFAULT_CODES = {
    "java": ("Java", '''public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}'''),
    "spring": ("Java", '''@RestController
public class HelloController {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring!";
    }
}'''),
    "python": ("Python", '''def main():
    print("Hello, Python!")

if __name__ == "__main__":
    main()'''),
    "javascript": ("JavaScript", '''function hello(name) {
    return \`Hello, \${name}!\`;
}
console.log(hello("World"));'''),
    "react": ("JavaScript", '''function App() {
    return <h1>Hello, React!</h1>;
}
export default App;'''),
    "algorithm": ("Python", '''def solution(n):
    return n'''),
    "db": ("SQL", '''SELECT * FROM users;'''),
    "network": ("Python", '''import socket'''),
    "os": ("C", '''#include <stdio.h>
int main() { return 0; }'''),
    "security": ("Java", '''// Security example'''),
    "devops": ("YAML", '''# DevOps config'''),
    "ai": ("Python", '''import numpy as np'''),
}


def get_topic_from_filename(filepath: str) -> tuple:
    """Extract topic keywords from file path"""
    path = Path(filepath)
    filename = path.stem.lower().replace('-', '_').replace(' ', '_')
    parent = path.parent.name.lower()
    full_path = str(path).lower()

    # Check specific topics
    for keyword, (lang, code) in TOPIC_CODES.items():
        kw = keyword.lower().replace('-', '_').replace(' ', '_')
        if kw in filename or kw in parent:
            return (lang, code, keyword)

    # Fall back to category default
    for category, (lang, code) in DEFAULT_CODES.items():
        if category in full_path:
            return (lang, code, category)

    return ("JavaScript", "// Example", "default")


def generate_html(filepath: str, lang: str, code: str, topic: str) -> str:
    """Generate HTML content"""
    path = Path(filepath)
    title = path.stem.replace('-', ' ').replace('_', ' ').title()

    colors = {
        "java": ("#f89820", "Java"),
        "spring": ("#6DB33F", "Spring"),
        "python": ("#3776AB", "Python"),
        "react": ("#61DAFB", "React"),
        "javascript": ("#F7DF1E", "JavaScript"),
        "algorithm": ("#00BCB4", "Algorithm"),
        "db": ("#336791", "Database"),
        "network": ("#0078D4", "Network"),
        "os": ("#0078D4", "OS"),
        "security": ("#d63384", "Security"),
        "devops": ("#2496ED", "DevOps"),
        "ai": ("#ff6f00", "AI/ML"),
    }

    color, badge = "#6366F1", "Study"
    for cat, (c, b) in colors.items():
        if cat in str(path).lower():
            color, badge = c, b
            break

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 코드마스터</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Pretendard', -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #e2e8f0; line-height: 1.8; min-height: 100vh; }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    .header {{ background: linear-gradient(135deg, {color}22 0%, {color}11 100%); border: 1px solid {color}44; border-radius: 20px; padding: 40px; margin-bottom: 32px; }}
    .badge {{ display: inline-block; background: {color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; margin-bottom: 16px; }}
    .title {{ font-size: 32px; font-weight: 800; margin-bottom: 16px; color: #fff; }}
    .meta {{ display: flex; gap: 16px; color: #94a3b8; font-size: 14px; }}
    .section {{ background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 32px; margin-bottom: 24px; }}
    .section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #fff; }}
    .code-block {{ background: #0f172a; border: 1px solid #334155; border-radius: 12px; overflow: hidden; }}
    .code-header {{ background: #1e293b; padding: 12px 20px; font-size: 14px; color: #94a3b8; border-bottom: 1px solid #334155; }}
    .code-content {{ padding: 20px; overflow-x: auto; }}
    pre {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; line-height: 1.6; }}
    code {{ color: #e2e8f0; }}
    .tip-box {{ background: linear-gradient(135deg, #3b82f622 0%, #3b82f611 100%); border: 1px solid #3b82f644; border-radius: 12px; padding: 20px; margin-top: 20px; }}
    .tip-title {{ font-weight: 600; margin-bottom: 8px; color: #3b82f6; }}
    .practice-box {{ background: linear-gradient(135deg, #6366F122 0%, #6366F111 100%); border: 1px solid #6366F144; border-radius: 12px; padding: 24px; }}
    .practice-title {{ font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #fff; }}
    .practice-list {{ list-style: decimal; padding-left: 24px; }}
    .practice-list li {{ margin-bottom: 12px; color: #cbd5e1; }}
    @media (max-width: 640px) {{ .container {{ padding: 20px 16px; }} .header {{ padding: 24px; }} .title {{ font-size: 24px; }} }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{badge}</span>
      <h1 class="title">{title}</h1>
      <div class="meta"><span>30분</span><span>입문~초급</span></div>
    </div>
    <div class="section">
      <h2 class="section-title">핵심 개념</h2>
      <p style="color: #94a3b8;">{title}의 기본 개념과 활용법을 학습합니다.</p>
    </div>
    <div class="section">
      <h2 class="section-title">코드 예제</h2>
      <div class="code-block">
        <div class="code-header">{lang}</div>
        <div class="code-content"><pre><code>{code}</code></pre></div>
      </div>
      <div class="tip-box">
        <div class="tip-title">핵심 포인트</div>
        <p style="color: #94a3b8;">코드를 직접 실행해보며 동작 원리를 이해하세요.</p>
      </div>
    </div>
    <div class="section">
      <h2 class="section-title">실습 문제</h2>
      <div class="practice-box">
        <h4 class="practice-title">직접 해보기</h4>
        <ol class="practice-list">
          <li>위 예제 코드를 직접 실행해보세요.</li>
          <li>코드를 수정하여 다른 결과를 만들어보세요.</li>
          <li>이 개념을 자신의 프로젝트에 적용해보세요.</li>
        </ol>
      </div>
    </div>
  </div>
</body>
</html>'''


def main():
    study_dir = Path(r"c:\tools\codemaster-next-main\public\study")
    updated = 0

    for html_file in study_dir.rglob("*.html"):
        if html_file.name == "index.html":
            continue
        try:
            lang, code, topic = get_topic_from_filename(str(html_file))
            content = generate_html(str(html_file), lang, code, topic)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            if updated % 100 == 0:
                print(f"Updated {updated}...")
        except Exception as e:
            print(f"Error: {html_file} - {e}")

    print(f"\nDone! Updated: {updated}")


if __name__ == "__main__":
    main()
