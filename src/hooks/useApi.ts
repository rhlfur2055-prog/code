import { useState, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
const AI_API_URL = process.env.NEXT_PUBLIC_AI_API_URL || 'http://localhost:8000';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
}

export function useApi() {
  const { token } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const request = useCallback(
    async <T>(endpoint: string, options: ApiOptions = {}): Promise<T> => {
      setIsLoading(true);
      setError(null);

      const { method = 'GET', body, headers = {} } = options;

      try {
        const response = await fetch(`${API_URL}${endpoint}`, {
          method,
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...headers,
          },
          ...(body ? { body: JSON.stringify(body) } : {}),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Request failed');
        }

        return data;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Request failed';
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [token]
  );

  const aiRequest = useCallback(
    async <T>(endpoint: string, options: ApiOptions = {}): Promise<T> => {
      setIsLoading(true);
      setError(null);

      const { method = 'GET', body, headers = {} } = options;

      try {
        const response = await fetch(`${AI_API_URL}${endpoint}`, {
          method,
          headers: {
            'Content-Type': 'application/json',
            ...headers,
          },
          ...(body ? { body: JSON.stringify(body) } : {}),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'AI request failed');
        }

        return data;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'AI request failed';
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  return { request, aiRequest, isLoading, error };
}
