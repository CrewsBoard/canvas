import { memo } from 'react';
import { Handle, Position, type Node, type NodeProps } from '@xyflow/react';
import { Tag, FileText, Play, CircleDot } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

type AgentNodeData = {
  nodeName: string;
  title: string;
  instructions: string;
  model: string;
  tokens: number;
  knowledge: string;
  children: number;
};

function AgentNode({ data }: NodeProps<Node<AgentNodeData>>) {
  return (
    <div className="react-flow__node-agent">
      <Card className="w-full max-w-md border-2 border-emerald-200 bg-emerald-50 rounded-xl shadow-sm">
        <CardHeader className="pb-2 pt-4 px-5 flex flex-row justify-between items-start">
          <div className="flex items-center gap-2 text-emerald-500">
            <Tag className="h-4 w-4" />
            <span className="text-sm font-normal">{data.nodeName}</span>
          </div>
          <button className="bg-blue-600 rounded-full p-1 text-white">
            <Play className="h-4 w-4 fill-current" />
          </button>
        </CardHeader>
        <CardContent className="px-5 pb-4 space-y-4">
          <h2 className="text-2xl font-bold text-emerald-900">{data.title}</h2>

          <div className="space-y-1">
            <div className="flex items-center gap-2 text-emerald-500">
              <FileText className="h-4 w-4" />
              <span className="text-sm font-normal">Instructions</span>
            </div>
            <p className="text-emerald-900 font-medium text-lg">
              {data.instructions}
            </p>
          </div>

          <div className="flex items-center gap-3 text-sm text-emerald-700 pt-2">
            <div className="flex items-center gap-1">
              <CircleDot className="h-5 w-5" />
              <span>{data.model}</span>
            </div>
            <span>·</span>
            <span>{data.tokens}</span>
            <span>·</span>
            <span>{data.knowledge}</span>
            <CircleDot className="h-4 w-4 text-emerald-500 fill-emerald-500" />
            <span>{data.children} Children</span>
          </div>
        </CardContent>
      </Card>

      {/* Handles */}
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-2 h-2 !bg-muted-foreground"
      />
    </div>
  );
}

export default memo(AgentNode);
