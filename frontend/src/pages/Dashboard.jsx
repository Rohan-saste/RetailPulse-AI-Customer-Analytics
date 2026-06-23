import React from 'react';
import KPICards from '../components/KPICards';
import RevenueChart from '../components/RevenueChart';
import CategoryChart from '../components/CategoryChart';
import CustomerSegment from '../components/CustomerSegment';
import RetentionChart from '../components/RetentionChart';
import LifetimeValue from '../components/LifetimeValue';
import ProductTable from '../components/ProductTable';
import AIInsights from '../components/AIInsights';

const Dashboard = () => {
  return (
    <div className="max-w-[1600px] mx-auto p-6 space-y-6">
      {/* KPI Row */}
      <KPICards />
      
      {/* Main Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-[70%_1fr] gap-6">
        <RevenueChart />
        <CategoryChart />
      </div>
      
      {/* Customer Intelligence */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <CustomerSegment />
        <RetentionChart />
        <LifetimeValue />
      </div>
      
      {/* Product Performance & AI Insights */}
      <div className="space-y-6">
        <ProductTable />
        <AIInsights />
      </div>
    </div>
  );
};

export default Dashboard;
