import { useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { Switch } from '@/components/ui/switch';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from '@/components/ui/accordion';

export default function InfoEditor() {
  const [globalNode, setGlobalNode] = useState(false);
  const [nodeName, setNodeName] = useState('Start');
  const [description, setDescription] = useState(
    'This is the start node of the LLM chain.'
  );
  const [instructions, setInstructions] = useState(
    'Greet the user warmly and tell him that you are ready to help him.'
  );

  return (
    <div className="max-w-lg mx-auto p-4 space-y-4 bg-white rounded-lg shadow-md">
      <h2 className="text-lg font-semibold text-gray-700">Overview</h2>

      <div className="flex items-center justify-between">
        <Label className="text-sm font-medium">Global Node</Label>
        <Switch checked={globalNode} onCheckedChange={setGlobalNode} />
      </div>
      <p className="text-xs text-gray-500">
        Global nodes are available to all agents.
      </p>

      <div>
        <Label htmlFor="node-name">Node Name</Label>
        <Input
          id="node-name"
          value={nodeName}
          onChange={(e) => setNodeName(e.target.value)}
        />
        <p className="text-xs text-gray-500">
          Should be a short, descriptive name for the node.
        </p>
      </div>

      <Card>
        <CardContent className="p-3">
          <Label>Description & When to Route to this Node</Label>
          <ReactQuill
            theme="snow"
            value={description}
            onChange={setDescription}
            placeholder="Start typing... Use {{ to insert tools or variables }}"
          />
          <p className="text-xs text-gray-500 mt-1">
            (Required if this node is global) Defines what the node does and is
            important when routing from and to this node.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-3">
          <Label>Instructions</Label>
          <ReactQuill
            theme="snow"
            value={instructions}
            onChange={setInstructions}
            placeholder="Enter instructions here"
          />
          <p className="text-xs text-gray-500 mt-1">
            The final instructions given to the AI when the routing agent
            chooses this node.
          </p>
        </CardContent>
      </Card>

      <Accordion type="single" collapsible className="border-t pt-2">
        <AccordionItem value="llm">
          <AccordionTrigger>LLM</AccordionTrigger>
          <AccordionContent>LLM settings go here.</AccordionContent>
        </AccordionItem>
        <AccordionItem value="tools">
          <AccordionTrigger>Tools</AccordionTrigger>
          <AccordionContent>Tool settings go here.</AccordionContent>
        </AccordionItem>
        <AccordionItem value="knowledge">
          <AccordionTrigger>Knowledge Base</AccordionTrigger>
          <AccordionContent>Knowledge base settings go here.</AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
