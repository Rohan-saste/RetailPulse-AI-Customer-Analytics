// ==============================================================
// RetailPulse Client – Sidebar Navigation
// ==============================================================

import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard, BarChart3, TrendingUp, Users, LineChart,
  AlertTriangle, Package, Activity, FileDown, Info, LogOut
} from 'lucide-react';

const navItems = [
  { section: 'Analytics' },
  { path: '/', label: 'Executive Dashboard', icon: LayoutDashboard },
  { path: '/eda', label: 'Exploratory Analysis', icon: BarChart3 },
  { path: '/sales', label: 'Sales Analytics', icon: TrendingUp },
  { section: 'Intelligence' },
  { path: '/segmentation', label: 'Customer Segments', icon: Users },
  { path: '/forecast', label: 'Demand Forecast', icon: LineChart },
  { path: '/churn', label: 'Churn Risk', icon: AlertTriangle },
  { section: 'Operations' },
  { path: '/inventory', label: 'Inventory Health', icon: Package },
  { path: '/mlops', label: 'MLOps Monitor', icon: Activity },
  { path: '/reports', label: 'Reports', icon: FileDown },
  { path: '/about', label: 'About', icon: Info },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">📊</div>
        <div className="sidebar-brand-text">
          <h1>RetailPulse</h1>
          <span>Enterprise BI</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item, i) =>
          item.section ? (
            <div key={i} className="sidebar-section-label">{item.section}</div>
          ) : (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
              end={item.path === '/'}
            >
              <item.icon />
              <span>{item.label}</span>
            </NavLink>
          )
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="sidebar-avatar">
            {user?.full_name?.[0] || user?.email?.[0] || 'U'}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{user?.full_name || user?.email}</div>
            <div className="sidebar-user-role">{user?.role}</div>
          </div>
          <button
            onClick={logout}
            style={{ background: 'none', border: 'none', color: 'var(--color-text-muted)', cursor: 'pointer', padding: 4 }}
            title="Logout"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </aside>
  );
}
