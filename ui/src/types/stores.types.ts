import { NodeRegistry, NodeUiConfig } from '@/types/flowNode.types.ts';

export interface NodeRegistryState {
    nodeUiConfigs: Record<string, NodeUiConfig>;
    nodeComponents: NodeRegistry;
    loading: boolean;
    error: string | null;
    loadFlowNodeUiBundle: (nodeUiConfigs: NodeUiConfig[]) => Promise<void>;
}
