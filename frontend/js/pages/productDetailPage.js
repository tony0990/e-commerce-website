// js/pages/productDetailPage.js — Single product detail

import { apiGetProduct, apiAddToWishlist } from '../api.js';
import { cart } from '../cart.js';
import { escapeHtml, formatPrice, setLoading } from '../utils.js';
import { showToast } from '../toast.js';
import { isLoggedIn } from '../session.js';

export async function renderProductDetailPage(container, productId) {
  container.innerHTML = `<div style="text-align:center;padding:4rem;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div>`;

  try {
    const p = await apiGetProduct(productId);
    const img = p.image_url || `https://placehold.co/600x600/e0f7fa/0eb5c8?text=${encodeURIComponent((p.name||'').slice(0,16))}`;

    container.innerHTML = `
      <div class="container">
        <div class="breadcrumb">
          <a href="#/">Home</a> / <a href="#/products">Products</a> / <span>${escapeHtml(p.name)}</span>
        </div>
        <div class="details-grid">
          <div class="details-gallery">
            <img src="${img}" alt="${escapeHtml(p.name)}" onerror="this.src='https://placehold.co/600x600/e0f7fa/0eb5c8?text=Product'">
          </div>
          <div>
            <div class="details-cat">${escapeHtml(p.category?.name || '')}</div>
            <h1 class="details-name">${escapeHtml(p.name)}</h1>
            <div class="details-price">${formatPrice(p.price)}</div>
            ${p.original_price && p.original_price > p.price ? `<div style="color:var(--text-mute);text-decoration:line-through;margin-top:-.8rem;margin-bottom:1rem;">${formatPrice(p.original_price)}</div>` : ''}
            <div class="details-desc">${escapeHtml(p.description)}</div>
            <div class="qty-row">
              <div class="qty-box">
                <button id="qty-minus">−</button>
                <span id="qty-val">1</span>
                <button id="qty-plus">+</button>
              </div>
              <span style="font-size:.85rem;color:var(--text-mute);">${p.stock > 0 ? `${p.stock} in stock` : '<span style="color:#ef4444;">Out of stock</span>'}</span>
            </div>
            <div class="details-actions">
              <button class="btn btn-primary" id="add-to-cart-btn" ${p.stock <= 0 ? 'disabled' : ''}>
                <i class="fas fa-shopping-bag"></i> Add to Cart
              </button>
              <button class="btn btn-outline" id="add-to-wishlist-btn">
                <i class="fas fa-heart"></i> Wishlist
              </button>
            </div>
            <div class="perks">
              <div class="perk"><i class="fas fa-truck"></i> Free Shipping over $500</div>
              <div class="perk"><i class="fas fa-undo"></i> 30-Day Returns</div>
              <div class="perk"><i class="fas fa-shield-alt"></i> 2-Year Warranty</div>
              <div class="perk"><i class="fas fa-lock"></i> Secure Checkout</div>
            </div>
          </div>
        </div>
      </div>`;

    // Quantity controls
    let qty = 1;
    const qtyVal = document.getElementById('qty-val');
    document.getElementById('qty-minus')?.addEventListener('click', () => { if (qty > 1) { qty--; qtyVal.textContent = qty; } });
    document.getElementById('qty-plus')?.addEventListener('click', () => { if (qty < (p.stock || 99)) { qty++; qtyVal.textContent = qty; } });

    // Add to cart
    document.getElementById('add-to-cart-btn')?.addEventListener('click', async (e) => {
      const btn = e.currentTarget;
      setLoading(btn, true, 'Adding…');
      await cart.add(p, qty);
      showToast(`${p.name} added to cart!`, 'success');
      setLoading(btn, false);
    });

    // Add to wishlist
    document.getElementById('add-to-wishlist-btn')?.addEventListener('click', async (e) => {
      if (!isLoggedIn()) { showToast('Please log in to use wishlist', 'info'); window.location.hash = '#/login'; return; }
      const btn = e.currentTarget;
      setLoading(btn, true, 'Adding…');
      try {
        await apiAddToWishlist(p.id);
        showToast(`${p.name} added to wishlist!`, 'success');
      } catch (err) { showToast(err.message, 'error'); }
      setLoading(btn, false);
    });

  } catch (err) {
    container.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-circle" style="font-size:3rem;color:var(--slate-soft);margin-bottom:1rem;"></i><h2>Product Not Found</h2><p style="color:var(--text-mute);">${escapeHtml(err.message)}</p><a href="#/products" class="btn btn-primary btn-sm" style="margin-top:1rem;">Browse Products</a></div>`;
  }
}
