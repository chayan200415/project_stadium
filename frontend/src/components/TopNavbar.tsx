import React from 'react';
import { Bell, Search, User } from 'lucide-react';
import { Input } from './ui/input';

export function TopNavbar() {
  return (
    <header className="h-16 border-b bg-background/80 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-20">
      <div className="w-96 relative flex items-center">
        <Search className="absolute left-3 text-muted-foreground h-4 w-4" />
        <Input 
          className="pl-9 bg-secondary/50 border-none focus-visible:ring-1 focus-visible:ring-primary/50" 
          placeholder="Search for gates, food, incidents..." 
        />
      </div>
      
      <div className="flex items-center space-x-4">
        <button className="relative p-2 rounded-full hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground">
          <Bell size={20} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-destructive rounded-full border border-background"></span>
        </button>
        <div className="h-8 w-8 bg-gradient-to-tr from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white cursor-pointer shadow-md">
          <User size={16} />
        </div>
      </div>
    </header>
  );
}
