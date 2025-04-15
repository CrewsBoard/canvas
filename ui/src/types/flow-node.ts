export type NodeTypes = 'agent' | 'condition' | 'tool' | 'crew';

export interface NodeUiConfig {
  id?: string;
  is_start_node?: boolean;
  debug_mode?: boolean;
  type: NodeTypes;
  name: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  inputs: InputTypes[];
  outputs: OutputTypes[];
  fields: NodeUiFields[];
  node_template_id: string;
}

export interface InputTypes {
  name: string;
  type: string;
  label: string;
  required: boolean;
  description?: string;
}

export interface OutputTypes {
  name: string;
  type: string;
  label: string;
  required: boolean;
  description?: string;
}

export interface NodeUiFields {
  name: string;
  type: 'string' | 'boolean' | 'number' | 'array' | 'object';
  label: string;
  default: any;
  required?: boolean;
  description?: string;
  visible?: Record<string, string>;
  enum?: string[];
  items?: Record<string, string>;
  properties?: Record<string, Record<string, string | string[]>>;
} 