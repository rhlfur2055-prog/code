'use client';

interface Detection {
  class_name?: string;
  className?: string;
  confidence: number;
  bbox: number[];
}

interface DetectionResultProps {
  detections: Detection[];
  imageUrl?: string;
}

const confidenceColor = (conf: number) => {
  if (conf > 0.9) return '#00C471';
  if (conf > 0.7) return '#3B82F6';
  if (conf > 0.5) return '#F59E0B';
  return '#EF4444';
};

export default function DetectionResult({ detections, imageUrl }: DetectionResultProps) {
  return (
    <div style={{
      backgroundColor: '#25252B',
      borderRadius: '12px',
      padding: '20px'
    }}>
      <h3 style={{
        fontSize: '1.125rem',
        fontWeight: 'bold',
        marginBottom: '16px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        🎯 탐지 결과
        <span style={{
          backgroundColor: '#00C471',
          color: '#000',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '0.875rem'
        }}>
          {detections.length}개
        </span>
      </h3>

      {imageUrl && (
        <div style={{
          position: 'relative',
          marginBottom: '16px',
          borderRadius: '8px',
          overflow: 'hidden'
        }}>
          <img
            src={imageUrl}
            alt="Analyzed"
            style={{ width: '100%', display: 'block' }}
          />
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {detections.map((det, idx) => {
          const className = det.class_name || det.className || 'unknown';
          const conf = det.confidence;

          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backgroundColor: '#1B1B1F',
                padding: '12px 16px',
                borderRadius: '8px',
                borderLeft: `3px solid ${confidenceColor(conf)}`
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '1.25rem' }}>
                  {className === 'person' ? '👤' :
                   className === 'car' ? '🚗' :
                   className === 'dog' ? '🐕' :
                   className === 'cat' ? '🐈' : '📦'}
                </span>
                <span style={{ fontWeight: 500 }}>{className}</span>
              </div>
              <div style={{
                color: confidenceColor(conf),
                fontWeight: 'bold',
                fontFamily: 'monospace'
              }}>
                {(conf * 100).toFixed(1)}%
              </div>
            </div>
          );
        })}

        {detections.length === 0 && (
          <p style={{
            textAlign: 'center',
            color: '#6B7280',
            padding: '20px'
          }}>
            탐지된 객체가 없습니다
          </p>
        )}
      </div>
    </div>
  );
}
