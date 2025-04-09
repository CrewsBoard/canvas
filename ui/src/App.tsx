import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
  NodeTypes,
  BackgroundVariant,
} from 'reactflow';
import 'reactflow/dist/style.css';
import InputNode from './components/flow-nodes/InputNode';
import OutputNode from './components/flow-nodes/OutputNode';
import TransformNode from './components/flow-nodes/TransformNode';

const nodeTypes: NodeTypes = {
  input: InputNode,
  output: OutputNode,
  transform: TransformNode,
};

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    position: { x: 250, y: 25 },
    data: { 
      label: 'Input Node',
      input: { message: 'Hello World' }
    },
  },
  {
    id: '2',
    type: 'transform',
    position: { x: 250, y: 125 },
    data: { label: 'Transform Node' },
  },
  {
    id: '3',
    type: 'output',
    position: { x: 250, y: 225 },
    data: { label: 'Output Node' },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2' },
  { id: 'e2-3', source: '2', target: '3' },
];

const nodeTemplates = [
  { type: 'input', label: 'Input Node', description: 'Receives input data' },
  { type: 'transform', label: 'Transform Node', description: 'Transforms data' },
  { type: 'output', label: 'Output Node', description: 'Sends data to external systems' },
];

function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const onDragOver = (event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const type = event.dataTransfer.getData('application/reactflow');
    const reactFlowBounds = event.currentTarget.getBoundingClientRect();
    const position = {
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    };

    const newNode: Node = {
      id: `${type}-${nodes.length + 1}`,
      type,
      position,
      data: { label: `${type} Node` },
    };

    setNodes((nds) => nds.concat(newNode));
  };

  // Process data through the flow
  useEffect(() => {
    const processData = async () => {
      const updatedNodes = [...nodes];
      
      // Find input node
      const inputNode = updatedNodes.find(node => node.type === 'input');
      if (!inputNode) return;

      // Process through the flow
      let currentData = inputNode.data.input;
      let currentNode = inputNode;

      while (currentNode) {
        // Find next node
        const edge = edges.find(e => e.source === currentNode.id);
        if (!edge) break;

        const nextNode = updatedNodes.find(n => n.id === edge.target);
        if (!nextNode) break;

        // Process data based on node type
        switch (nextNode.type) {
          case 'transform':
            // Example transformation
            nextNode.data.input = currentData;
            nextNode.data.output = {
              ...currentData,
              transformed: true,
              timestamp: new Date().toISOString()
            };
            currentData = nextNode.data.output;
            break;
          case 'output':
            nextNode.data.input = currentData;
            nextNode.data.output = currentData;
            break;
        }

        currentNode = nextNode;
      }

      setNodes(updatedNodes);
    };

    processData();
  }, [nodes, edges]);

  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', background: '#1a1a1a', padding: '20px', borderRight: '1px solid #333' }}>
        <h3 style={{ color: 'white', marginBottom: '20px' }}>Node Types</h3>
        {nodeTemplates.map((node) => (
          <div
            key={node.type}
            draggable
            onDragStart={(e) => onDragStart(e, node.type)}
            style={{
              background: '#2a2a2a',
              padding: '10px',
              marginBottom: '10px',
              borderRadius: '5px',
              cursor: 'grab',
              color: 'white',
            }}
          >
            <div style={{ fontWeight: 'bold' }}>{node.label}</div>
            <div style={{ fontSize: '12px', opacity: 0.7 }}>{node.description}</div>
          </div>
        ))}
      </div>

      {/* Flow Area */}
      <div style={{ flex: 1, height: '100vh' }} onDragOver={onDragOver} onDrop={onDrop}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}

export default App; 