import ChatBox from '@/components/chat';
import { Button } from '@/components/ui/button';
import { RotateCcw, Phone } from 'lucide-react';

export default function ChatBoxArea() {
  return (
    <div className="h-full flex flex-col p-3 min-w-md bg-gray-50">
      <div className="w-full grid grid-cols-2 gap-2 mb-2">
        <Button variant="outline" className="col-span-1 border-2 py-4">
          <RotateCcw /> Reset Agent
        </Button>
        <Button className="col-span-1 py-4">
          <Phone /> Test Voice
        </Button>
      </div>
      <div className="h-[83vh]">
        <ChatBox />
      </div>
    </div>
  );
}
