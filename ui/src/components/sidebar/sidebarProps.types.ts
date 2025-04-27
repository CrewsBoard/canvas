import {NodeUiConfig} from "@/types/flowNode.types.ts";
import React from "react";

export interface SidebarProps {
    nodeUiConfigs: Record<string, NodeUiConfig>;
    onDragStart: (event: React.DragEvent, nodeType: string) => void;
}
