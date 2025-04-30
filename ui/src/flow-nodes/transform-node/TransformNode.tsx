import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const TransformNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  return (
    <div className={`node ${selected ? 'selected' : ''}`} style={{ borderColor: '#2196F3' }}>
      <div className="node-header">
        <h3>{data.title}</h3>
      </div>
      <div className="node-content">
        <p>Transformations: {data?.transformations ? 'Configured' : 'Not set'}</p>
      </div>
      <div className="node-ports">
        <div className="input-port" data-handleid="success" />
        <div className="output-port" data-handleid="success" />
        <div className="output-port" data-handleid="failure" />
      </div>

      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-muted-foreground" />
      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-muted-foreground" />
    </div>
  );
};

export default TransformNode;
