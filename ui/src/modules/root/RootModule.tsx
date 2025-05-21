import {
    Background,
    Controls,
    MarkerType,
    MiniMap,
    Node,
    type OnConnect,
    OnEdgesChange,
    OnNodesChange,
    Panel,
    ReactFlow,
    addEdge,
    applyEdgeChanges,
    applyNodeChanges,
    useReactFlow,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { v4 } from 'uuid';

import DnDPanel from '@/modules/root/dndPanel';
import { ActionButtonPanel, NodeEditorPanel } from '@/modules/root/panels';
import { useFlowStateStore } from '@/stores/flowStateStore';
import { useNodeRegistryStore } from '@/stores/nodeRegistryStore';
import { NodeComponentProps } from '@/types/flowNode.types.ts';

const defaultEdgeOptions = {
    type: 'default',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
};

const flowKey = 'crews-flow';

const RootModule: React.FC = () => {
    const [showNodeEditor, setShowNodeEditor] = useState(false);
    const [selectedEditorTemplate, setSelectedEditorTemplate] = useState<string>('');

    const { setViewport, toObject } = useReactFlow();
    const reactFlowWrapper = useRef<HTMLDivElement>(null);

    const { nodeUiConfigs, nodeComponents } = useNodeRegistryStore();

    const { nodes, getNodes, setNodes } = useFlowStateStore();
    const { edges, getEdges, setEdges } = useFlowStateStore();

    const onNodesChange: OnNodesChange = useCallback(
        changes => setNodes(applyNodeChanges(changes, getNodes())),
        [setNodes, getNodes]
    );

    const onEdgesChange: OnEdgesChange = useCallback(
        changes => setEdges(applyEdgeChanges(changes, getEdges())),
        [setEdges, getEdges]
    );

    const onDragStart = useCallback((event: React.DragEvent, nodeType: string, templateType: string) => {
        event.dataTransfer.setData('application/reactflow/node', nodeType);
        event.dataTransfer.setData('application/reactflow/template', templateType);
        event.dataTransfer.effectAllowed = 'move';
    }, []);

    const toggleNodeEditor = useCallback(
        (templateType: string) => {
            if (selectedEditorTemplate !== templateType) {
                setSelectedEditorTemplate(templateType);
            }
            setShowNodeEditor(show => !show);
        },
        [selectedEditorTemplate]
    );

    const onDrop = useCallback(
        (event: React.DragEvent) => {
            event.preventDefault();

            const reactFlowBounds = event.currentTarget.getBoundingClientRect();
            if (!reactFlowBounds) return;

            const position = {
                x: event.clientX - reactFlowBounds.left,
                y: event.clientY - reactFlowBounds.top,
            };

            const type = event.dataTransfer.getData('application/reactflow/node');
            const template = event.dataTransfer.getData('application/reactflow/template');
            const nodeType = nodeUiConfigs[type];

            const newNode: Node = {
                id: `${type}-${v4()}}`,
                type,
                position,
                data: {
                    template: template,
                    title: nodeType?.title,
                    agentRole: 'Dummy agent role',
                    agentGoal: 'Dummy agent goal',
                    settings: {},
                    config: nodeType,
                    toggleEditor: () => toggleNodeEditor(template),
                },
            };

            setNodes(getNodes().concat(newNode));
        },
        [nodeUiConfigs, getNodes, setNodes, toggleNodeEditor]
    );

    const onDragOver = useCallback((event: React.DragEvent) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onConnect: OnConnect = useCallback(
        connection => setEdges(addEdge(connection, getEdges())),
        [setEdges, getEdges]
    );

    const onSave = useCallback(() => {
        const flow = toObject();
        localStorage.setItem(flowKey, JSON.stringify(flow));
    }, [toObject]);

    const onRestore = useCallback(() => {
        const restoreFlow = async () => {
            const flowString = localStorage.getItem(flowKey);
            if (!flowString) return;

            const flow = JSON.parse(flowString);
            if (flow) {
                const { x = 0, y = 0, zoom = 1 } = flow.viewport || {};
                setNodes(flow.nodes || []);
                setEdges(flow.edges || []);
                setViewport({ x, y, zoom });
            }
        };

        restoreFlow();
    }, [setNodes, setEdges, setViewport]);

    useEffect(() => {
        onRestore();
    }, [onRestore]);

    const nodeComponentsParser = Object.entries(nodeUiConfigs).reduce<Record<string, React.FC<NodeComponentProps>>>(
        (componentRecords, [type]) => {
            const component = nodeComponents[type];
            if (component) {
                componentRecords[type] = component.uiComponent;
            }
            return componentRecords;
        },
        {}
    );

    return (
        <div className="h-full flex flex-row" ref={reactFlowWrapper}>
            <ReactFlow
                nodes={nodes}
                nodeTypes={nodeComponentsParser}
                onNodesChange={onNodesChange}
                edges={edges}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onDragOver={onDragOver}
                onDrop={onDrop}
                defaultEdgeOptions={defaultEdgeOptions}
                fitView
            >
                <Background />
                <MiniMap />
                <Controls />
                <Panel position="top-left">
                    <DnDPanel nodeTypes={nodeUiConfigs} onDragStart={onDragStart} />
                </Panel>

                {showNodeEditor ? (
                    <NodeEditorPanel templateType={selectedEditorTemplate} />
                ) : (
                    <ActionButtonPanel onSave={onSave} onRestore={onRestore} />
                )}
            </ReactFlow>
        </div>
    );
};

export default RootModule;
