import type { Edge } from '@xyflow/react';
import { MarkerType } from '@xyflow/react';

export const initialEdges: Edge[] = [
  {
    id: 'a->c',
    type: 'input',
    source: 'a',
    target: 'c',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'b->d',
    type: 'input',
    source: 'b',
    target: 'd',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'c->d',
    type: 'input',
    source: 'c',
    target: 'd',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
];
