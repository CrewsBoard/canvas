import React from 'react';
import { Handle, Position } from 'reactflow';
import { NodeUIConfig } from '../../types/flow-node';

interface NodeBaseProps {
  config: NodeUIConfig;
  children?: React.ReactNode;
  data?: {
    input?: any;
    output?: any;
  };
}

const NodeBase: React.FC<NodeBaseProps> = ({ config, children, data }) => {
  return (
    <div
      style={{
        padding: '10px',
        borderRadius: '5px',
        backgroundColor: config.color,
        color: 'white',
        minWidth: '150px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}
    >
      {/* Input Handles */}
      {config.inputs.map((input, index) => (
        <Handle
          key={`input-${input.name}`}
          type="target"
          position={Position.Left}
          id={input.name}
          style={{
            top: `${(index + 1) * 30}px`,
            background: input.required ? '#ff4444' : '#555',
            width: '8px',
            height: '8px'
          }}
        />
      ))}

      {/* Node Content */}
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
        <span style={{ marginRight: '8px', fontSize: '20px' }}>{config.icon}</span>
        <div>
          <div style={{ fontWeight: 'bold' }}>{config.title}</div>
          <div style={{ fontSize: '12px', opacity: 0.8 }}>{config.description}</div>
        </div>
      </div>

      {/* Input Data */}
      {data?.input && (
        <div style={{ 
          background: 'rgba(0,0,0,0.2)', 
          padding: '8px', 
          borderRadius: '4px',
          marginBottom: '8px',
          fontSize: '12px'
        }}>
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Input:</div>
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {JSON.stringify(data.input, null, 2)}
          </pre>
        </div>
      )}

      {/* Output Data */}
      {data?.output && (
        <div style={{ 
          background: 'rgba(0,0,0,0.2)', 
          padding: '8px', 
          borderRadius: '4px',
          marginBottom: '8px',
          fontSize: '12px'
        }}>
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Output:</div>
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {JSON.stringify(data.output, null, 2)}
          </pre>
        </div>
      )}

      {/* Output Handles */}
      {config.outputs.map((output, index) => (
        <Handle
          key={`output-${output.name}`}
          type="source"
          position={Position.Right}
          id={output.name}
          style={{
            top: `${(index + 1) * 30}px`,
            background: output.required ? '#ff4444' : '#555',
            width: '8px',
            height: '8px'
          }}
        />
      ))}

      {children}
    </div>
  );
};

export default NodeBase; 