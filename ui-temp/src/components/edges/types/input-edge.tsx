import React from 'react';
import {
  BaseEdge,
  Edge,
  EdgeLabelRenderer,
  EdgeProps,
  getBezierPath,
  useReactFlow,
} from '@xyflow/react';

import { Input } from '@/components/ui/input';
interface InputEdgeData {
  text?: string;
  [key: string]: unknown;
}

export default function InputEdge(props: EdgeProps<Edge<InputEdgeData>>) {
  const {
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    style = {},
    markerEnd,
    data,
  } = props;
  const { setEdges } = useReactFlow();
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const onInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEdges((eds: Edge[]) =>
      eds.map((edge: Edge) => {
        if (edge.id === id) {
          edge.data = { ...edge.data, text: event.target.value };
        }
        return edge;
      })
    );
  };

  return (
    <>
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            fontSize: 12,
            pointerEvents: 'all',
          }}
          className="nodrag nopan"
        >
          <Input
            id={`${id}-input`}
            name={`${id}-input`}
            onChange={onInputChange}
            className="w-32 h-8"
            defaultValue={data?.text ?? ''}
            placeholder=""
          />
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
