// js/pages/wishlistPage.js — Wishlist

import { apiGetWishlist, apiRemoveFromWishlist } from '../api.js';
import { cart } from '../cart.js';
import { escapeHtml, formatPrice } from '../utils.js';
import { showToast } from '../toast.js';

export async function renderWishlistPage(container) {
  container.innerHTML = `<div class="page-header"><h1><i class="fas fa-heart" style="color:var(--cyan);"></i> My Wishlist</h1></div><div id="wishlist-grid" class="product-grid"><div style="text-align:center;padding:3rem;grid-column:1/-1;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div></div>`;

  try {
    const items = await apiGetWishlist();
    const el = document.getElementById('wishlist-grid');

    if (!items || !items.length) {
      el.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><i class="fas fa-heart"></i><h2>Wishlist is empty</h2><p>Save products you love for later!</p><a href="#/products" class="btn btn-primary">Browse Products</a></div>`;
      return;
    }

    el.innerHTML = items.map(w => {
      const p = w.product || {};
      const img = p.image_url || `https://placehold.co/400x400/e0f7fa/0eb5c8?text=Product`;
      return `
        <div class="product-card fade-up">
          <a href="#/products/${p.id}" class="product-card__img"><img src="${img}" alt="${escapeHtml(p.name)}" loading="lazy"></a>
          <div class="product-card__body">
            <div class="product-card__cat">${escapeHtml(p.category?.name || '')}</div>
            <div class="product-card__name">${escapeHtml(p.name)}</div>
            <div class="product-card__footer">
              <div class="product-card__price">${formatPrice(p.price)}</div>
              <div style="display:flex;gap:.4rem;">
                <button class="add-btn move-to-cart" data-product='${JSON.stringify({id:p.id,name:p.name,price:p.price,image_url:p.image_url,category:p.category})}' title="Add to cart"><i class="fas fa-shopping-bag"></i></button>
                <button class="add-btn remove-wish" data-product-id="${p.id}" style="background:#ef4444;" title="Remove"><i class="fas fa-times"></i></button>
              </div>
            </div>
          </div>
        </div>`;
    }).join('');

    // Move to cart
    el.querySelectorAll('.move-to-cart').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const p = JSON.parse(btn.dataset.product);
        await cart.add(p);
        showToast(`${p.name} added to cart`, 'success');
      });
    });

    // Remove from wishlist
    el.querySelectorAll('.remove-wish').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const pid = parseInt(btn.dataset.productId);
        try {
          await apiRemoveFromWishlist(pid);
          btn.closest('.product-card')?.remove();
          showToast('Removed from wishlist', 'info');
          // If no items left
          if (!document.querySelectorAll('#wishlist-grid .product-card').length) {
            renderWishlistPage(container);
          }
        } catch (err) { showToast(err.message, 'error'); }
      });
    });
  } catch (err) {
    document.getElementById('wishlist-grid').innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><h2>Failed to load wishlist</h2><p>${escapeHtml(err.message)}</p></div>`;
  }
}
