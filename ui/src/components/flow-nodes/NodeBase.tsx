import React, { useState } from 'react';
import { Handle, Position } from 'reactflow';
import { NodeUiConfig, NodeTypes } from '../../types/flow-node';
import NodeForm from '../NodeForm';
import AgentNode from './AgentNode';
import ConditionNode from './ConditionNode';
import ToolNode from './ToolNode';
import CrewNode from './CrewNode';

interface NodeBaseProps {
  config?: NodeUiConfig;
  children?: React.ReactNode;
  data?: {
    input?: any;
    output?: any;
    settings?: Record<string, any>;
    config?: NodeUiConfig;
  };
  onSettingsChange?: (settings: Record<string, any>) => void;
}

const NodeBase: React.FC<NodeBaseProps> = ({ 
  config: propConfig, 
  children, 
  data,
  onSettingsChange 
}) => {
  const [showForm, setShowForm] = useState(false);
  const config = propConfig || data?.config;

  if (!config) {
    return null;
  }

  const handleSettingsSave = (values: Record<string, any>) => {
    if (onSettingsChange) {
      onSettingsChange(values);
    }
    setShowForm(false);
  };

  const hasFields = config.fields && config.fields.length > 0;

  const renderNodeContent = () => {
    const nodeProps = {
      config,
      data: {
        settings: data?.settings,
        input: data?.input,
        output: data?.output
      }
    };

    // @todo take it from node_template_id
    switch (config.type as NodeTypes) {
      case 'agent':
        return <AgentNode {...nodeProps} />;
      case 'condition':
        return <ConditionNode {...nodeProps} />;
      case 'tool':
        return <ToolNode {...nodeProps} />;
      case 'crew':
        return <CrewNode {...nodeProps} />;
      default:
        return null;
    }
  };

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
      {config.inputs?.map((input, index) => (
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
      {renderNodeContent()}

      {/* Settings Button */}
      {hasFields && (
        <button
          onClick={() => setShowForm(true)}
          style={{
            background: 'rgba(255,255,255,0.2)',
            border: 'none',
            padding: '4px 8px',
            borderRadius: '4px',
            color: 'white',
            cursor: 'pointer',
            marginBottom: '8px'
          }}
        >
          Configure
        </button>
      )}

      {/* Output Handles */}
      {config.outputs?.map((output, index) => (
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

      {/* Settings Form */}
      {showForm && hasFields && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 1000,
          marginTop: '10px'
        }}>
          <NodeForm
            fields={config.fields}
            onSave={handleSettingsSave}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      {children}
    </div>
  );
};

export default NodeBase; 