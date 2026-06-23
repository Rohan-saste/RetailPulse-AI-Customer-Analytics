// ==============================================================
// RetailPulse Client – API Hooks
// ==============================================================

import { useState, useEffect, useCallback } from 'react';
import api from './client';

/** Generic data fetcher hook */
function useApiData(url, params = {}, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get(url, { params });
      setData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [url, JSON.stringify(params)]);

  useEffect(() => { fetch(); }, [fetch, ...deps]);

  return { data, loading, error, refetch: fetch };
}

/** Build query string from filter state */
function buildFilterParams(filters) {
  const params = {};
  if (filters.countries?.length) params.countries = filters.countries.join(',');
  if (filters.years?.length) params.years = filters.years.join(',');
  if (filters.startDate) params.start_date = filters.startDate;
  if (filters.endDate) params.end_date = filters.endDate;
  if (filters.segments?.length) params.segments = filters.segments.join(',');
  return params;
}

// ── Dashboard Hooks ────────────────────────────────────────
export function useFilters() {
  return useApiData('/dashboard/filters');
}

export function useDashboardKPIs(filters = {}) {
  return useApiData('/dashboard/kpis', buildFilterParams(filters), [filters]);
}

export function useMonthlyRevenue(filters = {}) {
  return useApiData('/dashboard/monthly-revenue', buildFilterParams(filters), [filters]);
}

export function useGeoRevenue(filters = {}) {
  return useApiData('/dashboard/geo-revenue', buildFilterParams(filters), [filters]);
}

export function useTopProducts(filters = {}, n = 10) {
  return useApiData('/dashboard/top-products', { ...buildFilterParams(filters), n }, [filters]);
}

export function useTopCountries(filters = {}, n = 8) {
  return useApiData('/dashboard/top-countries', { ...buildFilterParams(filters), n }, [filters]);
}

// ── EDA Hooks ──────────────────────────────────────────────
export function useDistributions(filters = {}) {
  return useApiData('/eda/distributions', buildFilterParams(filters), [filters]);
}

export function useTemporalHeatmap(filters = {}) {
  return useApiData('/eda/temporal-heatmap', buildFilterParams(filters), [filters]);
}

export function useWeeklyRevenue(filters = {}) {
  return useApiData('/eda/weekly-revenue', buildFilterParams(filters), [filters]);
}

export function useCorrelations(filters = {}) {
  return useApiData('/eda/correlations', buildFilterParams(filters), [filters]);
}

export function useStats(filters = {}) {
  return useApiData('/eda/stats', buildFilterParams(filters), [filters]);
}

// ── Analytics Hooks ────────────────────────────────────────
export function useTreemap(filters = {}) {
  return useApiData('/analytics/treemap', buildFilterParams(filters), [filters]);
}

export function useScatter(filters = {}) {
  return useApiData('/analytics/scatter', buildFilterParams(filters), [filters]);
}

// ── Segmentation Hooks ─────────────────────────────────────
export function useSegmentComposition(filters = {}) {
  return useApiData('/segmentation/composition', buildFilterParams(filters), [filters]);
}

export function useSegmentProfile(filters = {}) {
  return useApiData('/segmentation/profile', buildFilterParams(filters), [filters]);
}

export function useClusters3D(filters = {}) {
  return useApiData('/segmentation/clusters-3d', buildFilterParams(filters), [filters]);
}

// ── Forecast Hooks ─────────────────────────────────────────
export function useForecastData(horizon = 90) {
  return useApiData('/forecast/data', { horizon_days: horizon }, [horizon]);
}

// ── Churn Hooks ────────────────────────────────────────────
export function useChurnOverview() {
  return useApiData('/churn/overview');
}

export function useChurnRiskList(n = 100) {
  return useApiData('/churn/risk-list', { n }, [n]);
}

export async function predictChurn(features) {
  const res = await api.post('/churn/predict', features);
  return res.data;
}

// ── Inventory Hooks ────────────────────────────────────────
export function useInventorySummary() {
  return useApiData('/inventory/summary');
}

export function useFastMovers(n = 10) {
  return useApiData('/inventory/fast-movers', { n });
}

export function useSlowMovers(n = 10) {
  return useApiData('/inventory/slow-movers', { n });
}

export function useInventoryLedger(statusFilter = null) {
  return useApiData('/inventory/ledger', statusFilter ? { status_filter: statusFilter } : {}, [statusFilter]);
}

// ── MLOps Hooks ────────────────────────────────────────────
export function useDriftReport() {
  return useApiData('/mlops/drift-report');
}

export async function triggerRetrain() {
  const res = await api.post('/mlops/retrain');
  return res.data;
}

// ── Reports ────────────────────────────────────────────────
export async function downloadExcel() {
  const res = await api.get('/reports/excel', { responseType: 'blob' });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'retailpulse_executive_workbook.xlsx');
  document.body.appendChild(link);
  link.click();
  link.remove();
}

export async function downloadMarkdown() {
  const res = await api.get('/reports/markdown', { responseType: 'blob' });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'retailpulse_executive_report.md');
  document.body.appendChild(link);
  link.click();
  link.remove();
}
