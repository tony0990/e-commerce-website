// js/cart.js — Dual-mode cart: localStorage (guest) + API (authenticated)

import { isLoggedIn } from './session.js';
import { apiGetCart, apiAddToCart, apiRemoveCartItem, apiUpdateCartItem, apiClearCart, apiSyncCart } from './api.js';

const CART_KEY     = 'ps_cart';
const DELIVERY_FEE = 70;

class CartManager {
  constructor() {
    this.items = [];
    this._loadLocal();
  }

  // ── Local Storage ───────────────────────────────────────────
  _loadLocal() {
    try {
      this.items = JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch { this.items = []; }
  }

  _saveLocal() {
    localStorage.setItem(CART_KEY, JSON.stringify(this.items));
    this._updateBadge();
  }

  // ── Sync on Login ─────────────────────────────────────────
  async syncOnLogin() {
    if (!isLoggedIn()) return;

    try {
      if (this.items.length > 0) {
        // Merge local cart into DB
        const synced = await apiSyncCart(
          this.items.map(i => ({ product_id: i.id, quantity: i.qty }))
        );
        this._updateFromDb(synced);
      } else {
        // Load DB cart
        const dbCart = await apiGetCart();
        this._updateFromDb(dbCart);
      }
    } catch (err) {
      console.error('Cart sync failed:', err);
    }
  }

  _updateFromDb(dbCart) {
    if (!dbCart || !dbCart.items) return;
    this.items = dbCart.items.map(item => ({
      id:         item.product?.id || item.product_id,
      name:       item.product?.name || 'Product',
      price:      item.product?.price || 0,
      image:      item.product?.image_url || '',
      category:   item.product?.category?.name || '',
      qty:        item.quantity,
      cartItemId: item.id, // The cart_item DB id (needed for update/delete)
    }));
    this._saveLocal();
  }

  // ── Cart Operations ─────────────────────────────────────────

  async add(product, qty = 1) {
    const existing = this.items.find(i => i.id === product.id);
    if (existing) {
      existing.qty += qty;
    } else {
      this.items.push({
        id:       product.id,
        name:     product.name,
        price:    product.price,
        image:    product.image_url || product.image || '',
        category: product.category?.name || product.category || '',
        qty,
      });
    }
    this._saveLocal();

    if (isLoggedIn()) {
      try { await apiAddToCart(product.id, qty); } catch (e) { console.error(e); }
    }
  }

  async remove(productId) {
    // Find the cart item ID before removing
    const item = this.items.find(i => i.id === productId);
    this.items = this.items.filter(i => i.id !== productId);
    this._saveLocal();

    if (isLoggedIn()) {
      try {
        // Need to find the DB cart_item_id
        if (item?.cartItemId) {
          await apiRemoveCartItem(item.cartItemId);
        } else {
          // Fallback: fetch DB cart and find by product_id
          const dbCart = await apiGetCart();
          const dbItem = dbCart.items?.find(i => i.product_id === productId);
          if (dbItem) await apiRemoveCartItem(dbItem.id);
        }
      } catch (e) { console.error(e); }
    }
  }

  async setQty(productId, qty) {
    const item = this.items.find(i => i.id === productId);
    if (!item) return;
    item.qty = Math.max(1, qty);
    this._saveLocal();

    if (isLoggedIn()) {
      try {
        if (item.cartItemId) {
          await apiUpdateCartItem(item.cartItemId, item.qty);
        } else {
          const dbCart = await apiGetCart();
          const dbItem = dbCart.items?.find(i => i.product_id === productId);
          if (dbItem) await apiUpdateCartItem(dbItem.id, item.qty);
        }
      } catch (e) { console.error(e); }
    }
  }

  async clear() {
    this.items = [];
    this._saveLocal();
    if (isLoggedIn()) {
      try { await apiClearCart(); } catch (e) { console.error(e); }
    }
  }

  // ── Getters ─────────────────────────────────────────────────

  getItems()    { return [...this.items]; }
  getCount()    { return this.items.reduce((c, i) => c + i.qty, 0); }
  getSubtotal() { return this.items.reduce((s, i) => s + i.price * i.qty, 0); }
  getDeliveryFee() { return this.items.length ? DELIVERY_FEE : 0; }
  getTotal()    { return this.items.length ? this.getSubtotal() + DELIVERY_FEE : 0; }

  // ── Badge Update ────────────────────────────────────────────

  _updateBadge() {
    document.querySelectorAll('.cart-badge').forEach(b => {
      const n = this.getCount();
      b.textContent = n;
      b.style.display = n > 0 ? 'flex' : 'none';
    });
  }

  updateBadge() { this._updateBadge(); }
}

export const cart = new CartManager();
export { DELIVERY_FEE };
