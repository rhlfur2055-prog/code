// ============================================
// 🚀 코드마스터 - TypeScript 타입 정의
// ============================================

// 난이도 타입
export type Level = 'beginner' | 'basic' | 'intermediate' | 'advanced';

// 태그 타입
export type Tag = 'required' | 'interview' | 'practical' | 'coding';

// 콘텐츠 타입
export type ContentType = 'theory' | 'practice' | 'quiz' | 'interview' | 'project';

// 콘텐츠 인터페이스
export interface Content {
  id: string;
  slug: string;
  title: string;
  category: string;
  subcategory: string;
  level: Level;
  tags: Tag[];
  type: ContentType;
  time: string;
  day: number;
  order: number;
}

// 카테고리 인터페이스
export interface Category {
  id: string;
  name: string;
  nameKo: string;
  icon: string;
  color: string;
  description: string;
  contentCount: number;
  days: number[];
}

// 30일 스케줄 인터페이스
export interface DaySchedule {
  day: number;
  title: string;
  description: string;
  categories: string[];
  hours: number;
}

// 학습 진행률
export interface Progress {
  contentId: string;
  completed: boolean;
  completedAt?: string;
}

// 북마크
export interface Bookmark {
  contentId: string;
  addedAt: string;
}

// ============================================
// 🔐 인증 관련 타입
// ============================================

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'USER' | 'ADMIN';
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  user: User;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  timestamp: string;
}

// ============================================
// 🤖 AI 분석 관련 타입
// ============================================

export interface SentimentResult {
  label: 'positive' | 'negative' | 'neutral';
  score: number;
  details?: {
    positive_indicators: number;
    negative_indicators: number;
    text_length: number;
  };
}

export interface KeywordResult {
  word: string;
  count: number;
  score: number;
}

export interface TextAnalysisResponse {
  success: boolean;
  sentiment?: SentimentResult;
  keywords?: KeywordResult[];
  summary?: string;
  processing_time_ms?: number;
  error_message?: string;
}

// 난이도 정보
export const LEVELS: Record<Level, { emoji: string; label: string; color: string; description: string }> = {
  beginner: { emoji: '🌱', label: '입문', color: 'level-beginner', description: '프로그래밍을 처음 접하는 분들을 위한 단계' },
  basic: { emoji: '🌿', label: '초급', color: 'level-basic', description: '기본 문법과 개념을 익히는 단계' },
  intermediate: { emoji: '🌳', label: '중급', color: 'level-intermediate', description: '실무에서 자주 사용되는 핵심 기술 단계' },
  advanced: { emoji: '🏔️', label: '고급', color: 'level-advanced', description: '깊이 있는 이해와 최적화를 다루는 단계' },
};

// 태그 정보
export const TAGS: Record<Tag, { emoji: string; label: string; color: string; description: string }> = {
  required: { emoji: '🔥', label: '필수', color: 'tag-required', description: '반드시 알아야 할 핵심 내용' },
  interview: { emoji: '💼', label: '면접', color: 'tag-interview', description: '기술 면접에 자주 나오는 질문' },
  practical: { emoji: '🛠️', label: '실무', color: 'tag-practical', description: '실무에서 바로 쓸 수 있는 기술' },
  coding: { emoji: '📝', label: '코테', color: 'tag-coding', description: '코딩 테스트 대비 문제 풀이' },
};

// 콘텐츠 타입 정보
export const CONTENT_TYPES: Record<ContentType, { emoji: string; label: string }> = {
  theory: { emoji: '📚', label: '이론' },
  practice: { emoji: '🛠️', label: '실습' },
  quiz: { emoji: '✅', label: '퀴즈' },
  interview: { emoji: '💼', label: '면접' },
  project: { emoji: '🏆', label: '프로젝트' },
};

// 카테고리 목록 (40일 기준) - 총 760개 콘텐츠
export const CATEGORIES: Category[] = [
  { id: 'java', name: 'java', nameKo: 'Java 완전 정복', icon: '☕', color: '#F97316', description: 'OOP, 컬렉션, 스트림, JVM', contentCount: 80, days: [1, 2, 3, 4, 5, 6, 7] },
  { id: 'spring', name: 'spring', nameKo: 'Spring Boot', icon: '🍃', color: '#22C55E', description: 'DI, MVC, JPA, Security', contentCount: 100, days: [8, 9, 10, 11, 12, 13, 14] },
  { id: 'python', name: 'python', nameKo: 'Python', icon: '🐍', color: '#3B82F6', description: 'FastAPI, pytest, async', contentCount: 60, days: [15, 16, 17] },
  { id: 'algorithm', name: 'algorithm', nameKo: '알고리즘', icon: '📊', color: '#8B5CF6', description: 'DP, BFS/DFS, 그리디', contentCount: 80, days: [18, 19, 20, 21] },
  { id: 'db', name: 'db', nameKo: 'Database', icon: '🗄️', color: '#EAB308', description: 'SQL, 인덱스, 트랜잭션', contentCount: 50, days: [22, 23] },
  { id: 'network', name: 'network', nameKo: '네트워크', icon: '📡', color: '#06B6D4', description: 'HTTP, TCP, JWT', contentCount: 40, days: [24] },
  { id: 'os', name: 'os', nameKo: '운영체제', icon: '💻', color: '#EC4899', description: '프로세스, 메모리', contentCount: 40, days: [25] },
  { id: 'cleancode', name: 'cleancode', nameKo: '클린코드', icon: '📝', color: '#10B981', description: 'SOLID, 리팩토링', contentCount: 30, days: [26] },
  { id: 'security', name: 'security', nameKo: '보안', icon: '🔒', color: '#EF4444', description: 'XSS, CSRF, 암호화', contentCount: 30, days: [27] },
  { id: 'devops', name: 'devops', nameKo: 'DevOps', icon: '🐳', color: '#0EA5E9', description: 'Docker, CI/CD', contentCount: 40, days: [28] },
  { id: 'tools', name: 'tools', nameKo: '개발도구', icon: '🛠️', color: '#F59E0B', description: 'IntelliJ, Postman', contentCount: 30, days: [29] },
  { id: 'collaboration', name: 'collaboration', nameKo: '협업 & Git', icon: '👥', color: '#6366F1', description: 'Git, 애자일', contentCount: 40, days: [30] },
  // Day 31-40: 신규 추가
  { id: 'html-css', name: 'html-css', nameKo: 'HTML/CSS', icon: '🌐', color: '#E34F26', description: 'HTML, CSS, Flexbox, Grid', contentCount: 30, days: [31, 32, 33] },
  { id: 'javascript', name: 'javascript', nameKo: 'JavaScript', icon: '⚡', color: '#F7DF1E', description: 'ES6+, DOM, 비동기', contentCount: 40, days: [34, 35, 36] },
  { id: 'react', name: 'react', nameKo: 'React', icon: '⚛️', color: '#61DAFB', description: '컴포넌트, Hooks, State', contentCount: 30, days: [37, 38] },
  { id: 'ai', name: 'ai', nameKo: 'AI 활용', icon: '🤖', color: '#00C471', description: 'YOLO, Whisper, 풀스택 AI', contentCount: 40, days: [39, 40] },
  { id: 'pcce', name: 'pcce', nameKo: 'PCCE 시험대비', icon: '🎯', color: '#FF4081', description: '12시간 완성, 10대 함정, 모의고사', contentCount: 15, days: [] },
];

// 40일 로드맵
export const ROADMAP: DaySchedule[] = [
  { day: 1, title: 'Java 입문 & 기초 문법', description: '자바 설치, 변수, 연산자, 조건문', categories: ['java'], hours: 6 },
  { day: 2, title: 'Java 객체지향 (OOP)', description: '클래스, 상속, 다형성, 인터페이스', categories: ['java'], hours: 8 },
  { day: 3, title: 'Java 핵심문법 & 컬렉션', description: 'String, 예외처리, ArrayList, HashMap', categories: ['java'], hours: 7 },
  { day: 4, title: 'Java 함수형 & 스트림', description: '람다, Stream API, Optional', categories: ['java'], hours: 6 },
  { day: 5, title: 'Java 멀티스레딩', description: '스레드, 동기화, ExecutorService', categories: ['java'], hours: 5 },
  { day: 6, title: 'Java JVM & GC', description: 'JVM 구조, 메모리, GC 종류', categories: ['java'], hours: 5 },
  { day: 7, title: 'Java 디자인패턴 & 테스트', description: '싱글톤, 팩토리, JUnit5', categories: ['java'], hours: 6 },
  { day: 8, title: 'Spring 입문 & 핵심개념', description: 'IoC, DI, Bean', categories: ['spring'], hours: 7 },
  { day: 9, title: 'Spring IoC/DI 심화', description: '생성자 주입, 빈 생명주기', categories: ['spring'], hours: 6 },
  { day: 10, title: 'Spring MVC & REST API', description: 'Controller, RequestMapping', categories: ['spring'], hours: 7 },
  { day: 11, title: 'Spring JPA 기초', description: 'Entity, Repository, CRUD', categories: ['spring'], hours: 6 },
  { day: 12, title: 'Spring JPA 연관관계 & N+1', description: 'ManyToOne, Fetch Join', categories: ['spring'], hours: 7 },
  { day: 13, title: 'Spring Security & JWT', description: '인증, 인가, JWT 구현', categories: ['spring'], hours: 8 },
  { day: 14, title: 'Spring 테스트 & 문서화', description: 'MockMvc, Swagger', categories: ['spring'], hours: 6 },
  { day: 15, title: 'Python 입문 & 기초', description: '설치, 자료형, 함수', categories: ['python'], hours: 6 },
  { day: 16, title: 'Python 중급 & 객체지향', description: '데코레이터, 제너레이터, 클래스', categories: ['python'], hours: 7 },
  { day: 17, title: 'Python 비동기 & FastAPI', description: 'async/await, FastAPI CRUD', categories: ['python'], hours: 8 },
  { day: 18, title: '알고리즘 기초 & 배열', description: '시간복잡도, 투포인터, 슬라이딩 윈도우', categories: ['algorithm'], hours: 6 },
  { day: 19, title: '스택/큐 & 정렬/탐색', description: '스택, 큐, 이진탐색, 퀵소트', categories: ['algorithm'], hours: 7 },
  { day: 20, title: '그래프 & 최단경로', description: 'DFS, BFS, 다익스트라', categories: ['algorithm'], hours: 8 },
  { day: 21, title: 'DP & 그리디 & 백트래킹', description: '피보나치, 냅색, N-Queen', categories: ['algorithm'], hours: 8 },
  { day: 22, title: 'SQL 기초 & JOIN', description: 'SELECT, JOIN, 서브쿼리', categories: ['db'], hours: 6 },
  { day: 23, title: '인덱스 & 트랜잭션 & NoSQL', description: 'B-Tree, ACID, Redis', categories: ['db'], hours: 7 },
  { day: 24, title: '네트워크 완전 정복', description: 'HTTP, TCP/UDP, REST, JWT', categories: ['network'], hours: 8 },
  { day: 25, title: '운영체제 완전 정복', description: '프로세스, 스레드, 메모리', categories: ['os'], hours: 7 },
  { day: 26, title: '클린코드 & SOLID', description: '네이밍, SRP, OCP, 리팩토링', categories: ['cleancode'], hours: 5 },
  { day: 27, title: '보안 완전 정복', description: 'SQL Injection, XSS, CSRF', categories: ['security'], hours: 5 },
  { day: 28, title: 'Docker & CI/CD', description: 'Dockerfile, GitHub Actions', categories: ['devops'], hours: 6 },
  { day: 29, title: '개발도구 마스터', description: 'IntelliJ 단축키, Postman', categories: ['tools'], hours: 4 },
  { day: 30, title: 'Git & 협업 & 포트폴리오', description: 'Git Flow, PR, 코드리뷰', categories: ['collaboration'], hours: 6 },
  // Day 31-40: 신규 추가
  { day: 31, title: 'HTML 기초', description: '태그, 구조, 폼', categories: ['html-css'], hours: 4 },
  { day: 32, title: 'CSS 기초 & Flexbox', description: '선택자, 박스모델, Flexbox', categories: ['html-css'], hours: 5 },
  { day: 33, title: 'CSS Grid & 반응형', description: 'Grid 레이아웃, 미디어 쿼리', categories: ['html-css'], hours: 5 },
  { day: 34, title: 'JavaScript 기초', description: '변수, 함수, 객체', categories: ['javascript'], hours: 5 },
  { day: 35, title: 'DOM 조작', description: '선택자, 이벤트, 동적 생성', categories: ['javascript'], hours: 5 },
  { day: 36, title: '비동기 & API', description: 'Promise, async/await, fetch', categories: ['javascript'], hours: 6 },
  { day: 37, title: 'React 기초', description: '컴포넌트, Props, State', categories: ['react'], hours: 6 },
  { day: 38, title: 'React Hooks', description: 'useState, useEffect, Custom Hooks', categories: ['react'], hours: 6 },
  { day: 39, title: 'AI 기초 & 연동', description: 'YOLO, Whisper, API 연동', categories: ['ai'], hours: 6 },
  { day: 40, title: '풀스택 AI 프로젝트', description: 'React + Spring + Python AI', categories: ['ai'], hours: 8 },
];
