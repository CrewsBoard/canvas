import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Panel,
  addEdge,
  useNodesState,
  useEdgesState,
  useReactFlow,
  type OnConnect,
  MarkerType,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { v4 as uuid } from 'uuid';

import { nodeTypes } from '@/components/nodes';
import { edgeTypes } from '@/components/edges/types/edge-types';
import DnDPanel from './dnd-panel';
import NodeEditor from './node-editor';
import { useTheme } from '@/hooks/useTheme';
import { useDnD } from '@/hooks/useDnD';
import { sampleData } from '@/mock/sample';

type OnDrop = (event: React.DragEvent) => void;
type OnDragOver = (event: React.DragEvent) => void;

export default function Flow() {
  const [showNodeEditor, setShowNodeEditor] = useState(false);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { screenToFlowPosition } = useReactFlow();
  const { theme } = useTheme();
  const [nodes, setNodes, onNodesChange] = useNodesState([] as Node[]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([] as Edge[]);
  const { draggedType } = useDnD();

  const toggleNodeEditor = useCallback(() => {
    setShowNodeEditor((show) => !show);
  }, []);

  const onConnect: OnConnect = useCallback(
    (connection) => setEdges((edges) => addEdge(connection, edges)),
    [setEdges]
  );

  const onDragOver: OnDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const handleDeleteNode = useCallback(
    (nodeId: string) => {
      setNodes((nds) => nds.filter((node) => node.id !== nodeId));
      setEdges((eds) =>
        eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId)
      );
    },
    [setNodes, setEdges]
  );

  const handleCopyNode = useCallback(
    (nodeId: string) => {
      setNodes((nds) => {
        const node = nds.find((node) => node.id === nodeId);
        if (node) {
          const newNode = {
            ...node,
            id: uuid(),
            position: {
              x: node.position.x + 50,
              y: node.position.y + 50,
            },
            data: {
              ...node.data,
              title: `${node.data.title} (copy)`,
              onCopy: () => handleCopyNode(newNode.id),
              onDelete: () => handleDeleteNode(newNode.id),
              showEditor: toggleNodeEditor,
            },
          };
          return [...nds, newNode];
        }
        return nds;
      });
    },
    [setNodes, handleDeleteNode, toggleNodeEditor]
  );

  // NOTE: do api call here
  useEffect(() => {
    const initialNodes = sampleData.nodes.map((node) => ({
      ...node,
      data: {
        ...node.data,
        onCopy: () => handleCopyNode(node.id),
        onDelete: () => handleDeleteNode(node.id),
        showEditor: toggleNodeEditor,
      },
    }));
    setNodes(initialNodes);
    setEdges(sampleData.edges);
  }, [setNodes, setEdges, handleCopyNode, handleDeleteNode, toggleNodeEditor]);

  const onDrop: OnDrop = useCallback(
    (event) => {
      event.preventDefault();

      if (!draggedType) {
        return;
      }

      const reactFlowBounds = reactFlowWrapper.current?.getBoundingClientRect();

      if (!reactFlowBounds) {
        return;
      }

      // Calculate position relative to the pane
      const position = screenToFlowPosition({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode = {
        id: uuid(),
        type: draggedType || 'info',
        position,
        data: {
          title: `${draggedType || 'New'} Node`,
          name: draggedType || 'new_node',
          description: 'A new node added via drag and drop',
          is_start_node: false,
          debug_mode: false,
          fields: [],
          node_template_id: draggedType || 'default',
          onCopy: handleCopyNode,
          onDelete: handleDeleteNode,
          showEditor: toggleNodeEditor,
        },
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [
      setNodes,
      handleCopyNode,
      handleDeleteNode,
      draggedType,
      screenToFlowPosition,
      toggleNodeEditor,
    ]
  );

  const defaultEdgeOptions = {
    type: 'input',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  };

  return (
    <div className="h-full flex flex-row" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        edges={edges}
        edgeTypes={edgeTypes}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onDragOver={onDragOver}
        onDrop={onDrop}
        defaultEdgeOptions={defaultEdgeOptions}
        fitView
        colorMode={theme}
      >
        <Background />
        <MiniMap />
        <Controls />
        <Panel position="top-left">
          <DnDPanel />
        </Panel>
        <Panel position="top-right">{showNodeEditor && <NodeEditor />}</Panel>
      </ReactFlow>
      {/* <ChatBoxArea /> */}
    </div>
  );
}
