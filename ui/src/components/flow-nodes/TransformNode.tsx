import React from 'react';
import { Handle, Position } from 'reactflow';
import NodeBase from './NodeBase';
import { NodeUIConfig } from '../../types/flow-node';

const transformNodeConfig: NodeUIConfig = {
  title: 'Transform',
  description: 'Transform and modify data',
  icon: 'transform',
  color: '#FFA500',
  inputs: [
    {
      name: 'input',
      type: 'any',
      label: 'Input',
      required: true
    }
  ],
  outputs: [
    {
      name: 'output',
      type: 'any',
      label: 'Output',
      required: true
    }
  ],
  settings: [
    {
      name: 'transform',
      type: 'string',
      label: 'Transform Function',
      default: '',
      visible: {},
      enum: [],
      items: {},
      properties: {}
    }
  ]
};

const TransformNode: React.FC = () => {
  return (
    <NodeBase config={transformNodeConfig}>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </NodeBase>
  );
};

export default TransformNode; 