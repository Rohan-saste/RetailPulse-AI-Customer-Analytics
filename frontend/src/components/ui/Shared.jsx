// ==============================================================
// RetailPulse Client – Loading & Insight Components
// ==============================================================

export function LoadingSpinner() {
  return (
    <div className="loading-spinner">
      <div className="spinner" />
    </div>
  );
}

export function InsightBox({ title, children }) {
  return (
    <div className="insight-box">
      <h4>💡 {title}</h4>
      <p>{children}</p>
    </div>
  );
}

export function PageHeader({ title, subtitle }) {
  return (
    <div className="page-header fade-in">
      <h2>{title}</h2>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
}

export function ErrorMessage({ message }) {
  return (
    <div style={{ padding: 40, textAlign: 'center', color: 'var(--color-danger)' }}>
      <p>⚠️ {message}</p>
    </div>
  );
}
