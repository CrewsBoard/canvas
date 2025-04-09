export interface NodeUIConfig {
  title: string;
  description: string;
  icon: string;
  color: string;
  inputs: NodePort[];
  outputs: NodePort[];
  settings: NodeSetting[];
}

export interface NodePort {
  name: string;
  type: string;
  label: string;
  required: boolean;
}

export interface NodeSetting {
  name: string;
  type: 'string' | 'boolean' | 'number' | 'array' | 'object';
  label: string;
  default: any;
  visible: Record<string, string>;
  enum: string[];
  items: Record<string, string>;
  properties: Record<string, Record<string, string | string[]>>;
} 