const fs = require('fs');
const path = require('path');

// HTML 파일에서 정보 추출
function extractFromHtml(htmlContent, filename) {
  // 제목 추출
  const titleMatch = htmlContent.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const title = titleMatch ? titleMatch[1].trim() : filename.replace('.html', '');

  // 배지(언어) 추출
  const badgeMatch = htmlContent.match(/<span class="badge">([^<]+)<\/span>/);
  const language = badgeMatch ? badgeMatch[1].trim() : 'Text';

  // 학습 목표 추출
  const descMatch = htmlContent.match(/<div class="desc">[\s\S]*?<p>([^<]+)<\/p>/);
  const description = descMatch ? descMatch[1].trim() : '';

  // 코드 추출
  const codeMatch = htmlContent.match(/<pre><code>([\s\S]*?)<\/code><\/pre>/);
  const code = codeMatch ? codeMatch[1].trim() : '';

  // 플레이스홀더 확인
  const isPlaceholder =
    description.includes('해당 주제의 핵심 원리') ||
    code.includes('예제 코드를 작성하며 학습하세요') ||
    description.includes('Java 클래스와 메인 메서드 구조') ||
    description.includes('Python 변수, 제어문 기초');

  return { title, language, description, code, isPlaceholder };
}

// 카테고리별 변환
function convertCategory(category) {
  const htmlDir = path.join(__dirname, '..', 'public', 'study', category);
  const outputFile = path.join(__dirname, '..', 'src', 'data', 'contents', `${category}.json`);

  if (!fs.existsSync(htmlDir)) {
    console.log(`⚠️  ${category}: 폴더 없음`);
    return { total: 0, placeholder: 0 };
  }

  // 하위 폴더 포함 모든 HTML 파일 찾기
  const allFiles = [];

  function findHtmlFiles(dir, prefix = '') {
    const items = fs.readdirSync(dir);
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        findHtmlFiles(fullPath, prefix ? `${prefix}/${item}` : item);
      } else if (item.endsWith('.html')) {
        allFiles.push({
          path: fullPath,
          name: item,
          subdir: prefix
        });
      }
    });
  }

  findHtmlFiles(htmlDir);

  const contents = {};
  let placeholderCount = 0;

  allFiles.forEach(file => {
    try {
      const html = fs.readFileSync(file.path, 'utf-8');
      const extracted = extractFromHtml(html, file.name);

      const slug = file.name.replace('.html', '');
      const id = file.subdir ? `${file.subdir}/${slug}` : slug;

      if (extracted.isPlaceholder) {
        placeholderCount++;
      }

      contents[id] = {
        id: id,
        title: extracted.title,
        category: category,
        subCategory: file.subdir || null,
        language: extracted.language,
        description: extracted.description,
        isPlaceholder: extracted.isPlaceholder,
        sections: extracted.isPlaceholder ? [] : [
          {
            type: 'concept',
            title: extracted.title,
            content: extracted.description
          },
          {
            type: 'code',
            language: extracted.language,
            code: extracted.code
          }
        ]
      };
    } catch (err) {
      console.error(`  ❌ ${file.name}: ${err.message}`);
    }
  });

  // 출력 폴더 생성
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputFile, JSON.stringify(contents, null, 2), 'utf-8');

  return { total: allFiles.length, placeholder: placeholderCount };
}

// 메인 실행
console.log('🚀 HTML → JSON 변환 시작\n');

const categories = [
  'java', 'spring', 'algorithm', 'python',
  'db', 'network', 'os', 'cleancode',
  'security', 'devops', 'javascript', 'collaboration',
  'html-css', 'ai', 'ai-roadmap', 'ai-tech',
  'design-pattern', 'react', 'typescript', 'nextjs'
];

let totalFiles = 0;
let totalPlaceholder = 0;

console.log('카테고리           파일수    플레이스홀더');
console.log('─'.repeat(45));

categories.forEach(cat => {
  const result = convertCategory(cat);
  if (result.total > 0) {
    const status = result.placeholder === result.total ? '⚠️ 전체' :
                   result.placeholder > 0 ? '⚠️ 일부' : '✅';
    console.log(
      `${cat.padEnd(18)} ${String(result.total).padStart(4)}개    ${String(result.placeholder).padStart(4)}개 ${status}`
    );
    totalFiles += result.total;
    totalPlaceholder += result.placeholder;
  }
});

console.log('─'.repeat(45));
console.log(`${'총계'.padEnd(18)} ${String(totalFiles).padStart(4)}개    ${String(totalPlaceholder).padStart(4)}개`);
console.log(`\n플레이스홀더 비율: ${((totalPlaceholder/totalFiles)*100).toFixed(1)}%`);
console.log('\n✅ 변환 완료! src/data/contents/ 폴더 확인');
