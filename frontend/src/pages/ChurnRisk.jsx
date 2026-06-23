// ==============================================================
// RetailPulse Client – Churn Risk Intelligence Page
// ==============================================================

import { useState } from 'react';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import MetricCard from '../components/ui/MetricCard';
import { useChurnOverview, useChurnRiskList, predictChurn } from '../api/hooks';

export default function ChurnRisk() {
  const { data: overview, loading } = useChurnOverview();
  const { data: riskList } = useChurnRiskList(50);

  // Simulator state
  const [recency, setRecency] = useState(100);
  const [frequency, setFrequency] = useState(5);
  const [monetary, setMonetary] = useState(500);
  const [avgRevenue, setAvgRevenue] = useState(20);
  const [totalItems, setTotalItems] = useState(200);
  const [avgQuantity, setAvgQuantity] = useState(10);
  const [prediction, setPrediction] = useState(null);
  const [predLoading, setPredLoading] = useState(false);

  const handlePredict = async () => {
    setPredLoading(true);
    try {
      const result = await predictChurn({
        recency, frequency, monetary,
        avg_revenue: avgRevenue,
        total_items: totalItems,
        avg_quantity: avgQuantity,
      });
      setPrediction(result);
    } catch { setPrediction(null); }
    finally { setPredLoading(false); }
  };

  if (loading) return <LoadingSpinner />;

  const gaugeColor = prediction?.risk_level === 'High' ? 'gauge-high' : prediction?.risk_level === 'Medium' ? 'gauge-medium' : 'gauge-low';

  return (
    <div className="fade-in">
      <PageHeader title="Churn Risk Intelligence" subtitle="ML-powered customer retention analysis and risk simulation" />

      <InsightBox title="Churn Analysis">
        Customers inactive for 90+ days are classified as churned. The Random Forest model uses 6 RFM features with 95%+ accuracy. Use the simulator below to test risk scenarios.
      </InsightBox>

      {/* Overview KPIs */}
      {overview && !overview.error && (
        <div className="metrics-grid">
          <MetricCard label="Total Customers" value={overview.total_customers.toLocaleString()} variant="info" />
          <MetricCard label="Churned" value={overview.churned_customers.toLocaleString()} variant="danger" />
          <MetricCard label="Churn Rate" value={`${(overview.churn_rate * 100).toFixed(1)}%`} variant="warning" />
        </div>
      )}

      <div className="charts-grid">
        {/* Risk Simulator */}
        <div className="card">
          <div className="card-header"><span className="card-title">Churn Risk Simulator</span></div>

          {[
            { label: 'Recency (days since last purchase)', value: recency, set: setRecency, min: 1, max: 500 },
            { label: 'Frequency (total purchases)', value: frequency, set: setFrequency, min: 1, max: 100 },
            { label: 'Monetary (total spend £)', value: monetary, set: setMonetary, min: 10, max: 50000 },
            { label: 'Avg Revenue per Transaction', value: avgRevenue, set: setAvgRevenue, min: 1, max: 500 },
            { label: 'Total Items Purchased', value: totalItems, set: setTotalItems, min: 1, max: 10000 },
            { label: 'Avg Quantity per Transaction', value: avgQuantity, set: setAvgQuantity, min: 1, max: 200 },
          ].map((s, i) => (
            <div key={i} className="slider-container">
              <div className="slider-header">
                <span className="slider-label">{s.label}</span>
                <span className="slider-value">{s.value.toLocaleString()}</span>
              </div>
              <input type="range" min={s.min} max={s.max} value={s.value} onChange={e => s.set(Number(e.target.value))} />
            </div>
          ))}

          <button className="btn btn-primary w-full mt-1" onClick={handlePredict} disabled={predLoading}>
            {predLoading ? 'Analyzing...' : '🔮 Predict Churn Risk'}
          </button>
        </div>

        {/* Prediction Result */}
        <div className="card">
          <div className="card-header"><span className="card-title">Risk Assessment</span></div>
          {prediction ? (
            <div className="gauge-container">
              <div className={`gauge-value ${gaugeColor}`}>{(prediction.probability * 100).toFixed(1)}%</div>
              <div className={`gauge-label ${gaugeColor}`}>{prediction.risk_level} Risk</div>
              <p style={{ marginTop: 16, color: 'var(--color-text-secondary)', fontSize: 13, textAlign: 'center' }}>
                {prediction.risk_level === 'High'
                  ? '⚠️ This customer profile shows high churn probability. Immediate retention campaign recommended.'
                  : prediction.risk_level === 'Medium'
                  ? '⚡ Moderate risk detected. Consider proactive engagement strategies.'
                  : '✅ Low churn risk. Continue standard engagement protocols.'}
              </p>
              <div className="mt-2" style={{ width: '100%', height: 12, background: 'var(--color-surface)', borderRadius: 6, overflow: 'hidden' }}>
                <div style={{
                  width: `${prediction.probability * 100}%`,
                  height: '100%',
                  borderRadius: 6,
                  background: prediction.risk_level === 'High' ? 'var(--color-danger)' : prediction.risk_level === 'Medium' ? 'var(--color-warning)' : 'var(--color-success)',
                  transition: 'width 0.5s ease',
                }} />
              </div>
            </div>
          ) : (
            <div style={{ padding: 40, textAlign: 'center', color: 'var(--color-text-muted)' }}>
              <p style={{ fontSize: 48, marginBottom: 8 }}>🔮</p>
              <p>Adjust the sliders and click predict to analyze churn risk</p>
            </div>
          )}
        </div>
      </div>

      {/* Risk Directory */}
      {riskList && riskList.length > 0 && (
        <div className="card mt-2">
          <div className="card-header"><span className="card-title">High-Risk Customer Directory</span></div>
          <div style={{ maxHeight: 350, overflowY: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr><th>Customer ID</th><th>Recency (days)</th><th>Frequency</th><th>Monetary (£)</th><th>Status</th></tr>
              </thead>
              <tbody>
                {riskList.map((row, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 600 }}>#{row.customer_id}</td>
                    <td>{row.recency}</td>
                    <td>{row.frequency}</td>
                    <td>£{row.monetary.toLocaleString()}</td>
                    <td><span className="badge badge-danger">Churned</span></td>
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
