// ==============================================================
// RetailPulse Client – Metric Card with Sparkline
// ==============================================================


const colorMap = {
  primary: '#6366f1',
  success: '#10b981',
  warning: '#f59e0b',
  info: '#3b82f6',
  danger: '#ef4444',
  accent: '#06b6d4',
};

export default function MetricCard({ label, value, variant = 'primary', sparklineData }) {
  return (
    <div className={`metric-card ${variant}`}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {sparklineData && sparklineData.length > 1 && (
        <div className="metric-sparkline">
          <svg viewBox={`0 0 ${sparklineData.length * 10} 32`} style={{ width: '100%', height: '100%' }}>
            <polyline
              fill="none"
              stroke={colorMap[variant] || colorMap.primary}
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={sparklineData
                .map((v, i) => {
                  const max = Math.max(...sparklineData);
                  const min = Math.min(...sparklineData);
                  const range = max - min || 1;
                  const x = (i / (sparklineData.length - 1)) * (sparklineData.length * 10 - 10) + 5;
                  const y = 30 - ((v - min) / range) * 26;
                  return `${x},${y}`;
                })
                .join(' ')}
            />
          </svg>
        </div>
      )}
    </div>
  );
}
