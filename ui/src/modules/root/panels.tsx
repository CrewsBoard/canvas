import { Button } from '@/components/ui/button';
import NodeEditor from '@/modules/root/editor';
import { Panel } from '@xyflow/react';
import React from 'react';

interface NodeEditorPanelProps {
  templateType: string;
}

export const NodeEditorPanel: React.FC<NodeEditorPanelProps> = ({ templateType }) => {
  return (
    <Panel position="top-right">
      <NodeEditor templateType={templateType} />
    </Panel>
  );
};

interface ActionButtonPanelProps {
  onSave: () => void;
  onRestore: () => void;
}

export const ActionButtonPanel: React.FC<ActionButtonPanelProps> = ({ onSave, onRestore }) => {
  return (
    <Panel position="top-right">
      <div className="flex gap-2">
        <Button variant="outline" onClick={onSave}>
          save
        </Button>
        <Button variant="outline" onClick={onRestore}>
          restore
        </Button>
      </div>
    </Panel>
  );
};
