// js/pages/loginPage.js — Login form

import { apiLogin } from '../api.js';
import { showToast } from '../toast.js';
import { setLoading } from '../utils.js';
import { renderNavbar } from '../navbar.js';
import { saveUser } from '../session.js';
import { cart } from '../cart.js';

export function renderLoginPage(container) {
  container.innerHTML = `
    <div class="page-header" style="text-align:center;padding:4rem 0 2rem;">
      <h1>Welcome Back</h1>
      <p>Sign in to your account to continue shopping</p>
    </div>

    <div style="max-width:440px;margin:0 auto;">
      <div class="form-section">
        <form id="login-form" novalidate>
          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input type="email" class="form-control" id="login-email"
                   placeholder="you@example.com" required autocomplete="email" />
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <div style="position:relative;">
              <input type="password" class="form-control" id="login-password"
                     placeholder="••••••••" required autocomplete="current-password" />
              <button type="button" id="toggle-pw" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--slate-mute);cursor:pointer;font-size:.9rem;">
                <i class="fas fa-eye" id="toggle-pw-icon"></i>
              </button>
            </div>
          </div>
          <div id="login-error" class="form-error" style="display:none;"></div>
          <button type="submit" class="btn btn-primary" id="login-submit-btn" style="width:100%;justify-content:center;margin-top:.5rem;">
            <i class="fas fa-sign-in-alt"></i> Sign In
          </button>
        </form>

        <p style="text-align:center;margin-top:1.5rem;font-size:.88rem;color:var(--text-mute);">
          Don't have an account?
          <a href="#/register" style="color:var(--cyan);font-weight:600;">Create one</a>
        </p>
      </div>
    </div>`;

  // Toggle password visibility
  const toggleBtn  = document.getElementById('toggle-pw');
  const pwInput    = document.getElementById('login-password');
  const toggleIcon = document.getElementById('toggle-pw-icon');

  toggleBtn?.addEventListener('click', () => {
    const shown = pwInput.type === 'text';
    pwInput.type = shown ? 'password' : 'text';
    toggleIcon.className = shown ? 'fas fa-eye' : 'fas fa-eye-slash';
  });

  // Form submit
  const form      = document.getElementById('login-form');
  const errorEl   = document.getElementById('login-error');
  const submitBtn = document.getElementById('login-submit-btn');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email    = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
      showError(errorEl, 'Please enter your email and password.');
      return;
    }

    setLoading(submitBtn, true, 'Signing in…');
    errorEl.style.display = 'none';

    try {
      const result = await apiLogin(email, password);

      // Cache user data
      if (result.data?.user) saveUser(result.data.user);

      // Sync cart on login
      await cart.syncOnLogin();

      renderNavbar();
      showToast('Welcome back! 👋', 'success');
      window.location.hash = '#/';
    } catch (err) {
      showError(errorEl, err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(submitBtn, false);
    }
  });
}

function showError(el, msg) {
  el.textContent = msg;
  el.style.display = 'block';
}
