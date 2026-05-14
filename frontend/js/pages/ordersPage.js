// js/pages/ordersPage.js — My orders list

import { apiGetMyOrders, apiTrackOrder } from '../api.js';
import { escapeHtml, formatPrice, statusBadge, formatDate } from '../utils.js';
import { showToast } from '../toast.js';

export async function renderOrdersPage(container) {
  container.innerHTML = `<div class="page-header"><h1>My Orders</h1><p>Track and manage your orders</p></div><div id="orders-list" style="max-width:800px;"><div style="text-align:center;padding:3rem;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div></div>`;

  try {
    const orders = await apiGetMyOrders();
    const el = document.getElementById('orders-list');
    if (!orders || !orders.length) {
      el.innerHTML = `<div class="empty-state"><i class="fas fa-box-open"></i><h2>No orders yet</h2><p>Your orders will appear here once you make a purchase.</p><a href="#/products" class="btn btn-primary">Start Shopping</a></div>`;
      return;
    }

    el.innerHTML = orders.map(order => `
      <div class="form-section" style="margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem;">
          <div>
            <strong>Order #${order.id}</strong>
            <span style="color:var(--text-mute);font-size:.82rem;margin-left:.5rem;">${formatDate(order.created_at)}</span>
          </div>
          <div style="display:flex;gap:.5rem;align-items:center;">
            ${statusBadge(order.status)}
            <button class="btn btn-sm btn-outline track-btn" data-order-id="${order.id}"><i class="fas fa-map-marker-alt"></i> Track</button>
          </div>
        </div>
        ${(order.items || []).map(item => `
          <div style="display:flex;gap:1rem;align-items:center;padding:.5rem 0;border-top:1px solid var(--slate-soft);">
            <div style="font-size:.88rem;flex:1;">${escapeHtml(item.product?.name || `Product #${item.product_id}`)} <span style="color:var(--text-mute);">×${item.quantity}</span></div>
            <div style="font-weight:700;">${formatPrice(item.total_price)}</div>
          </div>`).join('')}
        <div style="display:flex;justify-content:space-between;border-top:1px solid var(--slate-soft);padding-top:.75rem;margin-top:.5rem;">
          <span style="font-weight:700;">Total</span>
          <span style="font-weight:800;font-size:1.05rem;">${formatPrice(order.total_amount)}</span>
        </div>
        <div id="track-info-${order.id}" style="display:none;margin-top:.75rem;padding:.75rem;background:var(--cyan-light);border-radius:8px;font-size:.85rem;"></div>
      </div>`).join('');

    // Track handlers
    el.querySelectorAll('.track-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const orderId = parseInt(btn.dataset.orderId);
        const infoEl = document.getElementById(`track-info-${orderId}`);
        if (infoEl.style.display === 'block') { infoEl.style.display = 'none'; return; }
        try {
          const track = await apiTrackOrder(orderId);
          infoEl.innerHTML = `<i class="fas fa-truck" style="color:var(--cyan);margin-right:.5rem;"></i><strong>Status:</strong> ${track.status} ${track.tracking_number ? `| <strong>Tracking:</strong> ${escapeHtml(track.tracking_number)}` : ''}<br><em>${escapeHtml(track.message)}</em>`;
          infoEl.style.display = 'block';
        } catch (err) { showToast(err.message, 'error'); }
      });
    });
  } catch (err) {
    document.getElementById('orders-list').innerHTML = `<div class="empty-state"><h2>Failed to load orders</h2><p>${escapeHtml(err.message)}</p></div>`;
  }
}
