import { useState } from 'react';
import { ChevronDown, Moon, Sun, ArrowUpRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export default function AppBar() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <header className="w-full h-[56px] border-b bg-white dark:bg-gray-900 shadow-sm">
      <div className="container mx-auto flex items-center justify-between p-3">
        {/* Breadcrumb Navigation */}
        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
          <Avatar className="h-6 w-6">
            <AvatarFallback>A</AvatarFallback>
          </Avatar>
          <span className="text-sm">/</span>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                className="flex items-center text-sm font-medium"
              >
                <Avatar className="h-6 w-6 mr-2">
                  <AvatarImage
                    src="https://via.placeholder.com/32"
                    alt="User"
                  />
                  <AvatarFallback>U</AvatarFallback>
                </Avatar>
                Workspace <ChevronDown className="ml-1 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              <DropdownMenuItem>Personal Workspace</DropdownMenuItem>
              <DropdownMenuItem>Team Workspace</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <span className="text-sm">/</span>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                className="flex items-center text-sm font-medium"
              >
                <Avatar className="h-6 w-6 mr-2">
                  <AvatarFallback>A</AvatarFallback>
                </Avatar>
                Selected Agent <ChevronDown className="ml-1 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              <DropdownMenuItem>Agent 1</DropdownMenuItem>
              <DropdownMenuItem>Agent 2</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        {/* Right Side Controls */}
        <div className="flex items-center gap-4">
          <Button variant="outline" className="text-blue-600 border-blue-600">
            Blue-Light
          </Button>
          <Button variant="outline" className="flex items-center">
            API Docs <ArrowUpRight className="ml-1 h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setDarkMode(!darkMode)}
          >
            {darkMode ? (
              <Sun className="h-5 w-5 text-yellow-500" />
            ) : (
              <Moon className="h-5 w-5 text-gray-600" />
            )}
          </Button>
        </div>
      </div>
    </header>
  );
}
