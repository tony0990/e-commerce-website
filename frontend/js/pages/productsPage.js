// js/pages/productsPage.js — Browse all products with filters + pagination

import { apiGetProducts, apiGetCategories } from '../api.js';
import { skeletonCards, paginationHtml, attachPaginationHandlers, escapeHtml, formatPrice } from '../utils.js';
import { cart } from '../cart.js';
import { showToast } from '../toast.js';

let currentPage = 1, currentCategoryId = null, currentSearch = '', allCategories = [];

export async function renderProductsPage(container) {
  const hashParams = new URLSearchParams(window.location.hash.split('?')[1] || '');
  currentCategoryId = hashParams.get('category_id') || null;
  currentSearch = hashParams.get('search') || '';
  currentPage = 1;

  container.innerHTML = `
    <div class="page-header"><h1>All Products</h1><p>Browse our complete collection</p></div>
    <div class="filter-bar">
      <input type="text" class="form-control" id="product-search" placeholder="Search products…" value="${escapeHtml(currentSearch)}" style="max-width:300px;">
      <select class="form-control" id="category-filter" style="max-width:200px;"><option value="">All Categories</option></select>
      <span class="filter-count" id="product-count"></span>
    </div>
    <div id="products-grid" class="product-grid">${skeletonCards(8)}</div>
    <div id="products-pagination" style="margin-top:2rem;"></div>`;

  try {
    allCategories = await apiGetCategories();
    const select = document.getElementById('category-filter');
    allCategories.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat.id; opt.textContent = cat.name;
      if (String(cat.id) === String(currentCategoryId)) opt.selected = true;
      select.appendChild(opt);
    });
  } catch {}

  document.getElementById('category-filter')?.addEventListener('change', e => { currentCategoryId = e.target.value || null; currentPage = 1; loadProducts(); });
  let t; document.getElementById('product-search')?.addEventListener('input', e => { clearTimeout(t); t = setTimeout(() => { currentSearch = e.target.value.trim(); currentPage = 1; loadProducts(); }, 400); });
  await loadProducts();
}

async function loadProducts() {
  const grid = document.getElementById('products-grid'), paginEl = document.getElementById('products-pagination'), countEl = document.getElementById('product-count');
  if (!grid) return;
  grid.innerHTML = skeletonCards(8);
  try {
    const params = { page: currentPage, page_size: 20 };
    if (currentCategoryId) params.category_id = currentCategoryId;
    if (currentSearch) params.search = currentSearch;
    const data = await apiGetProducts(params);
    const products = data.items || [], total = data.total || 0, totalPages = Math.ceil(total / (data.page_size || 20));
    if (countEl) countEl.textContent = `${total} product${total !== 1 ? 's' : ''}`;
    if (!products.length) { grid.innerHTML = '<div class="empty-state" style="grid-column:1/-1;"><i class="fas fa-search" style="font-size:3rem;color:var(--slate-soft);margin-bottom:1rem;display:block;"></i><h2>No products found</h2><p style="color:var(--text-mute);">Try adjusting your search or filter.</p></div>'; if (paginEl) paginEl.innerHTML = ''; return; }
    grid.innerHTML = products.map(p => productCardHtml(p)).join('');
    attachAddToCartHandlers(grid, products);
    if (paginEl) { paginEl.innerHTML = paginationHtml(currentPage, totalPages, 'pp'); attachPaginationHandlers(paginEl, 'pp', pg => { currentPage = pg; loadProducts(); window.scrollTo({top:0,behavior:'smooth'}); }, totalPages); }
  } catch (err) { grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><h2>Failed to load</h2><p>${escapeHtml(err.message)}</p><button class="btn btn-primary btn-sm" id="retry-p">Retry</button></div>`; document.getElementById('retry-p')?.addEventListener('click', loadProducts); }
}

export function productCardHtml(p) {
  const img = p.image_url || `https://placehold.co/400x400/e0f7fa/0eb5c8?text=${encodeURIComponent((p.name||'').slice(0,16))}`;
  return `<div class="product-card fade-up" data-id="${p.id}"><a href="#/products/${p.id}" class="product-card__img"><img src="${img}" alt="${escapeHtml(p.name)}" loading="lazy" onerror="this.src='https://placehold.co/400x400/e0f7fa/0eb5c8?text=Product'"></a><div class="product-card__body"><div class="product-card__cat">${escapeHtml(p.category?.name||'')}</div><div class="product-card__name">${escapeHtml(p.name)}</div><div class="product-card__footer"><div class="product-card__price">${formatPrice(p.price)}</div><button class="add-btn" title="Add to cart" data-product-id="${p.id}"><i class="fas fa-plus"></i></button></div></div></div>`;
}

export function attachAddToCartHandlers(el, products) {
  el.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.preventDefault(); e.stopPropagation();
      const product = products.find(p => p.id === parseInt(btn.dataset.productId));
      if (!product) return;
      await cart.add(product);
      btn.classList.add('added'); btn.innerHTML = '<i class="fas fa-check"></i>';
      showToast(`${product.name} added to cart`, 'success');
      setTimeout(() => { btn.classList.remove('added'); btn.innerHTML = '<i class="fas fa-plus"></i>'; }, 1200);
    });
  });
}
