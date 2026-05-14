// js/navbar.js — Dynamic navbar based on auth state

import { isLoggedIn, getUserRole, removeTokens, getCurrentUser } from './session.js';
import { cart } from './cart.js';

export function renderNavbar() {
  const nav = document.getElementById('nav-links');
  if (!nav) return;

  const loggedIn = isLoggedIn();
  const role     = getUserRole();
  const user     = getCurrentUser();

  let html = `
    <a href="#/" class="nav-link-item ${isActive('#/')}">Home</a>
    <a href="#/products" class="nav-link-item ${isActive('#/products')}">Products</a>
    <a href="#/category" class="nav-link-item ${isActive('#/category')}">Categories</a>`;

  if (!loggedIn) {
    html += `
      <a href="#/login" class="nav-link-item ${isActive('#/login')}"><i class="fas fa-sign-in-alt"></i> Login</a>
      <a href="#/register" class="nav-link-item ${isActive('#/register')}"><i class="fas fa-user-plus"></i> Register</a>`;
  } else {
    // Wishlist + Orders for all logged-in users
    html += `
      <a href="#/wishlist" class="nav-link-item ${isActive('#/wishlist')}"><i class="fas fa-heart"></i></a>
      <a href="#/orders" class="nav-link-item ${isActive('#/orders')}">Orders</a>`;

    // Admin link
    if (role === 'admin') {
      html += `<a href="#/admin" class="nav-link-item ${isActive('#/admin')}"><i class="fas fa-shield-alt"></i> Admin</a>`;
    }

    // Profile + Logout
    html += `
      <a href="#/profile" class="nav-link-item ${isActive('#/profile')}"><i class="fas fa-user"></i></a>
      <button id="logout-btn" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</button>`;
  }

  // Cart (always visible)
  html += `
    <a href="#/cart" class="nav-cart ${isActive('#/cart')}">
      <i class="fas fa-shopping-bag"></i>
      <span class="cart-badge" style="display:none;">0</span>
    </a>`;

  nav.innerHTML = html;

  // Logout handler
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      removeTokens();
      window.location.hash = '#/';
      renderNavbar();
    });
  }

  // Update cart badge
  cart.updateBadge();
}

function isActive(hash) {
  const current = window.location.hash || '#/';
  if (hash === '#/') return current === '#/' || current === '' ? 'active' : '';
  return current.startsWith(hash) ? 'active' : '';
}
