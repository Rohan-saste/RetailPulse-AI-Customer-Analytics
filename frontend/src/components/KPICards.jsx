import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const kpis = [
  { label: 'Revenue', value: '£877K', trend: '+12.4%', isPositive: true },
  { label: 'Orders', value: '19,495', trend: '+8.1%', isPositive: true },
  { label: 'Customer', value: '4,420', trend: '+5.3%', isPositive: true },
  { label: 'AOV', value: '£45', trend: '+4.0%', isPositive: true },
];

const KPICards = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      {kpis.map((kpi, idx) => (
        <div key={idx} className="bg-card border border-borderLine rounded-2xl p-6 shadow-sm flex flex-col justify-between h-[140px]">
          <h3 className="text-textMuted font-medium text-sm tracking-wide uppercase">{kpi.label}</h3>
          <div>
            <div className="text-3xl font-bold text-textMain">{kpi.value}</div>
            <div className={`flex items-center gap-1 mt-2 text-sm font-semibold ${kpi.isPositive ? 'text-success' : 'text-danger'}`}>
              {kpi.isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              {kpi.trend}
              <span className="text-textMuted font-normal ml-1">vs last month</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default KPICards;
