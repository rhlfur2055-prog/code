'use client';

interface ProgressBarProps {
  percentage: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

export function ProgressBar({ percentage, size = 'md', showLabel = false }: ProgressBarProps) {
  const heightClasses = { sm: 'h-1', md: 'h-2', lg: 'h-3' };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>진행률</span>
          <span>{percentage}%</span>
        </div>
      )}
      <div className={`progress-bar ${heightClasses[size]}`}>
        <div className="progress-fill" style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }} />
      </div>
    </div>
  );
}
