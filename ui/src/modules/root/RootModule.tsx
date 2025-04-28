import React, {useCallback, useState} from 'react';
import {
    applyEdgeChanges,
    applyNodeChanges,
    Background,
    Controls,
    Edge,
    EdgeChange,
    Node,
    NodeChange,
    ReactFlow
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import Sidebar from '@/components/sidebar/Sidebar';
import {useNodeRegistryStore} from '@/stores/nodeRegistryStore';
import {NodeComponentProps} from "@/types/flowNode.types.ts";

const RootModule: React.FC = () => {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const {nodeUiConfigs, nodeComponents} = useNodeRegistryStore();

    const onDragStart = useCallback((event: React.DragEvent, nodeType: string) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    }, []);

    const onDrop = useCallback((event: React.DragEvent) => {
        event.preventDefault();

        const reactFlowBounds = event.currentTarget.getBoundingClientRect();
        const type = event.dataTransfer.getData('application/reactflow');
        const position = {
            x: event.clientX - reactFlowBounds.left,
            y: event.clientY - reactFlowBounds.top,
        };

        const nodeType = nodeUiConfigs[type];
        const newNode: Node = {
            id: `${type}-${Date.now()}`,
            type,
            position,
            data: {
                title: nodeType?.title,
                agentRole: '',
                agentGoal: '',
                settings: {},
                config: nodeType
            },
        };

        setNodes((nds) => nds.concat(newNode));
    }, [nodeUiConfigs]);

    const onDragOver = useCallback((event: React.DragEvent) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const nodeComponentsParser = Object.entries(nodeUiConfigs).reduce<Record<string, React.FC<NodeComponentProps>>>((componentRecords, [type]) => {
        const component = nodeComponents[type];
        if (component) {
            componentRecords[type] = component.uiComponent;
        }
        return componentRecords;
    }, {});

    return (
        <div style={{width: '100%', height: '100%', position: 'relative'}}>
            <Sidebar nodeTypes={nodeUiConfigs} onDragStart={onDragStart}/>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeComponentsParser}
                onNodesChange={(changes: NodeChange[]) => {
                    setNodes((nds) => applyNodeChanges(changes, nds));
                }}
                onEdgesChange={(changes: EdgeChange[]) => {
                    setEdges((eds) => applyEdgeChanges(changes, eds));
                }}
                onDrop={onDrop}
                onDragOver={onDragOver}
            >
                <Background/>
                <Controls/>
            </ReactFlow>
        </div>
    );
};

export default RootModule;
