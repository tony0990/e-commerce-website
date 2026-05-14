// js/pages/cartPage.js — Shopping cart

import { cart, DELIVERY_FEE } from '../cart.js';
import { escapeHtml, formatPrice } from '../utils.js';
import { isLoggedIn } from '../session.js';
import { showToast } from '../toast.js';

export function renderCartPage(container) {
  const items = cart.getItems();

  if (items.length === 0) {
    container.innerHTML = `<div class="empty-state"><i class="fas fa-shopping-bag"></i><h2>Your cart is empty</h2><p>Looks like you haven't added anything yet.</p><a href="#/products" class="btn btn-primary">Continue Shopping</a></div>`;
    return;
  }

  container.innerHTML = `
    <div class="page-header"><h1>Shopping Cart</h1><p>${cart.getCount()} item${cart.getCount() !== 1 ? 's' : ''} in your cart</p></div>
    <div class="cart-layout">
      <div id="cart-items"></div>
      <div class="order-card">
        <h3>Order Summary</h3>
        <div class="order-row"><span>Subtotal</span><span id="cart-subtotal">${formatPrice(cart.getSubtotal())}</span></div>
        <div class="order-row"><span>Delivery</span><span>${formatPrice(DELIVERY_FEE)}</span></div>
        <div class="order-row bold"><span>Total</span><span id="cart-total">${formatPrice(cart.getTotal())}</span></div>
        <button class="btn btn-primary" id="checkout-btn" style="width:100%;justify-content:center;margin-top:1.5rem;">
          <i class="fas fa-lock"></i> Proceed to Checkout
        </button>
        <a href="#/products" style="display:block;text-align:center;margin-top:1rem;font-size:.85rem;color:var(--cyan);font-weight:600;">Continue Shopping</a>
      </div>
    </div>`;

  renderCartItems();

  document.getElementById('checkout-btn')?.addEventListener('click', () => {
    if (!isLoggedIn()) { showToast('Please log in to checkout', 'info'); window.location.hash = '#/login'; return; }
    window.location.hash = '#/checkout';
  });
}

function renderCartItems() {
  const el = document.getElementById('cart-items');
  if (!el) return;
  const items = cart.getItems();

  el.innerHTML = items.map(item => {
    const img = item.image || `https://placehold.co/220x220/e0f7fa/0eb5c8?text=${encodeURIComponent((item.name||'').slice(0,10))}`;
    return `
      <div class="cart-item" data-id="${item.id}">
        <div class="cart-item__img"><img src="${img}" alt="${escapeHtml(item.name)}" onerror="this.src='https://placehold.co/220x220/e0f7fa/0eb5c8?text=Product'"></div>
        <div>
          <div class="cart-item__cat">${escapeHtml(item.category)}</div>
          <div class="cart-item__name">${escapeHtml(item.name)}</div>
          <div class="cart-item__price">${formatPrice(item.price)}</div>
          <div class="qty-box" style="margin-top:.5rem;">
            <button class="qty-minus" data-id="${item.id}">−</button>
            <span>${item.qty}</span>
            <button class="qty-plus" data-id="${item.id}">+</button>
          </div>
        </div>
        <div class="cart-item__right">
          <div class="cart-item__total">${formatPrice(item.price * item.qty)}</div>
          <button class="cart-item__remove" data-id="${item.id}"><i class="fas fa-trash"></i> Remove</button>
        </div>
      </div>`;
  }).join('');

  // Qty handlers
  el.querySelectorAll('.qty-minus').forEach(btn => btn.addEventListener('click', async () => {
    const id = parseInt(btn.dataset.id);
    const item = cart.getItems().find(i => i.id === id);
    if (item && item.qty > 1) { await cart.setQty(id, item.qty - 1); refreshCart(); }
  }));
  el.querySelectorAll('.qty-plus').forEach(btn => btn.addEventListener('click', async () => {
    const id = parseInt(btn.dataset.id);
    const item = cart.getItems().find(i => i.id === id);
    if (item) { await cart.setQty(id, item.qty + 1); refreshCart(); }
  }));
  el.querySelectorAll('.cart-item__remove').forEach(btn => btn.addEventListener('click', async () => {
    await cart.remove(parseInt(btn.dataset.id));
    refreshCart();
    showToast('Item removed from cart', 'info');
  }));
}

function refreshCart() {
  const items = cart.getItems();
  if (items.length === 0) { window.location.hash = '#/cart'; return; }
  renderCartItems();
  const sub = document.getElementById('cart-subtotal');
  const tot = document.getElementById('cart-total');
  if (sub) sub.textContent = formatPrice(cart.getSubtotal());
  if (tot) tot.textContent = formatPrice(cart.getTotal());
}
