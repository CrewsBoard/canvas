import React from 'react';
import BootstrapperProvider from '@/libs/providers/BootstrapperProvider';
import RoutesProvider from "@/Routes.tsx";
import QueryProvider from '@/libs/providers/QueryProvider';
import {BrowserRouter} from 'react-router-dom';

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <QueryProvider>
                <BootstrapperProvider>
                    <RoutesProvider/>
                </BootstrapperProvider>
            </QueryProvider>
        </BrowserRouter>
    );
};

export default App;
