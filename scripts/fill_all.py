# -*- coding: utf-8 -*-
"""952 content generator - fixed encoding"""
import os
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent
STUDY_DIR = BASE_DIR / "public" / "study"

def get_title_from_filename(filename):
    """Convert filename to title"""
    name = Path(filename).stem
    # Remove number prefix
    name = re.sub(r'^\d+[_-]?', '', name)
    # Convert kebab/snake to title
    name = name.replace('-', ' ').replace('_', ' ')
    return name.title()

def get_category_info(category):
    """Get category display name and color"""
    categories = {
        'java': ('Java', '#f89820'),
        'python': ('Python', '#3776ab'),
        'javascript': ('JavaScript', '#f7df1e'),
        'react': ('React', '#61dafb'),
        'spring': ('Spring', '#6db33f'),
        'os': ('Operating System', '#0078d4'),
        'algorithm': ('Algorithm', '#ff6b6b'),
        'db': ('Database', '#336791'),
        'network': ('Network', '#00d4aa'),
        'devops': ('DevOps', '#2496ed'),
        'html-css': ('HTML/CSS', '#e34f26'),
        'ai': ('AI/ML', '#ff6f00'),
        'security': ('Security', '#d63384'),
        'cleancode': ('Clean Code', '#28a745'),
        'collaboration': ('Collaboration', '#6f42c1'),
        'tools': ('Tools', '#495057'),
    }
    for key, (name, color) in categories.items():
        if key in category.lower():
            return name, color
    return category.title(), '#6366F1'

def generate_code_example(title, category):
    """Generate appropriate code example based on title and category"""
    title_lower = title.lower()
    cat_lower = category.lower()

    # Java examples
    if 'java' in cat_lower:
        if 'intro' in title_lower or 'basic' in title_lower:
            return 'java', '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");

        // Variables
        String name = "CodeMaster";
        int number = 42;

        System.out.println("Welcome, " + name);
    }
}'''
        elif 'class' in title_lower or 'object' in title_lower:
            return 'java', '''public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void greet() {
        System.out.println("Hello, I'm " + name);
    }
}

// Usage
Person person = new Person("Kim", 25);
person.greet();'''
        elif 'inherit' in title_lower:
            return 'java', '''class Animal {
    protected String name;

    public void eat() {
        System.out.println(name + " is eating");
    }
}

class Dog extends Animal {
    public Dog(String name) {
        this.name = name;
    }

    @Override
    public void eat() {
        System.out.println(name + " is eating dog food");
    }

    public void bark() {
        System.out.println("Woof!");
    }
}'''
        elif 'interface' in title_lower:
            return 'java', '''public interface Flyable {
    void fly();

    default void land() {
        System.out.println("Landing...");
    }
}

public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("Bird is flying!");
    }
}'''
        elif 'collection' in title_lower or 'list' in title_lower:
            return 'java', '''import java.util.*;

List<String> list = new ArrayList<>();
list.add("Apple");
list.add("Banana");

Set<String> set = new HashSet<>();
set.add("Apple");

Map<String, Integer> map = new HashMap<>();
map.put("Apple", 1000);

// Iteration
for (String item : list) {
    System.out.println(item);
}

map.forEach((k, v) -> System.out.println(k + ": " + v));'''
        elif 'stream' in title_lower:
            return 'java', '''import java.util.stream.*;

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * 2)
    .collect(Collectors.toList());

int sum = numbers.stream()
    .reduce(0, Integer::sum);'''
        elif 'thread' in title_lower:
            return 'java', '''// Thread creation
Thread t = new Thread(() -> {
    System.out.println("Running in thread");
});
t.start();

// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(2);
executor.submit(() -> System.out.println("Task 1"));
executor.shutdown();'''
        elif 'exception' in title_lower:
            return 'java', '''try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero!");
} finally {
    System.out.println("Always executed");
}

// Custom exception
public class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
    }
}'''
        else:
            return 'java', '''public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, World!");

        int x = 10;
        int y = 20;
        int sum = x + y;

        System.out.println("Sum: " + sum);
    }
}'''

    # Python examples
    elif 'python' in cat_lower:
        if 'variable' in title_lower:
            return 'python', '''# Variables
name = "Python"
age = 30
height = 175.5
is_developer = True

# Multiple assignment
x, y, z = 1, 2, 3

# Type checking
print(type(name))  # <class 'str'>

# f-string formatting
message = f"Name: {name}, Age: {age}"
print(message)'''
        elif 'function' in title_lower:
            return 'python', '''def greet(name):
    return f"Hello, {name}!"

# Default parameters
def power(base, exp=2):
    return base ** exp

# *args and **kwargs
def sum_all(*args):
    return sum(args)

# Lambda
square = lambda x: x ** 2

print(greet("CodeMaster"))
print(power(3))  # 9
print(sum_all(1, 2, 3, 4, 5))  # 15'''
        elif 'class' in title_lower:
            return 'python', '''class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def study(self):
        return f"{self.name} is studying"

person = Person("Kim", 25)
student = Student("Lee", 20, "MIT")'''
        else:
            return 'python', '''# Python basics
name = "CodeMaster"
numbers = [1, 2, 3, 4, 5]

# List comprehension
squares = [x**2 for x in numbers]

# Dictionary
person = {"name": "Kim", "age": 25}

# Loop
for num in numbers:
    print(num)

# Function
def greet(name):
    return f"Hello, {name}!"'''

    # Spring examples
    elif 'spring' in cat_lower:
        if 'intro' in title_lower or 'boot' in title_lower:
            return 'java', '''@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }

    @PostMapping
    public User createUser(@RequestBody UserDto dto) {
        return userService.create(dto);
    }
}'''
        elif 'jpa' in title_lower or 'data' in title_lower:
            return 'java', '''@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;
}

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);
}

@Service
@Transactional
public class UserService {
    private final UserRepository userRepository;

    public User create(UserDto dto) {
        return userRepository.save(new User(dto));
    }
}'''
        else:
            return 'java', '''@Service
public class UserService {
    private final UserRepository userRepository;

    // Constructor injection
    public UserService(UserRepository repository) {
        this.userRepository = repository;
    }

    public List<User> findAll() {
        return userRepository.findAll();
    }
}'''

    # React examples
    elif 'react' in cat_lower:
        if 'hook' in title_lower:
            return 'javascript', '''import { useState, useEffect } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        document.title = `Count: ${count}`;
    }, [count]);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}'''
        else:
            return 'javascript', '''function App() {
    return (
        <div className="app">
            <h1>Hello React!</h1>
            <Greeting name="CodeMaster" />
        </div>
    );
}

function Greeting({ name }) {
    return <p>Welcome, {name}!</p>;
}

export default App;'''

    # Algorithm examples
    elif 'algorithm' in cat_lower:
        if 'binary' in title_lower or 'search' in title_lower:
            return 'python', '''def binary_search(arr, target):
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

numbers = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(numbers, 7))  # 3'''
        elif 'sort' in title_lower:
            return 'python', '''# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)'''
        elif 'dfs' in title_lower or 'bfs' in title_lower:
            return 'python', '''from collections import deque

graph = {1: [2, 3], 2: [4, 5], 3: [6], 4: [], 5: [], 6: []}

# DFS
def dfs(node, visited=set()):
    visited.add(node)
    print(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

# BFS
def bfs(start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)'''
        else:
            return 'python', '''# Dynamic Programming - Fibonacci
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

print(fib(100))'''

    # Database examples
    elif 'db' in cat_lower:
        if 'join' in title_lower:
            return 'sql', '''-- INNER JOIN
SELECT u.name, o.product
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN
SELECT u.name, o.order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Subquery
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders WHERE total > 10000
);'''
        else:
            return 'sql', '''-- SELECT
SELECT * FROM users WHERE age >= 20;
SELECT name, email FROM users ORDER BY age DESC LIMIT 10;

-- GROUP BY
SELECT city, COUNT(*) as cnt FROM users GROUP BY city;

-- INSERT
INSERT INTO users (name, email) VALUES ('Kim', 'kim@test.com');

-- UPDATE
UPDATE users SET age = 26 WHERE name = 'Kim';

-- DELETE
DELETE FROM users WHERE id = 1;'''

    # Network examples
    elif 'network' in cat_lower:
        if 'http' in title_lower:
            return 'python', '''import requests

# GET
response = requests.get('https://api.example.com/users')
print(response.json())

# POST
data = {'name': 'Kim', 'email': 'kim@test.com'}
response = requests.post('https://api.example.com/users', json=data)

# Headers
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/me', headers=headers)'''
        else:
            return 'python', '''import socket

# TCP Server
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        data = client.recv(1024)
        client.send(b"Hello from server!")
        client.close()

# TCP Client
def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    client.send(b"Hello!")
    response = client.recv(1024)'''

    # DevOps examples
    elif 'devops' in cat_lower:
        if 'docker' in title_lower:
            return 'dockerfile', '''# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password'''
        elif 'git' in title_lower:
            return 'bash', '''# Basic Git commands
git init
git clone <url>
git status
git add .
git commit -m "message"
git push origin main

# Branch
git checkout -b feature
git merge feature
git branch -d feature

# Undo
git reset --soft HEAD~1
git revert <commit>'''
        else:
            return 'bash', '''# CI/CD pipeline commands
npm install
npm test
npm run build

# Docker
docker build -t myapp .
docker run -p 3000:3000 myapp

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods'''

    # OS examples
    elif 'os' in cat_lower:
        return 'c', '''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("Child PID: %d\\n", getpid());
    } else {
        // Parent process
        printf("Parent PID: %d\\n", getpid());
        wait(NULL);
    }

    return 0;
}'''

    # Default
    return 'javascript', '''// Example code
function hello(name) {
    return `Hello, ${name}!`;
}

const result = hello("CodeMaster");
console.log(result);'''

def create_html(title, category, code_lang, code):
    """Create HTML content"""
    cat_name, cat_color = get_category_info(category)

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - CodeMaster</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Pretendard', -apple-system, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: #e2e8f0; line-height: 1.8; min-height: 100vh;
    }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    .header {{
      background: linear-gradient(135deg, {cat_color}22 0%, {cat_color}11 100%);
      border: 1px solid {cat_color}44;
      border-radius: 20px; padding: 40px; margin-bottom: 32px;
    }}
    .badge {{
      display: inline-block; background: {cat_color};
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
      <span class="badge">{cat_name}</span>
      <h1 class="title">{title}</h1>
      <div class="meta">
        <span>30min</span>
        <span>Beginner~Intermediate</span>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Core Concepts</h2>
      <p style="color: #94a3b8;">Learn the fundamental concepts of {title}.</p>
    </div>

    <div class="section">
      <h2 class="section-title">Code Example</h2>
      <div class="code-block">
        <div class="code-header">{code_lang.upper()}</div>
        <div class="code-content">
          <pre><code>{code}</code></pre>
        </div>
      </div>
      <div class="tip-box">
        <div class="tip-title">Key Point</div>
        <p style="color: #94a3b8;">Try running this code and understand how it works.</p>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Practice</h2>
      <div class="practice-box">
        <h4 class="practice-title">Try it yourself</h4>
        <ol class="practice-list">
          <li>Run the example code above.</li>
          <li>Modify the code to get different results.</li>
          <li>Apply this concept to your own project.</li>
        </ol>
      </div>
    </div>
  </div>
</body>
</html>'''

def process_all():
    """Process all HTML files"""
    count = 0
    for html_file in STUDY_DIR.rglob("*.html"):
        if "index.html" in str(html_file):
            continue

        category = html_file.parent.name
        if category.startswith(('0', '1')):
            category = html_file.parent.parent.name

        title = get_title_from_filename(html_file.name)
        code_lang, code = generate_code_example(title, category)

        html_content = create_html(title, category, code_lang, code)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        count += 1
        if count % 50 == 0:
            print(f"Processed {count} files...")

    print(f"\nComplete: {count} files updated")

if __name__ == "__main__":
    process_all()
