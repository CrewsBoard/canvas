import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const CrewaiAgentNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  // const toggleShowEditor = () => {
  //   // data?.showEditor();
  // };

  return (
    <div className="react-flow__node-info">
      <div className={`node ${selected ? 'selected' : ''}`} style={{ borderColor: '#9C27B0' }}>
        <div className="node-header">
          <h3>{data.title}</h3>
        </div>
        <div className="node-content">
          <p>Role: {data?.agentRole || 'Not set'}</p>
          <p>Goal: {data?.agentGoal || 'Not set'}</p>
        </div>
        <div className="node-ports">
          <div className="input-port" data-handleid="success" />
          <div className="output-port" data-handleid="success" />
        </div>

        <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-muted-foreground" />
        <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-muted-foreground" />
      </div>
    </div>
  );
};

export default CrewaiAgentNode;
