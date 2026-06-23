// ==============================================================
// RetailPulse Client – Customer Segmentation Page
// ==============================================================

import { useState } from 'react';
import Plot from 'react-plotly.js';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import { useSegmentComposition, useSegmentProfile, useClusters3D } from '../api/hooks';

const segColors = {
  'Premium Customers': '#10b981',
  'Loyal Customers': '#3b82f6',
  'Regular Customers': '#f59e0b',
  'At Risk Customers': '#ef4444',
};

const plotLayout = {
  paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
  font: { color: '#94a3b8', family: 'Plus Jakarta Sans' },
  margin: { t: 40, b: 50, l: 60, r: 20 },
};

export default function CustomerSegmentation() {
  const [filters] = useState({});
  const { data: composition, loading } = useSegmentComposition(filters);
  const { data: profile } = useSegmentProfile(filters);
  const { data: clusters3d } = useClusters3D(filters);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="fade-in">
      <PageHeader title="Customer Segmentation" subtitle="RFM-based customer clusters and behavioral profiles" />

      <InsightBox title="Segmentation Strategy">
        Customers are segmented using RFM (Recency, Frequency, Monetary) analysis with K-Means clustering (K=4). Each segment receives tailored marketing strategies.
      </InsightBox>

      <div className="charts-grid">
        {/* Segment Pie */}
        <div className="card">
          <div className="card-header"><span className="card-title">Segment Composition</span></div>
          {composition && !composition.error && (
            <Plot
              data={[{
                labels: composition.map(d => d.segment),
                values: composition.map(d => d.count),
                type: 'pie',
                hole: 0.55,
                marker: { colors: composition.map(d => segColors[d.segment] || '#6366f1') },
                textinfo: 'percent+label',
                textfont: { size: 11 },
              }]}
              layout={{ ...plotLayout, height: 380, showlegend: false }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%' }}
            />
          )}
        </div>

        {/* Profile Table */}
        <div className="card">
          <div className="card-header"><span className="card-title">Segment Centroid Profile</span></div>
          {profile && !profile.error && (
            <table className="data-table">
              <thead>
                <tr><th>Segment</th><th>Recency</th><th>Frequency</th><th>Monetary</th></tr>
              </thead>
              <tbody>
                {profile.map((row, i) => (
                  <tr key={i}>
                    <td>
                      <span className="badge" style={{ background: `${segColors[row.segment]}22`, color: segColors[row.segment] }}>
                        {row.segment}
                      </span>
                    </td>
                    <td>{row.recency} days</td>
                    <td>{row.frequency}×</td>
                    <td>£{row.monetary.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* 3D Cluster Scatter */}
        <div className="card full-width">
          <div className="card-header"><span className="card-title">3D RFM Cluster Visualization</span></div>
          {clusters3d && !clusters3d.error && (
            <Plot
              data={Object.keys(segColors).map(seg => {
                const pts = clusters3d.filter(d => d.segment === seg);
                return {
                  x: pts.map(d => d.recency),
                  y: pts.map(d => d.frequency),
                  z: pts.map(d => d.monetary),
                  mode: 'markers',
                  type: 'scatter3d',
                  name: seg,
                  marker: { size: 3, color: segColors[seg], opacity: 0.7 },
                };
              })}
              layout={{
                ...plotLayout,
                height: 500,
                scene: {
                  xaxis: { title: 'Recency', gridcolor: 'rgba(71,85,105,0.3)', color: '#94a3b8' },
                  yaxis: { title: 'Frequency', gridcolor: 'rgba(71,85,105,0.3)', color: '#94a3b8' },
                  zaxis: { title: 'Monetary', gridcolor: 'rgba(71,85,105,0.3)', color: '#94a3b8' },
                  bgcolor: 'rgba(0,0,0,0)',
                },
                legend: { font: { color: '#94a3b8' } },
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
