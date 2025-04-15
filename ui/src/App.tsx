import React, { useState, useCallback, useEffect, useMemo } from 'react';
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
import { fetchNodeTypes } from './services/nodeService';
import { NodeUIConfig } from './types/flow-node';
import NodeBase from './components/flow-nodes/NodeBase';

const initialEdges: Edge[] = [];

function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeTypes, setNodeTypes] = useState<NodeUIConfig[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadNodeTypes = async () => {
      try {
        const types = await fetchNodeTypes();
        setNodeTypes(types);
      } catch (error) {
        console.error('Error loading node types:', error);
      } finally {
        setLoading(false);
      }
    };

    loadNodeTypes();
  }, []);

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

    const nodeConfig = nodeTypes.find(nt => nt.title === type);
    if (!nodeConfig) return;

    const newNode: Node = {
      id: `${type}-${nodes.length + 1}`,
      type: 'nodeBase',
      position,
      data: { 
        label: type,
        config: nodeConfig,
        settings: {}
      },
    };

    setNodes((nds) => nds.concat(newNode));
  };

  const handleNodeSettingsChange = useCallback((nodeId: string, settings: Record<string, any>) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          return {
            ...node,
            data: {
              ...node.data,
              settings
            }
          };
        }
        return node;
      })
    );
  }, []);

  const customNodeTypes = useMemo<NodeTypes>(() => ({
    nodeBase: (props) => (
      <NodeBase
        {...props}
        onSettingsChange={(settings) => handleNodeSettingsChange(props.id, settings)}
      />
    ),
  }), [handleNodeSettingsChange]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', background: '#1a1a1a', padding: '20px', borderRight: '1px solid #333' }}>
        <h3 style={{ color: 'white', marginBottom: '20px' }}>Node Types</h3>
        {nodeTypes.map((node) => (
          <div
            key={node.title}
            draggable
            onDragStart={(e) => onDragStart(e, node.title)}
            style={{
              background: '#2a2a2a',
              padding: '10px',
              marginBottom: '10px',
              borderRadius: '5px',
              cursor: 'grab',
              color: 'white',
            }}
          >
            <div style={{ fontWeight: 'bold' }}>{node.title}</div>
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
          nodeTypes={customNodeTypes}
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