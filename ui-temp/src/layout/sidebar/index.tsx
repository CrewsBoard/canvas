import { useState } from 'react';
import {
  CirclePlus,
  Users,
  Bug,
  CalendarDays,
  Key,
  Building2,
  UserRound,
  Zap,
  Plus,
  ChevronDown,
} from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

export default function Sidebar() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div
      className={`h-full z-50 bg-white/90 backdrop-blur-sm border-r shadow-sm transition-all duration-300 ease-initial ${
        isExpanded ? 'w-60' : 'w-16'
      }`}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
    >
      <div className="h-full flex flex-col">
        <div className="flex-1 overflow-y-auto pt-4">
          <ul className="space-y-1 px-2">
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <CirclePlus className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>New Agent</span>}
              </button>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <Users className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Agents</span>}
              </button>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-lg border-2 border-indigo-600 bg-indigo-50/90 text-indigo-600 hover:bg-indigo-50/90 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <Bug className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Crawler</span>}
              </button>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <CalendarDays className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Events</span>}
              </button>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <Key className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Credentials</span>}
              </button>
            </li>
            <li className="py-2">
              <div className="h-px bg-gray-200/70 w-full"></div>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <Building2 className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Agency</span>}
              </button>
            </li>
            <li>
              <button
                className={`flex items-center w-full p-2 rounded-md hover:bg-gray-100/80 transition-colors ${
                  isExpanded ? 'justify-start gap-3' : 'justify-center'
                }`}
              >
                <UserRound className="h-5 w-5 flex-shrink-0" />
                {isExpanded && <span>Clients</span>}
              </button>
            </li>
          </ul>
        </div>

        <div className="mt-auto p-3">
          <button
            className={`w-full bg-indigo-100/90 text-indigo-700 rounded-lg font-medium mb-4 hover:bg-indigo-200/90 transition-colors ${
              isExpanded ? 'py-3 px-2' : 'p-2 flex justify-center'
            }`}
          >
            {isExpanded ? (
              <span>Upgrade Plan</span>
            ) : (
              <Zap className="h-5 w-5" />
            )}
          </button>

          <div
            className={`flex items-center gap-2 mb-3 ${
              isExpanded ? '' : 'justify-center'
            }`}
          >
            <Avatar className="h-8 w-8 border shrink-0">
              <AvatarFallback>AS</AvatarFallback>
            </Avatar>
            {isExpanded && (
              <>
                <div className="min-w-0 overflow-hidden">
                  <p className="text-sm font-medium truncate">John Doe</p>
                  <p className="text-xs text-muted-foreground truncate">
                    johndoe@example.com
                  </p>
                </div>
                <ChevronDown className="h-4 w-4 ml-auto shrink-0" />
              </>
            )}
          </div>

          <div
            className={`flex items-center gap-2 bg-gray-100/80 p-2 rounded-lg ${
              isExpanded ? '' : 'justify-center'
            }`}
          >
            <Zap className="h-5 w-5 shrink-0" />
            {isExpanded && (
              <>
                <span className="font-medium truncate">745.6 Creds</span>
                <button className="bg-white/90 p-1 rounded-md shadow-sm ml-auto shrink-0 hover:bg-gray-50/90">
                  <Plus className="h-4 w-4" />
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
