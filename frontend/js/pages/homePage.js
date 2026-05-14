// js/pages/homePage.js — Landing page: hero + products from API + categories

import { apiGetProducts, apiGetCategories } from '../api.js';
import { cart } from '../cart.js';
import { escapeHtml, formatPrice, skeletonCards } from '../utils.js';
import { showToast } from '../toast.js';
import { isLoggedIn } from '../session.js';

export async function renderHomePage(container) {
  container.innerHTML = `
    <!-- Hero -->
    <section class="hero">
      <div class="container hero-content">
        <h1>Discover Products<br><span>You'll Actually Love</span></h1>
        <p>Curated electronics, fashion, furniture, home living, and luxury watches — all in one beautifully designed store.</p>
        <a href="#/products" class="btn btn-ghost">Browse All Products <i class="fas fa-arrow-right"></i></a>
      </div>
    </section>

    <main class="container">
      <!-- Trending -->
      <section class="section">
        <div class="section-head">
          <h2 class="section-title">Trending Now</h2>
          <a href="#/products" class="view-all">View All →</a>
        </div>
        <div id="trending-grid" class="product-grid">${skeletonCards(5)}</div>
      </section>

      <!-- Categories -->
      <section class="section">
        <div class="section-head">
          <h2 class="section-title">Shop by Category</h2>
        </div>
        <div id="category-grid" class="category-grid"></div>
      </section>

      <!-- Banner -->
      <div class="banner-strip">
        <div>
          <h2>🎉 Best Deals of the Season</h2>
          <p>Hand-picked savings across all categories. Limited stock — grab yours before it's gone.</p>
        </div>
        <a href="#/products" class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,.5);background:rgba(255,255,255,.12);">Shop Deals <i class="fas fa-tag"></i></a>
      </div>

      <!-- Featured -->
      <section class="section">
        <div class="section-head">
          <h2 class="section-title">Featured Products</h2>
          <a href="#/products" class="view-all">View All →</a>
        </div>
        <div id="featured-grid" class="product-grid">${skeletonCards(5)}</div>
      </section>
    </main>`;

  // Load products and categories in parallel
  try {
    const [trendingRes, featuredRes, categories] = await Promise.all([
      apiGetProducts({ page: 1, page_size: 10 }),
      apiGetProducts({ page: 2, page_size: 10 }),
      apiGetCategories().catch(() => []),
    ]);

    renderProductGrid('trending-grid', trendingRes.items || []);
    renderProductGrid('featured-grid', featuredRes.items || []);
    renderCategoryGrid('category-grid', categories || []);
  } catch (err) {
    document.getElementById('trending-grid').innerHTML =
      `<p style="color:var(--text-mute);grid-column:1/-1;text-align:center;">Could not load products. Is the backend running?</p>`;
    document.getElementById('featured-grid').innerHTML = '';
  }
}

function productCardHtml(p) {
  const imgSrc = p.image_url || `https://placehold.co/400x400/e0f7fa/0eb5c8?text=${encodeURIComponent((p.name || '').slice(0, 16))}`;
  const catName = p.category?.name || '';
  return `
    <div class="product-card fade-up" data-id="${p.id}">
      <a href="#/products/${p.id}" class="product-card__img">
        <img src="${imgSrc}" alt="${escapeHtml(p.name)}" loading="lazy"
             onerror="this.src='https://placehold.co/400x400/e0f7fa/0eb5c8?text=Product'">
      </a>
      <div class="product-card__body">
        <div class="product-card__cat">${escapeHtml(catName)}</div>
        <div class="product-card__name">${escapeHtml(p.name)}</div>
        <div class="product-card__footer">
          <div class="product-card__price">${formatPrice(p.price)}</div>
          <button class="add-btn" title="Add to cart" data-product-id="${p.id}">
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>
    </div>`;
}

function renderProductGrid(gridId, products) {
  const el = document.getElementById(gridId);
  if (!el) return;

  if (products.length === 0) {
    el.innerHTML = `<p style="color:var(--text-mute);grid-column:1/-1;text-align:center;">No products found.</p>`;
    return;
  }

  el.innerHTML = products.map(productCardHtml).join('');

  // Add to cart handlers
  el.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      const id = parseInt(btn.dataset.productId);
      const product = products.find(p => p.id === id);
      if (!product) return;

      await cart.add(product);
      btn.classList.add('added');
      btn.innerHTML = '<i class="fas fa-check"></i>';
      showToast(`${product.name} added to cart`, 'success');
      setTimeout(() => {
        btn.classList.remove('added');
        btn.innerHTML = '<i class="fas fa-plus"></i>';
      }, 1200);
    });
  });
}

const categoryIcons = {
  'electronics': 'fa-laptop',
  'fashion':     'fa-shirt',
  'furniture':   'fa-chair',
  'home':        'fa-house',
  'watches':     'fa-clock',
  'home & living': 'fa-house',
};

function renderCategoryGrid(gridId, categories) {
  const el = document.getElementById(gridId);
  if (!el) return;

  if (categories.length === 0) {
    el.innerHTML = '<p style="color:var(--text-mute);text-align:center;">No categories yet.</p>';
    return;
  }

  el.innerHTML = categories.map(cat => {
    const icon = categoryIcons[cat.name?.toLowerCase()] || 'fa-tag';
    return `
      <a href="#/products?category_id=${cat.id}" class="category-card">
        <i class="fas ${icon}"></i>
        <span>${escapeHtml(cat.name)}</span>
      </a>`;
  }).join('');
}

// Export for reuse
export { productCardHtml, renderProductGrid };
