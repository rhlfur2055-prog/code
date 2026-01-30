import os
from pathlib import Path

# ==========================================
# 1. 콘텐츠 데이터베이스 (정밀 매핑)
# ==========================================
CONTENT_DB = {
    # ---------------- PYTHON ----------------
    "python_basic": {
        "title": "Python 기초 문법",
        "desc": "Python의 변수, 자료형, 기본 입출력을 학습합니다.",
        "code": """# 변수와 자료형
name = "CodeMaster"  # 문자열
age = 25             # 정수
is_active = True     # 불리언
rating = 4.5         # 실수

# 출력 formatting
print(f"이름: {name}, 나이: {age}")

# 리스트 기본
skills = ["Python", "Java", "SQL"]
skills.append("Git")
print(skills[0])  # Python""",
        "lang": "Python"
    },
    "python_flow": {
        "title": "Python 제어문",
        "desc": "if 조건문과 for, while 반복문의 다양한 패턴을 익힙니다.",
        "code": """score = 85

# 조건문
if score >= 90:
    print("A학점")
elif score >= 80:
    print("B학점")
else:
    print("재수강")

# 반복문 (List Comprehension)
numbers = [1, 2, 3, 4, 5]
squares = [n ** 2 for n in numbers if n % 2 != 0]
print(f"홀수의 제곱: {squares}")""",
        "lang": "Python"
    },
    "python_pandas": {
        "title": "Pandas 데이터 분석",
        "desc": "데이터프레임을 생성하고 조작하는 핵심 기법을 다룹니다.",
        "code": """import pandas as pd

data = {
    'name': ['Kim', 'Lee', 'Park'],
    'age': [25, 30, 22],
    'city': ['Seoul', 'Busan', 'Incheon']
}

# DataFrame 생성
df = pd.read_csv('data.csv') # 또는 pd.DataFrame(data)

# 데이터 조회
print(df.head())
print(df.describe())

# 필터링
adults = df[df['age'] >= 20]
print(adults)""",
        "lang": "Python"
    },
    
    # ---------------- JAVA ----------------
    "java_basic": {
        "title": "Java 기본 문법",
        "desc": "Java의 타입 시스템과 변수 선언, 연산자 활용을 학습합니다.",
        "code": """public class Main {
    public static void main(String[] args) {
        // 기본 자료형
        int number = 10;
        double pi = 3.14;
        boolean isJavaFun = true;
        
        // 참조 자료형 (String)
        String message = "Hello CodeMaster!";
        
        System.out.println(message);
        System.out.println("점수: " + number);
    }
}""",
        "lang": "Java"
    },
    "java_oop": {
        "title": "Java 객체지향 프로그래밍",
        "desc": "클래스, 객체, 상속, 다형성의 원리를 코드로 이해합니다.",
        "code": """// 부모 클래스
class Animal {
    void sound() {
        System.out.println("동물 소리");
    }
}

// 상속과 오버라이딩
class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("멍멍!");
    }
}

public class Main {
    public static void main(String[] args) {
        Animal myDog = new Dog(); // 다형성
        myDog.sound(); // "멍멍!" 출력
    }
}""",
        "lang": "Java"
    },
    
    # ---------------- SPRING ----------------
    "spring_core": {
        "title": "Spring DI & IoC",
        "desc": "스프링 컨테이너가 빈(Bean)을 관리하고 주입하는 원리를 배웁니다.",
        "code": """@Service
public class UserService {
    
    private final UserRepository userRepository;

    // 생성자 주입 (권장)
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findUser(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));
    }
}""",
        "lang": "Java"
    },
    "spring_web": {
        "title": "Spring Web MVC",
        "desc": "REST Controller를 생성하고 HTTP 요청을 처리하는 방법입니다.",
        "code": """@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        UserDto user = userService.getUser(id);
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<Void> createUser(@RequestBody UserDto dto) {
        userService.save(dto);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}""",
        "lang": "Java"
    },

    # ---------------- REACT ----------------
    "react_basic": {
        "title": "React 컴포넌트 기초",
        "desc": "JSX 문법과 함수형 컴포넌트의 구조를 이해합니다.",
        "code": """import React from 'react';

function Welcome({ name }) {
  return (
    <div className="card">
      <h1>Hello, {name}!</h1>
      <p>React의 세계에 오신 것을 환영합니다.</p>
    </div>
  );
}

export default function App() {
  return <Welcome name="Developer" />;
}""",
        "lang": "JavaScript"
    },
    "react_hooks": {
        "title": "React Hooks (useState, useEffect)",
        "desc": "상태 관리와 사이드 이펙트 처리를 위한 Hooks 사용법입니다.",
        "code": """import { useState, useEffect } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `현재 카운트: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        증가
      </button>
    </div>
  );
}""",
        "lang": "JavaScript"
    },

    # ---------------- ALGORITHM ----------------
    "algo_bfs_dfs": {
        "title": "BFS / DFS 탐색",
        "desc": "그래프 탐색의 기본인 너비 우선 탐색과 깊이 우선 탐색 구현입니다.",
        "code": """from collections import deque

# BFS (너비 우선 탐색)
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        n = queue.popleft()
        print(n, end=' ')
        
        for neighbor in graph[n]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

# DFS (깊이 우선 탐색)
def dfs(graph, v, visited):
    visited[v] = True
    print(v, end=' ')
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)""",
        "lang": "Python"
    },
    
    # ---------------- SQL ----------------
    "sql_basic": {
        "title": "SQL 기초 (SELECT, INSERT)",
        "desc": "데이터베이스에서 데이터를 조회하고 생성하는 쿼리문입니다.",
        "code": """-- 데이터 조회
SELECT id, name, email 
FROM users 
WHERE created_at > '2024-01-01'
ORDER BY name ASC;

-- 데이터 삽입
INSERT INTO users (name, email, age)
VALUES ('Hong GilDong', 'hong@example.com', 28);""",
        "lang": "SQL"
    },
    
    "default": {
        "title": "학습 주제",
        "desc": "이 주제에 대한 심도 있는 학습과 실습을 진행합니다.",
        "code": "// 여기에 실습 코드를 작성하며 학습하세요.\nconsole.log('Ready to code!');",
        "lang": "Text"
    }
}

# ==========================================
# 2. 로직 (경로 + 파일명 -> 최적의 콘텐츠 매칭)
# ==========================================
def get_best_content(filepath):
    path_str = str(filepath).lower().replace('\\', '/')
    filename = filepath.name.lower()
    
    # 1. Spring (우선순위 높음)
    if "spring" in path_str:
        if any(k in filename for k in ["mvc", "controller", "rest", "api"]): return CONTENT_DB["spring_web"]
        if any(k in filename for k in ["security", "auth", "login"]): return CONTENT_DB["spring_core"] # 보안 템플릿 있다면 교체
        if any(k in filename for k in ["data", "jpa", "db", "repository"]): return CONTENT_DB["spring_core"] # JPA 템플릿 있다면 교체
        return CONTENT_DB["spring_core"]

    # 2. Java (Spring이 아닌 순수 자바)
    if "java" in path_str:
        if any(k in filename for k in ["oop", "class", "interface", "extends"]): return CONTENT_DB["java_oop"]
        if any(k in filename for k in ["basic", "intro", "variable", "syntax"]): return CONTENT_DB["java_basic"]
        return CONTENT_DB["java_basic"]

    # 3. Python (AI, Numpy 등 포함)
    if "python" in path_str or "ai" in path_str:
        if any(k in filename for k in ["pandas", "dataframe", "analysis"]): return CONTENT_DB["python_pandas"]
        if any(k in filename for k in ["basic", "variable", "print", "setup"]): return CONTENT_DB["python_basic"]
        if any(k in filename for k in ["flow", "if", "loop", "control"]): return CONTENT_DB["python_flow"]
        return CONTENT_DB["python_basic"] # 기본값

    # 4. React / JS
    if "react" in path_str or "javascript" in path_str or "js" in path_str:
        if any(k in filename for k in ["hook", "effect", "state"]): return CONTENT_DB["react_hooks"]
        if any(k in filename for k in ["basic", "intro", "component", "jsx"]): return CONTENT_DB["react_basic"]
        return CONTENT_DB["react_basic"]

    # 5. Algorithm
    if "algorithm" in path_str or "coding" in path_str:
        if any(k in filename for k in ["bfs", "dfs", "search", "graph"]): return CONTENT_DB["algo_bfs_dfs"]
        # 정렬, 스택/큐 등 추가 가능
        return CONTENT_DB["algo_bfs_dfs"] # 임시 기본값

    # 6. Database
    if "db" in path_str or "sql" in path_str:
        return CONTENT_DB["sql_basic"]

    return CONTENT_DB["default"]

def generate_html(filepath, content_data):
    # 파일명에서 타이틀 추출 (ex: java-basic-syntax.html -> Java Basic Syntax)
    display_title = filepath.stem.replace("-", " ").replace("_", " ").title()
    
    # HTML 템플릿
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{display_title} - 코드마스터</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Pretendard', -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #e2e8f0; line-height: 1.8; min-height: 100vh; }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    .header {{ background: linear-gradient(135deg, #3b82f622 0%, #3b82f611 100%); border: 1px solid #3b82f644; border-radius: 20px; padding: 40px; margin-bottom: 32px; }}
    .badge {{ display: inline-block; background: #3b82f6; color: white; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; margin-bottom: 16px; }}
    .title {{ font-size: 32px; font-weight: 800; margin-bottom: 16px; color: #fff; }}
    .meta {{ display: flex; gap: 16px; color: #94a3b8; font-size: 14px; }}
    .section {{ background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 32px; margin-bottom: 24px; }}
    .section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #fff; border-left: 4px solid #3b82f6; padding-left: 12px; }}
    .code-block {{ background: #0f172a; border: 1px solid #334155; border-radius: 12px; overflow: hidden; margin-top: 16px; }}
    .code-header {{ background: #1e293b; padding: 12px 20px; font-size: 14px; color: #94a3b8; border-bottom: 1px solid #334155; font-family: monospace; }}
    .code-content {{ padding: 20px; overflow-x: auto; color: #a5b4fc; font-family: 'JetBrains Mono', monospace; font-size: 14px; line-height: 1.6; }}
    .tip-box {{ background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 20px; margin-top: 24px; }}
    .tip-title {{ color: #10b981; font-weight: 700; margin-bottom: 8px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{content_data['lang']}</span>
      <h1 class="title">{display_title}</h1>
      <div class="meta">
        <span>⏱ 30분</span>
        <span>📊 난이도: 초급~중급</span>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">학습 목표</h2>
      <p style="color: #cbd5e1; font-size: 1.1rem;">
        이번 시간에는 <strong>{display_title}</strong>에 대해 학습합니다.<br>
        {content_data['desc']}
      </p>
    </div>

    <div class="section">
      <h2 class="section-title">핵심 예제</h2>
      <p>아래 코드를 직접 작성하고 실행 결과를 확인해보세요.</p>
      <div class="code-block">
        <div class="code-header">{display_title}.{content_data['lang'].lower()}</div>
        <pre class="code-content">{content_data['code']}</pre>
      </div>
      
      <div class="tip-box">
        <div class="tip-title">💡 핵심 포인트</div>
        <ul style="padding-left: 20px; color: #cbd5e1;">
            <li>코드를 복사하지 말고 직접 타이핑해보세요.</li>
            <li>변수 값을 변경하여 결과가 어떻게 달라지는지 확인하세요.</li>
            <li>에러가 발생하면 에러 메시지를 읽고 수정해보세요.</li>
        </ul>
      </div>
    </div>
  </div>
</body>
</html>"""

def main():
    base_dir = Path("./public/study")
    count = 0
    
    print("🚀 [Master Content Gen] 시작: 모든 파일을 정밀 분석하여 컨텐츠를 교체합니다...")
    
    for html_file in base_dir.rglob("*.html"):
        if html_file.name == "index.html": continue
        
        # 1. 파일 분석 및 컨텐츠 매핑
        content_data = get_best_content(html_file)
        
        # 2. HTML 생성
        new_html = generate_html(html_file, content_data)
        
        # 3. 쓰기
        try:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1
            # 진행상황 표시 (너무 많으니 50개마다)
            if count % 50 == 0:
                print(f"   ...{count}개 파일 처리 완료")
        except Exception as e:
            print(f"❌ 오류 발생: {html_file} - {e}")

    print(f"\n🎉 작업 완료! 총 {count}개의 파일이 '진짜' 관련 내용으로 채워졌습니다.")
    print("이제 'npm run dev'로 확인해보세요.")

if __name__ == "__main__":
    main()