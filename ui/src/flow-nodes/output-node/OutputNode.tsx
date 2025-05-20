import { Handle, Position } from '@xyflow/react';
import { OctagonMinus, Play, Tag } from 'lucide-react';
import React from 'react';

import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/libs/utils';
import { NodeComponentProps } from '@/types/flowNode.types.ts';

const OutputNode: React.FC<NodeComponentProps> = ({ data, selected }) => {
    return (
        <Card
            className={cn(
                'min-w-[200px] p-0 text-center gap-0',
                selected ? 'border-2 border-primary border-dashed' : ''
            )}
            onDoubleClick={data?.toggleEditor}
        >
            <CardHeader className="p-4 rounded-tl-lg rounded-tr-lg bg-red-600 text-white">
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
            <CardContent className="p-4 rounded-bl-lg rounded-br-lg text-white bg-red-400">
                <div className="flex items-center gap-2">
                    <OctagonMinus className="h-4 w-4" />
                    <span className="text-sm font-normal">End of Flow</span>
                </div>
            </CardContent>

            <Handle type="target" position={Position.Top} className="w-4 h-4 !bg-muted-foreground" />
        </Card>
    );
};

export default OutputNode;
