import os
import random

# 프로젝트 루트 경로 (현재 위치 기준)
BASE_DIR = "./public/study"

# 언어별 템플릿 데이터베이스
TEMPLATES = {
    "python": {
        "lang": "Python",
        "code": "def solve():\n    data = [1, 2, 3, 4, 5]\n    result = [x * 2 for x in data]\n    print(f'Result: {result}')\n\nif __name__ == '__main__':\n    solve()",
        "desc": "Python의 강력한 기능을 활용하여 {topic} 문제를 해결하는 효율적인 방법을 학습합니다."
    },
    "java": {
        "lang": "Java",
        "code": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Learning {topic} with Java\");\n        // TODO: Implement logic here\n    }\n}",
        "desc": "Java의 객체지향 특성을 살려 {topic} 구조를 설계하고 구현하는 방법을 익힙니다."
    },
    "javascript": {
        "lang": "JavaScript",
        "code": "const process = (data) => {\n    console.log(`Processing ${data} for {topic}...`);\n};\n\nprocess('Sample Data');",
        "desc": "JavaScript의 비동기 처리와 유연한 문법을 통해 {topic} 기능을 웹 환경에서 구현합니다."
    },
    "react": {
        "lang": "TypeScript (React)",
        "code": "import React, { useState } from 'react';\n\nexport default function {topic}Component() {\n    const [state, setState] = useState(0);\n    return <div>{topic} Demo</div>;\n}",
        "desc": "React의 컴포넌트 기반 아키텍처를 이해하고 {topic} 기능을 UI로 구현합니다."
    },
    "sql": {
        "lang": "SQL",
        "code": "SELECT * \nFROM users \nWHERE status = 'ACTIVE' \nAND topic = '{topic}';",
        "desc": "데이터베이스에서 {topic} 관련 데이터를 효율적으로 조회하고 관리하는 쿼리를 작성합니다."
    },
    "html": {
        "lang": "HTML",
        "code": "<div class=\"container\">\n    <h1>{topic}</h1>\n    <p>Understanding the structure.</p>\n</div>",
        "desc": "웹 표준을 준수하며 {topic} 요소를 사용하여 시멘틱한 웹 구조를 설계합니다."
    },
    "default": {
        "lang": "Text",
        "code": "# {topic} 예제\n개념을 이해하고 실습을 통해 익혀봅시다.",
        "desc": "{topic}의 핵심 개념을 파악하고 실무에 적용하는 방법을 심도 있게 학습합니다."
    }
}

def detect_type(path):
    path = path.lower()
    if "java" in path or "spring" in path: return "java"
    if "python" in path or "ai" in path or "numpy" in path: return "python"
    if "react" in path or "next" in path: return "react"
    if "js" in path or "javascript" in path or "node" in path: return "javascript"
    if "sql" in path or "db" in path: return "sql"
    if "html" in path or "css" in path: return "html"
    return "default"

def get_html_content(title, file_type):
    template = TEMPLATES.get(file_type, TEMPLATES["default"])
    clean_title = title.replace("-", " ").replace("_", " ").title().replace(".Html", "")
    
    # 제목에 맞는 동적 설명 생성
    description = template["desc"].format(topic=clean_title)
    code_snippet = template["code"].format(topic=clean_title)
    
    return f"""
<div class="prose max-w-none">
    <h1 class="text-3xl font-bold mb-4">{clean_title}</h1>
    <div class="flex gap-2 mb-6">
        <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">15분</span>
        <span class="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">초급~중급</span>
        <span class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm">{template['lang']}</span>
    </div>

    <h2 class="text-2xl font-semibold mt-8 mb-4">학습 목표</h2>
    <p class="mb-4 text-gray-700">
        이번 시간에는 <strong>{clean_title}</strong>에 대해 깊이 있게 다룹니다. 
        {description}
        이론적인 배경부터 시작하여 실제 동작하는 코드를 작성해보며 원리를 깨우치는 것이 목표입니다.
    </p>

    <div class="my-8 p-4 bg-gray-50 border-l-4 border-blue-500">
        <p class="font-medium">💡 핵심 포인트</p>
        <ul class="list-disc ml-4 mt-2 space-y-1 text-gray-600">
            <li>{clean_title}의 정의와 중요성 이해</li>
            <li>실무에서 자주 사용되는 패턴 학습</li>
            <li>직접 코드를 작성하며 트러블슈팅 능력 배양</li>
        </ul>
    </div>

    <h2 class="text-2xl font-semibold mt-8 mb-4">예제 코드</h2>
    <p class="mb-4">아래는 {clean_title}의 기본적인 구현 예제입니다.</p>
    <pre class="bg-gray-900 text-white p-4 rounded-lg overflow-x-auto"><code>{code_snippet}</code></pre>

    <h2 class="text-2xl font-semibold mt-8 mb-4">실전 연습</h2>
    <p class="mb-4">
        위 코드를 바탕으로 다음 과제를 수행해보세요:
    </p>
    <ol class="list-decimal ml-6 space-y-2 text-gray-700">
        <li>위 코드를 로컬 환경에서 실행하여 결과를 확인하세요.</li>
        <li>입력 값을 변경하여 결과가 어떻게 달라지는지 관찰하세요.</li>
        <li>자신만의 기능을 추가하여 코드를 확장해보세요.</li>
    </ol>
</div>
"""

def smart_fill():
    count = 0
    print("🚀 지능형 컨텐츠 분석 및 생성 시작...")
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # 파일 타입 분석 (Python? Java? React?)
                file_type = detect_type(file_path)
                
                # 컨텐츠 생성
                new_content = get_html_content(file, file_type)
                
                # 파일 쓰기
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ [{file_type.upper()}] 업데이트: {file}")
                    count += 1
                except Exception as e:
                    print(f"❌ 실패: {file} - {e}")

    print(f"\n🎉 총 {count}개의 파일이 스마트하게 업데이트 되었습니다!")

if __name__ == "__main__":
    smart_fill()