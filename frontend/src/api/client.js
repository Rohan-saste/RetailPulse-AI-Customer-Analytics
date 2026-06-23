// ==============================================================
// RetailPulse Client – Axios API Client
// ==============================================================

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// ── JWT Interceptor ─────────────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('rp_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── 401 Handler ─────────────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('rp_token');
      localStorage.removeItem('rp_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
