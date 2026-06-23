import React from 'react';
import { LayoutDashboard, LineChart, Users, Package, ShoppingCart, BrainCircuit, FileText, Settings } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { name: 'Dashboard', icon: LayoutDashboard, path: '/' },
  { name: 'Analytics', icon: LineChart, path: '/analytics' },
  { name: 'Customers', icon: Users, path: '/customers' },
  { name: 'Products', icon: Package, path: '/products' },
  { name: 'Orders', icon: ShoppingCart, path: '/orders' },
  { name: 'Predictions', icon: BrainCircuit, path: '/predictions' },
  { name: 'Reports', icon: FileText, path: '/reports' },
  { name: 'Settings', icon: Settings, path: '/settings' },
];

const Sidebar = () => {
  return (
    <aside className="w-[280px] bg-sidebar text-slate-300 min-h-[calc(100vh-60px)] flex flex-col py-6 sticky top-[60px] h-[calc(100vh-60px)] overflow-y-auto hidden md:flex shrink-0">
      <div className="px-6 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Main Menu</div>
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive 
                  ? 'bg-primary/10 text-primary' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div className="px-6 mt-auto">
        <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
          <p className="text-xs text-slate-400 mb-2">Platform Status</p>
          <div className="flex items-center gap-2 text-sm text-white">
            <span className="w-2 h-2 rounded-full bg-success"></span>
            All systems operational
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
