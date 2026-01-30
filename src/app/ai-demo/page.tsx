'use client';

import Link from 'next/link';
import { aiDemos, getCategories } from '@/data/ai-demos';
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

export default function AIDemoPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('전체');
  const categories = ['전체', ...getCategories()];

  const filteredDemos = selectedCategory === '전체'
    ? aiDemos
    : aiDemos.filter(demo => demo.category === selectedCategory);

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1B1B1F',
      color: '#fff',
      padding: '24px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '32px' }}>
          <Link href="/" style={{ color: '#00C471', textDecoration: 'none', marginBottom: '16px', display: 'inline-block' }}>
            ← 홈으로
          </Link>
          <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '8px' }}>
            🎮 AI 체험하기
          </h1>
          <p style={{ color: '#9CA3AF', fontSize: '1rem' }}>
            가입 없이 바로 실행! Hugging Face Spaces 기반 AI 데모
          </p>
        </div>

        {/* Category Filter */}
        <div style={{
          display: 'flex',
          gap: '8px',
          flexWrap: 'wrap',
          marginBottom: '24px'
        }}>
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: 'none',
                backgroundColor: selectedCategory === category ? '#00C471' : '#25252B',
                color: selectedCategory === category ? '#000' : '#fff',
                cursor: 'pointer',
                fontSize: '0.875rem',
                fontWeight: selectedCategory === category ? 'bold' : 'normal',
                transition: 'all 0.2s'
              }}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Demo Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: '20px'
        }}>
          {filteredDemos.map(demo => (
            <Link
              key={demo.slug}
              href={`/ai-demo/${demo.slug}`}
              style={{ textDecoration: 'none' }}
            >
              <div style={{
                backgroundColor: '#25252B',
                borderRadius: '12px',
                padding: '20px',
                transition: 'transform 0.2s, box-shadow 0.2s',
                cursor: 'pointer',
                height: '100%',
                display: 'flex',
                flexDirection: 'column'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 4px 20px rgba(0, 196, 113, 0.2)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }}
              >
                {/* Difficulty Badge */}
                <div style={{ marginBottom: '12px' }}>
                  <span style={{
                    backgroundColor: difficultyColors[demo.difficulty] + '20',
                    color: difficultyColors[demo.difficulty],
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                    fontWeight: 'bold'
                  }}>
                    {difficultyEmojis[demo.difficulty]} {demo.difficulty}
                  </span>
                  <span style={{
                    marginLeft: '8px',
                    color: '#6B7280',
                    fontSize: '0.75rem'
                  }}>
                    {demo.category}
                  </span>
                </div>

                {/* Title */}
                <h3 style={{
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#fff',
                  marginBottom: '8px'
                }}>
                  {demo.name}
                </h3>

                {/* Description */}
                <p style={{
                  color: '#9CA3AF',
                  fontSize: '0.875rem',
                  marginBottom: '16px',
                  flex: 1
                }}>
                  {demo.description}
                </p>

                {/* Tags */}
                <div style={{
                  display: 'flex',
                  gap: '6px',
                  flexWrap: 'wrap'
                }}>
                  {demo.tags.slice(0, 3).map(tag => (
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

                {/* CTA */}
                <div style={{
                  marginTop: '16px',
                  color: '#00C471',
                  fontSize: '0.875rem',
                  fontWeight: 'bold'
                }}>
                  체험하기 →
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Footer */}
        <div style={{
          marginTop: '48px',
          padding: '24px',
          backgroundColor: '#25252B',
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <p style={{ color: '#9CA3AF', marginBottom: '8px' }}>
            모든 데모는 Hugging Face Spaces에서 제공됩니다.
          </p>
          <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
            무료 서비스이므로 트래픽이 많을 때 느려질 수 있습니다.
          </p>
        </div>
      </div>
    </div>
  );
}
