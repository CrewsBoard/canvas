import type { Edge, Node } from '@xyflow/react';

import { NodeRegistry, NodeUiConfig } from '@/types/flowNode.types.ts';

export interface NodeRegistryState {
    nodeUiConfigs: Record<string, NodeUiConfig>;
    nodeComponents: NodeRegistry;
    loading: boolean;
    error: string | null;
    loadFlowNodeUiBundle: (nodeUiConfigs: NodeUiConfig[]) => Promise<void>;
}

export interface FlowState {
    nodes: Node[];
    edges: Edge[];
    setNodes: (nodes: Node[]) => void;
    getNodes: () => Node[];
    getNodeById: (id: string) => Node | undefined;
    setNodeById: (id: string, node: Node) => void;
    setEdges: (edges: Edge[]) => void;
    getEdges: () => Edge[];
    getEdgeById: (id: string) => Edge | undefined;
    setEdgeById: (id: string, edge: Edge) => void;
}
