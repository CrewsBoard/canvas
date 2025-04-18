import { useState } from 'react';
import { Mic, Send } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: 'bot',
      text: "Why don't scientists trust atoms? Because they make up everything!",
    },
  ]);
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    const newMessage: Message = { sender: 'user', text: input };
    setMessages([...messages, newMessage, { sender: 'bot', text: getJoke() }]);
    setInput('');
  };

  const getJoke = () => {
    const jokes = [
      'Why did the scarecrow win an award? Because he was outstanding in his field!',
      "Why don't skeletons fight each other? They don't have the guts!",
      "I'm reading a book on anti-gravity. It's impossible to put down!",
    ];
    return jokes[Math.floor(Math.random() * jokes.length)];
  };

  return (
    <div className="h-full w-full max-w-md mx-auto border rounded-lg shadow-md bg-white flex flex-col">
      <div className="bg-purple-700 text-white py-3 px-4 flex justify-between items-center rounded-t-lg">
        <span className="font-semibold">Test</span>
        <Button variant="ghost" size="icon" className="text-white">
          ⨉
        </Button>
      </div>
      <ScrollArea className="flex-1 p-4 space-y-3 overflow-y-auto">
        {messages.map((msg, index) => (
          <Card
            key={index}
            className={`max-w-[80%] ${
              msg.sender === 'user'
                ? 'ml-auto bg-blue-500 text-white'
                : 'bg-gray-200'
            }`}
          >
            <CardContent className="p-3">{msg.text}</CardContent>
          </Card>
        ))}
      </ScrollArea>
      <div className="flex items-center gap-2 p-3 border-t">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Message"
          className="flex-1"
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <Button variant="ghost" size="icon">
          <Mic size={20} />
        </Button>
        <Button onClick={sendMessage} size="icon">
          <Send size={20} />
        </Button>
      </div>
    </div>
  );
}
