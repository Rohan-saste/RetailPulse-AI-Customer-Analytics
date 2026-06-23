import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Home, 
  BarChart2, 
  TrendingUp, 
  Users, 
  Box, 
  AlertTriangle, 
  Package, 
  Settings, 
  FileText, 
  Info,
  Menu,
  X
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Executive Dashboard', icon: Home },
  { path: '/eda', label: 'Exploratory Data Analysis', icon: BarChart2 },
  { path: '/sales', label: 'Sales & Financial', icon: TrendingUp },
  { path: '/customers', label: 'Customer Segmentation', icon: Users },
  { path: '/forecast', label: 'Demand Forecast', icon: Box },
  { path: '/churn', label: 'Churn Risk', icon: AlertTriangle },
  { path: '/inventory', label: 'Inventory Health', icon: Package },
  { path: '/mlops', label: 'MLOps Observability', icon: Settings },
  { path: '/reports', label: 'Reports Center', icon: FileText },
  { path: '/about', label: 'About Platform', icon: Info },
];

export default function Sidebar({ isOpen, toggleSidebar }) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:sticky top-0 left-0 z-50 h-screen w-72 bg-sidebar text-white
        transition-transform duration-300 ease-in-out border-r border-slate-800
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        flex flex-col
      `}>
        <div className="p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-500/20 p-2 rounded-lg">
              <TrendingUp className="w-8 h-8 text-blue-400" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">RetailPulse</h1>
              <p className="text-xs text-blue-400 font-bold uppercase tracking-widest">Enterprise BI</p>
            </div>
          </div>
          <button className="lg:hidden text-slate-400 hover:text-white" onClick={toggleSidebar}>
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="px-6 pb-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Navigation
        </div>

        <nav className="flex-1 overflow-y-auto px-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `
                  flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
                  ${isActive 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }
                `}
                onClick={() => {
                  if (window.innerWidth < 1024) toggleSidebar();
                }}
              >
                <Icon className="w-5 h-5" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="p-6 border-t border-slate-800">
          <div className="text-xs text-slate-400 space-y-1">
            <p>Platform: v2.0.4</p>
            <p>Engine: FastAPI + React</p>
          </div>
          <div className="mt-4 text-[10px] text-slate-500 text-center">
            © 2026 RetailPulse Inc.
          </div>
        </div>
      </aside>
    </>
  );
}
