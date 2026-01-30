import { useState, useCallback } from 'react';

const AI_API_URL = process.env.NEXT_PUBLIC_AI_API_URL || 'http://localhost:8080/api/ai';

interface Detection {
  class_name: string;
  confidence: number;
  bbox: number[];
}

interface DetectionResponse {
  success: boolean;
  detections: Detection[];
  count: number;
}

interface TranscriptionResponse {
  success: boolean;
  text: string;
  language?: string;
}

interface CaptionResponse {
  success: boolean;
  caption: string;
}

export function useAiApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const callApi = useCallback(async <T>(
    endpoint: string,
    file: File | Blob,
    filename?: string
  ): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file, filename || 'file');

      const response = await fetch(`${AI_API_URL}${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      return await response.json();
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const detectObjects = useCallback(async (file: File): Promise<DetectionResponse | null> => {
    return callApi<DetectionResponse>('/detect', file);
  }, [callApi]);

  const transcribe = useCallback(async (file: File | Blob): Promise<TranscriptionResponse | null> => {
    return callApi<TranscriptionResponse>('/transcribe', file, 'audio.webm');
  }, [callApi]);

  const removeBackground = useCallback(async (file: File): Promise<{ success: boolean; image: string } | null> => {
    return callApi('/remove-background', file);
  }, [callApi]);

  const imageCaption = useCallback(async (file: File): Promise<CaptionResponse | null> => {
    return callApi<CaptionResponse>('/caption', file);
  }, [callApi]);

  const checkHealth = useCallback(async (): Promise<boolean> => {
    try {
      const response = await fetch(`${AI_API_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }, []);

  return {
    detectObjects,
    transcribe,
    removeBackground,
    imageCaption,
    checkHealth,
    loading,
    error,
  };
}
