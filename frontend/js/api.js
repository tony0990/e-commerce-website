// js/api.js — Centralized API client with JWT token refresh

const BASE_URL = 'http://localhost:8000/api/v1';

import { getAccessToken, getRefreshToken, saveTokens, removeTokens } from './session.js';
import { showToast } from './toast.js';

/**
 * Core fetch wrapper. Attaches Bearer token, handles 401 refresh, extracts errors.
 */
async function request(endpoint, options = {}) {
  const token = getAccessToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let res;
  try {
    res = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
  } catch (err) {
    throw new Error('Network error — is the backend running?');
  }

  // Handle 401 — attempt token refresh
  if (res.status === 401) {
    const refreshed = await attemptRefresh();
    if (refreshed) {
      // Retry original request with new token
      headers['Authorization'] = `Bearer ${getAccessToken()}`;
      res = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
    } else {
      removeTokens();
      window.location.hash = '#/login';
      showToast('Session expired. Please log in again.', 'error');
      throw new Error('Unauthorized');
    }
  }

  // 204 No Content
  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    let message = 'An error occurred';
    if (data.detail) {
      if (Array.isArray(data.detail)) {
        message = data.detail.map(e => e.msg || e.message || JSON.stringify(e)).join(', ');
      } else {
        message = data.detail;
      }
    } else if (data.message) {
      message = data.message;
    } else if (data.errors) {
      message = data.errors.map(e => `${e.field}: ${e.message}`).join(', ');
    }
    throw new Error(message);
  }

  return data;
}

/**
 * Attempt to refresh tokens using the stored refresh token.
 */
async function attemptRefresh() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  try {
    const res = await fetch(`${BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!res.ok) return false;

    const data = await res.json();
    if (data.tokens) {
      saveTokens(data.tokens.access_token, data.tokens.refresh_token);
      return true;
    }
  } catch { /* refresh failed */ }
  return false;
}


// ══════════════════════════════════════════════════════════════
// AUTH
// ══════════════════════════════════════════════════════════════

export async function apiLogin(email, password) {
  const data = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  // Response: { success, data: { user, tokens: { access_token, refresh_token } } }
  const tokens = data.data?.tokens || data.tokens || {};
  saveTokens(tokens.access_token, tokens.refresh_token);
  return data;
}

export async function apiRegister(userData) {
  const data = await request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
  // Auto-login: save tokens from registration response
  const tokens = data.data?.tokens || data.tokens || {};
  if (tokens.access_token) {
    saveTokens(tokens.access_token, tokens.refresh_token);
  }
  return data;
}

export async function apiGetMe() {
  return request('/auth/me');
}

export async function apiChangePassword(currentPassword, newPassword, confirmNewPassword) {
  return request('/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
      confirm_new_password: confirmNewPassword,
    }),
  });
}


// ══════════════════════════════════════════════════════════════
// PRODUCTS
// ══════════════════════════════════════════════════════════════

export async function apiGetProducts(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/products/?${query}`);
}

export async function apiGetProduct(id) {
  return request(`/products/${id}`);
}

export async function apiCreateProduct(data) {
  return request('/products/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function apiUpdateProduct(id, data) {
  return request(`/products/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function apiDeleteProduct(id) {
  return request(`/products/${id}`, { method: 'DELETE' });
}

export async function apiGetCategories() {
  return request('/products/categories');
}

export async function apiCreateCategory(data) {
  return request('/products/categories', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}


// ══════════════════════════════════════════════════════════════
// CART
// ══════════════════════════════════════════════════════════════

export async function apiGetCart() {
  return request('/cart/');
}

export async function apiAddToCart(productId, quantity = 1) {
  return request('/cart/items', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export async function apiUpdateCartItem(itemId, quantity) {
  return request(`/cart/items/${itemId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
}

export async function apiRemoveCartItem(itemId) {
  return request(`/cart/items/${itemId}`, { method: 'DELETE' });
}

export async function apiClearCart() {
  return request('/cart/', { method: 'DELETE' });
}

export async function apiSyncCart(items) {
  return request('/cart/sync', {
    method: 'POST',
    body: JSON.stringify({ items }),
  });
}


// ══════════════════════════════════════════════════════════════
// ORDERS
// ══════════════════════════════════════════════════════════════

export async function apiPlaceOrder(orderData) {
  return request('/orders', {
    method: 'POST',
    body: JSON.stringify(orderData),
  });
}

export async function apiGetMyOrders() {
  return request('/orders/me');
}

export async function apiGetAllOrders() {
  return request('/orders/all');
}

export async function apiGetOrder(id) {
  return request(`/orders/${id}`);
}

export async function apiUpdateOrderStatus(id, status) {
  return request(`/orders/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}

export async function apiTrackOrder(id) {
  return request(`/orders/${id}/track`);
}


// ══════════════════════════════════════════════════════════════
// WISHLIST
// ══════════════════════════════════════════════════════════════

export async function apiGetWishlist() {
  return request('/wishlist/');
}

export async function apiAddToWishlist(productId) {
  return request('/wishlist/', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId }),
  });
}

export async function apiRemoveFromWishlist(productId) {
  return request(`/wishlist/${productId}`, { method: 'DELETE' });
}


// ══════════════════════════════════════════════════════════════
// USERS (Profile)
// ══════════════════════════════════════════════════════════════

export async function apiGetProfile() {
  return request('/users/me/profile');
}

export async function apiUpdateProfile(data) {
  return request('/users/me/profile', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}


// ══════════════════════════════════════════════════════════════
// ADMIN — Users
// ══════════════════════════════════════════════════════════════

export async function apiGetAllUsers(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/users/?${query}`);
}

export async function apiGetUserCount() {
  return request('/users/count');
}

export async function apiAdminCreateUser(data) {
  return request('/users/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function apiAdminUpdateUser(id, data) {
  return request(`/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function apiAdminDeleteUser(id) {
  return request(`/users/${id}`, { method: 'DELETE' });
}

export async function apiToggleUserStatus(id) {
  return request(`/users/${id}/toggle-status`, { method: 'PATCH' });
}


// ══════════════════════════════════════════════════════════════
// ADMIN — Dashboard
// ══════════════════════════════════════════════════════════════

export async function apiGetDashboardStats() {
  return request('/dashboard/stats');
}

export async function apiGetMetrics() {
  return request('/dashboard/metrics');
}

export async function apiGetLogs(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/dashboard/logs?${query}`);
}

export async function apiGetLogStats() {
  return request('/dashboard/logs/stats');
}
