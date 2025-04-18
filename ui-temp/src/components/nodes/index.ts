import type { NodeTypes } from '@xyflow/react';

import { type AppNode } from './types/node-types';
import InfoNode from './types/info-node';
import StartNode from './types/start-node';

// Re-export the AppNode type
export type { AppNode };

export const initialNodes: AppNode[] = [
  {
    id: 'a',
    type: 'info',
    position: { x: 0, y: 0 },
    data: {
      label: 'wire',
      onCopy: () => {},
      onDelete: () => {},
      showEditor: () => {},
    },
  },
  {
    id: 'b',
    type: 'info',
    position: { x: -100, y: 100 },
    data: {
      label: 'drag me!',
      onCopy: () => {},
      onDelete: () => {},
      showEditor: () => {},
    },
  },
];

export const nodeTypes = {
  info: InfoNode,
  start: StartNode,
} satisfies NodeTypes;
