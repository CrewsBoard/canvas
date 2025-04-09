import React from 'react';
import { Handle, Position } from 'reactflow';
import NodeBase from './NodeBase';
import { NodeUIConfig } from '../../types/flow-node';

const outputNodeConfig: NodeUIConfig = {
  title: 'Output',
  description: 'Output data destination',
  icon: 'output',
  color: '#2196F3',
  inputs: [
    {
      name: 'input',
      type: 'any',
      label: 'Input',
      required: true
    }
  ],
  outputs: [],
  settings: [
    {
      name: 'destination',
      type: 'string',
      label: 'Data Destination',
      default: '',
      visible: {},
      enum: [],
      items: {},
      properties: {}
    }
  ]
};

const OutputNode: React.FC = () => {
  return (
    <NodeBase config={outputNodeConfig}>
      <Handle type="target" position={Position.Left} />
    </NodeBase>
  );
};

export default OutputNode; 