import React from 'react';
import { BrowserRouter } from 'react-router-dom';

import RoutesProvider from '@/Routes.tsx';
import BootstrapperProvider from '@/libs/providers/BootstrapperProvider';
import QueryProvider from '@/libs/providers/QueryProvider';

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <QueryProvider>
                <BootstrapperProvider>
                    <RoutesProvider />
                </BootstrapperProvider>
            </QueryProvider>
        </BrowserRouter>
    );
};

export default App;
