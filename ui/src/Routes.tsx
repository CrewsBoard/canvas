import React from 'react';
import { Route, Routes } from 'react-router-dom';

import RootPage from '@/pages/RootPage';

const RoutesProvider: React.FC = () => {
    return (
        <Routes>
            <Route path="/" element={<RootPage />} />
        </Routes>
    );
};

export default RoutesProvider;
