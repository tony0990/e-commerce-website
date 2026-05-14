// js/app.js — Main entry point: hash router + page dispatch

import { renderNavbar }           from './navbar.js';
import { isLoggedIn, getUserRole } from './session.js';
import { showToast }               from './toast.js';

// Page renderers
import { renderHomePage }          from './pages/homePage.js';
import { renderLoginPage }         from './pages/loginPage.js';
import { renderRegisterPage }      from './pages/registerPage.js';
import { renderProductsPage }      from './pages/productsPage.js';
import { renderProductDetailPage } from './pages/productDetailPage.js';
import { renderCartPage }          from './pages/cartPage.js';
import { renderCheckoutPage }      from './pages/checkoutPage.js';
import { renderOrdersPage }        from './pages/ordersPage.js';
import { renderWishlistPage }      from './pages/wishlistPage.js';
import { renderProfilePage }       from './pages/profilePage.js';
import { renderAdminPage }         from './pages/adminPage.js';

// ── Initial render ──────────────────────────────────────────
renderNavbar();
route();

// Listen for hash changes
window.addEventListener('hashchange', () => {
  route();
  renderNavbar();
});

// ── Router ──────────────────────────────────────────────────
async function route() {
  const hash    = window.location.hash || '#/';
  const content = document.getElementById('page-content');
  if (!content) return;

  window.scrollTo({ top: 0, behavior: 'smooth' });

  // ── Route matching ────────────────────────────────────────

  // Home
  if (hash === '#/' || hash === '') {
    document.title = 'PremiumStore — Modern Shopping';
    return renderHomePage(content);
  }

  // Login
  if (hash === '#/login') {
    if (isLoggedIn()) { window.location.hash = '#/'; return; }
    document.title = 'Sign In — PremiumStore';
    return renderLoginPage(content);
  }

  // Register
  if (hash === '#/register') {
    if (isLoggedIn()) { window.location.hash = '#/'; return; }
    document.title = 'Create Account — PremiumStore';
    return renderRegisterPage(content);
  }

  // Products listing (also handles #/products?category_id=X&search=Y)
  if (hash === '#/products' || hash.startsWith('#/products?')) {
    document.title = 'Products — PremiumStore';
    return renderProductsPage(content);
  }

  // Product detail — #/products/:id
  const productMatch = hash.match(/^#\/products\/(\d+)$/);
  if (productMatch) {
    document.title = 'Product — PremiumStore';
    return renderProductDetailPage(content, parseInt(productMatch[1]));
  }

  // Categories (redirect to products with filter)
  if (hash === '#/category' || hash.startsWith('#/category')) {
    document.title = 'Categories — PremiumStore';
    return renderProductsPage(content);
  }

  // Cart
  if (hash === '#/cart') {
    document.title = 'Cart — PremiumStore';
    return renderCartPage(content);
  }

  // Checkout (auth required)
  if (hash === '#/checkout') {
    if (!guardAuth()) return;
    document.title = 'Checkout — PremiumStore';
    return renderCheckoutPage(content);
  }

  // Orders (auth required)
  if (hash === '#/orders') {
    if (!guardAuth()) return;
    document.title = 'My Orders — PremiumStore';
    return renderOrdersPage(content);
  }

  // Wishlist (auth required)
  if (hash === '#/wishlist') {
    if (!guardAuth()) return;
    document.title = 'Wishlist — PremiumStore';
    return renderWishlistPage(content);
  }

  // Profile (auth required)
  if (hash === '#/profile') {
    if (!guardAuth()) return;
    document.title = 'Profile — PremiumStore';
    return renderProfilePage(content);
  }

  // Admin (admin only)
  if (hash === '#/admin') {
    if (!guardAuth()) return;
    if (!guardRole(['admin'], 'Admin access only.')) return;
    document.title = 'Admin — PremiumStore';
    return renderAdminPage(content);
  }

  // 404
  render404(content);
}

// ── Route Guards ────────────────────────────────────────────
function guardAuth() {
  if (!isLoggedIn()) {
    showToast('Please log in to continue.', 'info');
    window.location.hash = '#/login';
    return false;
  }
  return true;
}

function guardRole(allowedRoles, message = 'Access denied.') {
  const role = getUserRole();
  if (!role || !allowedRoles.includes(role)) {
    showToast(message, 'error');
    window.location.hash = '#/';
    return false;
  }
  return true;
}

function render404(container) {
  document.title = '404 — PremiumStore';
  container.innerHTML = `
    <div class="empty-state" style="min-height:50vh;">
      <i class="fas fa-ghost" style="font-size:4rem;color:var(--slate-soft);margin-bottom:1.5rem;display:block;"></i>
      <h2 style="font-size:2rem;">404 — Page Not Found</h2>
      <p>The page you're looking for doesn't exist.</p>
      <a href="#/" class="btn btn-primary" style="margin-top:1rem;"><i class="fas fa-home"></i> Go Home</a>
    </div>`;
}
