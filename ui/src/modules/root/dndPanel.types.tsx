import { NodeUiConfig } from '@/types/flowNode.types.ts';

export interface DnDPanelProps {
  nodeUiConfigs?: Record<string, NodeUiConfig>;
  onDragStart?: (event: React.DragEvent, nodeType: string) => void;
  nodeTypes: Record<string, NodeUiConfig>;
}
