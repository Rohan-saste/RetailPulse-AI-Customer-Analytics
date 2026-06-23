import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'M1', rate: 100 },
  { name: 'M2', rate: 65 },
  { name: 'M3', rate: 50 },
  { name: 'M4', rate: 45 },
  { name: 'M5', rate: 38 },
];

const RetentionChart = () => {
  return (
    <div className="bg-card border border-borderLine rounded-2xl p-6 shadow-sm flex flex-col h-[250px]">
      <h3 className="text-textMain font-bold text-lg mb-4">Retention Analysis</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748B', fontSize: 12 }} dy={5} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748B', fontSize: 12 }} tickFormatter={(val) => `${val}%`} />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: '1px solid #E2E8F0', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              cursor={{ fill: '#F1F5F9' }}
            />
            <Bar dataKey="rate" fill="#2563EB" radius={[4, 4, 0, 0]} barSize={24} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RetentionChart;
