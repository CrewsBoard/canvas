import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const OutputNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  return (
    <div className={`node ${selected ? 'selected' : ''}`} style={{ borderColor: '#FF9800' }}>
      <div className="node-header">
        <h3>{data.title}</h3>
      </div>
      <div className="node-content">
        <p>Output Data: {data?.outputData || 'Not set'}</p>
      </div>
      <div className="node-ports">
        <div className="input-port" data-handleid="success" />
      </div>

      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-muted-foreground" />
    </div>
  );
};

export default OutputNode;
