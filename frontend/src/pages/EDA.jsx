// ==============================================================
// RetailPulse Client – Exploratory Data Analysis Page
// ==============================================================

import { useState } from 'react';
import Plot from 'react-plotly.js';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import { useDistributions, useTemporalHeatmap, useWeeklyRevenue, useCorrelations, useStats } from '../api/hooks';

const plotLayout = {
  paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
  font: { color: '#94a3b8', family: 'Plus Jakarta Sans' },
  margin: { t: 40, b: 50, l: 60, r: 20 },
  xaxis: { gridcolor: 'rgba(71,85,105,0.3)' },
  yaxis: { gridcolor: 'rgba(71,85,105,0.3)' },
};

export default function EDA() {
  const [filters] = useState({});
  const { data: dist, loading: dLoad } = useDistributions(filters);
  const { data: heatmap } = useTemporalHeatmap(filters);
  const { data: weekly } = useWeeklyRevenue(filters);
  const { data: corr } = useCorrelations(filters);
  const { data: stats } = useStats(filters);

  if (dLoad) return <LoadingSpinner />;

  return (
    <div className="fade-in">
      <PageHeader title="Exploratory Data Analysis" subtitle="Statistical distributions, temporal patterns, and correlations" />

      <InsightBox title="EDA Insight">
        Revenue distribution is right-skewed — most transactions are small, with a few high-value bulk orders. Thursday–Wednesday see peak activity.
      </InsightBox>

      <div className="charts-grid">
        {/* Revenue Distribution */}
        <div className="card">
          <div className="card-header"><span className="card-title">Revenue Distribution</span></div>
          {dist && (
            <Plot
              data={[{ x: dist.revenue, type: 'histogram', nbinsx: 60, marker: { color: '#6366f1' } }]}
              layout={{ ...plotLayout, height: 320, xaxis: { ...plotLayout.xaxis, title: 'Revenue (£)' }, yaxis: { ...plotLayout.yaxis, title: 'Count' } }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Price Distribution */}
        <div className="card">
          <div className="card-header"><span className="card-title">Price Distribution</span></div>
          {dist && (
            <Plot
              data={[{ x: dist.price, type: 'histogram', nbinsx: 60, marker: { color: '#f59e0b' } }]}
              layout={{ ...plotLayout, height: 320, xaxis: { ...plotLayout.xaxis, title: 'Price (£)' }, yaxis: { ...plotLayout.yaxis, title: 'Count' } }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Weekly Revenue */}
        <div className="card">
          <div className="card-header"><span className="card-title">Revenue by Day of Week</span></div>
          {weekly && (
            <Plot
              data={[{
                x: weekly.map(d => d.weekday), y: weekly.map(d => d.revenue), type: 'bar',
                marker: { color: weekly.map((_, i) => `hsl(${200 + i * 20}, 70%, 55%)`) },
              }]}
              layout={{ ...plotLayout, height: 320, yaxis: { ...plotLayout.yaxis, title: 'Revenue (£)' } }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Correlation Heatmap */}
        <div className="card">
          <div className="card-header"><span className="card-title">Correlation Matrix</span></div>
          {corr && (
            <Plot
              data={[{
                z: corr.matrix, x: corr.labels, y: corr.labels, type: 'heatmap',
                colorscale: [[0, '#1e1b4b'], [0.5, '#6366f1'], [1, '#c4b5fd']],
                text: corr.matrix.map(row => row.map(v => v.toFixed(2))), texttemplate: '%{text}',
              }]}
              layout={{ ...plotLayout, height: 320, xaxis: { side: 'bottom' } }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Temporal Heatmap */}
        <div className="card full-width">
          <div className="card-header"><span className="card-title">Temporal Revenue Heatmap (Weekday × Hour)</span></div>
          {heatmap && (
            <Plot
              data={[{
                z: heatmap.values, x: heatmap.hours, y: heatmap.weekdays, type: 'heatmap',
                colorscale: [[0, '#0f172a'], [0.5, '#6366f1'], [1, '#fbbf24']],
                colorbar: { title: '£', tickfont: { color: '#94a3b8' } },
              }]}
              layout={{ ...plotLayout, height: 350, xaxis: { ...plotLayout.xaxis, title: 'Hour of Day', dtick: 1 }, yaxis: { autorange: 'reversed' } }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>
      </div>

      {/* Stats Table */}
      {stats && stats.length > 0 && (
        <div className="card mt-2">
          <div className="card-header"><span className="card-title">Descriptive Statistics</span></div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Metric</th>
                {Object.keys(stats[0]).filter(k => k !== 'metric').map(k => <th key={k}>{k}</th>)}
              </tr>
            </thead>
            <tbody>
              {stats.map((row, i) => (
                <tr key={i}>
                  <td style={{ fontWeight: 600, color: 'var(--color-text)' }}>{row.metric}</td>
                  {Object.entries(row).filter(([k]) => k !== 'metric').map(([k, v]) => (
                    <td key={k}>{typeof v === 'number' ? v.toLocaleString(undefined, { maximumFractionDigits: 2 }) : v}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
