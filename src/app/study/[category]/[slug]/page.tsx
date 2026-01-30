'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, ArrowRight, Clock, BookOpen } from 'lucide-react';
import { ProgressButton } from '@/components/ProgressButton';
import { BookmarkButton } from '@/components/BookmarkButton';
import { CATEGORIES } from '@/types';
import { useEffect, useState } from 'react';
import contentsData from '@/data/contents.json';

// 카테고리별 JSON 콘텐츠 import
import pythonContents from '@/data/contents/python.json';
import javascriptContents from '@/data/contents/javascript.json';
import javaContents from '@/data/contents/java.json';
import springContents from '@/data/contents/spring.json';
import algorithmContents from '@/data/contents/algorithm.json';
import dbContents from '@/data/contents/db.json';
import networkContents from '@/data/contents/network.json';
import htmlCssContents from '@/data/contents/html-css.json';
import aiContents from '@/data/contents/ai.json';
import devopsContents from '@/data/contents/devops.json';
import cleancodeContents from '@/data/contents/cleancode.json';
import collaborationContents from '@/data/contents/collaboration.json';
import securityContents from '@/data/contents/security.json';
import osContents from '@/data/contents/os.json';
import reactContents from '@/data/contents/react.json';

interface ContentData {
  id: string;
  slug: string;
  title: string;
  category: string;
  subcategory: string;
  fsPath?: string;
  level: string;
  tags: string[];
  type: string;
  time: string;
  order: number;
}

interface JsonContent {
  id: string;
  title: string;
  category: string;
  subCategory: string | null;
  language: string;
  description: string;
  isPlaceholder: boolean;
  sections: Array<{
    type: string;
    title?: string;
    content?: string;
    language?: string;
    code?: string;
  }>;
}

// 카테고리별 JSON 매핑
const categoryJsonMap: Record<string, Record<string, JsonContent>> = {
  python: pythonContents,
  javascript: javascriptContents,
  java: javaContents,
  spring: springContents,
  algorithm: algorithmContents,
  db: dbContents,
  network: networkContents,
  'html-css': htmlCssContents,
  ai: aiContents,
  devops: devopsContents,
  cleancode: cleancodeContents,
  collaboration: collaborationContents,
  security: securityContents,
  os: osContents,
  react: reactContents,
};

// 마크다운을 HTML로 변환하는 간단한 파서
function parseMarkdownToHtml(markdown: string): string {
  if (!markdown) return '';

  let html = markdown;

  // 코드 블록 먼저 처리 (``` ... ```)
  const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
  const codeBlocks: string[] = [];
  html = html.replace(codeBlockRegex, (match, lang, code) => {
    const placeholder = `___CODEBLOCK_${codeBlocks.length}___`;
    const escaped = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    codeBlocks.push(`<pre style="background: #0f172a; padding: 15px; border-radius: 8px; overflow-x: auto; margin: 15px 0;"><code style="color: #a5b4fc; font-family: 'Courier New', monospace;">${escaped}</code></pre>`);
    return placeholder;
  });

  // 인라인 코드 처리 (` ... `)
  html = html.replace(/`([^`]+)`/g, '<code style="background: #334155; padding: 2px 6px; border-radius: 4px; color: #10b981; font-family: \'Courier New\', monospace;">$1</code>');

  // 헤딩 처리
  html = html.replace(/^### (.+)$/gm, '<h3 style="color: #60a5fa; font-size: 1.25rem; font-weight: 600; margin: 20px 0 10px 0;">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 style="color: #3b82f6; font-size: 1.5rem; font-weight: 700; margin: 25px 0 15px 0; border-bottom: 2px solid #1e40af; padding-bottom: 8px;">$1</h2>');

  // 볼드/이탤릭 처리
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong style="color: #fbbf24; font-weight: 700;">$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em style="color: #a5f3fc;">$1</em>');

  // 리스트 처리 (- 로 시작)
  const lines = html.split('\n');
  const processedLines: string[] = [];
  let inList = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const isListItem = /^[-*]\s+(.+)$/.test(line);

    if (isListItem) {
      if (!inList) {
        processedLines.push('<ul style="margin: 10px 0; padding-left: 25px; list-style: none;">');
        inList = true;
      }
      const content = line.replace(/^[-*]\s+/, '');
      processedLines.push(`<li style="margin: 8px 0; position: relative; padding-left: 20px;"><span style="position: absolute; left: 0; color: #10b981;">▸</span>${content}</li>`);
    } else {
      if (inList) {
        processedLines.push('</ul>');
        inList = false;
      }
      processedLines.push(line);
    }
  }
  if (inList) processedLines.push('</ul>');
  html = processedLines.join('\n');

  // 테이블 처리
  html = html.replace(/\|(.+)\|/g, (match) => {
    const cells = match.split('|').filter(c => c.trim());
    const isHeader = match.includes('---');
    if (isHeader) return '';
    const cellsHtml = cells.map(c => `<td style="border: 1px solid #475569; padding: 8px; color: #e2e8f0;">${c.trim()}</td>`).join('');
    return `<tr>${cellsHtml}</tr>`;
  });
  if (html.includes('<tr>')) {
    html = `<table style="width: 100%; border-collapse: collapse; margin: 15px 0; background: #1e293b; border-radius: 8px; overflow: hidden;">${html}</table>`;
  }

  // 구분선 처리
  html = html.replace(/^---+$/gm, '<hr style="border: none; border-top: 2px solid #334155; margin: 20px 0;" />');

  // 코드 블록 복원
  codeBlocks.forEach((block, i) => {
    html = html.replace(`___CODEBLOCK_${i}___`, block);
  });

  // 줄바꿈 처리 (연속 두 줄바꿈 = <p>, 한 줄바꿈 = <br>)
  const paragraphs = html.split('\n\n').filter(p => p.trim());
  html = paragraphs.map(p => {
    if (p.startsWith('<') || p.includes('___CODEBLOCK')) return p;
    const withBreaks = p.replace(/\n/g, '<br>');
    return `<p style="color: #e2e8f0; line-height: 1.8; margin: 12px 0;">${withBreaks}</p>`;
  }).join('');

  return html;
}

// JSON 섹션을 HTML로 변환
function renderJsonToHtml(content: JsonContent): string {
  if (!content || content.isPlaceholder || content.sections.length === 0) {
    return '';
  }

  return content.sections.map(section => {
    if (section.type === 'concept') {
      const parsedContent = parseMarkdownToHtml(section.content || '');
      return `
        <div class="desc" style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #10b981; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
          <h3 style="color: #10b981; margin-bottom: 15px; font-size: 1.4rem; font-weight: 700;">${section.title || '📚 개념'}</h3>
          <div style="color: #e2e8f0; line-height: 1.8;">${parsedContent}</div>
        </div>
      `;
    } else if (section.type === 'code') {
      const escapedCode = (section.code || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      return `
        <div style="margin: 25px 0;">
          <h3 style="color: #3b82f6; margin-bottom: 12px; font-size: 1.3rem; font-weight: 700;">💻 ${section.title || '예제 코드'}</h3>
          <pre style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); padding: 20px; border-radius: 12px; overflow-x: auto; border: 1px solid #334155; box-shadow: 0 4px 6px rgba(0,0,0,0.3);"><code style="color: #a5b4fc; font-family: 'Courier New', monospace; font-size: 0.95rem; line-height: 1.6;">${escapedCode}</code></pre>
        </div>
      `;
    } else if (section.type === 'tip') {
      const parsedContent = parseMarkdownToHtml(section.content || '');
      return `
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #0f1e3a 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #3b82f6; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
          <h3 style="color: #60a5fa; margin-bottom: 15px; font-size: 1.4rem; font-weight: 700;">💡 ${section.title || '팁'}</h3>
          <div style="color: #e2e8f0; line-height: 1.8;">${parsedContent}</div>
        </div>
      `;
    } else if (section.type === 'quiz') {
      // 퀴즈 섹션 렌더링
      const questions = (section as any).questions || [];
      const questionsHtml = questions.map((q: any, i: number) => {
        const answerParsed = parseMarkdownToHtml(q.answer || '');
        return `
          <details style="background: #1e293b; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #f59e0b; cursor: pointer;">
            <summary style="color: #fbbf24; font-weight: 600; font-size: 1.1rem; cursor: pointer; user-select: none;">
              Q${i + 1}. ${q.question}
            </summary>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #334155;">
              ${answerParsed}
            </div>
          </details>
        `;
      }).join('');

      return `
        <div style="background: linear-gradient(135deg, #431407 0%, #1c0a00 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #f59e0b; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
          <h3 style="color: #fbbf24; margin-bottom: 15px; font-size: 1.4rem; font-weight: 700;">${section.title || '💼 면접 질문'}</h3>
          ${questionsHtml}
        </div>
      `;
    }
    return '';
  }).join('');
}

export default function ContentPage() {
  const params = useParams();
  const category = params.category as string;
  const slug = params.slug as string;
  const [contentHtml, setContentHtml] = useState<string>('');
  const [loading, setLoading] = useState(true);

  const categoryData = CATEGORIES.find(c => c.name === category);
  const contentInfo = (contentsData.contents as ContentData[]).find(
    c => c.category === category && c.slug === slug
  );
  const contentId = `${category}-${slug}`;

  useEffect(() => {
    async function loadContent() {
      if (!contentInfo) {
        setLoading(false);
        return;
      }

      try {
        // 1. 먼저 JSON 콘텐츠 확인
        const jsonContents = categoryJsonMap[category];
        if (jsonContents) {
          // subcategory/slug 또는 slug로 찾기
          const jsonKey = contentInfo.subcategory
            ? `${contentInfo.subcategory}/${slug}`
            : slug;
          const jsonContent = jsonContents[jsonKey];

          if (jsonContent && !jsonContent.isPlaceholder && jsonContent.sections.length > 0) {
            const html = renderJsonToHtml(jsonContent);
            if (html) {
              setContentHtml(`
                <div class="container" style="max-width: 800px;">
                  <span class="badge" style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">${jsonContent.language}</span>
                  <h1 style="color: #fff; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-top: 10px;">${jsonContent.title}</h1>
                  ${html}
                </div>
              `);
              setLoading(false);
              return;
            }
          }
        }

        // 2. JSON에 없으면 HTML 파일 fetch
        const contentPath = contentInfo.fsPath || `/study/${category}/${contentInfo.subcategory}/${slug}.html`;
        const response = await fetch(contentPath);
        if (response.ok) {
          const html = await response.text();
          setContentHtml(html);
        } else {
          setContentHtml(`
            <div class="py-10 text-center text-gray-400">
              <p class="text-lg mb-2">🚧 콘텐츠 준비 중입니다.</p>
              <p class="text-sm">이 주제는 곧 업데이트될 예정입니다.</p>
            </div>
          `);
        }
      } catch (error) {
        console.error('Failed to load content:', error);
        setContentHtml('<p>콘텐츠를 불러오는 중 오류가 발생했습니다.</p>');
      } finally {
        setLoading(false);
      }
    }

    loadContent();
  }, [category, slug, contentInfo]);

  if (!contentInfo) {
    return <div className="text-center py-10">콘텐츠를 찾을 수 없습니다.</div>;
  }

  return (
    <div className="space-y-6">
      {/* 상단 네비게이션 */}
      <div className="flex items-center justify-between">
        <Link 
          href={`/study/${category}`}
          className="flex items-center gap-2 text-gray-400 hover:text-primary transition"
        >
          <ArrowLeft className="w-4 h-4" />
          {categoryData?.nameKo || category} 목록
        </Link>
        
        <div className="flex items-center gap-2">
          <BookmarkButton contentId={contentId} />
          <ProgressButton contentId={contentId} />
        </div>
      </div>

      {/* 콘텐츠 헤더 */}
      <div className="card">
        <div className="flex items-center gap-2 text-sm text-gray-400 mb-2">
          <span>{categoryData?.icon}</span>
          <span>{categoryData?.nameKo}</span>
          <span className="mx-2">|</span>
          <span>{contentInfo.subcategory}</span>
        </div>
        <h1 className="text-2xl font-bold mb-4">{contentInfo.title}</h1>
        
        <div className="flex items-center gap-4 text-sm text-gray-400">
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {contentInfo.time}
          </span>
          <span className="flex items-center gap-1">
            <BookOpen className="w-4 h-4" />
            {contentInfo.type}
          </span>
        </div>
      </div>

      {/* 콘텐츠 본문 */}
      <div className="card prose prose-invert max-w-none">
        {loading ? (
          <div className="flex justify-center py-10">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        ) : (
          <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
        )}
      </div>

      {/* 하단 네비게이션 */}
      <div className="flex items-center justify-between">
        <button className="btn btn-outline flex items-center gap-2" onClick={() => window.history.back()}>
          <ArrowLeft className="w-4 h-4" />
          이전 학습
        </button>
        <Link href={`/study/${category}`} className="btn btn-primary flex items-center gap-2">
          목록으로
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
