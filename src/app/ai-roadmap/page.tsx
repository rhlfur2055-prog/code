'use client';

import Link from 'next/link';
import { useState } from 'react';

interface RoadmapStep {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  color: string;
  difficulty: string;
  duration: string;
  description: string;
  topics: string[];
  link: string;
}

const roadmapData: RoadmapStep[] = [
  {
    id: 'python-basics',
    title: 'Python 기초',
    subtitle: 'AI의 시작점',
    icon: '🐍',
    color: '#3B82F6',
    difficulty: '입문',
    duration: '2주',
    description: 'AI 라이브러리 대부분이 Python으로 작성됨',
    topics: ['변수, 자료형', '함수, 클래스', 'pip, venv'],
    link: '/study/python'
  },
  {
    id: 'data-processing',
    title: '데이터 처리',
    subtitle: 'NumPy, Pandas',
    icon: '📊',
    color: '#8B5CF6',
    difficulty: '초급',
    duration: '1주',
    description: 'AI 모델의 입출력은 배열/텐서',
    topics: ['NumPy 배열 연산', 'Pandas DataFrame', 'Matplotlib 시각화'],
    link: '/study/python'
  },
  {
    id: 'opencv',
    title: 'OpenCV',
    subtitle: '이미지 처리',
    icon: '🖼️',
    color: '#06B6D4',
    difficulty: '초급',
    duration: '1주',
    description: 'YOLO, SAM 등 입력 전처리 필수',
    topics: ['이미지 읽기/저장', '크기 조절, 색상 변환', '동영상 처리'],
    link: '/study/ai-tech'
  },
  {
    id: 'ai-libs',
    title: 'AI 라이브러리',
    subtitle: 'PyTorch, YOLO',
    icon: '🤖',
    color: '#F59E0B',
    difficulty: '중급',
    duration: '2주',
    description: '실제 AI 모델 사용법',
    topics: ['Ultralytics YOLO', 'Hugging Face Transformers', 'OpenAI Whisper'],
    link: '/study/ai-tech'
  },
  {
    id: 'java-basics',
    title: 'Java 기초',
    subtitle: '백엔드 언어',
    icon: '☕',
    color: '#F97316',
    difficulty: '입문',
    duration: '2주',
    description: 'Spring Boot로 AI API 서버 구축',
    topics: ['클래스, 객체, 상속', '컬렉션 (List, Map)', '예외 처리'],
    link: '/study/java'
  },
  {
    id: 'spring-boot',
    title: 'Spring Boot',
    subtitle: 'API 서버',
    icon: '🍃',
    color: '#22C55E',
    difficulty: '초급',
    duration: '2주',
    description: 'AI 모델을 웹 서비스로 배포',
    topics: ['REST API', '파일 업로드', 'JSON 처리'],
    link: '/study/spring'
  },
  {
    id: 'ai-api',
    title: 'AI API 연동',
    subtitle: 'Spring + Python',
    icon: '🔗',
    color: '#EC4899',
    difficulty: '중급',
    duration: '1주',
    description: 'Java에서 Python AI 서버 호출',
    topics: ['RestTemplate', 'WebClient', '비동기 처리'],
    link: '/study/spring'
  },
  {
    id: 'fullstack-ai',
    title: '풀스택 AI',
    subtitle: '프로젝트',
    icon: '🚀',
    color: '#00C471',
    difficulty: '중급',
    duration: '2주',
    description: 'React + Spring + Python AI 통합',
    topics: ['이미지 업로드 → YOLO', '음성 → Whisper', '풀스택 배포'],
    link: '/ai-demo'
  }
];

const difficultyColors: Record<string, string> = {
  '입문': '#00C471',
  '초급': '#3B82F6',
  '중급': '#F59E0B',
};

export default function AIRoadmapPage() {
  const [selectedStep, setSelectedStep] = useState<string | null>(null);

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1B1B1F',
      color: '#fff',
      padding: '24px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '40px', textAlign: 'center' }}>
          <Link href="/" style={{ color: '#00C471', textDecoration: 'none', marginBottom: '16px', display: 'inline-block' }}>
            ← 홈으로
          </Link>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '12px' }}>
            🗺️ AI 개발자 로드맵
          </h1>
          <p style={{ color: '#9CA3AF', fontSize: '1.125rem' }}>
            Python 기초부터 풀스택 AI 프로젝트까지, 단계별 학습 가이드
          </p>
        </div>

        {/* Stats */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: '16px',
          marginBottom: '40px'
        }}>
          {[
            { label: '총 학습 기간', value: '약 13주', icon: '📅' },
            { label: '단계', value: '8단계', icon: '📚' },
            { label: '실습 프로젝트', value: '3개', icon: '🛠️' },
            { label: 'AI 데모', value: '10개', icon: '🎮' }
          ].map(stat => (
            <div key={stat.label} style={{
              backgroundColor: '#25252B',
              borderRadius: '12px',
              padding: '20px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>{stat.icon}</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#00C471' }}>{stat.value}</div>
              <div style={{ color: '#6B7280', fontSize: '0.875rem' }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Roadmap */}
        <div style={{ position: 'relative' }}>
          {/* Connection Line */}
          <div style={{
            position: 'absolute',
            left: '50%',
            top: '0',
            bottom: '0',
            width: '4px',
            backgroundColor: '#333',
            transform: 'translateX(-50%)',
            zIndex: 0
          }} />

          {/* Steps */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            {roadmapData.map((step, index) => (
              <div
                key={step.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  marginBottom: '24px',
                  flexDirection: index % 2 === 0 ? 'row' : 'row-reverse'
                }}
              >
                {/* Card */}
                <div
                  onClick={() => setSelectedStep(selectedStep === step.id ? null : step.id)}
                  style={{
                    flex: 1,
                    backgroundColor: selectedStep === step.id ? '#2D2D35' : '#25252B',
                    borderRadius: '16px',
                    padding: '24px',
                    cursor: 'pointer',
                    border: `2px solid ${selectedStep === step.id ? step.color : 'transparent'}`,
                    transition: 'all 0.3s',
                    marginRight: index % 2 === 0 ? '24px' : '0',
                    marginLeft: index % 2 === 1 ? '24px' : '0'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
                    <span style={{
                      fontSize: '2rem',
                      width: '50px',
                      height: '50px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: step.color + '20',
                      borderRadius: '12px'
                    }}>
                      {step.icon}
                    </span>
                    <div>
                      <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '4px' }}>
                        {step.title}
                      </h3>
                      <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
                        {step.subtitle}
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
                    <span style={{
                      backgroundColor: difficultyColors[step.difficulty] + '20',
                      color: difficultyColors[step.difficulty],
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.75rem'
                    }}>
                      {step.difficulty}
                    </span>
                    <span style={{
                      backgroundColor: '#1B1B1F',
                      color: '#9CA3AF',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.75rem'
                    }}>
                      ⏱️ {step.duration}
                    </span>
                  </div>

                  <p style={{ color: '#9CA3AF', fontSize: '0.875rem', marginBottom: '12px' }}>
                    {step.description}
                  </p>

                  {/* Expanded Content */}
                  {selectedStep === step.id && (
                    <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #333' }}>
                      <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '8px' }}>
                        📖 학습 내용
                      </h4>
                      <ul style={{
                        listStyle: 'none',
                        padding: 0,
                        margin: 0
                      }}>
                        {step.topics.map(topic => (
                          <li key={topic} style={{
                            color: '#9CA3AF',
                            fontSize: '0.875rem',
                            padding: '4px 0',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                          }}>
                            <span style={{ color: step.color }}>•</span>
                            {topic}
                          </li>
                        ))}
                      </ul>
                      <Link href={step.link} style={{
                        display: 'inline-block',
                        marginTop: '16px',
                        padding: '10px 20px',
                        backgroundColor: step.color,
                        color: '#000',
                        borderRadius: '8px',
                        textDecoration: 'none',
                        fontWeight: 'bold',
                        fontSize: '0.875rem'
                      }}>
                        학습 시작 →
                      </Link>
                    </div>
                  )}
                </div>

                {/* Center Node */}
                <div style={{
                  width: '60px',
                  height: '60px',
                  backgroundColor: step.color,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.5rem',
                  fontWeight: 'bold',
                  color: '#000',
                  flexShrink: 0,
                  boxShadow: `0 0 20px ${step.color}40`
                }}>
                  {index + 1}
                </div>

                {/* Empty space for the other side */}
                <div style={{ flex: 1 }} />
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div style={{
          marginTop: '60px',
          padding: '40px',
          backgroundColor: '#25252B',
          borderRadius: '16px',
          textAlign: 'center'
        }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '12px' }}>
            🎮 바로 AI 체험하기
          </h2>
          <p style={{ color: '#9CA3AF', marginBottom: '24px' }}>
            코드 없이 바로 실행할 수 있는 10개의 AI 데모
          </p>
          <Link href="/ai-demo" style={{
            display: 'inline-block',
            padding: '14px 32px',
            backgroundColor: '#00C471',
            color: '#000',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '1rem'
          }}>
            AI 데모 체험하기 →
          </Link>
        </div>
      </div>
    </div>
  );
}
