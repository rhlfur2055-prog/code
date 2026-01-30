'use client';

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getDemoBySlug, aiDemos } from '@/data/ai-demos';
import { useState } from 'react';

const difficultyColors: Record<string, string> = {
  '입문': '#00C471',
  '초급': '#3B82F6',
  '중급': '#F59E0B',
};

const difficultyEmojis: Record<string, string> = {
  '입문': '🌱',
  '초급': '🌿',
  '중급': '🌳',
};

export default function AIDemoDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const demo = getDemoBySlug(slug);
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);

  // 현재 데모의 인덱스
  const currentIndex = aiDemos.findIndex(d => d.slug === slug);
  const prevDemo = currentIndex > 0 ? aiDemos[currentIndex - 1] : null;
  const nextDemo = currentIndex < aiDemos.length - 1 ? aiDemos[currentIndex + 1] : null;

  if (!demo) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#1B1B1F',
        color: '#fff',
        padding: '24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontSize: '2rem', marginBottom: '16px' }}>404</h1>
          <p style={{ color: '#9CA3AF', marginBottom: '24px' }}>데모를 찾을 수 없습니다.</p>
          <Link href="/ai-demo" style={{ color: '#00C471' }}>
            ← 데모 목록으로
          </Link>
        </div>
      </div>
    );
  }

  const copyCode = () => {
    if (demo.codeExample) {
      navigator.clipboard.writeText(demo.codeExample);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1B1B1F',
      color: '#fff'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#25252B',
        padding: '16px 24px',
        borderBottom: '1px solid #333'
      }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <Link href="/ai-demo" style={{ color: '#00C471', textDecoration: 'none', fontSize: '0.875rem' }}>
                ← AI 데모 목록
              </Link>
              <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginTop: '8px' }}>
                {demo.name}
              </h1>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{
                backgroundColor: difficultyColors[demo.difficulty] + '20',
                color: difficultyColors[demo.difficulty],
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '0.875rem',
                fontWeight: 'bold'
              }}>
                {difficultyEmojis[demo.difficulty]} {demo.difficulty}
              </span>
              <span style={{
                backgroundColor: '#1B1B1F',
                color: '#9CA3AF',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '0.875rem'
              }}>
                {demo.category}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 350px',
          gap: '24px'
        }}>
          {/* Demo iframe */}
          <div>
            <div style={{
              backgroundColor: '#25252B',
              borderRadius: '12px',
              overflow: 'hidden'
            }}>
              <iframe
                src={demo.embedUrl}
                style={{
                  width: '100%',
                  height: '700px',
                  border: 'none'
                }}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
            <p style={{
              color: '#6B7280',
              fontSize: '0.75rem',
              marginTop: '8px',
              textAlign: 'center'
            }}>
              Powered by <a href="https://huggingface.co/spaces" target="_blank" rel="noopener" style={{ color: '#00C471' }}>Hugging Face Spaces</a>
            </p>
          </div>

          {/* Sidebar */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Description */}
            <div style={{
              backgroundColor: '#25252B',
              borderRadius: '12px',
              padding: '20px'
            }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '12px' }}>
                📖 설명
              </h3>
              <p style={{ color: '#9CA3AF', fontSize: '0.875rem', lineHeight: '1.6' }}>
                {demo.description}
              </p>

              {/* Tags */}
              <div style={{
                display: 'flex',
                gap: '6px',
                flexWrap: 'wrap',
                marginTop: '16px'
              }}>
                {demo.tags.map(tag => (
                  <span
                    key={tag}
                    style={{
                      backgroundColor: '#1B1B1F',
                      color: '#6B7280',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.75rem'
                    }}
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Code Example */}
            {demo.codeExample && (
              <div style={{
                backgroundColor: '#25252B',
                borderRadius: '12px',
                padding: '20px'
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '12px'
                }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 'bold' }}>
                    💻 Python 코드
                  </h3>
                  <button
                    onClick={() => setShowCode(!showCode)}
                    style={{
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: '#00C471',
                      cursor: 'pointer',
                      fontSize: '0.875rem'
                    }}
                  >
                    {showCode ? '접기' : '펼치기'}
                  </button>
                </div>

                {showCode && (
                  <>
                    <div style={{
                      backgroundColor: '#1B1B1F',
                      borderRadius: '8px',
                      padding: '16px',
                      overflow: 'auto',
                      maxHeight: '300px'
                    }}>
                      <pre style={{
                        margin: 0,
                        fontSize: '0.8rem',
                        color: '#E5E7EB',
                        whiteSpace: 'pre-wrap',
                        fontFamily: 'monospace'
                      }}>
                        {demo.codeExample}
                      </pre>
                    </div>
                    <button
                      onClick={copyCode}
                      style={{
                        width: '100%',
                        marginTop: '12px',
                        padding: '10px',
                        backgroundColor: copied ? '#00C471' : '#1B1B1F',
                        color: copied ? '#000' : '#fff',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        fontWeight: 'bold',
                        transition: 'all 0.2s'
                      }}
                    >
                      {copied ? '✓ 복사됨!' : '📋 코드 복사'}
                    </button>
                  </>
                )}
              </div>
            )}

            {/* Tips */}
            <div style={{
              backgroundColor: '#00C47110',
              border: '1px solid #00C47130',
              borderRadius: '12px',
              padding: '20px'
            }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '12px', color: '#00C471' }}>
                💡 사용 팁
              </h3>
              <ul style={{
                color: '#9CA3AF',
                fontSize: '0.875rem',
                lineHeight: '1.8',
                paddingLeft: '20px',
                margin: 0
              }}>
                <li>이미지는 드래그 앤 드롭으로 업로드</li>
                <li>무료 서비스로 처리 시간이 길 수 있음</li>
                <li>결과물은 다운로드 가능</li>
              </ul>
            </div>

            {/* Navigation */}
            <div style={{
              display: 'flex',
              gap: '12px'
            }}>
              {prevDemo && (
                <Link
                  href={`/ai-demo/${prevDemo.slug}`}
                  style={{
                    flex: 1,
                    backgroundColor: '#25252B',
                    borderRadius: '8px',
                    padding: '12px',
                    textDecoration: 'none',
                    color: '#fff',
                    textAlign: 'center',
                    fontSize: '0.875rem'
                  }}
                >
                  ← {prevDemo.name.split(' ')[0]}
                </Link>
              )}
              {nextDemo && (
                <Link
                  href={`/ai-demo/${nextDemo.slug}`}
                  style={{
                    flex: 1,
                    backgroundColor: '#25252B',
                    borderRadius: '8px',
                    padding: '12px',
                    textDecoration: 'none',
                    color: '#fff',
                    textAlign: 'center',
                    fontSize: '0.875rem'
                  }}
                >
                  {nextDemo.name.split(' ')[0]} →
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
