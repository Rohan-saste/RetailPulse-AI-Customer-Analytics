import React from 'react';
import { Search, Bell, User, Moon } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="h-[60px] bg-card border-b border-borderLine flex items-center justify-between px-6 sticky top-0 z-10 shadow-sm">
      <div className="flex items-center gap-2">
        <div className="bg-primary text-white p-1.5 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
        </div>
        <span className="font-bold text-xl text-textMain tracking-tight">RetailPulse</span>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-textMuted" />
          <input 
            type="text" 
            placeholder="Search..." 
            className="pl-9 pr-4 py-2 bg-background border border-borderLine rounded-lg text-sm focus:outline-none focus:border-primary transition-colors w-64"
          />
        </div>
        
        <div className="flex items-center gap-3 pl-4 border-l border-borderLine">
          <button className="p-2 text-textMuted hover:bg-background rounded-full transition-colors relative">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-danger rounded-full"></span>
          </button>
          <button className="p-2 text-textMuted hover:bg-background rounded-full transition-colors">
            <Moon className="w-5 h-5" />
          </button>
          <button className="flex items-center justify-center w-8 h-8 bg-primary/10 text-primary rounded-full font-semibold text-sm ml-2">
            RS
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
