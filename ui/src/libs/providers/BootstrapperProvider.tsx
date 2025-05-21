import React, { useEffect } from 'react';

import { useHttpClientQuery } from '@/libs/hooks/useHttpClient.ts';
import { useNodeRegistryStore } from '@/stores/nodeRegistryStore';
import { NodeUiConfig } from '@/types/flowNode.types.ts';
import { BootstrapperProviderProps } from '@/types/providers.types.ts';

export const BootstrapperProvider: React.FC<BootstrapperProviderProps> = ({ children }) => {
    const {
        loading: flowNodeRegistryLoading,
        error: flowNodeRegistryError,
        loadFlowNodeUiBundle,
    } = useNodeRegistryStore();

    const {
        data: nodeTypes,
        isLoading,
        error,
    } = useHttpClientQuery<NodeUiConfig[]>({
        queryKey: ['node-ui-configs'],
        url: '/node-types',
        transformResponse: data => data as NodeUiConfig[],
    });

    useEffect(() => {
        if (nodeTypes) {
            loadFlowNodeUiBundle(nodeTypes);
        }
    }, [nodeTypes, loadFlowNodeUiBundle]);

    if (isLoading || flowNodeRegistryLoading) {
        return <div>Loading nodes...</div>;
    }

    if (error || flowNodeRegistryError) {
        return <div>Error loading nodes: {error?.message || flowNodeRegistryError}</div>;
    }

    return <>{children}</>;
};

export default BootstrapperProvider;
