# -*- coding: utf-8 -*-
"""953개 파일 한국어 변환"""
import os
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent
STUDY_DIR = BASE_DIR / "public" / "study"

def get_korean_title(filename):
    """파일명을 한국어 제목으로 변환"""
    name = Path(filename).stem
    name = re.sub(r'^\d+[_-]?', '', name)

    # 영어 -> 한국어 매핑
    translations = {
        'kernel': '커널',
        'process': '프로세스',
        'thread': '스레드',
        'memory': '메모리',
        'scheduling': '스케줄링',
        'deadlock': '데드락',
        'mutex': '뮤텍스',
        'semaphore': '세마포어',
        'os-structure': '운영체제 구조',
        'os-intro': '운영체제 소개',
        'system-call': '시스템 콜',
        'intro': '소개',
        'basic': '기초',
        'basics': '기초',
        'syntax': '문법',
        'variables': '변수',
        'variable': '변수',
        'control-flow': '제어문',
        'control_flow': '제어문',
        'functions': '함수',
        'function': '함수',
        'classes': '클래스',
        'class': '클래스',
        'object': '객체',
        'class-object': '클래스와 객체',
        'inheritance': '상속',
        'polymorphism': '다형성',
        'encapsulation': '캡슐화',
        'abstraction': '추상화',
        'interface': '인터페이스',
        'exception': '예외 처리',
        'collection': '컬렉션',
        'stream': '스트림',
        'lambda': '람다',
        'generic': '제네릭',
        'annotation': '어노테이션',
        'reflection': '리플렉션',
        'io': '입출력',
        'file': '파일',
        'network': '네트워크',
        'socket': '소켓',
        'http': 'HTTP 프로토콜',
        'https': 'HTTPS',
        'tcp': 'TCP',
        'udp': 'UDP',
        'tcp-udp': 'TCP vs UDP',
        'osi': 'OSI 7계층',
        'osi-model': 'OSI 7계층',
        'ip': 'IP 주소',
        'dns': 'DNS',
        'rest': 'REST API',
        'restful': 'RESTful API',
        'api': 'API',
        'json': 'JSON',
        'xml': 'XML',
        'database': '데이터베이스',
        'sql': 'SQL',
        'sql-basic': 'SQL 기초',
        'sql-join': 'SQL JOIN',
        'nosql': 'NoSQL',
        'mysql': 'MySQL',
        'postgresql': 'PostgreSQL',
        'mongodb': 'MongoDB',
        'redis': 'Redis',
        'orm': 'ORM',
        'jpa': 'JPA',
        'hibernate': 'Hibernate',
        'transaction': '트랜잭션',
        'index': '인덱스',
        'normalization': '정규화',
        'algorithm': '알고리즘',
        'data-structure': '자료구조',
        'array': '배열',
        'list': '리스트',
        'linked-list': '연결 리스트',
        'stack': '스택',
        'queue': '큐',
        'tree': '트리',
        'binary-tree': '이진 트리',
        'bst': '이진 탐색 트리',
        'heap': '힙',
        'graph': '그래프',
        'hash': '해시',
        'hashmap': '해시맵',
        'sorting': '정렬',
        'sort': '정렬',
        'search': '탐색',
        'binary-search': '이진 탐색',
        'linear-search': '선형 탐색',
        'dfs': 'DFS',
        'bfs': 'BFS',
        'dfs-bfs': 'DFS & BFS',
        'dijkstra': '다익스트라',
        'dynamic-programming': '동적 프로그래밍',
        'dp': '동적 프로그래밍',
        'greedy': '그리디',
        'recursion': '재귀',
        'backtracking': '백트래킹',
        'divide-conquer': '분할 정복',
        'spring': 'Spring',
        'spring-intro': 'Spring 소개',
        'spring-boot': 'Spring Boot',
        'spring-mvc': 'Spring MVC',
        'spring-di': '의존성 주입',
        'spring-aop': 'Spring AOP',
        'spring-security': 'Spring Security',
        'spring-jpa': 'Spring Data JPA',
        'spring-rest': 'Spring REST',
        'controller': '컨트롤러',
        'service': '서비스',
        'repository': '리포지토리',
        'entity': '엔티티',
        'dto': 'DTO',
        'react': 'React',
        'react-intro': 'React 소개',
        'react-hooks': 'React Hooks',
        'component': '컴포넌트',
        'props': 'Props',
        'state': 'State',
        'usestate': 'useState',
        'useeffect': 'useEffect',
        'context': 'Context API',
        'redux': 'Redux',
        'router': '라우터',
        'jsx': 'JSX',
        'virtual-dom': '가상 DOM',
        'docker': 'Docker',
        'docker-intro': 'Docker 소개',
        'container': '컨테이너',
        'image': '이미지',
        'dockerfile': 'Dockerfile',
        'docker-compose': 'Docker Compose',
        'kubernetes': 'Kubernetes',
        'k8s': 'Kubernetes',
        'ci-cd': 'CI/CD',
        'jenkins': 'Jenkins',
        'github-actions': 'GitHub Actions',
        'git': 'Git',
        'git-basic': 'Git 기초',
        'branch': '브랜치',
        'merge': '머지',
        'rebase': '리베이스',
        'conflict': '충돌 해결',
        'linux': 'Linux',
        'command': '명령어',
        'shell': '셸',
        'bash': 'Bash',
        'vim': 'Vim',
        'aws': 'AWS',
        'cloud': '클라우드',
        'ec2': 'EC2',
        's3': 'S3',
        'rds': 'RDS',
        'lambda-aws': 'AWS Lambda',
        'security': '보안',
        'authentication': '인증',
        'authorization': '인가',
        'jwt': 'JWT',
        'oauth': 'OAuth',
        'encryption': '암호화',
        'hashing': '해싱',
        'xss': 'XSS',
        'csrf': 'CSRF',
        'sql-injection': 'SQL Injection',
        'clean-code': '클린 코드',
        'refactoring': '리팩토링',
        'solid': 'SOLID 원칙',
        'design-pattern': '디자인 패턴',
        'singleton': '싱글톤',
        'factory': '팩토리',
        'observer': '옵저버',
        'strategy': '전략 패턴',
        'test': '테스트',
        'unit-test': '단위 테스트',
        'integration-test': '통합 테스트',
        'tdd': 'TDD',
        'mock': '목 객체',
        'ai': 'AI',
        'ml': '머신러닝',
        'machine-learning': '머신러닝',
        'deep-learning': '딥러닝',
        'neural-network': '신경망',
        'sklearn': 'Scikit-learn',
        'sklearn-guide': 'Scikit-learn 가이드',
        'tensorflow': 'TensorFlow',
        'pytorch': 'PyTorch',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'html': 'HTML',
        'css': 'CSS',
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'java': 'Java',
        'java-intro': 'Java 소개',
        'java-basic': 'Java 기초',
        'java-oop': 'Java 객체지향',
        'python': 'Python',
        'python-intro': 'Python 소개',
        'python-basic': 'Python 기초',
        'modules': '모듈',
        'packages': '패키지',
        'pip': 'pip',
        'venv': '가상환경',
        'decorator': '데코레이터',
        'generator': '제너레이터',
        'iterator': '이터레이터',
        'async': '비동기',
        'await': 'await',
        'promise': 'Promise',
        'callback': '콜백',
        'event-loop': '이벤트 루프',
        'concurrency': '동시성',
        'parallel': '병렬 처리',
        'multithreading': '멀티스레딩',
    }

    name_lower = name.lower().replace('_', '-')

    if name_lower in translations:
        return translations[name_lower]

    # 부분 매칭
    for eng, kor in translations.items():
        if eng in name_lower:
            return kor

    # 기본값: 파일명 그대로 (공백 처리)
    return name.replace('-', ' ').replace('_', ' ').title()

def get_category_korean(category):
    """카테고리 한국어 변환"""
    cat_map = {
        'java': 'Java',
        'python': 'Python',
        'javascript': 'JavaScript',
        'react': 'React',
        'spring': 'Spring',
        'os': '운영체제',
        'algorithm': '알고리즘',
        'db': '데이터베이스',
        'network': '네트워크',
        'devops': 'DevOps',
        'html-css': 'HTML/CSS',
        'ai': 'AI/ML',
        'ai-roadmap': 'AI 로드맵',
        'ai-tech': 'AI 기술',
        'security': '보안',
        'cleancode': '클린코드',
        'collaboration': '협업',
        'tools': '개발 도구',
        'react-basics': 'React 기초',
    }
    return cat_map.get(category.lower(), category.title())

def get_code_example(title, category):
    """카테고리에 맞는 코드 예제"""
    cat = category.lower()
    title_lower = title.lower()

    if 'java' in cat:
        if '상속' in title or 'inherit' in title_lower:
            return 'java', '''// 부모 클래스
class Animal {
    protected String name;

    public void eat() {
        System.out.println(name + "이(가) 먹습니다.");
    }
}

// 자식 클래스
class Dog extends Animal {
    public Dog(String name) {
        this.name = name;
    }

    @Override
    public void eat() {
        System.out.println(name + "이(가) 사료를 먹습니다.");
    }

    public void bark() {
        System.out.println("멍멍!");
    }
}

// 사용
Dog dog = new Dog("바둑이");
dog.eat();   // 바둑이이(가) 사료를 먹습니다.
dog.bark();  // 멍멍!'''
        elif '클래스' in title or 'class' in title_lower:
            return 'java', '''// 클래스 정의
public class Person {
    // 필드 (속성)
    private String name;
    private int age;

    // 생성자
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 메서드 (행동)
    public void introduce() {
        System.out.println("안녕하세요, " + name + "입니다.");
        System.out.println("나이는 " + age + "살입니다.");
    }

    // Getter/Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}

// 객체 생성 및 사용
Person person = new Person("김철수", 25);
person.introduce();'''
        elif '컬렉션' in title or 'collection' in title_lower:
            return 'java', '''import java.util.*;

// List - 순서 있음, 중복 허용
List<String> list = new ArrayList<>();
list.add("사과");
list.add("바나나");
list.add("사과");  // 중복 가능

// Set - 순서 없음, 중복 불가
Set<String> set = new HashSet<>();
set.add("사과");
set.add("바나나");
set.add("사과");  // 무시됨 (중복)

// Map - 키-값 쌍
Map<String, Integer> map = new HashMap<>();
map.put("사과", 1000);
map.put("바나나", 2000);

// 순회
for (String item : list) {
    System.out.println(item);
}

map.forEach((k, v) -> System.out.println(k + ": " + v + "원"));'''
        else:
            return 'java', '''public class HelloWorld {
    public static void main(String[] args) {
        // 콘솔 출력
        System.out.println("안녕하세요, Java!");

        // 변수 선언
        String name = "코드마스터";
        int age = 25;
        double score = 95.5;
        boolean isStudent = true;

        // 출력
        System.out.println("이름: " + name);
        System.out.println("나이: " + age + "살");
        System.out.println("점수: " + score);
    }
}'''

    elif 'python' in cat:
        if '함수' in title or 'function' in title_lower:
            return 'python', '''# 기본 함수
def greet(name):
    return f"안녕하세요, {name}님!"

# 기본값 매개변수
def power(base, exp=2):
    return base ** exp

# 가변 인자 (*args)
def sum_all(*numbers):
    return sum(numbers)

# 키워드 인자 (**kwargs)
def create_user(**info):
    return info

# 람다 함수
square = lambda x: x ** 2

# 사용 예시
print(greet("코드마스터"))      # 안녕하세요, 코드마스터님!
print(power(3))                  # 9
print(power(2, 3))               # 8
print(sum_all(1, 2, 3, 4, 5))    # 15
print(create_user(name="김철수", age=25))'''
        elif '클래스' in title or 'class' in title_lower:
            return 'python', '''class Person:
    """사람을 나타내는 클래스"""

    # 클래스 변수
    species = "Homo sapiens"

    # 생성자
    def __init__(self, name, age):
        self.name = name  # 인스턴스 변수
        self.age = age

    # 인스턴스 메서드
    def introduce(self):
        return f"안녕하세요, {self.name}입니다. {self.age}살입니다."

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
student = Student("이영희", 20, "서울대")
print(person.introduce())
print(student.study())'''
        else:
            return 'python', '''# 변수와 자료형
name = "코드마스터"
age = 25
height = 175.5
is_student = True

# 리스트
fruits = ["사과", "바나나", "체리"]
fruits.append("오렌지")

# 딕셔너리
person = {
    "name": "김철수",
    "age": 25,
    "city": "서울"
}

# 반복문
for fruit in fruits:
    print(fruit)

# 조건문
if age >= 20:
    print("성인입니다")
else:
    print("미성년자입니다")

# 리스트 컴프리헨션
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]'''

    elif 'spring' in cat:
        if 'jpa' in title_lower or 'data' in title_lower:
            return 'java', '''// 엔티티
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
}

// 리포지토리
public interface UserRepository extends JpaRepository<User, Long> {
    // 쿼리 메서드
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);

    // JPQL
    @Query("SELECT u FROM User u WHERE u.age > :age")
    List<User> findUsersOlderThan(@Param("age") int age);
}

// 서비스
@Service
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository userRepository;

    @Transactional
    public User create(UserDto dto) {
        User user = new User(dto.getName(), dto.getEmail());
        return userRepository.save(user);
    }
}'''
        else:
            return 'java', '''// 메인 클래스
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// REST 컨트롤러
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

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}'''

    elif 'react' in cat:
        if 'hook' in title_lower:
            return 'javascript', '''import { useState, useEffect } from 'react';

function Counter() {
    // useState - 상태 관리
    const [count, setCount] = useState(0);
    const [name, setName] = useState('');

    // useEffect - 부수 효과
    useEffect(() => {
        document.title = \`카운트: \${count}\`;

        // 클린업 함수
        return () => {
            console.log('컴포넌트 언마운트');
        };
    }, [count]);  // count 변경 시 실행

    return (
        <div>
            <h1>카운트: {count}</h1>
            <button onClick={() => setCount(count + 1)}>증가</button>
            <button onClick={() => setCount(count - 1)}>감소</button>

            <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="이름 입력"
            />
            <p>입력: {name}</p>
        </div>
    );
}'''
        else:
            return 'javascript', '''// 함수형 컴포넌트
function App() {
    return (
        <div className="app">
            <h1>안녕하세요, React!</h1>
            <Greeting name="코드마스터" />
            <Counter />
        </div>
    );
}

// Props 전달
function Greeting({ name }) {
    return <p>환영합니다, {name}님!</p>;
}

// 상태 관리
function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>카운트: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                증가
            </button>
        </div>
    );
}

export default App;'''

    elif 'algorithm' in cat:
        if '이진' in title or 'binary' in title_lower:
            return 'python', '''def binary_search(arr, target):
    """이진 탐색 - O(log n)"""
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

# 사용 예시
numbers = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(numbers, 7))  # 3
print(lower_bound(numbers, 6))    # 3'''
        elif '정렬' in title or 'sort' in title_lower:
            return 'python', '''# 퀵 정렬 - O(n log n)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# 병합 정렬 - O(n log n)
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
    return result

# 사용
arr = [64, 34, 25, 12, 22, 11, 90]
print(quick_sort(arr))'''
        elif 'dfs' in title_lower or 'bfs' in title_lower:
            return 'python', '''from collections import deque

# 그래프 (인접 리스트)
graph = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [], 5: [], 6: []
}

# DFS (깊이 우선 탐색) - 스택/재귀
def dfs(node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node, end=' ')

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

# BFS (너비 우선 탐색) - 큐
def bfs(start):
    visited = {start}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

print("DFS:", end=' ')
dfs(1)  # 1 2 4 5 3 6
print("\\nBFS:", end=' ')
bfs(1)  # 1 2 3 4 5 6'''
        else:
            return 'python', '''# 동적 프로그래밍 - 피보나치
def fib_memo(n, memo={}):
    """메모이제이션 방식"""
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

def fib_tab(n):
    """타뷸레이션 방식"""
    if n <= 2:
        return 1
    dp = [0] * (n + 1)
    dp[1] = dp[2] = 1
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

print(fib_memo(50))  # 12586269025
print(fib_tab(50))   # 12586269025'''

    elif 'db' in cat:
        if 'join' in title_lower:
            return 'sql', '''-- INNER JOIN (교집합)
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

-- 서브쿼리
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders WHERE total > 10000
);

-- SELF JOIN
SELECT e.name as 직원, m.name as 매니저
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;'''
        else:
            return 'sql', '''-- SELECT (조회)
SELECT * FROM users WHERE age >= 20;
SELECT name, email FROM users ORDER BY age DESC LIMIT 10;

-- WHERE 조건
SELECT * FROM users
WHERE age BETWEEN 20 AND 30
  AND city IN ('서울', '부산')
  AND name LIKE '김%';

-- GROUP BY & 집계 함수
SELECT city, COUNT(*) as 인원수, AVG(age) as 평균나이
FROM users
GROUP BY city
HAVING COUNT(*) > 5;

-- INSERT
INSERT INTO users (name, email, age)
VALUES ('김철수', 'kim@example.com', 25);

-- UPDATE
UPDATE users SET age = 26 WHERE name = '김철수';

-- DELETE
DELETE FROM users WHERE id = 1;'''

    elif 'network' in cat:
        if 'http' in title_lower:
            return 'python', '''import requests

# GET 요청
response = requests.get('https://api.example.com/users')
print(response.status_code)  # 200
print(response.json())

# POST 요청
data = {'name': '김철수', 'email': 'kim@example.com'}
response = requests.post('https://api.example.com/users', json=data)

# 헤더 설정
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/me', headers=headers)

# HTTP 상태 코드
# 2xx 성공: 200 OK, 201 Created
# 3xx 리다이렉션: 301 Moved, 304 Not Modified
# 4xx 클라이언트 에러: 400 Bad Request, 404 Not Found
# 5xx 서버 에러: 500 Internal Server Error'''
        else:
            return 'python', '''import socket

# TCP 서버
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("서버 시작: 포트 8080")

    while True:
        client, addr = server.accept()
        print(f"연결됨: {addr}")
        data = client.recv(1024)
        client.send("안녕하세요, 클라이언트님!".encode())
        client.close()

# TCP 클라이언트
def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    client.send("안녕하세요, 서버님!".encode())
    response = client.recv(1024)
    print(f"응답: {response.decode()}")
    client.close()'''

    elif 'devops' in cat:
        if 'docker' in title_lower:
            return 'dockerfile', '''# Dockerfile
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
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:'''
        elif 'git' in title_lower:
            return 'bash', '''# Git 기본 명령어
git init                    # 저장소 초기화
git clone <url>             # 저장소 복제
git status                  # 상태 확인
git add .                   # 스테이징
git commit -m "메시지"      # 커밋
git push origin main        # 푸시
git pull origin main        # 풀

# 브랜치 관리
git branch feature          # 브랜치 생성
git checkout feature        # 브랜치 전환
git checkout -b feature     # 생성 + 전환
git merge feature           # 병합
git branch -d feature       # 브랜치 삭제

# 되돌리기
git reset --soft HEAD~1     # 커밋 취소 (변경 유지)
git reset --hard HEAD~1     # 커밋 삭제 (변경 삭제)
git revert <commit>         # 커밋 되돌리기'''
        else:
            return 'bash', '''# CI/CD 파이프라인
npm install
npm test
npm run build

# Docker 명령어
docker build -t myapp .
docker run -p 3000:3000 myapp
docker ps
docker logs <container>

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs <pod>'''

    elif 'os' in cat:
        return 'c', '''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();  // 프로세스 복제

    if (pid == 0) {
        // 자식 프로세스
        printf("자식 프로세스 PID: %d\\n", getpid());
        printf("부모 프로세스 PID: %d\\n", getppid());
    } else if (pid > 0) {
        // 부모 프로세스
        printf("부모입니다. 자식 PID: %d\\n", pid);
        wait(NULL);  // 자식 종료 대기
        printf("자식 프로세스 종료됨\\n");
    } else {
        // 에러
        perror("fork 실패");
        return 1;
    }

    return 0;
}

/* 프로세스 상태
 * New -> Ready -> Running -> Waiting -> Terminated
 */'''

    # 기본값
    return 'javascript', '''// 예제 코드
function hello(name) {
    return \`안녕하세요, \${name}님!\`;
}

const result = hello("코드마스터");
console.log(result);

// 배열 처리
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
console.log(doubled);  // [2, 4, 6, 8, 10]'''

def create_korean_html(title, category, code_lang, code):
    """한국어 HTML 생성"""
    cat_colors = {
        'java': '#f89820',
        'python': '#3776ab',
        'javascript': '#f7df1e',
        'react': '#61dafb',
        'spring': '#6db33f',
        'os': '#0078d4',
        'algorithm': '#ff6b6b',
        'db': '#336791',
        'network': '#00d4aa',
        'devops': '#2496ed',
        'html-css': '#e34f26',
        'ai': '#ff6f00',
        'security': '#d63384',
        'cleancode': '#28a745',
        'collaboration': '#6f42c1',
        'tools': '#495057',
    }

    cat_lower = category.lower()
    color = '#6366F1'
    for key, c in cat_colors.items():
        if key in cat_lower:
            color = c
            break

    cat_korean = get_category_korean(category)

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 코드마스터</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Pretendard', -apple-system, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: #e2e8f0; line-height: 1.8; min-height: 100vh;
    }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    .header {{
      background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
      border: 1px solid {color}44;
      border-radius: 20px; padding: 40px; margin-bottom: 32px;
    }}
    .badge {{
      display: inline-block; background: {color};
      color: white; padding: 6px 16px; border-radius: 20px;
      font-size: 14px; font-weight: 600; margin-bottom: 16px;
    }}
    .title {{ font-size: 32px; font-weight: 800; margin-bottom: 16px; color: #fff; }}
    .meta {{ display: flex; gap: 16px; color: #94a3b8; font-size: 14px; }}
    .section {{
      background: #1e293b; border: 1px solid #334155;
      border-radius: 16px; padding: 32px; margin-bottom: 24px;
    }}
    .section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #fff; }}
    .code-block {{
      background: #0f172a; border: 1px solid #334155;
      border-radius: 12px; overflow: hidden;
    }}
    .code-header {{
      background: #1e293b; padding: 12px 20px;
      font-size: 14px; color: #94a3b8; border-bottom: 1px solid #334155;
    }}
    .code-content {{ padding: 20px; overflow-x: auto; }}
    pre {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; line-height: 1.6; }}
    code {{ color: #e2e8f0; }}
    .tip-box {{
      background: linear-gradient(135deg, #3b82f622 0%, #3b82f611 100%);
      border: 1px solid #3b82f644; border-radius: 12px;
      padding: 20px; margin-top: 20px;
    }}
    .tip-title {{ font-weight: 600; margin-bottom: 8px; color: #3b82f6; }}
    .practice-box {{
      background: linear-gradient(135deg, #6366F122 0%, #6366F111 100%);
      border: 1px solid #6366F144; border-radius: 12px; padding: 24px;
    }}
    .practice-title {{ font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #fff; }}
    .practice-list {{ list-style: decimal; padding-left: 24px; }}
    .practice-list li {{ margin-bottom: 12px; color: #cbd5e1; }}
    @media (max-width: 640px) {{
      .container {{ padding: 20px 16px; }}
      .header {{ padding: 24px; }}
      .title {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{cat_korean}</span>
      <h1 class="title">{title}</h1>
      <div class="meta">
        <span>30분</span>
        <span>입문~초급</span>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">핵심 개념</h2>
      <p style="color: #94a3b8;">{title}의 기본 개념을 학습합니다.</p>
    </div>

    <div class="section">
      <h2 class="section-title">코드 예제</h2>
      <div class="code-block">
        <div class="code-header">{code_lang.upper()}</div>
        <div class="code-content">
          <pre><code>{code}</code></pre>
        </div>
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

def process_all():
    """모든 파일 처리"""
    count = 0
    for html_file in STUDY_DIR.rglob("*.html"):
        if "index.html" in str(html_file):
            continue

        category = html_file.parent.name
        if category.startswith(('0', '1')):
            category = html_file.parent.parent.name

        title = get_korean_title(html_file.name)
        code_lang, code = get_code_example(title, category)

        html_content = create_korean_html(title, category, code_lang, code)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        count += 1
        if count % 100 == 0:
            print(f"{count}개 처리 완료...")

    print(f"\n완료: {count}개 파일 한국어 변환")

if __name__ == "__main__":
    process_all()
