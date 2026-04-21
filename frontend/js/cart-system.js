/**
 * PremiumStore Cart System
 * localStorage-persisted cart with $70 delivery fee.
 */
const CART_KEY = 'premiumstore_cart';
const DELIVERY_FEE = 70;

class Cart {
  constructor() {
    this._load();
  }

  _load()  { try { this.items = JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch { this.items = []; } }
  _save()  { localStorage.setItem(CART_KEY, JSON.stringify(this.items)); }

  add(product, qty = 1) {
    const ex = this.items.find(i => i.id === product.id);
    if (ex) { ex.qty += qty; } else { this.items.push({ ...product, qty }); }
    this._save(); this._badge();
  }

  remove(id) { this.items = this.items.filter(i => i.id !== id); this._save(); this._badge(); }

  setQty(id, qty) {
    const item = this.items.find(i => i.id === id);
    if (item) { item.qty = Math.max(1, qty); this._save(); }
  }

  subtotal() { return this.items.reduce((s, i) => s + i.price * i.qty, 0); }
  total()    { return this.items.length ? this.subtotal() + DELIVERY_FEE : 0; }
  count()    { return this.items.reduce((c, i) => c + i.qty, 0); }

  clear() { this.items = []; this._save(); this._badge(); }

  _badge() {
    document.querySelectorAll('.cart-badge').forEach(b => {
      const n = this.count();
      b.textContent = n;
      b.style.display = n > 0 ? 'flex' : 'none';
    });
  }
}

const cart = new Cart();

// Intercept profile icon clicks
document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');

  if (token && userStr) {
    try {
      const user = JSON.parse(userStr);
      const targetHref = user.role === 'admin' ? 'admin.html' : 'profile.html';
      
      // Update all anchor tags pointing to auth.html to the correct dashboard
      document.querySelectorAll('a[href="auth.html"]').forEach(a => {
        a.href = targetHref;
      });
    } catch(err) {}
  }
});

export { cart, DELIVERY_FEE };
