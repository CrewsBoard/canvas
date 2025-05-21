import type { Edge, Node } from '@xyflow/react';
import { create } from 'zustand';

import { FlowState } from '@/types/stores.types.ts';

export const useFlowStateStore = create<FlowState>((set, get) => ({
    // nodes
    nodes: [],
    setNodes: nodes => set(state => ({ ...state, nodes: typeof nodes === 'function' ? nodes(state.nodes) : nodes })),
    getNodes: (): Node[] => get().nodes,
    getNodeById: (id: string): Node | undefined => {
        return get().nodes.find((node: Node) => node.id === id) || undefined;
    },
    setNodeById: (id: string, node: Node) => {
        set((state: FlowState) => ({
            nodes: state.nodes.map((n: Node) => (n.id === id ? node : n)),
        }));
    },
    // edges
    edges: [],
    setEdges: edges => set(state => ({ ...state, edges: typeof edges === 'function' ? edges(state.edges) : edges })),
    getEdges: (): Edge[] => get().edges,
    getEdgeById: (id: string): Edge | undefined => {
        return get().edges.find((edge: Edge) => edge.id === id) || undefined;
    },
    setEdgeById: (id: string, edge: Edge) => {
        set((state: FlowState) => ({
            edges: state.edges.map((n: Edge) => (n.id === id ? edge : n)),
        }));
    },
    // selected node
    selectedNode: null,
    setSelectedNode: node => set({ selectedNode: node }),
}));
