import type { Node } from '@xyflow/react';

export type ControlNodeData = {
  label: string;
  onCopy: (nodeId: string, xPos: number, yPos: number) => void;
  onDelete: (nodeId: string) => void;
  showEditor: () => void;
};

export type ControlNode = Node<ControlNodeData>;
export type AppNode = ControlNode;

// Define valid node types
export type NodeTypes = 'input' | 'output' | 'default' | 'info' | 'start';
