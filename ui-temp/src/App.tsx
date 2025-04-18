import { BrowserRouter } from 'react-router-dom';
import { ReactFlowProvider } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import { DnDProvider } from '@/contexts/DnDContext';
import Routes from '@/routes';

export default function App() {
  return (
    <BrowserRouter>
      <ReactFlowProvider>
        <DnDProvider>
          <Routes />
        </DnDProvider>
      </ReactFlowProvider>
    </BrowserRouter>
  );
}
