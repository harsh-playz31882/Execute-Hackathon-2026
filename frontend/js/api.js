/**
 * API helpers for Renewable Energy Marketplace
 */

const API_BASE = '/api/v1';
const TOKEN_KEY = 'energy_marketplace_token';

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function isLoggedIn() {
  return !!getToken();
}

async function fetchJson(path, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || JSON.stringify(data.detail) || `HTTP ${res.status}`);
  }
  return data;
}

async function fetchForm(path, formData, options = {}) {
  const token = getToken();
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, {
    method: 'POST',
    body: formData,
    headers: { ...headers, ...options.headers },
  });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || JSON.stringify(data.detail) || `HTTP ${res.status}`);
  }
  return data;
}

/* Auth */
async function register(body) {
  return fetchJson('/auth/register', { method: 'POST', body: JSON.stringify(body) });
}

async function login(username, password) {
  const form = new FormData();
  form.append('username', username);
  form.append('password', password);
  return fetchForm('/auth/login', form);
}

async function getMe() {
  return fetchJson('/auth/me');
}

/* Assets */
async function listAssets(params = {}) {
  const q = new URLSearchParams(params).toString();
  return fetchJson('/assets/' + (q ? '?' + q : ''));
}

async function getAsset(id) {
  return fetchJson('/assets/' + id);
}

async function createAsset(body) {
  return fetchJson('/assets/', { method: 'POST', body: JSON.stringify(body) });
}

async function updateAsset(id, body) {
  return fetchJson('/assets/' + id, { method: 'PUT', body: JSON.stringify(body) });
}

async function listMyAssets() {
  return fetchJson('/assets/owner/me');
}

/* Interests */
async function createInterest(assetId, message) {
  return fetchJson('/interests/', {
    method: 'POST',
    body: JSON.stringify({ asset_id: assetId, message: message || '' }),
  });
}

async function listMyInterests() {
  return fetchJson('/interests/mine');
}

async function listReceivedInterests() {
  return fetchJson('/interests/received');
}

async function updateInterestStatus(id, status) {
  return fetchJson('/interests/' + id, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}
