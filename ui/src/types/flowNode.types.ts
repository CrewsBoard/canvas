import React from 'react';

export type NodeTypes = 'agent' | 'condition' | 'tool' | 'crew';

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
    default: never;
    required?: boolean;
    description?: string;
    visible?: Record<string, string>;
    enum?: string[];
    items?: Record<string, string>;
    properties?: Record<string, Record<string, string | string[]>>;
}

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
    ui_bundle?: string;
}

export interface NodeComponentProps {
    id: string;
    data: Record<string, never>;
    isConnectable: boolean;
    selected: boolean;
}

export interface NodeRegistry {
    [key: string]: {
        uiComponent: React.FC<NodeComponentProps>;
    };
}

export interface NodeModule {
    nodes: NodeRegistry;
    initialize: (nodeUiConfigs: NodeUiConfig[]) => Promise<void>;
    cleanup: () => Promise<void>;
}
