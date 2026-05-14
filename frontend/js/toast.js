// js/toast.js — Toast notification system

/**
 * Show a toast notification.
 * @param {string} message
 * @param {'success'|'error'|'info'} type
 */
export function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-stack';
    document.body.appendChild(container);
  }

  const icons = {
    success: 'fa-check-circle',
    error:   'fa-times-circle',
    info:    'fa-info-circle',
  };

  const el = document.createElement('div');
  el.className = `toast-item ${type}`;
  el.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${escapeHtml(message)}</span>`;

  container.appendChild(el);

  const timeout = setTimeout(() => dismiss(el), 4000);
  el.addEventListener('click', () => { clearTimeout(timeout); dismiss(el); });
}

function dismiss(el) {
  el.classList.add('slide-out');
  el.addEventListener('animationend', () => el.remove(), { once: true });
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}
