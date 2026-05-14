// js/pages/adminPage.js — Admin dashboard with full CRUD

import {
  apiGetDashboardStats, apiGetAllUsers, apiGetAllOrders,
  apiUpdateOrderStatus, apiToggleUserStatus, apiAdminDeleteUser,
  apiGetLogs, apiGetProducts, apiGetProduct, apiCreateProduct,
  apiUpdateProduct, apiDeleteProduct, apiGetCategories,
  apiCreateCategory
} from '../api.js';
import { escapeHtml, formatPrice, statusBadge, formatDate, confirmModal, setLoading } from '../utils.js';
import { showToast } from '../toast.js';

// Cache categories for product forms
let categoriesCache = [];

export async function renderAdminPage(container) {
  container.innerHTML = `
    <div class="page-header"><h1><i class="fas fa-shield-alt" style="color:var(--cyan);"></i> Admin Dashboard</h1></div>
    <div id="admin-tabs" class="filter-bar" style="margin-bottom:2rem;">
      <button class="btn btn-sm btn-primary admin-tab active" data-tab="overview">Overview</button>
      <button class="btn btn-sm btn-outline admin-tab" data-tab="products">Products</button>
      <button class="btn btn-sm btn-outline admin-tab" data-tab="categories">Categories</button>
      <button class="btn btn-sm btn-outline admin-tab" data-tab="users">Users</button>
      <button class="btn btn-sm btn-outline admin-tab" data-tab="orders">Orders</button>
      <button class="btn btn-sm btn-outline admin-tab" data-tab="logs">Logs</button>
    </div>
    <div id="admin-content"><div style="text-align:center;padding:3rem;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div></div>`;

  // Pre-load categories
  try { categoriesCache = await apiGetCategories(); } catch { categoriesCache = []; }

  // Tab switching
  document.querySelectorAll('.admin-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.admin-tab').forEach(b => { b.classList.remove('btn-primary','active'); b.classList.add('btn-outline'); });
      btn.classList.add('btn-primary','active'); btn.classList.remove('btn-outline');
      loadTab(btn.dataset.tab);
    });
  });

  await loadTab('overview');
}

async function loadTab(tab) {
  const el = document.getElementById('admin-content');
  el.innerHTML = '<div style="text-align:center;padding:3rem;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div>';

  try {
    if (tab === 'overview')    await renderOverview(el);
    else if (tab === 'products')   await renderProductsTab(el);
    else if (tab === 'categories') await renderCategoriesTab(el);
    else if (tab === 'users')      await renderUsersTab(el);
    else if (tab === 'orders')     await renderOrdersTab(el);
    else if (tab === 'logs')       await renderLogsTab(el);
  } catch (err) { el.innerHTML = `<div class="empty-state"><h2>Error</h2><p>${escapeHtml(err.message)}</p></div>`; }
}

// ══════════════════════════════════════════════════════════════
// OVERVIEW
// ══════════════════════════════════════════════════════════════

async function renderOverview(el) {
  const stats = await apiGetDashboardStats();
  el.innerHTML = `
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.2rem;margin-bottom:2rem;">
      ${statCard('fa-dollar-sign', 'Revenue', formatPrice(stats.total_revenue || 0))}
      ${statCard('fa-box', 'Total Orders', stats.total_orders || 0)}
      ${statCard('fa-clock', 'Pending', stats.pending_orders || 0)}
      ${statCard('fa-users', 'Users', stats.total_users || 0)}
    </div>
    ${stats.top_products?.length ? `<div class="form-section"><h3>Top Products</h3>${stats.top_products.map(p => `<div class="order-row"><span>${escapeHtml(p.name || p.product_name || 'Product')}</span><span>${p.total_sold || p.count || 0} sold</span></div>`).join('')}</div>` : ''}`;
}

function statCard(icon, label, value) {
  return `<div class="form-section" style="text-align:center;"><i class="fas ${icon}" style="font-size:1.8rem;color:var(--cyan);margin-bottom:.5rem;display:block;"></i><div style="font-size:1.8rem;font-weight:800;">${value}</div><div style="font-size:.82rem;color:var(--text-mute);font-weight:600;">${label}</div></div>`;
}

// ══════════════════════════════════════════════════════════════
// PRODUCTS MANAGEMENT
// ══════════════════════════════════════════════════════════════

async function renderProductsTab(el) {
  const data = await apiGetProducts({ page: 1, page_size: 100 });
  const products = data.items || [];

  el.innerHTML = `
    <div class="form-section">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
        <h3 style="margin:0;"><i class="fas fa-box"></i> Products (${products.length})</h3>
        <button class="btn btn-primary btn-sm" id="add-product-btn"><i class="fas fa-plus"></i> Add Product</button>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--slate-soft);text-align:left;">
              <th style="padding:.6rem;">ID</th>
              <th>Image</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${products.map(p => `
              <tr style="border-bottom:1px solid var(--slate-soft);">
                <td style="padding:.6rem;">${p.id}</td>
                <td><img src="${p.image_url || 'https://placehold.co/40x40/e0f7fa/0eb5c8?text=P'}" style="width:40px;height:40px;border-radius:6px;object-fit:cover;" onerror="this.src='https://placehold.co/40x40/e0f7fa/0eb5c8?text=P'"></td>
                <td style="font-weight:600;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(p.name)}</td>
                <td>${escapeHtml(p.category?.name || '—')}</td>
                <td style="font-weight:700;">${formatPrice(p.price)}</td>
                <td>${p.stock}</td>
                <td>${p.is_active ? '<span style="color:#22c55e;font-weight:600;">Active</span>' : '<span style="color:#ef4444;font-weight:600;">Inactive</span>'}</td>
                <td style="white-space:nowrap;">
                  <button class="btn btn-sm btn-outline edit-product" data-id="${p.id}" title="Edit"><i class="fas fa-edit"></i></button>
                  <button class="btn btn-sm btn-danger del-product" data-id="${p.id}" title="Delete"><i class="fas fa-trash"></i></button>
                </td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Product Form Modal -->
    <div id="product-form-overlay" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(15,23,42,.88);align-items:center;justify-content:center;">
      <div style="background:white;border-radius:20px;padding:2.5rem;max-width:600px;width:90%;max-height:90vh;overflow-y:auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
          <h3 id="product-form-title" style="margin:0;">Add Product</h3>
          <button id="close-product-form" style="background:none;border:none;font-size:1.3rem;cursor:pointer;color:var(--slate-mid);"><i class="fas fa-times"></i></button>
        </div>
        <form id="product-form" novalidate>
          <input type="hidden" id="pf-id">
          <div class="form-group">
            <label class="form-label">Product Name *</label>
            <input class="form-control" id="pf-name" required placeholder="e.g. Wireless Headphones">
          </div>
          <div class="form-group">
            <label class="form-label">Description *</label>
            <textarea class="form-control" id="pf-desc" rows="3" required placeholder="Product description…"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Price *</label>
              <input type="number" class="form-control" id="pf-price" step="0.01" min="0.01" required placeholder="99.99">
            </div>
            <div class="form-group">
              <label class="form-label">Original Price</label>
              <input type="number" class="form-control" id="pf-original-price" step="0.01" min="0" placeholder="149.99">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Stock *</label>
              <input type="number" class="form-control" id="pf-stock" min="0" required placeholder="50">
            </div>
            <div class="form-group">
              <label class="form-label">Category *</label>
              <select class="form-control" id="pf-category" required>
                <option value="">Select category</option>
                ${categoriesCache.map(c => `<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('')}
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Image URL</label>
            <input class="form-control" id="pf-image" placeholder="https://example.com/image.jpg">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;font-size:.88rem;font-weight:600;color:var(--slate-mid);">
                <input type="checkbox" id="pf-active" checked style="accent-color:var(--cyan);transform:scale(1.2);"> Active
              </label>
            </div>
            <div class="form-group">
              <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;font-size:.88rem;font-weight:600;color:var(--slate-mid);">
                <input type="checkbox" id="pf-offer" style="accent-color:var(--cyan);transform:scale(1.2);"> On Offer
              </label>
            </div>
          </div>
          <div class="form-group" id="pf-offer-price-group" style="display:none;">
            <label class="form-label">Offer Price</label>
            <input type="number" class="form-control" id="pf-offer-price" step="0.01" min="0" placeholder="79.99">
          </div>
          <div id="product-form-error" class="form-error" style="display:none;"></div>
          <div style="display:flex;gap:1rem;margin-top:1rem;">
            <button type="submit" class="btn btn-primary" id="product-form-submit" style="flex:1;justify-content:center;">
              <i class="fas fa-save"></i> Save Product
            </button>
            <button type="button" class="btn btn-outline" id="product-form-cancel">Cancel</button>
          </div>
        </form>
      </div>
    </div>`;

  // ── Event: Add Product ──────────────────────────────────
  document.getElementById('add-product-btn')?.addEventListener('click', () => {
    openProductForm(null);
  });

  // ── Event: Edit Product ─────────────────────────────────
  el.querySelectorAll('.edit-product').forEach(btn => {
    btn.addEventListener('click', async () => {
      try {
        const product = await apiGetProduct(parseInt(btn.dataset.id));
        openProductForm(product);
      } catch (err) { showToast(err.message, 'error'); }
    });
  });

  // ── Event: Delete Product ───────────────────────────────
  el.querySelectorAll('.del-product').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (await confirmModal('Delete this product permanently? This cannot be undone.', 'Delete Product')) {
        try {
          await apiDeleteProduct(parseInt(btn.dataset.id));
          showToast('Product deleted', 'success');
          await renderProductsTab(el);
        } catch (err) { showToast(err.message, 'error'); }
      }
    });
  });

  // ── Event: Close Form ───────────────────────────────────
  document.getElementById('close-product-form')?.addEventListener('click', closeProductForm);
  document.getElementById('product-form-cancel')?.addEventListener('click', closeProductForm);
  document.getElementById('product-form-overlay')?.addEventListener('click', (e) => {
    if (e.target.id === 'product-form-overlay') closeProductForm();
  });

  // ── Event: Offer checkbox toggle ────────────────────────
  document.getElementById('pf-offer')?.addEventListener('change', (e) => {
    document.getElementById('pf-offer-price-group').style.display = e.target.checked ? 'block' : 'none';
  });

  // ── Event: Submit Product Form ──────────────────────────
  document.getElementById('product-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById('product-form-error');
    const submitBtn = document.getElementById('product-form-submit');

    const name        = document.getElementById('pf-name').value.trim();
    const description = document.getElementById('pf-desc').value.trim();
    const price       = parseFloat(document.getElementById('pf-price').value);
    const stock       = parseInt(document.getElementById('pf-stock').value);
    const categoryId  = parseInt(document.getElementById('pf-category').value);

    if (!name || !description || isNaN(price) || isNaN(stock) || isNaN(categoryId)) {
      errorEl.textContent = 'Please fill in all required fields.';
      errorEl.style.display = 'block';
      return;
    }

    const productData = {
      name,
      description,
      price,
      stock,
      category_id: categoryId,
      image_url: document.getElementById('pf-image').value.trim() || undefined,
      is_active: document.getElementById('pf-active').checked,
      is_offer: document.getElementById('pf-offer').checked,
    };

    const origPrice = parseFloat(document.getElementById('pf-original-price').value);
    if (!isNaN(origPrice) && origPrice > 0) productData.original_price = origPrice;

    if (productData.is_offer) {
      const offerPrice = parseFloat(document.getElementById('pf-offer-price').value);
      if (!isNaN(offerPrice) && offerPrice > 0) productData.offer_price = offerPrice;
    }

    const editId = document.getElementById('pf-id').value;

    setLoading(submitBtn, true, 'Saving…');
    errorEl.style.display = 'none';

    try {
      if (editId) {
        await apiUpdateProduct(parseInt(editId), productData);
        showToast('Product updated!', 'success');
      } else {
        await apiCreateProduct(productData);
        showToast('Product created!', 'success');
      }
      closeProductForm();
      await renderProductsTab(el);
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
    } finally {
      setLoading(submitBtn, false);
    }
  });
}

function openProductForm(product) {
  const overlay = document.getElementById('product-form-overlay');
  const title   = document.getElementById('product-form-title');

  document.getElementById('pf-id').value           = product?.id || '';
  document.getElementById('pf-name').value          = product?.name || '';
  document.getElementById('pf-desc').value          = product?.description || '';
  document.getElementById('pf-price').value         = product?.price || '';
  document.getElementById('pf-original-price').value = product?.original_price || '';
  document.getElementById('pf-stock').value         = product?.stock ?? '';
  document.getElementById('pf-category').value      = product?.category_id || product?.category?.id || '';
  document.getElementById('pf-image').value         = product?.image_url || '';
  document.getElementById('pf-active').checked      = product ? product.is_active : true;
  document.getElementById('pf-offer').checked       = product?.is_offer || false;
  document.getElementById('pf-offer-price').value   = product?.offer_price || '';
  document.getElementById('pf-offer-price-group').style.display = product?.is_offer ? 'block' : 'none';
  document.getElementById('product-form-error').style.display = 'none';

  title.textContent = product ? `Edit Product #${product.id}` : 'Add New Product';
  overlay.style.display = 'flex';
}

function closeProductForm() {
  document.getElementById('product-form-overlay').style.display = 'none';
}

// ══════════════════════════════════════════════════════════════
// CATEGORIES MANAGEMENT
// ══════════════════════════════════════════════════════════════

async function renderCategoriesTab(el) {
  const categories = await apiGetCategories();
  categoriesCache = categories;

  el.innerHTML = `
    <div class="form-section">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
        <h3 style="margin:0;"><i class="fas fa-tags"></i> Categories (${categories.length})</h3>
      </div>

      <!-- Add Category Form (inline) -->
      <div style="background:var(--bg);border-radius:var(--radius-sm);padding:1.25rem;margin-bottom:1.5rem;border:1.5px dashed var(--slate-soft);">
        <h4 style="font-size:.92rem;font-weight:700;margin-bottom:1rem;"><i class="fas fa-plus" style="color:var(--cyan);"></i> Add New Category</h4>
        <form id="add-category-form" style="display:flex;gap:1rem;flex-wrap:wrap;align-items:flex-end;">
          <div class="form-group" style="flex:1;min-width:200px;margin-bottom:0;">
            <label class="form-label">Name *</label>
            <input class="form-control" id="cat-name" required placeholder="e.g. Electronics">
          </div>
          <div class="form-group" style="flex:2;min-width:250px;margin-bottom:0;">
            <label class="form-label">Description</label>
            <input class="form-control" id="cat-desc" placeholder="Category description (optional)">
          </div>
          <div class="form-group" style="flex:1;min-width:200px;margin-bottom:0;">
            <label class="form-label">Image URL</label>
            <input class="form-control" id="cat-image" placeholder="https://…">
          </div>
          <button type="submit" class="btn btn-primary btn-sm" id="add-cat-btn" style="height:42px;">
            <i class="fas fa-plus"></i> Add
          </button>
        </form>
        <div id="cat-form-error" class="form-error" style="display:none;margin-top:.75rem;"></div>
      </div>

      <!-- Categories List -->
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--slate-soft);text-align:left;">
              <th style="padding:.6rem;">ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Products</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            ${categories.map(c => `
              <tr style="border-bottom:1px solid var(--slate-soft);">
                <td style="padding:.6rem;">${c.id}</td>
                <td style="font-weight:700;">${escapeHtml(c.name)}</td>
                <td style="color:var(--text-mute);max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(c.description || '—')}</td>
                <td>—</td>
                <td style="font-size:.82rem;color:var(--text-mute);">${c.created_at ? formatDate(c.created_at) : '—'}</td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
      ${categories.length === 0 ? '<p style="text-align:center;color:var(--text-mute);padding:2rem;">No categories yet. Add one above!</p>' : ''}
    </div>`;

  // ── Event: Add Category ─────────────────────────────────
  document.getElementById('add-category-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorEl  = document.getElementById('cat-form-error');
    const submitBtn = document.getElementById('add-cat-btn');
    const name = document.getElementById('cat-name').value.trim();

    if (!name) {
      errorEl.textContent = 'Category name is required.';
      errorEl.style.display = 'block';
      return;
    }

    setLoading(submitBtn, true, 'Adding…');
    errorEl.style.display = 'none';

    try {
      await apiCreateCategory({
        name,
        description: document.getElementById('cat-desc').value.trim() || undefined,
        image_url: document.getElementById('cat-image').value.trim() || undefined,
      });
      showToast(`Category "${name}" created!`, 'success');
      await renderCategoriesTab(el);
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
    } finally {
      setLoading(submitBtn, false);
    }
  });
}

// ══════════════════════════════════════════════════════════════
// USERS
// ══════════════════════════════════════════════════════════════

async function renderUsersTab(el) {
  const res = await apiGetAllUsers({ page: 1, page_size: 50 });
  const users = res.data || res.items || res || [];

  el.innerHTML = `<div class="form-section">
    <h3><i class="fas fa-users"></i> User Management (${users.length})</h3>
    <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
        <thead><tr style="border-bottom:2px solid var(--slate-soft);text-align:left;">
          <th style="padding:.6rem;">ID</th><th>Email</th><th>Name</th><th>Role</th><th>Status</th><th>Actions</th>
        </tr></thead>
        <tbody>${users.map(u => `<tr style="border-bottom:1px solid var(--slate-soft);">
          <td style="padding:.6rem;">${u.id}</td>
          <td>${escapeHtml(u.email)}</td>
          <td>${escapeHtml((u.first_name||'')+' '+(u.last_name||''))}</td>
          <td>${statusBadge(u.role)}</td>
          <td>${u.is_active ? '<span style="color:#22c55e;font-weight:600;">Active</span>' : '<span style="color:#ef4444;font-weight:600;">Inactive</span>'}</td>
          <td style="white-space:nowrap;">
            <button class="btn btn-sm btn-outline toggle-user" data-id="${u.id}">${u.is_active ? 'Deactivate' : 'Activate'}</button>
            <button class="btn btn-sm btn-danger del-user" data-id="${u.id}"><i class="fas fa-trash"></i></button>
          </td>
        </tr>`).join('')}</tbody>
      </table>
    </div>
  </div>`;

  el.querySelectorAll('.toggle-user').forEach(btn => btn.addEventListener('click', async () => {
    try { await apiToggleUserStatus(parseInt(btn.dataset.id)); showToast('User status updated', 'success'); await renderUsersTab(el); } catch (e) { showToast(e.message, 'error'); }
  }));
  el.querySelectorAll('.del-user').forEach(btn => btn.addEventListener('click', async () => {
    if (await confirmModal('Delete this user permanently?', 'Delete User')) {
      try { await apiAdminDeleteUser(parseInt(btn.dataset.id)); showToast('User deleted', 'success'); await renderUsersTab(el); } catch (e) { showToast(e.message, 'error'); }
    }
  }));
}

// ══════════════════════════════════════════════════════════════
// ORDERS
// ══════════════════════════════════════════════════════════════

async function renderOrdersTab(el) {
  const orders = await apiGetAllOrders();
  const statuses = ['pending','confirmed','processing','shipped','delivered','cancelled','refunded'];

  el.innerHTML = `<div class="form-section">
    <h3><i class="fas fa-truck"></i> Order Management (${(orders||[]).length})</h3>
    ${(orders||[]).length === 0 ? '<p style="color:var(--text-mute);text-align:center;padding:2rem;">No orders yet.</p>' : ''}
    ${(orders||[]).map(o => `
      <div style="border-bottom:1px solid var(--slate-soft);padding:1rem 0;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;">
          <div>
            <strong>Order #${o.id}</strong>
            <span style="color:var(--text-mute);font-size:.82rem;"> — ${escapeHtml(o.user?.email || 'User #'+o.user_id)} — ${formatPrice(o.total_amount)} — ${formatDate(o.created_at)}</span>
          </div>
          <div style="display:flex;gap:.5rem;align-items:center;">
            ${statusBadge(o.status)}
            <select class="form-control order-status-select" data-order-id="${o.id}" style="width:auto;padding:.3rem .5rem;font-size:.8rem;">
              ${statuses.map(s => `<option value="${s}" ${s===o.status?'selected':''}>${s}</option>`).join('')}
            </select>
          </div>
        </div>
      </div>`).join('')}
  </div>`;

  el.querySelectorAll('.order-status-select').forEach(sel => {
    sel.addEventListener('change', async () => {
      try { await apiUpdateOrderStatus(parseInt(sel.dataset.orderId), sel.value); showToast('Order status updated', 'success'); } catch (e) { showToast(e.message, 'error'); await renderOrdersTab(el); }
    });
  });
}

// ══════════════════════════════════════════════════════════════
// LOGS
// ══════════════════════════════════════════════════════════════

async function renderLogsTab(el) {
  const res = await apiGetLogs({ limit: 100 });
  const logs = res.logs || [];

  el.innerHTML = `<div class="form-section">
    <h3><i class="fas fa-file-alt"></i> Application Logs</h3>
    <div style="max-height:500px;overflow-y:auto;font-family:monospace;font-size:.78rem;line-height:1.8;">
      ${logs.length ? logs.map(l => `<div style="padding:.2rem 0;border-bottom:1px solid var(--slate-soft);"><span style="color:var(--cyan);">${escapeHtml(l.timestamp)}</span> <span style="color:${l.level==='ERROR'?'#ef4444':'var(--text-mute)'};font-weight:600;">[${l.level}]</span> <span style="color:var(--slate-mid);">[${l.type}]</span> ${escapeHtml(l.message)}</div>`).join('') : '<p style="color:var(--text-mute);">No logs found.</p>'}
    </div>
  </div>`;
}
