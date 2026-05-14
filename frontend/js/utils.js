// js/utils.js — Shared helper utilities

/**
 * Escape HTML to prevent XSS
 */
export function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  const d = document.createElement('div');
  d.textContent = String(str);
  return d.innerHTML;
}

/**
 * Format price with $ sign
 */
export function formatPrice(num) {
  return '$' + Number(num).toFixed(2);
}

/**
 * Relative time formatter ("3 hours ago", "just now")
 */
export function relativeTime(dateStr) {
  const date = new Date(dateStr);
  const now  = new Date();
  const diffMs  = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr  = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);

  if (diffSec < 60)  return 'just now';
  if (diffMin < 60)  return `${diffMin}m ago`;
  if (diffHr  < 24)  return `${diffHr}h ago`;
  if (diffDay < 30)  return `${diffDay}d ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * Full date format
 */
export function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric',
  });
}

/**
 * Truncate text
 */
export function truncate(text, maxLen = 150) {
  if (!text) return '';
  return text.length > maxLen ? text.slice(0, maxLen).trimEnd() + '…' : text;
}

/**
 * Set button loading state
 */
export function setLoading(btn, loading, text = '') {
  if (!btn) return;
  if (loading) {
    btn.disabled = true;
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text || 'Loading…'}`;
  } else {
    btn.disabled = false;
    btn.innerHTML = btn.dataset.originalText || text;
  }
}

/**
 * Promise-based confirmation modal
 */
export function confirmModal(message, title = 'Confirm Action') {
  return new Promise((resolve) => {
    const modal = document.getElementById('confirmModal');
    const labelEl = document.getElementById('confirmModalLabel');
    const bodyEl  = document.getElementById('confirmModalBody');
    const okBtn   = document.getElementById('confirmModalOk');
    const cancelBtn = document.getElementById('confirmModalCancel');

    if (!modal) { resolve(false); return; }

    labelEl.textContent = title;
    bodyEl.textContent  = message;
    modal.classList.add('show');
    modal.style.display = 'flex';

    const cleanup = () => {
      modal.classList.remove('show');
      modal.style.display = 'none';
      okBtn.removeEventListener('click', onOk);
      cancelBtn.removeEventListener('click', onCancel);
      modal.removeEventListener('click', onBackdrop);
    };

    const onOk = () => { cleanup(); resolve(true); };
    const onCancel = () => { cleanup(); resolve(false); };
    const onBackdrop = (e) => { if (e.target === modal) { cleanup(); resolve(false); } };

    okBtn.addEventListener('click', onOk);
    cancelBtn.addEventListener('click', onCancel);
    modal.addEventListener('click', onBackdrop);
  });
}

/**
 * Build pagination HTML
 */
export function paginationHtml(currentPage, totalPages, targetId = 'pager') {
  if (totalPages <= 1) return '';
  let items = '';

  items += `<button class="btn btn-sm btn-outline" data-page="${currentPage - 1}" data-target="${targetId}" ${currentPage === 1 ? 'disabled' : ''}>&laquo;</button>`;

  const start = Math.max(1, currentPage - 2);
  const end   = Math.min(totalPages, currentPage + 2);

  for (let i = start; i <= end; i++) {
    items += `<button class="btn btn-sm ${i === currentPage ? 'btn-primary' : 'btn-outline'}" data-page="${i}" data-target="${targetId}">${i}</button>`;
  }

  items += `<button class="btn btn-sm btn-outline" data-page="${currentPage + 1}" data-target="${targetId}" ${currentPage === totalPages ? 'disabled' : ''}>&raquo;</button>`;

  return `<div class="pagination-row">${items}</div>`;
}

/**
 * Attach pagination click handlers
 */
export function attachPaginationHandlers(container, targetId, callback, totalPages) {
  container.querySelectorAll(`[data-target="${targetId}"]`).forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const page = parseInt(btn.dataset.page);
      if (page >= 1 && page <= totalPages) callback(page);
    });
  });
}

/**
 * Skeleton card placeholder
 */
export function skeletonCards(count = 6) {
  return Array(count).fill('').map(() => `
    <div class="product-card" style="opacity:0.4;">
      <div class="product-card__img" style="background:var(--slate-soft);"></div>
      <div class="product-card__body">
        <div style="height:12px;width:40%;background:var(--slate-soft);border-radius:4px;margin-bottom:.5rem;"></div>
        <div style="height:14px;width:80%;background:var(--slate-soft);border-radius:4px;margin-bottom:.7rem;"></div>
        <div style="height:16px;width:30%;background:var(--slate-soft);border-radius:4px;"></div>
      </div>
    </div>`).join('');
}

/**
 * Status badge HTML with color coding
 */
export function statusBadge(status) {
  const colors = {
    pending:    { bg: '#fef3c7', color: '#92400e' },
    confirmed:  { bg: '#dbeafe', color: '#1e40af' },
    processing: { bg: '#e0e7ff', color: '#3730a3' },
    shipped:    { bg: '#cffafe', color: '#155e75' },
    delivered:  { bg: '#d1fae5', color: '#065f46' },
    cancelled:  { bg: '#fee2e2', color: '#991b1b' },
    refunded:   { bg: '#f3e8ff', color: '#6b21a8' },
    completed:  { bg: '#d1fae5', color: '#065f46' },
    failed:     { bg: '#fee2e2', color: '#991b1b' },
  };
  const c = colors[status] || { bg: '#f1f5f9', color: '#475569' };
  return `<span class="status-badge" style="background:${c.bg};color:${c.color};">${status}</span>`;
}
