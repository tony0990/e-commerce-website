// js/pages/checkoutPage.js — Checkout + order placement

import { cart, DELIVERY_FEE } from '../cart.js';
import { apiPlaceOrder, apiGetMe } from '../api.js';
import { escapeHtml, formatPrice, setLoading } from '../utils.js';
import { showToast } from '../toast.js';

export async function renderCheckoutPage(container) {
  const items = cart.getItems();
  if (!items.length) { window.location.hash = '#/cart'; return; }

  // Pre-fill from profile
  let user = {};
  try { const res = await apiGetMe(); user = res.data || res || {}; } catch {}

  container.innerHTML = `
    <div class="page-header"><h1>Checkout</h1></div>
    <div class="checkout-layout">
      <div>
        <div class="form-section">
          <h3><i class="fas fa-map-marker-alt"></i> Shipping Information</h3>
          <form id="checkout-form" novalidate>
            <div class="form-group">
              <label class="form-label">Address *</label>
              <input class="form-control" id="ship-address" value="${escapeHtml(user.address||'')}" required placeholder="123 Main Street">
            </div>
            <div class="form-row">
              <div class="form-group"><label class="form-label">City *</label><input class="form-control" id="ship-city" value="${escapeHtml(user.city||'')}" required placeholder="Cairo"></div>
              <div class="form-group"><label class="form-label">State</label><input class="form-control" id="ship-state" value="${escapeHtml(user.state||'')}" placeholder="Optional"></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label class="form-label">ZIP Code *</label><input class="form-control" id="ship-zip" value="${escapeHtml(user.zip_code||'')}" required placeholder="12345"></div>
              <div class="form-group"><label class="form-label">Country *</label><input class="form-control" id="ship-country" value="${escapeHtml(user.country||'Egypt')}" required></div>
            </div>
            <div class="form-group"><label class="form-label">Notes (optional)</label><textarea class="form-control" id="ship-notes" rows="2" placeholder="Delivery instructions…"></textarea></div>
          </form>
        </div>
        <div class="form-section">
          <h3><i class="fas fa-credit-card"></i> Payment Method</h3>
          <label class="pay-option selected"><input type="radio" name="payment" value="COD" checked><label>Cash on Delivery</label><span class="pay-tag">Default</span></label>
          <label class="pay-option"><input type="radio" name="payment" value="Online"><label>Online Payment</label></label>
        </div>
      </div>
      <div class="order-card">
        <h3>Order Summary</h3>
        ${items.map(i => `<div class="order-row"><span>${escapeHtml(i.name)} ×${i.qty}</span><span>${formatPrice(i.price*i.qty)}</span></div>`).join('')}
        <div class="order-row"><span>Subtotal</span><span>${formatPrice(cart.getSubtotal())}</span></div>
        <div class="order-row"><span>Delivery</span><span>${formatPrice(DELIVERY_FEE)}</span></div>
        <div class="order-row bold"><span>Total</span><span>${formatPrice(cart.getTotal())}</span></div>
        <div id="checkout-error" class="form-error" style="display:none;"></div>
        <button class="btn btn-primary" id="place-order-btn" style="width:100%;justify-content:center;margin-top:1.5rem;"><i class="fas fa-lock"></i> Place Order</button>
      </div>
    </div>
    <div class="success-modal" id="success-modal">
      <div class="success-box">
        <div class="success-icon"><i class="fas fa-check"></i></div>
        <h2>Order Placed!</h2>
        <p>Your order has been placed successfully. You can track it in your orders page.</p>
        <a href="#/orders" class="btn btn-primary" id="go-orders-btn">View My Orders</a>
      </div>
    </div>`;

  // Payment option toggle
  document.querySelectorAll('.pay-option').forEach(opt => {
    opt.addEventListener('click', () => {
      document.querySelectorAll('.pay-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input[type=radio]').checked = true;
    });
  });

  // Place order
  document.getElementById('place-order-btn')?.addEventListener('click', async () => {
    const errEl = document.getElementById('checkout-error');
    const addr = document.getElementById('ship-address').value.trim();
    const city = document.getElementById('ship-city').value.trim();
    const zip  = document.getElementById('ship-zip').value.trim();
    const country = document.getElementById('ship-country').value.trim();
    if (!addr || !city || !zip || !country) { errEl.textContent = 'Please fill in all required fields.'; errEl.style.display = 'block'; return; }

    const btn = document.getElementById('place-order-btn');
    setLoading(btn, true, 'Placing order…');
    errEl.style.display = 'none';

    try {
      await apiPlaceOrder({
        shipping_address: addr,
        shipping_city: city,
        shipping_state: document.getElementById('ship-state').value.trim() || undefined,
        shipping_zip: zip,
        shipping_country: country,
        payment_method: document.querySelector('input[name=payment]:checked')?.value || 'COD',
        notes: document.getElementById('ship-notes').value.trim() || undefined,
        items: cart.getItems().map(i => ({ product_id: i.id, quantity: i.qty })),
      });
      await cart.clear();
      document.getElementById('success-modal')?.classList.add('show');
    } catch (err) {
      errEl.textContent = err.message; errEl.style.display = 'block';
      showToast(err.message, 'error');
    } finally { setLoading(btn, false); }
  });
}
