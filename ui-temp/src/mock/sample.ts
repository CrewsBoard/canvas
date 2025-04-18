import { MarkerType } from '@xyflow/react';

export const sample = [
  {
    id: null,
    is_start_node: false,
    debug_mode: false,
    type: 'agent',
    name: 'crewai_agent_node',
    title: 'CrewAI Agent',
    description: 'An AI agent that can perform tasks using CrewAI',
    icon: 'ai',
    color: '#9C27B0',
    inputs: ['success'],
    outputs: ['success'],
    fields: [
      {
        label: 'Agent Role',
        description: 'Agent Role',
        type: 'str',
        default: '',
        required: true,
      },
      {
        label: 'Agent Goal',
        description: 'Agent Goal',
        type: 'str',
        default: '',
        required: true,
      },
      {
        label: 'Agent Backstory',
        description: 'Agent Backstory',
        type: 'str',
        default: '',
        required: true,
      },
      {
        label: 'Agent Tools',
        description: 'Agent Tools',
        type: 'list[str]',
        default: [],
        required: false,
      },
      {
        label: 'Max Iterations',
        description: 'Max Iterations',
        type: 'int',
        default: 1,
        required: false,
      },
      {
        label: 'Allow Delegation',
        description: 'Allow Delegation',
        type: 'bool',
        default: false,
        required: false,
      },
      {
        label: 'Model ID',
        description: 'Model ID',
        type: 'list[str]',
        default: '',
        required: true,
      },
    ],
    node_template_id: 'crewai_agent',
  },
  {
    id: null,
    is_start_node: false,
    debug_mode: false,
    type: 'tool',
    name: 'output_node',
    title: 'Output Node',
    description: 'Handles output messages and formatting',
    icon: 'output',
    color: '#FF9800',
    inputs: ['success'],
    outputs: [],
    fields: [
      {
        label: 'Output Data',
        description: 'The data to be output from the node',
        type: null,
        default: null,
        required: null,
      },
    ],
    node_template_id: 'output',
  },
  {
    id: null,
    is_start_node: false,
    debug_mode: false,
    type: 'tool',
    name: 'input_node',
    title: 'Input Node',
    description: 'Handles input messages and adds timestamps',
    icon: 'input',
    color: '#4CAF50',
    inputs: [],
    outputs: ['success'],
    fields: [
      {
        label: 'Input Data',
        description: 'The data to be input into the node',
        type: 'str',
        default: '',
        required: true,
      },
    ],
    node_template_id: 'input',
  },
  {
    id: null,
    is_start_node: true,
    debug_mode: false,
    type: 'crew',
    name: 'crewai_crew_start_node',
    title: 'CrewAI Crew Start Node',
    description: 'Start node for CrewAI',
    icon: 'ai',
    color: '#9C27B0',
    inputs: ['success'],
    outputs: ['success'],
    fields: [
      {
        label: 'Crew Node',
        description: 'This node is a CrewAI node',
        type: null,
        default: null,
        required: null,
      },
    ],
    node_template_id: 'crewai_crew',
  },
  {
    id: null,
    is_start_node: false,
    debug_mode: false,
    type: 'tool',
    name: 'transform_node',
    title: 'Transform Node',
    description: 'Transforms message data based on configuration',
    icon: 'transform',
    color: '#2196F3',
    inputs: ['success'],
    outputs: ['success', 'failure'],
    fields: [
      {
        label: 'Transformations',
        description: 'The transformations to be applied to the data',
        type: null,
        default: null,
        required: null,
      },
    ],
    node_template_id: 'transform',
  },
];

export const sampleNodes = [
  {
    id: 'a', // must required for react-flow
    position: { x: 0, y: 0 }, // must required for react-flow
    type: 'info', // must required for react-flow
    data: {
      // must required for react-flow
      is_start_node: false,
      debug_mode: false,
      name: 'crewai_agent_node',
      title: 'CrewAI Agent',
      description: 'An AI agent that can perform tasks using CrewAI',
      fields: [
        {
          id: 'agent_role',
          label: 'Agent Role',
          description: 'Agent Role',
          type: 'str',
          default: '',
          required: true,
        },
        {
          id: 'agent_goal',
          label: 'Agent Goal',
          description: 'Agent Goal',
          type: 'str',
          default: '',
          required: true,
        },
      ],
      node_template_id: 'crewai_agent',
    },
  },
  {
    id: 'b', // must required for react-flow
    position: { x: -100, y: -100 }, // must required for react-flow
    type: 'info', // must required for react-flow
    data: {
      // must required for react-flow
      is_start_node: false,
      debug_mode: false,
      name: 'output_node',
      title: 'Output Node',
      description: 'Handles output messages and formatting',
      fields: [
        {
          id: 'output_data',
          label: 'Output Data',
          description: 'The data to be output from the node',
          type: 'str',
          default: '',
          required: true,
        },
      ],
      node_template_id: 'output',
    },
  },
  {
    id: 'c', // must required for react-flow
    position: { x: -200, y: -200 }, // must required for react-flow
    type: 'info', // must required for react-flow
    data: {
      // must required for react-flow
      is_start_node: false,
      debug_mode: false,
      name: 'output_node',
      title: 'Output Node',
      description: 'Handles output messages and formatting',
      fields: [
        {
          id: 'output_data',
          label: 'Output Data',
          description: 'The data to be output from the node',
          type: 'str',
          default: '',
          required: true,
        },
      ],
      node_template_id: 'output',
    },
  },
];

// all fields required for react-flow in case of edge
export const sampleEdges = [
  {
    id: 'a->b', // id does not have to be formatted like this
    type: 'input',
    source: 'a',
    target: 'b',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'b->c', // id does not have to be formatted like this
    type: 'input',
    source: 'b',
    target: 'c',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'c->a', // id does not have to be formatted like this
    type: 'input',
    source: 'c',
    target: 'a',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
];

export const sampleData = {
  nodes: sampleNodes,
  edges: sampleEdges,
};
