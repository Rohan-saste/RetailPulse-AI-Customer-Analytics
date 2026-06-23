import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          {/* Add other routes here as placeholders */}
          <Route path="eda" element={<div className="p-4">EDA Content Placeholder</div>} />
          <Route path="sales" element={<div className="p-4">Sales Analytics Placeholder</div>} />
          <Route path="customers" element={<div className="p-4">Customer Segmentation Placeholder</div>} />
          <Route path="forecast" element={<div className="p-4">Demand Forecast Placeholder</div>} />
          <Route path="churn" element={<div className="p-4">Churn Risk Placeholder</div>} />
          <Route path="inventory" element={<div className="p-4">Inventory Health Placeholder</div>} />
          <Route path="mlops" element={<div className="p-4">MLOps Observability Placeholder</div>} />
          <Route path="reports" element={<div className="p-4">Reports Center Placeholder</div>} />
          <Route path="about" element={<div className="p-4">About Platform Placeholder</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
