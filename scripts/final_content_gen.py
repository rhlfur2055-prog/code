import os
from pathlib import Path

# ==========================================
# 주제별 맞춤 콘텐츠 데이터베이스 (All-in-One)
# ==========================================
CONTENT_DB = {
    # --- 네트워크 (Network) ---
    "network_tcp": { "title": "TCP/IP 4계층과 통신", "lang": "Python", "code": "import socket\n\n# TCP 소켓 생성 예제\nserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nserver_socket.bind(('127.0.0.1', 8080))\nserver_socket.listen()", "desc": "TCP/IP 프로토콜의 계층별 역할과 핸드셰이킹 과정을 학습합니다." },
    "network_http": { "title": "HTTP 프로토콜과 REST", "lang": "JavaScript", "code": "fetch('https://api.example.com/data', {\n  method: 'GET',\n  headers: { 'Content-Type': 'application/json' }\n})\n.then(res => res.json())\n.then(data => console.log(data));", "desc": "HTTP 메서드(GET, POST)와 상태 코드, 헤더 구조를 이해합니다." },
    
    # --- 운영체제 (OS) ---
    "os_process": { "title": "프로세스와 스레드", "lang": "C", "code": "#include <pthread.h>\n\nvoid* thread_func(void* arg) {\n    printf(\"Thread Running\\n\");\n    return NULL;\n}\n\nint main() {\n    pthread_t thread;\n    pthread_create(&thread, NULL, thread_func, NULL);\n    pthread_join(thread, NULL);\n    return 0;\n}", "desc": "프로세스 메모리 구조와 스레드 간의 컨텍스트 스위칭 원리를 파악합니다." },
    "os_memory": { "title": "메모리 관리와 가상 메모리", "lang": "C", "code": "// 동적 메모리 할당 예제\nint *ptr = (int*)malloc(sizeof(int) * 10);\nif (ptr != NULL) {\n    // 메모리 사용\n    free(ptr);\n}", "desc": "페이징, 세그멘테이션 및 페이지 교체 알고리즘을 학습합니다." },

    # --- 데이터베이스 (DB) ---
    "db_sql": { "title": "SQL 기본 및 조인", "lang": "SQL", "code": "SELECT u.name, o.order_date\nFROM users u\nJOIN orders o ON u.id = o.user_id\nWHERE u.active = 1;", "desc": "CRUD 쿼리 작성법과 다양한 JOIN 기법을 실습합니다." },
    "db_optimization": { "title": "인덱스와 쿼리 튜닝", "lang": "SQL", "code": "CREATE INDEX idx_user_email ON users(email);\n-- 실행 계획 확인\nEXPLAIN SELECT * FROM users WHERE email = 'test@test.com';", "desc": "인덱스 작동 원리와 실행 계획(Explain)을 통한 최적화를 다룹니다." },

    # --- 보안 (Security) ---
    "security_web": { "title": "웹 보안 (XSS, CSRF)", "lang": "Java", "code": "@Configuration\npublic class SecurityConfig {\n    @Bean\n    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {\n        http.csrf().disable(); // 개발 환경 설정\n        return http.build();\n    }\n}", "desc": "OWASP Top 10 취약점과 방어 코딩 기법을 학습합니다." },
    
    # --- 알고리즘 (Algorithm) ---
    "algo_basic": { "title": "기초 알고리즘", "lang": "Python", "code": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1", "desc": "정렬, 탐색 등 필수 알고리즘의 시간 복잡도와 구현을 익힙니다." },

    # --- 기존 언어들 ---
    "python_basic": { "title": "Python 기초", "lang": "Python", "code": "name = 'CodeMaster'\nprint(f'Hello, {name}')", "desc": "Python 변수, 제어문 기초입니다." },
    "java_basic": { "title": "Java 기초", "lang": "Java", "code": "public class Main {\n  public static void main(String[] args) {\n    System.out.println(\"Hello Java\");\n  }\n}", "desc": "Java 클래스와 메인 메서드 구조입니다." },
    "spring_core": { "title": "Spring Core", "lang": "Java", "code": "@Service\npublic class MyService {}", "desc": "스프링 빈과 DI 원리입니다." },
    "react_core": { "title": "React 기초", "lang": "JavaScript", "code": "export default function App() {\n  return <h1>Hello React</h1>\n}", "desc": "컴포넌트와 JSX 기초입니다." },
    
    "default": { "title": "심화 학습", "lang": "Text", "code": "// 예제 코드를 작성하며 학습하세요.", "desc": "해당 주제의 핵심 원리를 깊이 있게 탐구합니다." }
}

def get_content_by_path(path_str):
    p = path_str.lower()
    # 1. Network
    if "network" in p:
        if any(x in p for x in ["http", "rest", "web"]): return CONTENT_DB["network_http"]
        return CONTENT_DB["network_tcp"]
    # 2. OS
    if "os" in p:
        if "memory" in p: return CONTENT_DB["os_memory"]
        return CONTENT_DB["os_process"]
    # 3. DB
    if "db" in p or "sql" in p:
        if any(x in p for x in ["index", "tuning", "optimiz"]): return CONTENT_DB["db_optimization"]
        return CONTENT_DB["db_sql"]
    # 4. Security
    if "security" in p: return CONTENT_DB["security_web"]
    # 5. Algorithm
    if "algorithm" in p or "coding" in p: return CONTENT_DB["algo_basic"]
    
    # 6. Basic Langs
    if "spring" in p: return CONTENT_DB["spring_core"]
    if "java" in p: return CONTENT_DB["java_basic"]
    if "python" in p or "ai" in p: return CONTENT_DB["python_basic"]
    if "react" in p or "js" in p: return CONTENT_DB["react_core"]
    
    return CONTENT_DB["default"]

def generate_html(filepath, content):
    title = filepath.stem.replace("-", " ").replace("_", " ").title()
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 코드마스터</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Pretendard', sans-serif; background: #1a1a2e; color: #e2e8f0; line-height: 1.6; padding: 20px; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #fff; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }}
    .badge {{ background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }}
    pre {{ background: #0f172a; padding: 15px; border-radius: 8px; overflow-x: auto; color: #a5b4fc; }}
    .desc {{ background: #1e293b; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">{content['lang']}</span>
    <h1>{title}</h1>
    <div class="desc">
      <h3>학습 목표</h3>
      <p>{content['desc']}</p>
    </div>
    <h3>예제 코드</h3>
    <pre><code>{content['code']}</code></pre>
  </div>
</body>
</html>"""

def main():
    base_dir = Path("./public/study")
    count = 0
    print("🚀 [Final Generator] 모든 과목(네트워크, OS 포함) 컨텐츠 생성 시작...")
    
    for html_file in base_dir.rglob("*.html"):
        if html_file.name == "index.html": continue
        
        content = get_content_by_path(str(html_file))
        try:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(generate_html(html_file, content))
            count += 1
        except Exception as e:
            print(f"Error: {e}")

    print(f"\n🎉 100% 완료! 총 {count}개의 파일이 완벽하게 채워졌습니다.")

if __name__ == "__main__":
    main()