import {useMutation, useQuery, useQueryClient} from '@tanstack/react-query';
import {httpClient} from '@/libs/http/httpClient.ts';
import {HttpError, HttpOptions} from '@/types/http.types';

export function useHttpClientQuery<TData, TVariables = void>({
                                                                 queryKey,
                                                                 url,
                                                                 method = 'GET',
                                                                 enabled = true,
                                                                 onSuccess,
                                                                 onError,
                                                                 transformResponse,
                                                             }: HttpOptions<TData, TVariables>) {
    return useQuery<TData, HttpError>({
        queryKey,
        queryFn: async () => {
            try {
                const response = await httpClient.request<TData>(url, {method});
                const transformedData = transformResponse ? transformResponse(response) : response;
                onSuccess?.(transformedData);
                return transformedData;
            } catch (error) {
                if (error instanceof HttpError) {
                    onError?.(error);
                    throw error;
                }
                throw new HttpError(500, 'Unknown error occurred');
            }
        },
        enabled,
    });
}

export function useHttpClientMutation<TData, TVariables = void>({
                                                                    queryKey,
                                                                    url,
                                                                    method = 'POST',
                                                                    onSuccess,
                                                                    onError,
                                                                    transformResponse,
                                                                    transformRequest,
                                                                }: HttpOptions<TData, TVariables>) {
    const queryClient = useQueryClient();

    return useMutation<TData, HttpError, TVariables>({
        mutationFn: async (variables: TVariables) => {
            try {
                const body = transformRequest ? transformRequest(variables) : JSON.stringify(variables);
                const response = await httpClient.request<TData>(url, {
                    method,
                    body
                });
                return transformResponse ? transformResponse(response) : response;
            } catch (error) {
                if (error instanceof HttpError) {
                    onError?.(error);
                    throw error;
                }
                throw new HttpError(500, 'Unknown error occurred');
            }
        },
        onSuccess: (data: TData) => {
            queryClient.invalidateQueries({queryKey});
            onSuccess?.(data);
        },
    });
}
