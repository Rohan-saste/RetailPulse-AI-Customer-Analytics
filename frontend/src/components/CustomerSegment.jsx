import React from 'react';

const CustomerSegment = () => {
  return (
    <div className="bg-card border border-borderLine rounded-2xl p-6 shadow-sm flex flex-col h-[250px]">
      <h3 className="text-textMain font-bold text-lg mb-4">Customer Segments</h3>
      <div className="flex-1 flex flex-col justify-center space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-primary"></span>
            <span className="text-sm font-medium text-textMain">Premium</span>
          </div>
          <span className="text-sm font-bold">35%</span>
        </div>
        <div className="w-full bg-slate-100 rounded-full h-2">
          <div className="bg-primary h-2 rounded-full" style={{ width: '35%' }}></div>
        </div>
        
        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-success"></span>
            <span className="text-sm font-medium text-textMain">Loyal</span>
          </div>
          <span className="text-sm font-bold">45%</span>
        </div>
        <div className="w-full bg-slate-100 rounded-full h-2">
          <div className="bg-success h-2 rounded-full" style={{ width: '45%' }}></div>
        </div>
        
        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-warning"></span>
            <span className="text-sm font-medium text-textMain">At Risk</span>
          </div>
          <span className="text-sm font-bold">20%</span>
        </div>
        <div className="w-full bg-slate-100 rounded-full h-2">
          <div className="bg-warning h-2 rounded-full" style={{ width: '20%' }}></div>
        </div>
      </div>
    </div>
  );
};

export default CustomerSegment;
