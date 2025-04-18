import React from 'react';
import { useDnD } from '@/hooks/useDnD';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

export default function DnDPanel() {
  const { setDraggedType } = useDnD();

  const onDragStart = (
    event: React.DragEvent<HTMLDivElement | HTMLButtonElement>,
    nodeType: string
  ) => {
    setDraggedType(nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside className="space-y-4 w-48">
      <Button
        className="w-32 border-2 border-gray-300 py-5 font-normal cursor-pointer"
        variant="secondary"
        draggable
        onDragStart={(event) => onDragStart(event, 'info')}
      >
        <Plus />
        Info Node
      </Button>

      <Button
        className="w-32 border-2 border-gray-300 py-5 font-normal cursor-pointer"
        variant="secondary"
        draggable
        onDragStart={(event) => onDragStart(event, 'start')}
      >
        <Plus />
        Start Node
      </Button>
    </aside>
  );
}
