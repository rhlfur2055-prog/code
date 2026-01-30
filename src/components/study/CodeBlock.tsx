'use client';

import { useState } from 'react';
import { Copy, Check, FileCode } from 'lucide-react';

interface CodeBlockProps {
  language: string;
  code: string;
  filename?: string;
  highlight?: number[];
}

const languageColors: Record<string, string> = {
  JavaScript: 'text-yellow-400',
  TypeScript: 'text-blue-400',
  Python: 'text-green-400',
  Java: 'text-orange-400',
  HTML: 'text-red-400',
  CSS: 'text-blue-300',
  SQL: 'text-purple-400',
  Bash: 'text-gray-400',
};

export function CodeBlock({ language, code, filename, highlight = [] }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = code.trim().split('\n');
  const langColor = languageColors[language] || 'text-gray-400';

  return (
    <div className="rounded-xl overflow-hidden bg-gray-900 border border-gray-700 mb-6 group">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800/80 border-b border-gray-700">
        <div className="flex items-center gap-2">
          <FileCode size={16} className={langColor} />
          <span className={`text-sm font-medium ${langColor}`}>{language}</span>
          {filename && (
            <span className="text-gray-500 text-sm ml-2">• {filename}</span>
          )}
        </div>
        <button
          onClick={handleCopy}
          className={`
            flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium
            transition-all duration-200
            ${copied
              ? 'bg-green-500/20 text-green-400'
              : 'bg-gray-700 text-gray-400 hover:bg-gray-600 hover:text-white'
            }
          `}
        >
          {copied ? (
            <>
              <Check size={14} />
              복사됨!
            </>
          ) : (
            <>
              <Copy size={14} />
              복사
            </>
          )}
        </button>
      </div>

      {/* Code */}
      <div className="overflow-x-auto">
        <pre className="p-4 text-sm leading-relaxed">
          <code>
            {lines.map((line, index) => {
              const lineNumber = index + 1;
              const isHighlighted = highlight.includes(lineNumber);

              return (
                <div
                  key={index}
                  className={`
                    flex
                    ${isHighlighted ? 'bg-yellow-500/10 -mx-4 px-4' : ''}
                  `}
                >
                  <span className="select-none w-8 text-gray-600 text-right mr-4 flex-shrink-0">
                    {lineNumber}
                  </span>
                  <span className={isHighlighted ? 'text-yellow-200' : 'text-gray-300'}>
                    {line || ' '}
                  </span>
                </div>
              );
            })}
          </code>
        </pre>
      </div>
    </div>
  );
}
