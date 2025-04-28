export interface HttpClient {
    get<T>(url: string, options?: RequestOptions): Promise<T>;

    post<T>(url: string, body?: BodyInit, options?: RequestOptions): Promise<T>;

    put<T>(url: string, body?: BodyInit, options?: RequestOptions): Promise<T>;

    delete<T>(url: string, options?: RequestOptions): Promise<T>;

    request<T>(url: string, options: RequestOptions): Promise<T>;
}

export interface RequestOptions {
    headers?: HeadersInit;
    body?: BodyInit;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    credentials?: RequestCredentials;
    mode?: RequestMode;
    cache?: RequestCache;
}

export class HttpError extends Error {
    status: number;
    error: unknown;

    constructor(status: number, error: unknown) {
        const errorMessage = typeof error === 'string' ? error : JSON.stringify(error);
        super(errorMessage);
        this.status = status;
        this.error = error;
    }
}

// @todo take it from environment variables
export const BASE_URL = 'http://localhost:3001/api';

export interface HttpOptions<TData, TVariables = void> {
    // @todo query key can be the url so need to be decided
    queryKey: string[];
    url: string;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    enabled?: boolean;
    onSuccess?: (data: TData) => void;
    onError?: (error: HttpError) => void;
    transformResponse?: (data: unknown) => TData;
    transformRequest?: (variables: TVariables) => BodyInit;
}
