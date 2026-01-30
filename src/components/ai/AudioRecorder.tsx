'use client';

import { useState, useRef, useCallback } from 'react';

interface AudioRecorderProps {
  onRecordComplete: (blob: Blob) => void;
  loading?: boolean;
}

export default function AudioRecorder({ onRecordComplete, loading = false }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        onRecordComplete(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setDuration(0);

      timerRef.current = setInterval(() => {
        setDuration(d => d + 1);
      }, 1000);

    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('마이크 접근 권한이 필요합니다.');
    }
  }, [onRecordComplete]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  }, [isRecording]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '16px',
      padding: '32px',
      backgroundColor: '#25252B',
      borderRadius: '12px'
    }}>
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={loading}
        style={{
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          border: 'none',
          backgroundColor: isRecording ? '#EF4444' : '#00C471',
          cursor: loading ? 'not-allowed' : 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '2rem',
          transition: 'all 0.2s',
          animation: isRecording ? 'pulse 1.5s infinite' : 'none',
          opacity: loading ? 0.5 : 1
        }}
      >
        {isRecording ? '⏹️' : '🎤'}
      </button>

      {isRecording && (
        <div style={{
          color: '#EF4444',
          fontFamily: 'monospace',
          fontSize: '1.25rem'
        }}>
          {formatTime(duration)}
        </div>
      )}

      <p style={{ color: '#9CA3AF', fontSize: '0.875rem' }}>
        {loading ? '변환 중...' :
         isRecording ? '녹음 중... 클릭하여 중지' :
         '클릭하여 녹음 시작'}
      </p>

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
      `}</style>
    </div>
  );
}
