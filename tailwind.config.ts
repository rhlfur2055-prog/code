import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // 인프런 스타일 Primary
        primary: {
          DEFAULT: '#00C471',
          dark: '#00A85D',
          light: '#4CD99B',
        },
        // 다크 테마
        dark: {
          bg: '#1B1B1F',
          card: '#25252B',
          border: '#3F3F46',
        },
        // 라이트 테마
        light: {
          bg: '#F5F5F5',
          card: '#FFFFFF',
          border: '#E4E4E7',
        },
        // 난이도 컬러
        level: {
          beginner: '#22C55E',
          basic: '#3B82F6',
          intermediate: '#F59E0B',
          advanced: '#EF4444',
        },
        // 태그 컬러
        tag: {
          required: '#EF4444',
          interview: '#8B5CF6',
          practical: '#06B6D4',
          coding: '#F59E0B',
        },
      },
      fontFamily: {
        sans: ['Pretendard', 'Noto Sans KR', 'sans-serif'],
        mono: ['JetBrains Mono', 'D2Coding', 'monospace'],
      },
    },
  },
  plugins: [],
}
export default config
