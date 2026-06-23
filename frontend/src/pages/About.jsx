// ==============================================================
// RetailPulse Client – About Page
// ==============================================================

import { PageHeader } from '../components/ui/Shared';

export default function About() {
  return (
    <div className="fade-in">
      <PageHeader title="About RetailPulse" subtitle="Platform architecture and technology stack" />

      <div className="card mb-2">
        <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 12, color: 'var(--color-text)' }}>
          📊 RetailPulse Enterprise BI Platform
        </h3>
        <p style={{ fontSize: 14, color: 'var(--color-text-secondary)', lineHeight: 1.7, marginBottom: 16 }}>
          RetailPulse is an AI-powered customer analytics and demand forecasting platform built for retail enterprises.
          It combines RFM segmentation, Prophet forecasting, churn prediction, and real-time inventory monitoring into
          a unified intelligence hub.
        </p>

        <div className="insight-box">
          <h4>Architecture</h4>
          <p>
            <strong>Frontend:</strong> React + Vite + Plotly.js<br/>
            <strong>Backend:</strong> FastAPI + Python<br/>
            <strong>ML Models:</strong> scikit-learn (Random Forest, KMeans), Prophet<br/>
            <strong>Database:</strong> PostgreSQL (Supabase compatible) / CSV fallback<br/>
            <strong>Auth:</strong> JWT (bcrypt + PyJWT)<br/>
            <strong>Deployment:</strong> Vercel (frontend) + Render (backend)
          </p>
        </div>
      </div>

      <div className="charts-grid">
        <div className="card">
          <div className="card-header"><span className="card-title">ML Pipeline</span></div>
          <ul style={{ listStyle: 'none', padding: 0, fontSize: 13, color: 'var(--color-text-secondary)' }}>
            {[
              '01. Data Loading (Excel → CSV)',
              '02. Data Cleaning & Preprocessing',
              '03. Exploratory Data Analysis',
              '04. Feature Engineering (RFM)',
              '05. Customer Segmentation (KMeans)',
              '06. Demand Forecasting (Prophet)',
              '07. Churn Prediction (Random Forest)',
              '08. MLOps Monitoring (KS Drift)',
              '09. Retrain Pipeline Orchestration',
            ].map((step, i) => (
              <li key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--color-border-light)', display: 'flex', alignItems: 'center', gap: 10 }}>
                <span className="badge badge-primary" style={{ minWidth: 24, justifyContent: 'center' }}>{i + 1}</span>
                {step}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Key Features</span></div>
          <ul style={{ listStyle: 'none', padding: 0, fontSize: 13, color: 'var(--color-text-secondary)' }}>
            {[
              '📊 Executive KPI Dashboard with Sparklines',
              '🔍 Interactive Exploratory Analysis',
              '🌳 Product Revenue Treemaps',
              '👥 RFM Customer Segmentation (4 clusters)',
              '📈 Prophet Demand Forecasting (90-day)',
              '🔮 Churn Risk Simulator with ML',
              '📦 Inventory Health & Reorder Alerts',
              '🔄 MLOps Drift Monitoring & Retrain',
              '📥 Excel & Markdown Report Export',
              '🔐 JWT Authentication & RBAC',
              '🌍 Geographic Revenue Choropleth',
              '🐳 Docker & Cloud Deployment Ready',
            ].map((feat, i) => (
              <li key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--color-border-light)' }}>{feat}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card mt-2" style={{ textAlign: 'center', padding: 30 }}>
        <p style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>
          RetailPulse v2.0 • Built with React + FastAPI • © 2026
        </p>
      </div>
    </div>
  );
}
