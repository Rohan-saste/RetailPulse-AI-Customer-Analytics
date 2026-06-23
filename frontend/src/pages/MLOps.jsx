// ==============================================================
// RetailPulse Client – MLOps Observability Page
// ==============================================================

import { useState } from 'react';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import { useAuth } from '../context/AuthContext';
import { useDriftReport, triggerRetrain } from '../api/hooks';

export default function MLOps() {
  const { isAdmin } = useAuth();
  const { data: drift, loading } = useDriftReport();
  const [retraining, setRetraining] = useState(false);
  const [retrainResult, setRetrainResult] = useState(null);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainResult(null);
    try {
      const result = await triggerRetrain();
      setRetrainResult(result);
    } catch (err) {
      setRetrainResult({ status: 'failed', message: err.response?.data?.detail || err.message });
    } finally {
      setRetraining(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="fade-in">
      <PageHeader title="MLOps Observability" subtitle="Data drift monitoring, model health, and retrain pipeline" />

      <InsightBox title="Drift Detection">
        The Kolmogorov–Smirnov test compares feature distributions between reference and current periods. A p-value below 0.05 indicates statistically significant drift.
      </InsightBox>

      {drift && !drift.error && (
        <>
          {/* Drift Status Banner */}
          <div className="card mb-2">
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <span style={{ fontSize: 36 }}>{drift.drift_detected ? '⚠️' : '✅'}</span>
              <div>
                <h3 style={{ fontSize: 18, fontWeight: 700, color: drift.drift_detected ? 'var(--color-warning)' : 'var(--color-success)' }}>
                  {drift.drift_detected ? 'Data Drift Detected' : 'No Significant Drift'}
                </h3>
                <p style={{ fontSize: 13, color: 'var(--color-text-secondary)' }}>
                  Reference: {drift.reference_period} ({drift.reference_rows.toLocaleString()} rows) &nbsp;|&nbsp;
                  Current: {drift.current_period} ({drift.current_rows.toLocaleString()} rows)
                </p>
              </div>
            </div>
          </div>

          {/* KS Statistics Table */}
          <div className="card mb-2">
            <div className="card-header"><span className="card-title">Feature Drift Metrics</span></div>
            <table className="data-table">
              <thead>
                <tr><th>Feature</th><th>KS Statistic</th><th>P-Value</th><th>Ref Mean</th><th>Current Mean</th><th>Drift</th></tr>
              </thead>
              <tbody>
                {Object.entries(drift.metrics).map(([key, m]) => (
                  <tr key={key}>
                    <td style={{ fontWeight: 600, color: 'var(--color-text)' }}>{key}</td>
                    <td>{m.ks_statistic.toFixed(4)}</td>
                    <td>{m.p_value < 0.001 ? '<0.001' : m.p_value.toFixed(4)}</td>
                    <td>{m.ref_mean.toFixed(3)}</td>
                    <td>{m.curr_mean.toFixed(3)}</td>
                    <td>
                      <span className={`badge ${m.drift_detected ? 'badge-warning' : 'badge-success'}`}>
                        {m.drift_detected ? 'Drift' : 'Stable'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Retrain Pipeline */}
      <div className="card">
        <div className="card-header"><span className="card-title">Retrain Pipeline</span></div>
        <p style={{ fontSize: 13, color: 'var(--color-text-secondary)', marginBottom: 16 }}>
          Trigger a full model retraining pipeline: data cleaning → segmentation → forecasting → churn prediction → drift analysis.
        </p>
        {isAdmin ? (
          <button className="btn btn-primary" onClick={handleRetrain} disabled={retraining}>
            {retraining ? '⏳ Retraining...' : '🔄 Trigger Full Retrain'}
          </button>
        ) : (
          <p style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>
            🔒 Admin role required to trigger retrain pipeline.
          </p>
        )}
        {retrainResult && (
          <div className={`mt-2 ${retrainResult.status === 'completed' ? 'insight-box' : ''}`}
               style={retrainResult.status === 'failed' ? { marginTop: 16, padding: 12, background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 8 } : {}}>
            <p style={{ fontSize: 13, color: retrainResult.status === 'completed' ? 'var(--color-success)' : 'var(--color-danger)' }}>
              <strong>{retrainResult.status === 'completed' ? '✅' : '❌'} {retrainResult.status}:</strong> {retrainResult.message}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
