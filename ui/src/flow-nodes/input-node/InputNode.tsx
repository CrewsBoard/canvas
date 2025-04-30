import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const InputNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  return (
    <div className={`node ${selected ? 'selected' : ''}`} style={{ borderColor: '#4CAF50' }}>
      <div className="node-header">
        <h3>{data.title}</h3>
      </div>
      <div className="node-content">
        <p>Input Data: {data?.inputData || 'Not set'}</p>
      </div>
      <div className="node-ports">
        <div className="output-port" data-handleid="success" />
      </div>

      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-muted-foreground" />
    </div>
  );
};

export default InputNode;
