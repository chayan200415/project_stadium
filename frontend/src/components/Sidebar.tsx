import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Map, Users, AlertTriangle, Bus, Leaf, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: MessageSquare, label: 'AI Chat', path: '/chat' },
  { icon: Map, label: 'Navigation', path: '/navigation' },
  { icon: Users, label: 'Crowd Intel', path: '/crowd' },
  { icon: AlertTriangle, label: 'Operations', path: '/operations' },
  { icon: Bus, label: 'Transport', path: '/transport' },
  { icon: Leaf, label: 'Sustainability', path: '/sustainability' },
];

export function Sidebar() {
  return (
    <div className="w-64 border-r bg-card h-full flex flex-col p-4 shadow-xl z-10">
      <div className="flex items-center space-x-2 mb-8 px-2">
        <div className="w-8 h-8 bg-primary rounded-md flex items-center justify-center">
          <span className="font-bold text-primary-foreground text-xl">S</span>
        </div>
        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">StadiumGPT</h1>
      </div>
      
      <nav className="flex-1 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center space-x-3 px-3 py-2 rounded-md transition-all duration-200",
                isActive ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              )
            }
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto border-t border-border pt-4">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            cn(
              "flex items-center space-x-3 px-3 py-2 rounded-md transition-all duration-200",
              isActive ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-secondary hover:text-foreground"
            )
          }
        >
          <Settings size={20} />
          <span>Settings</span>
        </NavLink>
      </div>
    </div>
  );
}
