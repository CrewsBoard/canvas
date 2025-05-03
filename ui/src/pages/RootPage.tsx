import RootModule from '@/modules/root/RootModule';
import { ReactFlowProvider } from '@xyflow/react';
import React from 'react';

const RootPage: React.FC = () => {
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <ReactFlowProvider>
        <RootModule />
      </ReactFlowProvider>
    </div>
  );
};

export default RootPage;
