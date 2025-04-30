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
  type OnConnect,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import React, { useCallback, useRef, useState } from 'react';

const defaultEdgeOptions = {
  type: 'input',
  animated: true,
  markerEnd: { type: MarkerType.ArrowClosed },
};

const RootModule: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  console.log('🚀 ~ nodes:', nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  console.log('🚀 ~ edges:', edges);
  const { nodeUiConfigs, nodeComponents } = useNodeRegistryStore();
  const [showNodeEditor, setShowNodeEditor] = useState(false);

  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  const onDragStart = useCallback((event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  }, []);

  const toggleNodeEditor = useCallback(() => {
    console.log('clicked');
    setShowNodeEditor(show => !show);
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
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
    // <div style={{ width: '100%', height: '100%', position: 'relative' }}>
    //   <ReactFlow
    //     nodes={nodes}
    //     edges={edges}
    //     nodeTypes={nodeComponentsParser}
    //     onNodesChange={(changes: NodeChange[]) => {
    //       setNodes(nds => applyNodeChanges(changes, nds));
    //     }}
    //     onEdgesChange={(changes: EdgeChange[]) => {
    //       setEdges(eds => applyEdgeChanges(changes, eds));
    //     }}
    //     onDrop={onDrop}
    //     onDragOver={onDragOver}
    //   >
    //     <Background />
    //     <Controls />
    //   </ReactFlow>
    // </div>
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
      </ReactFlow>
    </div>
  );
};

export default RootModule;
