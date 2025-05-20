import { DnDPanelProps } from '@/modules/root/dndPanel.types';

export default function DnDPanel({ nodeTypes, onDragStart }: DnDPanelProps) {
    // const { setDraggedType } = useDnD();

    // const onDragStart = (
    //   event: React.DragEvent<HTMLDivElement | HTMLButtonElement>,
    //   nodeType: string
    // ) => {
    //   setDraggedType(nodeType);
    //   event.dataTransfer.effectAllowed = 'move';
    // };

    return (
        <aside className="space-y-4 w-40">
            {Object.entries(nodeTypes).map(([type, def]) => (
                <div
                    key={type}
                    draggable
                    onDragStart={e => onDragStart(e, type, def.node_template_id)}
                    className="p-2.5 bg-white border border-gray-300 rounded cursor-grab text-xs shadow-sm transition-all hover:translate-x-0.5 hover:shadow-md"
                >
                    <div className="font-medium text-gray-800">{def.title || type}</div>
                    {def.description && <div className="text-[11px] text-gray-500 mt-1">{def.description}</div>}
                </div>
            ))}
        </aside>
    );
}
