import React from 'react';
import { Sparkles, TrendingUp, AlertTriangle, Lightbulb } from 'lucide-react';

const AIInsights = () => {
  return (
    <div className="bg-gradient-to-br from-indigo-900 to-slate-900 border border-indigo-800/50 rounded-2xl p-6 shadow-lg flex flex-col mt-6 text-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 rounded-full bg-primary/20 blur-3xl pointer-events-none"></div>
      
      <div className="flex items-center gap-2 mb-6 relative z-10">
        <Sparkles className="w-5 h-5 text-blue-400" />
        <h3 className="font-bold text-lg tracking-wide">AI Business Insights</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative z-10">
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 flex gap-3 items-start">
          <div className="bg-success/20 p-2 rounded-lg text-success shrink-0">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-1 text-slate-200">Revenue Forecast</h4>
            <p className="text-sm text-slate-400">Revenue is projected to grow by <span className="text-success font-bold">12%</span> next month due to upcoming holiday trends.</p>
          </div>
        </div>
        
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 flex gap-3 items-start">
          <div className="bg-primary/20 p-2 rounded-lg text-blue-400 shrink-0">
            <Lightbulb className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-1 text-slate-200">Growth Driver</h4>
            <p className="text-sm text-slate-400"><span className="text-blue-400 font-bold">Electronics category</span> is driving 40% of the overall growth this quarter.</p>
          </div>
        </div>
        
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 flex gap-3 items-start">
          <div className="bg-warning/20 p-2 rounded-lg text-warning shrink-0">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-1 text-slate-200">Churn Risk Alert</h4>
            <p className="text-sm text-slate-400">High churn risk detected in <span className="text-warning font-bold">Segment C</span>. Recommend immediate retention campaign.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsights;
