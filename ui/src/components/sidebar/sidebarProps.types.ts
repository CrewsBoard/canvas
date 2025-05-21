import React from 'react';

import { NodeUiConfig } from '@/types/flowNode.types.ts';

export interface SidebarProps {
    nodeUiConfigs: Record<string, NodeUiConfig>;
    onDragStart: (event: React.DragEvent, nodeType: string) => void;
}
