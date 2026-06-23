import React from 'react';
import { TrendingUp } from 'lucide-react';

const LifetimeValue = () => {
  return (
    <div className="bg-card border border-borderLine rounded-2xl p-6 shadow-sm flex flex-col justify-between h-[250px]">
      <h3 className="text-textMain font-bold text-lg">Lifetime Value</h3>
      
      <div className="flex-1 flex flex-col justify-center items-center">
        <div className="text-4xl font-extrabold text-primary mb-2">£1,240</div>
        <p className="text-sm text-textMuted text-center">Average Customer LTV across all segments</p>
      </div>
      
      <div className="bg-background rounded-lg p-3 flex items-center justify-between mt-auto border border-borderLine">
        <span className="text-sm font-medium text-textMain">Projected Growth</span>
        <div className="flex items-center text-success font-bold text-sm">
          <TrendingUp className="w-4 h-4 mr-1" />
          +14.5%
        </div>
      </div>
    </div>
  );
};

export default LifetimeValue;
