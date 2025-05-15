import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/libs/utils';
import { NodeComponentProps } from '@/types/flowNode.types.ts';
import { Handle, Position } from '@xyflow/react';
import { CircleDot, FileText, Play, Tag } from 'lucide-react';
import React from 'react';

const InputNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
  return (
    <Card
      className={cn(
        'min-w-[200px] p-0 text-center gap-0',
        selected ? 'border-2 border-primary border-dashed' : ''
      )}
      onDoubleClick={data?.toggleEditor}
    >
      <CardHeader className="p-4 rounded-tl-lg rounded-tr-lg bg-green-600 text-white">
        <div className="flex flex-row justify-between items-start text-shadow-stone-200">
          <div className="flex items-center gap-2">
            <Tag className="h-4 w-4" />
            <span className="text-sm font-normal">Node Name</span>
          </div>
          <button className="bg-green-700 rounded-full p-1 text-white">
            <Play className="h-2 w-2 fill-current" />
          </button>
        </div>
        <p className="text-md text-left font-semibold">{data?.title || 'N/A'}</p>
      </CardHeader>
      <CardContent className="p-4 rounded-bl-lg rounded-br-lg text-white bg-green-400">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-shadow-stone-200">
            <FileText className="h-4 w-4" />
            <span className="text-sm font-normal">Instructions</span>
          </div>
          <p className="text-sm text-left font-medium">
            {data?.agentGoal ?? "Agent's goal not set"}
          </p>
        </div>

        <div className="flex items-center gap-3 text-sm pt-3">
          <div className="flex items-center gap-1">
            <CircleDot className="h-5 w-5" />
            <span>{data?.model ?? 'GPT-4o'}</span>
          </div>
          <span>·</span>
          <span>{data?.tokens ?? '2000'}</span>
          <span>·</span>
          <span>{data.knowledge}</span>
          <CircleDot className="h-4 w-4 " />
          <span>{data?.children ?? 1} Children</span>
        </div>
      </CardContent>

      <Handle type="source" position={Position.Bottom} className="w-4 h-4 !bg-muted-foreground" />
    </Card>
  );
};

export default InputNode;
