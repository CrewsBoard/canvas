import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/libs/utils';
import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import React from 'react';

const InputNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  return (
    <Card className={cn('min-w-[200px] p-4 text-center', selected ? 'bg-gray-200' : '')}>
      <CardHeader>{data.title}</CardHeader>
      <CardContent>
        <p>Input Data: {data?.inputData || 'Not set'}</p>
      </CardContent>

      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-muted-foreground" />
    </Card>
  );
};

export default InputNode;
