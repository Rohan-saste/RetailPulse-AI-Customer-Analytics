// ==============================================================
// RetailPulse Client – Sales Analytics Page
// ==============================================================

import { useState } from 'react';
import Plot from 'react-plotly.js';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import { useTreemap, useScatter } from '../api/hooks';

const plotLayout = {
  paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
  font: { color: '#94a3b8', family: 'Plus Jakarta Sans' },
  margin: { t: 40, b: 50, l: 60, r: 20 },
};

export default function SalesAnalytics() {
  const [filters] = useState({});
  const { data: treemap, loading } = useTreemap(filters);
  const { data: scatter } = useScatter(filters);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="fade-in">
      <PageHeader title="Sales & Financial Analytics" subtitle="Revenue distribution, product mix, and pricing patterns" />

      <InsightBox title="Revenue Strategy">
        The treemap reveals product concentration — top 10 products often drive 40%+ of revenue. The scatter shows price vs. quantity trade-offs.
      </InsightBox>

      <div className="charts-grid">
        {/* Product Revenue Treemap */}
        <div className="card full-width">
          <div className="card-header"><span className="card-title">Product Revenue Treemap (Top 35)</span></div>
          {treemap && (
            <Plot
              data={[{
                type: 'treemap',
                labels: treemap.map(d => d.description),
                parents: treemap.map(() => ''),
                values: treemap.map(d => d.revenue),
                textinfo: 'label+value+percent root',
                marker: {
                  colorscale: [[0, '#312e81'], [0.5, '#6366f1'], [1, '#c4b5fd']],
                  colors: treemap.map(d => d.revenue),
                },
              }]}
              layout={{ ...plotLayout, height: 500 }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Price vs Quantity Scatter */}
        <div className="card full-width">
          <div className="card-header"><span className="card-title">Price vs Quantity (Revenue-Sized)</span></div>
          {scatter && (
            <Plot
              data={[{
                x: scatter.map(d => d.quantity),
                y: scatter.map(d => d.price),
                mode: 'markers',
                type: 'scatter',
                marker: {
                  size: scatter.map(d => Math.max(3, Math.min(20, Math.sqrt(Math.abs(d.revenue))))),
                  color: scatter.map(d => d.revenue),
                  colorscale: [[0, '#6366f1'], [1, '#f59e0b']],
                  opacity: 0.6,
                  colorbar: { title: '£', tickfont: { color: '#94a3b8' } },
                },
              }]}
              layout={{
                ...plotLayout, height: 450,
                xaxis: { ...plotLayout.xaxis, title: 'Quantity', gridcolor: 'rgba(71,85,105,0.3)' },
                yaxis: { ...plotLayout.yaxis, title: 'Price (£)', gridcolor: 'rgba(71,85,105,0.3)' },
              }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>
      </div>
    </div>
  );
}
