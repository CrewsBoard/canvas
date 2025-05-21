import { create } from 'zustand';

import uiComponentLoader from '@/libs/services/uiComponentLoaderService.ts';
import { NodeUiConfig } from '@/types/flowNode.types';
import { NodeRegistryState } from '@/types/stores.types.ts';

export const useNodeRegistryStore = create<NodeRegistryState>(set => ({
    nodeUiConfigs: {},
    nodeComponents: {},
    loading: true,
    error: null,
    loadFlowNodeUiBundle: async (nodeUiConfigs: NodeUiConfig[]) => {
        try {
            await uiComponentLoader.initialize(nodeUiConfigs);
            const nodeUiConfig = nodeUiConfigs.reduce(
                (acc: Record<string, NodeUiConfig>, nodeType: NodeUiConfig) => {
                    acc[nodeType.name] = nodeType;
                    return acc;
                },
                {} as Record<string, NodeUiConfig>
            );

            set({
                nodeUiConfigs: nodeUiConfig,
                loading: false,
                error: null,
                nodeComponents: { ...uiComponentLoader.nodes },
            });
            console.log('Flow node ui bundles are loaded successfully');
        } catch (err) {
            console.error(err);
            set({
                error: err instanceof Error ? err.message : 'Failed to load flow node ui bundle',
                loading: false,
            });
        }
    },
}));
