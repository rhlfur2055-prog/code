/**
 * 40일 커리큘럼 데이터
 * 30일 기존 + 10일 추가 (HTML/CSS, JavaScript, React, AI 활용)
 */

export interface DayContent {
  day: number;
  title: string;
  category: string;
  topics: string[];
  files: string[];
}

export const curriculum: DayContent[] = [
  // Day 1-7: Java
  { day: 1, title: "Java 기초 1", category: "java", topics: ["변수", "자료형", "연산자"], files: ["java_basics_1.html"] },
  { day: 2, title: "Java 기초 2", category: "java", topics: ["조건문", "반복문"], files: ["java_basics_2.html"] },
  { day: 3, title: "Java 객체지향 1", category: "java", topics: ["클래스", "객체", "생성자"], files: ["java_oop_1.html"] },
  { day: 4, title: "Java 객체지향 2", category: "java", topics: ["상속", "다형성"], files: ["java_oop_2.html"] },
  { day: 5, title: "Java 객체지향 3", category: "java", topics: ["추상클래스", "인터페이스"], files: ["java_oop_3.html"] },
  { day: 6, title: "Java 컬렉션", category: "java", topics: ["List", "Map", "Set"], files: ["java_collections.html"] },
  { day: 7, title: "Java 고급", category: "java", topics: ["예외처리", "스트림", "람다"], files: ["java_advanced.html"] },

  // Day 8-14: Spring Boot
  { day: 8, title: "Spring Boot 시작", category: "spring", topics: ["프로젝트 생성", "구조 이해"], files: ["spring_start.html"] },
  { day: 9, title: "Controller & REST API", category: "spring", topics: ["@RestController", "HTTP 메서드"], files: ["spring_controller.html"] },
  { day: 10, title: "Service & ServiceImpl", category: "spring", topics: ["인터페이스", "구현체", "DI"], files: ["service_impl_pattern.html"] },
  { day: 11, title: "MyBatis 기초", category: "spring", topics: ["XML 매퍼", "동적 쿼리"], files: ["mybatis_basics.html"] },
  { day: 12, title: "MyBatis vs JPA", category: "spring", topics: ["차이점", "선택 기준"], files: ["mybatis_vs_jpa.html"] },
  { day: 13, title: "Mustache & Thymeleaf", category: "spring", topics: ["템플릿 엔진", "차이점"], files: ["mybatis_vs_mustache.html"] },
  { day: 14, title: "Spring Boot 실전", category: "spring", topics: ["CRUD 프로젝트", "점수 계산 API"], files: ["spring_project.html"] },

  // Day 15-17: Python
  { day: 15, title: "Python 기초", category: "python", topics: ["변수", "자료형", "조건문"], files: ["python_basics.html"] },
  { day: 16, title: "Python 함수 & 클래스", category: "python", topics: ["함수", "클래스", "모듈"], files: ["python_functions.html"] },
  { day: 17, title: "Python 점수 계산", category: "python", topics: ["실습 프로젝트"], files: ["python_score.html", "score_calculator.py"] },

  // Day 18-21: Algorithm
  { day: 18, title: "자료구조 기초", category: "algorithm", topics: ["배열", "연결리스트", "스택", "큐"], files: ["ds_basics.html"] },
  { day: 19, title: "정렬 알고리즘", category: "algorithm", topics: ["버블", "선택", "삽입", "퀵"], files: ["sorting.html"] },
  { day: 20, title: "탐색 알고리즘", category: "algorithm", topics: ["선형", "이진", "해시"], files: ["searching.html"] },
  { day: 21, title: "알고리즘 실전", category: "algorithm", topics: ["코딩테스트 유형"], files: ["algorithm_practice.html"] },

  // Day 22-23: Database
  { day: 22, title: "SQL 기초", category: "database", topics: ["SELECT", "JOIN", "서브쿼리"], files: ["sql_basics.html"] },
  { day: 23, title: "DB 설계", category: "database", topics: ["정규화", "인덱스", "트랜잭션"], files: ["db_design.html"] },

  // Day 24-27: CS 기초
  { day: 24, title: "네트워크", category: "network", topics: ["HTTP", "TCP/IP", "REST"], files: ["network.html"] },
  { day: 25, title: "운영체제", category: "os", topics: ["프로세스", "스레드", "메모리"], files: ["os.html"] },
  { day: 26, title: "클린코드", category: "cleancode", topics: ["명명규칙", "함수", "주석"], files: ["cleancode.html"] },
  { day: 27, title: "보안", category: "security", topics: ["인증", "암호화", "OWASP"], files: ["security.html"] },

  // Day 28-30: DevOps & Tools
  { day: 28, title: "Docker", category: "devops", topics: ["컨테이너", "이미지", "Compose"], files: ["docker.html"] },
  { day: 29, title: "개발 도구", category: "tools", topics: ["IDE", "디버깅", "프로파일링"], files: ["tools.html"] },
  { day: 30, title: "Git & 협업", category: "git", topics: ["브랜치", "PR", "코드리뷰"], files: ["git.html"] },

  // Day 31-33: HTML/CSS (신규)
  { day: 31, title: "HTML 기초", category: "html-css", topics: ["태그", "구조", "폼"], files: ["01_html_basics.html"] },
  { day: 32, title: "CSS 기초", category: "html-css", topics: ["선택자", "박스모델", "Flexbox"], files: ["02_css_basics.html", "03_flexbox.html"] },
  { day: 33, title: "레이아웃", category: "html-css", topics: ["Grid", "반응형"], files: ["04_grid.html", "05_responsive.html"] },

  // Day 34-36: JavaScript (신규)
  { day: 34, title: "JavaScript 기초", category: "javascript", topics: ["변수", "함수", "객체"], files: ["01_basics.html", "02_functions.html"] },
  { day: 35, title: "DOM 조작", category: "javascript", topics: ["선택자", "이벤트", "동적 생성"], files: ["03_dom.html"] },
  { day: 36, title: "비동기 & API", category: "javascript", topics: ["Promise", "async/await", "fetch"], files: ["04_async.html", "05_es6.html"] },

  // Day 37-38: React (신규)
  { day: 37, title: "React 기초", category: "react", topics: ["컴포넌트", "Props", "State"], files: ["01_basics.html", "02_state.html"] },
  { day: 38, title: "React Hooks", category: "react", topics: ["useState", "useEffect", "Custom Hooks"], files: ["03_hooks.html", "04_practice.html"] },

  // Day 39-40: AI 활용 (신규)
  { day: 39, title: "AI 기초 & 연동", category: "ai", topics: ["YOLO", "Whisper", "API 연동"], files: ["ai/ai_basics.html"] },
  { day: 40, title: "풀스택 AI 프로젝트", category: "ai", topics: ["React + Spring + Python AI"], files: ["ai/ai_fullstack.html"] },
];

export const categories = [
  { id: "java", name: "Java", icon: "☕", color: "#ED8B00", days: "1-7" },
  { id: "spring", name: "Spring Boot", icon: "🍃", color: "#6DB33F", days: "8-14" },
  { id: "python", name: "Python", icon: "🐍", color: "#3776AB", days: "15-17" },
  { id: "algorithm", name: "Algorithm", icon: "📊", color: "#FF6B6B", days: "18-21" },
  { id: "database", name: "Database", icon: "🗄️", color: "#336791", days: "22-23" },
  { id: "network", name: "Network", icon: "📡", color: "#4ECDC4", days: "24" },
  { id: "os", name: "OS", icon: "💻", color: "#9B59B6", days: "25" },
  { id: "cleancode", name: "CleanCode", icon: "📝", color: "#2ECC71", days: "26" },
  { id: "security", name: "Security", icon: "🔒", color: "#E74C3C", days: "27" },
  { id: "devops", name: "DevOps", icon: "🐳", color: "#2496ED", days: "28" },
  { id: "tools", name: "Tools", icon: "🛠️", color: "#F39C12", days: "29" },
  { id: "git", name: "Git", icon: "👥", color: "#F05032", days: "30" },
  { id: "html-css", name: "HTML/CSS", icon: "🌐", color: "#E34F26", days: "31-33" },
  { id: "javascript", name: "JavaScript", icon: "⚡", color: "#F7DF1E", days: "34-36" },
  { id: "react", name: "React", icon: "⚛️", color: "#61DAFB", days: "37-38" },
  { id: "ai", name: "AI 활용", icon: "🤖", color: "#00C471", days: "39-40" },
];

export const stats = {
  totalDays: 40,
  totalCategories: 16,
  totalContents: 500,
  newFeatures: [
    "40일 확장 커리큘럼",
    "HTML/CSS/JavaScript 기초",
    "React 입문",
    "AI 활용 프로젝트",
    "실제 동작하는 점수 계산 시스템",
    "Hugging Face AI 데모",
  ],
};
