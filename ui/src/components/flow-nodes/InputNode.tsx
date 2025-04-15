import React from 'react';
import { Handle, Position } from 'reactflow';
import NodeBase from './NodeBase';
import { useNodeConfig } from '../../hooks/useNodeConfig';

const InputNode: React.FC = () => {
  const { config, loading, error } = useNodeConfig('input');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!config) return <div>Configuration not found</div>;

  return (
    <NodeBase config={config}>
      <Handle
        type="source"
        position={Position.Right}
        id="output"
        style={{ background: '#555' }}
      />
    </NodeBase>
  );
};

export default InputNode; 