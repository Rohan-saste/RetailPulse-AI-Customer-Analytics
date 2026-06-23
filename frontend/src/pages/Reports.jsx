// ==============================================================
// RetailPulse Client – Reports & Downloads Page
// ==============================================================

import { useState } from 'react';
import { PageHeader, InsightBox } from '../components/ui/Shared';
import { downloadExcel, downloadMarkdown } from '../api/hooks';
import { FileSpreadsheet, FileText } from 'lucide-react';

export default function Reports() {
  const [downloading, setDownloading] = useState(null);

  const handleDownload = async (type) => {
    setDownloading(type);
    try {
      if (type === 'excel') await downloadExcel();
      if (type === 'markdown') await downloadMarkdown();
    } catch (err) {
      console.error('Download failed:', err);
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="fade-in">
      <PageHeader title="Reports & Downloads" subtitle="Export executive workbooks and summary reports" />

      <InsightBox title="Report Generator">
        Download consolidated analytics reports in Excel or Markdown format. Excel workbooks include multi-sheet data covering sales, segments, forecasts, churn risk, and inventory health.
      </InsightBox>

      <div className="charts-grid">
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <FileSpreadsheet size={48} color="var(--color-success)" style={{ marginBottom: 16 }} />
          <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Excel Workbook</h3>
          <p style={{ fontSize: 13, color: 'var(--color-text-secondary)', marginBottom: 20 }}>
            Multi-sheet workbook with Sales Summary, Customer Clusters, Demand Forecast, Churn Risk List, and Inventory Health.
          </p>
          <button className="btn btn-primary" onClick={() => handleDownload('excel')} disabled={downloading === 'excel'}>
            {downloading === 'excel' ? '⏳ Generating...' : '📥 Download Excel'}
          </button>
        </div>

        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <FileText size={48} color="var(--color-primary-light)" style={{ marginBottom: 16 }} />
          <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Executive Summary (Markdown)</h3>
          <p style={{ fontSize: 13, color: 'var(--color-text-secondary)', marginBottom: 20 }}>
            Formatted markdown report with KPI highlights, segment strategies, and inventory alerts for board presentations.
          </p>
          <button className="btn btn-primary" onClick={() => handleDownload('markdown')} disabled={downloading === 'markdown'}>
            {downloading === 'markdown' ? '⏳ Generating...' : '📥 Download Report'}
          </button>
        </div>
      </div>
    </div>
  );
}
