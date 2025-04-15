import React from 'react';
import { NodeUiConfig } from '../../types/flow-node';

interface ToolNodeProps {
  config: NodeUiConfig;
  data: {
    settings?: Record<string, any>;
    input?: any;
    output?: any;
  };
}

const ToolNode: React.FC<ToolNodeProps> = ({ config, data }) => {
  return (
    <div className="p-4">
      <div className="flex items-center space-x-2">
        <span className="text-2xl">{config.icon}</span>
        <div>
          <h3 className="font-bold">{config.title}</h3>
          <p className="text-sm text-gray-500">{config.description}</p>
        </div>
      </div>
      
      {/* Tool-specific content */}
      {data.settings && (
        <div className="mt-2">
          <h4 className="font-semibold">Tool Configuration</h4>
          <pre className="text-xs bg-gray-100 p-2 rounded">
            {JSON.stringify(data.settings, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ToolNode; 