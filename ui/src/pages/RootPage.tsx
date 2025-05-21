import { ReactFlowProvider } from '@xyflow/react';
import React from 'react';

import RootModule from '@/modules/root/RootModule';

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
