// ==============================================================
// RetailPulse Client – Demand Forecast Page
// ==============================================================

import { useState } from 'react';
import Plot from 'react-plotly.js';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import MetricCard from '../components/ui/MetricCard';
import { useForecastData } from '../api/hooks';

export default function DemandForecast() {
  const [horizon, setHorizon] = useState(90);
  const { data, loading } = useForecastData(horizon);

  if (loading) return <LoadingSpinner />;

  const plotLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#94a3b8', family: 'Plus Jakarta Sans' },
    margin: { t: 40, b: 50, l: 60, r: 20 },
    xaxis: { gridcolor: 'rgba(71,85,105,0.3)', title: 'Date' },
    yaxis: { gridcolor: 'rgba(71,85,105,0.3)', title: 'Revenue (£)' },
  };

  return (
    <div className="fade-in">
      <PageHeader title="Demand Forecasting" subtitle="Prophet-powered sales trajectory and confidence intervals" />

      <InsightBox title="Forecast Intelligence">
        The Prophet model captures weekly and yearly seasonality. November–December shows peak demand due to holiday shopping. Adjust the horizon slider to explore different prediction windows.
      </InsightBox>

      {/* Horizon Slider */}
      <div className="card mb-2">
        <div className="slider-container">
          <div className="slider-header">
            <span className="slider-label">Forecast Horizon</span>
            <span className="slider-value">{horizon} Days</span>
          </div>
          <input
            type="range"
            min={30}
            max={90}
            value={horizon}
            onChange={(e) => setHorizon(Number(e.target.value))}
          />
        </div>
      </div>

      {/* Summary KPIs */}
      {data?.summary && (
        <div className="metrics-grid">
          <MetricCard label="Projected Total" value={`£${(data.summary.projected_total / 1e6).toFixed(2)}M`} variant="primary" />
          <MetricCard label="Avg Daily Revenue" value={`£${(data.summary.projected_avg_daily / 1e3).toFixed(1)}K`} variant="success" />
          <MetricCard label="Horizon" value={`${data.summary.horizon_days} Days`} variant="info" />
        </div>
      )}

      {/* Forecast Chart */}
      <div className="card">
        <div className="card-header"><span className="card-title">Sales Forecast Trajectory</span></div>
        {data?.points && (
          <Plot
            data={[
              // Confidence band
              {
                x: [...data.points.map(d => d.ds), ...data.points.slice().reverse().map(d => d.ds)],
                y: [...data.points.map(d => d.yhat_upper), ...data.points.slice().reverse().map(d => d.yhat_lower)],
                fill: 'toself',
                fillcolor: 'rgba(99,102,241,0.1)',
                line: { color: 'transparent' },
                name: 'Confidence Interval',
                showlegend: true,
              },
              // Forecast line
              {
                x: data.points.map(d => d.ds),
                y: data.points.map(d => d.yhat),
                mode: 'lines',
                line: { color: '#6366f1', width: 2.5 },
                name: 'Forecast (ŷ)',
              },
              // Actual sales
              ...(data.actual_daily?.length > 0 ? [{
                x: data.actual_daily.map(d => d.ds),
                y: data.actual_daily.map(d => d.revenue),
                mode: 'markers',
                marker: { size: 2, color: '#22d3ee', opacity: 0.5 },
                name: 'Actual Sales',
              }] : []),
            ]}
            layout={{ ...plotLayout, height: 450, legend: { font: { color: '#94a3b8' } } }}
            config={{ displayModeBar: false, responsive: true }}
            style={{ width: '100%' }}
          />
        )}
      </div>

      {/* Forecast Table */}
      {data?.table && data.table.length > 0 && (
        <div className="card mt-2">
          <div className="card-header"><span className="card-title">Future Predictions Table</span></div>
          <div style={{ maxHeight: 300, overflowY: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr><th>Date</th><th>Predicted (£)</th><th>Lower Bound</th><th>Upper Bound</th></tr>
              </thead>
              <tbody>
                {data.table.slice(0, 30).map((row, i) => (
                  <tr key={i}>
                    <td>{row.ds?.split('T')[0]}</td>
                    <td>£{row.yhat.toLocaleString()}</td>
                    <td>£{row.yhat_lower.toLocaleString()}</td>
                    <td>£{row.yhat_upper.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
