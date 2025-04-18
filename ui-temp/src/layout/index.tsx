import { Outlet } from 'react-router-dom';

import AppBar from './appbar';
import Sidebar from './sidebar';

export default function Layout() {
  return (
    <div className="flex flex-col h-screen">
      <div className="fixed top-0 left-0 right-0 z-999">
        <AppBar />
      </div>
      <div className="flex flex-1 overflow-hidden mt-[56px]">
        <div className="h-[-webkit-fill-available] fixed top-[56px] left-0 z-998">
          <Sidebar />
        </div>
        <div className="flex-1 ml-16 overflow-auto h-[calc(100vh-64px)]">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
