// ==============================================================
// RetailPulse Client – Inventory Health Page
// ==============================================================

import { useState } from 'react';
import { PageHeader, LoadingSpinner, InsightBox } from '../components/ui/Shared';
import MetricCard from '../components/ui/MetricCard';
import { useInventorySummary, useFastMovers, useSlowMovers, useInventoryLedger } from '../api/hooks';

const statusBadge = (status) => {
  if (status === 'Critical Low Stock') return <span className="badge badge-danger">{status}</span>;
  if (status === 'Reorder Alert') return <span className="badge badge-warning">{status}</span>;
  return <span className="badge badge-success">{status}</span>;
};

export default function InventoryHealth() {
  const { data: summary, loading } = useInventorySummary();
  const { data: fast } = useFastMovers(10);
  const { data: slow } = useSlowMovers(10);
  const [statusFilter, setStatusFilter] = useState(null);
  const { data: ledger } = useInventoryLedger(statusFilter);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="fade-in">
      <PageHeader title="Inventory Health Monitor" subtitle="Real-time stock levels, reorder alerts, and demand velocity" />

      <InsightBox title="Supply Chain Intelligence">
        Safety stock is calculated as (max daily sales - avg daily sales) × lead time (7 days). Products below safety stock are flagged as critical.
      </InsightBox>

      {/* Summary KPIs */}
      {summary && !summary.error && (
        <div className="metrics-grid">
          <MetricCard label="Total SKUs" value={summary.total_skus.toLocaleString()} variant="info" />
          <MetricCard label="Critical Stock" value={summary.critical_skus.toLocaleString()} variant="danger" />
          <MetricCard label="Reorder Needed" value={summary.reorder_skus.toLocaleString()} variant="warning" />
          <MetricCard label="Healthy Stock" value={summary.healthy_skus.toLocaleString()} variant="success" />
        </div>
      )}

      <div className="charts-grid">
        {/* Fast Movers */}
        <div className="card">
          <div className="card-header"><span className="card-title">🚀 Fast-Moving Products</span></div>
          {fast && (
            <table className="data-table">
              <thead><tr><th>Product</th><th>Avg Daily Sales</th><th>Status</th></tr></thead>
              <tbody>
                {fast.map((item, i) => (
                  <tr key={i}>
                    <td style={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.description}</td>
                    <td>{item.avg_daily_sales}</td>
                    <td>{statusBadge(item.status)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Slow Movers */}
        <div className="card">
          <div className="card-header"><span className="card-title">🐌 Slow-Moving Products</span></div>
          {slow && (
            <table className="data-table">
              <thead><tr><th>Product</th><th>Avg Daily Sales</th><th>Status</th></tr></thead>
              <tbody>
                {slow.map((item, i) => (
                  <tr key={i}>
                    <td style={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.description}</td>
                    <td>{item.avg_daily_sales}</td>
                    <td>{statusBadge(item.status)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Full Ledger */}
      <div className="card mt-2">
        <div className="card-header">
          <span className="card-title">Reorder Ledger</span>
          <div style={{ display: 'flex', gap: 8 }}>
            {[null, 'Critical Low Stock', 'Reorder Alert', 'Healthy Stock'].map(f => (
              <button
                key={f || 'all'}
                className={`btn btn-sm ${statusFilter === f ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setStatusFilter(f)}
              >
                {f || 'All'}
              </button>
            ))}
          </div>
        </div>
        {ledger && (
          <div style={{ maxHeight: 400, overflowY: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr><th>Product</th><th>Avg Daily</th><th>Safety Stock</th><th>Reorder Point</th><th>Current Stock</th><th>Status</th></tr>
              </thead>
              <tbody>
                {ledger.slice(0, 50).map((item, i) => (
                  <tr key={i}>
                    <td style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.description}</td>
                    <td>{item.avg_daily_sales}</td>
                    <td>{item.safety_stock}</td>
                    <td>{item.reorder_point}</td>
                    <td>{item.current_stock}</td>
                    <td>{statusBadge(item.status)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
