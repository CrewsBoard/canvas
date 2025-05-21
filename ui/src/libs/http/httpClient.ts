import { BASE_URL, HttpClient, HttpError, RequestOptions } from '@/types/http.types.ts';

export const httpClient: HttpClient = {
    async get<T>(url: string, options: RequestOptions = {}): Promise<T> {
        return this.request<T>(url, { ...options, method: 'GET' });
    },

    async post<T>(url: string, body?: BodyInit, options: RequestOptions = {}): Promise<T> {
        return this.request<T>(url, { ...options, method: 'POST', body });
    },

    async put<T>(url: string, body?: BodyInit, options: RequestOptions = {}): Promise<T> {
        return this.request<T>(url, { ...options, method: 'PUT', body });
    },

    async delete<T>(url: string, options: RequestOptions = {}): Promise<T> {
        return this.request<T>(url, { ...options, method: 'DELETE' });
    },

    async request<T>(url: string, options: RequestOptions): Promise<T> {
        const fullUrl = url.startsWith('http') ? url : `${BASE_URL}/${url.replace(/^\//, '')}`;

        const defaultHeaders: HeadersInit = {
            'Content-Type': 'application/json',
        };

        const config: RequestInit = {
            method: options.method || 'GET',
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        };

        if (options.body) {
            config.body = options.body;
        }

        try {
            const response = await fetch(fullUrl, config);

            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json() as Promise<T>;
                }
                return response.text() as Promise<T>;
            }

            const error = await response.json().catch(() => response.statusText);
            throw new HttpError(response.status, error);
        } catch (error) {
            if (error instanceof HttpError) {
                throw error;
            }
            throw new HttpError(500, 'Network error');
        }
    },
};
