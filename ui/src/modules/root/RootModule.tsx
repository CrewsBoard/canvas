import { Button } from '@/components/ui/button';
import DnDPanel from '@/modules/root/dndPanel';
import NodeEditor from '@/modules/root/editor';
import { useNodeRegistryStore } from '@/stores/nodeRegistryStore';
import { NodeComponentProps } from '@/types/flowNode.types.ts';
import {
  addEdge,
  Background,
  Controls,
  Edge,
  MarkerType,
  MiniMap,
  Node,
  Panel,
  ReactFlow,
  useEdgesState,
  useNodesState,
  useReactFlow,
  type OnConnect,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import React, { useCallback, useEffect, useRef, useState } from 'react';

const defaultEdgeOptions = {
  type: 'default',
  animated: true,
  markerEnd: { type: MarkerType.ArrowClosed },
};

const flowKey = 'crews-flow';

const RootModule: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const { nodeUiConfigs, nodeComponents } = useNodeRegistryStore();
  const [showNodeEditor, setShowNodeEditor] = useState(false);
  const { setViewport, toObject } = useReactFlow();

  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  const onDragStart = useCallback(
    (event: React.DragEvent, nodeType: string, templateType: string) => {
      event.dataTransfer.setData('application/reactflow/node', nodeType);
      event.dataTransfer.setData('application/reactflow/template', templateType);
      event.dataTransfer.effectAllowed = 'move';
    },
    []
  );

  const toggleNodeEditor = useCallback(() => {
    setShowNodeEditor(show => !show);
  }, []);

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
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: {
          template: template,
          title: nodeType?.title,
          agentRole: '',
          agentGoal: '',
          settings: {},
          config: nodeType,
          showEditor: () => toggleNodeEditor,
        },
      };

      setNodes(nds => nds.concat(newNode));
    },
    [nodeUiConfigs, setNodes, toggleNodeEditor]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onConnect: OnConnect = useCallback(
    connection => setEdges(edges => addEdge(connection, edges)),
    [setEdges]
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

  const nodeComponentsParser = Object.entries(nodeUiConfigs).reduce<
    Record<string, React.FC<NodeComponentProps>>
  >((componentRecords, [type]) => {
    const component = nodeComponents[type];
    if (component) {
      componentRecords[type] = component.uiComponent;
    }
    return componentRecords;
  }, {});

  return (
    <div className="h-full flex flex-row" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        nodeTypes={nodeComponentsParser}
        onNodesChange={onNodesChange}
        edges={edges}
        // edgeTypes={edgeTypes}
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
        <Panel position="top-right">{showNodeEditor && <NodeEditor />}</Panel>
        <Panel position="top-right">
          <div className="flex gap-2">
            <Button variant="outline" onClick={onSave}>
              save
            </Button>
            <Button variant="outline" onClick={onRestore}>
              restore
            </Button>
          </div>
        </Panel>
      </ReactFlow>
    </div>
  );
};

export default RootModule;
