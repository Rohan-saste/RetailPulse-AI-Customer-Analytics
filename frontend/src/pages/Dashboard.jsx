import { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar 
} from 'recharts';
import { TrendingUp, Package, Users, DollarSign } from 'lucide-react';

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [monthlyRevenue, setMonthlyRevenue] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, we'd fetch from /api/v1/dashboard/kpis
    // Mocking the data structure based on the Streamlit dashboard for now
    // assuming no auth token is available yet
    setTimeout(() => {
      setKpis({
        total_revenue: 8245120,
        total_orders: 145020,
        total_customers: 4200,
        aov: 56.8,
        total_skus: 3840,
        revenue_growth: 14.82,
        new_customers: 9.45,
        markets: 38,
        monthly_revenue_spark: [100, 120, 110, 140, 130, 160],
      });
      setMonthlyRevenue([
        { name: 'Jan', revenue: 4000, target: 2400 },
        { name: 'Feb', revenue: 3000, target: 1398 },
        { name: 'Mar', revenue: 2000, target: 9800 },
        { name: 'Apr', revenue: 2780, target: 3908 },
        { name: 'May', revenue: 1890, target: 4800 },
        { name: 'Jun', revenue: 2390, target: 3800 },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-8 border border-slate-700 shadow-lg text-white">
        <h1 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-2">
          Executive Intelligence Portal
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Real-time revenue metrics, financial highlights, global footprints, and cross-channel performance analytics.
        </p>
      </div>

      {/* KPI Row 1 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard 
          title="Total Revenue" 
          value={`£${(kpis.total_revenue / 1000000).toFixed(2)}M`}
          subValue="+12.4% MoM"
          icon={<DollarSign className="w-5 h-5" />}
          color="blue"
        />
        <KpiCard 
          title="Total Orders" 
          value={kpis.total_orders.toLocaleString()}
          subValue="+8.1% MoM"
          icon={<Package className="w-5 h-5" />}
          color="green"
        />
        <KpiCard 
          title="Active Customers" 
          value={kpis.total_customers.toLocaleString()}
          subValue="+5.3% MoM"
          icon={<Users className="w-5 h-5" />}
          color="purple"
        />
        <KpiCard 
          title="Average Order Value" 
          value={`£${kpis.aov.toFixed(1)}`}
          subValue="+4.0% MoM"
          icon={<TrendingUp className="w-5 h-5" />}
          color="orange"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-card rounded-2xl p-6 border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-textMain mb-4">Monthly Sales Revenue Trend</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyRevenue} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.1}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748B'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748B'}} />
                <Tooltip 
                  contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                />
                <Area type="monotone" dataKey="revenue" stroke="#2563EB" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)" />
                <Line type="monotone" dataKey="target" stroke="#E11D48" strokeWidth={2} strokeDasharray="5 5" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-card rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col">
          <h3 className="text-lg font-bold text-textMain mb-4">Quick Stats</h3>
          <div className="flex-1 space-y-6">
            <div className="flex justify-between items-center border-b border-slate-100 pb-4">
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase">Total SKUs Sold</p>
                <p className="text-xl font-bold text-textMain">{kpis.total_skus.toLocaleString()}</p>
              </div>
            </div>
            <div className="flex justify-between items-center border-b border-slate-100 pb-4">
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase">Revenue Growth YTD</p>
                <p className="text-xl font-bold text-green-500">+{kpis.revenue_growth}%</p>
              </div>
            </div>
            <div className="flex justify-between items-center border-b border-slate-100 pb-4">
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase">New Customer Acquisition</p>
                <p className="text-xl font-bold text-green-500">+{kpis.new_customers}%</p>
              </div>
            </div>
            <div className="flex justify-between items-center pb-2">
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase">Markets Reached</p>
                <p className="text-xl font-bold text-textMain">{kpis.markets}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Insights Box */}
      <div className="insight-box">
        <h4 className="text-sm font-bold text-blue-600 uppercase mb-2">💡 Executive Insights & Strategic recommendations</h4>
        <div className="text-sm text-slate-700 space-y-2">
          <p><strong>📊 Key Observation:</strong> Nov-Dec periods capture massive revenue peaks aligning with European holiday spend seasons. Average Order Values track 14% higher during these months.</p>
          <p><strong>🔍 Business Insight:</strong> Sales density is heavily localized in the United Kingdom, but expanding margins are observed in Netherlands and Ireland.</p>
          <p><strong>📈 Strategic Recommendation:</strong> Reallocate localized marketing budgets to European territories showing high baseline customer growth.</p>
          <p><strong>⚡ Forecasted Impact:</strong> Increased focus on European channels projected to boost Q3 net margins by 4.2% while reducing inventory carrying costs.</p>
          <p><strong>🎯 Suggested Decision:</strong> <span className="text-blue-600 font-medium">Approve expansion budget of £250,000 for local marketing campaigns in Germany and France.</span></p>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, subValue, icon, color }) {
  const colorMap = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600',
  };

  return (
    <div className="bg-card rounded-2xl p-6 border border-slate-200 shadow-sm hover:-translate-y-1 hover:shadow-md transition-all duration-300 hover:border-blue-500">
      <div className="flex justify-between items-start mb-4">
        <div>
          <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">{title}</p>
          <h3 className="text-3xl font-extrabold text-slate-800 mt-1">{value}</h3>
        </div>
        <div className={`p-2 rounded-lg ${colorMap[color]}`}>
          {icon}
        </div>
      </div>
      <div>
        <p className="text-xs font-semibold text-green-500">▲ {subValue}</p>
      </div>
    </div>
  );
}
