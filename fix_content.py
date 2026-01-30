import os
import re

# 파일 성격에 맞는 진짜 콘텐츠 사전
CONTENTS = {
    "spring": {
        "lang": "Java",
        "desc": "Spring Framework의 의존성 주입(DI)과 제어 역전(IoC) 원리를 심도 있게 학습합니다.",
        "code": """@RestController
@RequestMapping("/api/v1")
public class ArticleController {
    private final ArticleService articleService;

    public ArticleController(ArticleService articleService) {
        this.articleService = articleService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Article> getArticle(@PathVariable Long id) {
        return ResponseEntity.ok(articleService.findById(id));
    }
}"""
    },
    "yml": {
        "lang": "YAML",
        "desc": "Spring Boot의 프로필별 환경 설정과 리소스 관리 방법을 다룹니다.",
        "code": """spring:
  profiles:
    active: dev
  datasource:
    url: jdbc:mysql://localhost:3306/dev_db
    username: dev_user
    password: dev_password
server:
  port: 8080"""
    },
    "python": {
        "lang": "Python",
        "desc": "Python의 강력한 라이브러리를 활용하여 데이터 분석 및 자동화 스크립트를 구현합니다.",
        "code": """import pandas as pd
from sklearn.model_selection import train_test_split

def process_data(filepath):
    df = pd.read_csv(filepath)
    # 결측치 처리
    df = df.dropna()
    return df

if __name__ == "__main__":
    data = process_data('dataset.csv')
    print(f"Data processed: {len(data)} rows")"""
    },
    "react": {
        "lang": "TypeScript",
        "desc": "React Hooks와 상태 관리 라이브러리를 사용하여 모던 웹 애플리케이션을 구축합니다.",
        "code": """import React, { useState, useEffect } from 'react';

interface UserProps {
  userId: string;
}

export const UserProfile: React.FC<UserProps> = ({ userId }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      setUser(data);
    }
    fetchData();
  }, [userId]);

  if (!user) return <div>Loading...</div>;
  return <h1>Hello, {user.name}</h1>;
};"""
    },
    "sql": {
        "lang": "SQL",
        "desc": "복잡한 데이터 관계를 쿼리로 효율적으로 조회하고 인덱싱을 통해 성능을 최적화합니다.",
        "code": """SELECT p.product_name, SUM(o.quantity) as total_sales
FROM products p
JOIN order_items o ON p.id = o.product_id
JOIN orders ord ON o.order_id = ord.id
WHERE ord.order_date >= '2024-01-01'
GROUP BY p.id
HAVING total_sales > 100
ORDER BY total_sales DESC;"""
    },
    "docker": {
        "lang": "Dockerfile",
        "desc": "컨테이너 가상화 기술을 사용하여 애플리케이션의 배포 및 실행 환경을 표준화합니다.",
        "code": """FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
    }
}

def get_content_by_path(path):
    p = path.lower()
    if "spring" in p or "java" in p: return CONTENTS["spring"]
    if "yml" in p or "yaml" in p: return CONTENTS["yml"]
    if "react" in p or "next" in p or "js" in p: return CONTENTS["react"]
    if "db" in p or "sql" in p: return CONTENTS["sql"]
    if "docker" in p or "k8s" in p: return CONTENTS["docker"]
    return CONTENTS["python"]

def fix_files(start_dir):
    if not os.path.exists(start_dir):
        print(f"❌ 오류: '{start_dir}' 폴더를 찾을 수 없습니다.")
        return

    count = 0
    # 잘못된 템플릿 텍스트 패턴
    target_pattern = r"기본 개념과 활용법을 학습합니다"
    
    print(f"🚀 콘텐츠 심폐소생 시작: {start_dir}")

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 내용 교체가 필요한 파일인지 확인
                    if re.search(target_pattern, content) or "import numpy as np" in content:
                        new_data = get_content_by_path(path)
                        
                        # 1. 설명 텍스트 교체
                        new_content = re.sub(target_pattern + r"\.", new_data["desc"], content)
                        new_content = re.sub(target_pattern, new_data["desc"], new_content)
                        
                        # 2. 코드 블록 교체 (<code> 태그 내부)
                        # 간단한 패턴 매칭으로 코드 부분만 싹 바꿈
                        code_regex = r"(<code[^>]*>)([\s\S]*?)(</code>)"
                        if re.search(code_regex, new_content):
                            replacement = f"\\1\n{new_data['code']}\n\\3"
                            new_content = re.sub(code_regex, replacement, new_content)
                        
                        # 파일 저장
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ 수정됨: {file} ({new_data['lang']})")
                        count += 1
                except Exception as e:
                    print(f"⚠️ 읽기 실패: {path} - {e}")

    print(f"\n🎉 작업 완료! 총 {count}개의 파일 내용을 채웠습니다.")

# 실행
if __name__ == "__main__":
    # 실제 경로에 맞게 public/study 지정
    fix_files("./public/study")