import { memo } from 'react';
import {
  Handle,
  Position,
  NodeToolbar,
  type Node,
  type NodeProps,
} from '@xyflow/react';

import { Button } from '@/components/ui/button';
import { Copy, Delete } from 'lucide-react';

import AgentTemplate from '../templates/agent_node';
import OutpuTemplate from '../templates/output_node';

export type InfoNodeData = {
  onCopy: (id: string) => void;
  onDelete: (id: string) => void;
  showEditor: () => void;
  node_template_id: string;
  [key: string]: unknown;
};

function InfoNode({ data, id }: NodeProps<Node<InfoNodeData>>) {
  const handleCopy = () => {
    data.onCopy?.(id);
  };

  const handleDelete = () => {
    data.onDelete?.(id);
  };

  const toggleShowEditor = () => {
    data.showEditor?.();
  };

  const getInfoTypeNodeTemplate = () => {
    switch (data.node_template_id) {
      case 'crewai_agent':
        return <AgentTemplate data={data} />;
      case 'output':
        return <OutpuTemplate data={data} />;
      default:
        return null;
    }
  };

  return (
    <div className="react-flow__node-info" onDoubleClick={toggleShowEditor}>
      {getInfoTypeNodeTemplate()}

      {/* Node Toolbar */}
      <NodeToolbar offset={0} position={Position.Right}>
        <div className="flex flex-col">
          <Button
            variant="outline"
            className="rounded-none"
            onClick={handleCopy}
          >
            <Copy />
          </Button>
          <Button
            variant="outline"
            className="rounded-none"
            onClick={handleDelete}
          >
            <Delete />
          </Button>
        </div>
      </NodeToolbar>

      {/* Handles */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-2 h-2 !bg-muted-foreground"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-2 h-2 !bg-muted-foreground"
      />
    </div>
  );
}

export default memo(InfoNode);
