'use client';

import { useState, useCallback } from 'react';

interface ImageUploaderProps {
  onUpload: (file: File) => void;
  loading?: boolean;
  accept?: string;
}

export default function ImageUploader({
  onUpload,
  loading = false,
  accept = 'image/*'
}: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = useCallback((file: File) => {
    if (file) {
      setPreview(URL.createObjectURL(file));
      onUpload(file);
    }
  }, [onUpload]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      style={{
        border: `2px dashed ${isDragging ? '#00C471' : '#444'}`,
        borderRadius: '12px',
        padding: '32px',
        textAlign: 'center',
        cursor: loading ? 'not-allowed' : 'pointer',
        backgroundColor: isDragging ? 'rgba(0, 196, 113, 0.1)' : '#25252B',
        transition: 'all 0.2s',
        opacity: loading ? 0.5 : 1,
      }}
    >
      <input
        type="file"
        accept={accept}
        onChange={handleChange}
        disabled={loading}
        style={{ display: 'none' }}
        id="file-upload"
      />
      <label htmlFor="file-upload" style={{ cursor: loading ? 'not-allowed' : 'pointer' }}>
        {preview ? (
          <img
            src={preview}
            alt="Preview"
            style={{
              maxHeight: '200px',
              maxWidth: '100%',
              borderRadius: '8px'
            }}
          />
        ) : (
          <div>
            <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📷</div>
            <p style={{ color: '#9CA3AF', marginBottom: '8px' }}>
              이미지를 드래그하거나 클릭하세요
            </p>
            <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
              PNG, JPG, WEBP (최대 50MB)
            </p>
          </div>
        )}
        {loading && (
          <p style={{ marginTop: '16px', color: '#00C471' }}>
            분석 중...
          </p>
        )}
      </label>
    </div>
  );
}
