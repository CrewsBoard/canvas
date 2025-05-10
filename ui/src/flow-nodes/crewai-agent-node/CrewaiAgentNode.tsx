import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/libs/utils';
import NodeTemplateFactory from '@/node-templates/NodeTemplateFactory';
import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const CrewaiAgentNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  console.log('🚀 ~ data:', data);
  return (
    <Card
      className={cn('min-w-[200px] p-4 text-center', selected ? 'border-2 border-primary' : '')}
    >
      <CardHeader>{data.title}</CardHeader>
      <CardContent className="p-0">
        <NodeTemplateFactory type={data?.template} />
      </CardContent>

      <Handle type="target" position={Position.Top} className="w-7 h-7 !bg-muted-foreground" />
      <Handle type="source" position={Position.Bottom} className="w-4 h-4 !bg-muted-foreground" />
    </Card>
  );
};

export default CrewaiAgentNode;
