// js/pages/categoriesPage.js — Browse all categories

import { apiGetCategories } from '../api.js';
import { escapeHtml } from '../utils.js';

const categoryIcons = {
  'electronics': 'fa-laptop',
  'fashion':     'fa-shirt',
  'furniture':   'fa-chair',
  'home':        'fa-house',
  'watches':     'fa-clock',
  'home & living': 'fa-house',
  'clothing':    'fa-shirt',
  'sports':      'fa-futbol',
  'books':       'fa-book',
  'beauty':      'fa-spa',
  'toys':        'fa-puzzle-piece',
  'food':        'fa-utensils',
  'automotive':  'fa-car',
  'health':      'fa-heart-pulse',
  'gaming':      'fa-gamepad',
  'music':       'fa-music',
};

const categoryColors = [
  ['#6366f1', '#818cf8'],
  ['#0ea5e9', '#38bdf8'],
  ['#10b981', '#34d399'],
  ['#f59e0b', '#fbbf24'],
  ['#ef4444', '#f87171'],
  ['#8b5cf6', '#a78bfa'],
  ['#ec4899', '#f472b6'],
  ['#14b8a6', '#2dd4bf'],
];

export async function renderCategoriesPage(container) {
  container.innerHTML = `
    <main class="container">
      <div class="page-header">
        <h1>Shop by Category</h1>
        <p>Browse our collection organized by category</p>
      </div>
      <div id="categories-grid" class="categories-page-grid">
        <div style="grid-column:1/-1;text-align:center;padding:3rem;">
          <i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--slate-soft);"></i>
          <p style="color:var(--text-mute);margin-top:1rem;">Loading categories…</p>
        </div>
      </div>
    </main>`;

  try {
    const categories = await apiGetCategories();
    const grid = document.getElementById('categories-grid');
    if (!grid) return;

    if (!categories || categories.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column:1/-1;">
          <i class="fas fa-tags" style="font-size:3rem;color:var(--slate-soft);margin-bottom:1rem;display:block;"></i>
          <h2>No Categories Yet</h2>
          <p style="color:var(--text-mute);">Categories will appear here once they are created.</p>
        </div>`;
      return;
    }

    grid.innerHTML = categories.map((cat, i) => {
      const icon = categoryIcons[cat.name?.toLowerCase()] || 'fa-tag';
      const [color1, color2] = categoryColors[i % categoryColors.length];

      return `
        <a href="#/products?category_id=${cat.id}" class="cat-page-card">
          <div class="cat-page-icon" style="background:linear-gradient(135deg, ${color1}, ${color2});">
            <i class="fas ${icon}"></i>
          </div>
          <div class="cat-page-info">
            <h3>${escapeHtml(cat.name)}</h3>
            ${cat.description ? `<p>${escapeHtml(cat.description)}</p>` : ''}
          </div>
          <i class="fas fa-arrow-right cat-page-arrow"></i>
        </a>`;
    }).join('');

  } catch (err) {
    const grid = document.getElementById('categories-grid');
    if (grid) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column:1/-1;">
          <h2>Failed to load categories</h2>
          <p style="color:var(--text-mute);">${escapeHtml(err.message)}</p>
          <button class="btn btn-primary btn-sm" id="retry-cats">Retry</button>
        </div>`;
      document.getElementById('retry-cats')?.addEventListener('click', () => renderCategoriesPage(container));
    }
  }
}
