// js/pages/registerPage.js — Registration form

import { apiRegister } from '../api.js';
import { showToast } from '../toast.js';
import { setLoading } from '../utils.js';
import { renderNavbar } from '../navbar.js';
import { saveUser } from '../session.js';
import { cart } from '../cart.js';

export function renderRegisterPage(container) {
  container.innerHTML = `
    <div class="page-header" style="text-align:center;padding:4rem 0 2rem;">
      <h1>Create Account</h1>
      <p>Join PremiumStore for the best shopping experience</p>
    </div>

    <div style="max-width:520px;margin:0 auto;">
      <div class="form-section">
        <form id="register-form" novalidate>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input type="text" class="form-control" id="reg-first-name" placeholder="Ahmed" required />
            </div>
            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input type="text" class="form-control" id="reg-last-name" placeholder="Mohamed" required />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Email Address *</label>
            <input type="email" class="form-control" id="reg-email" placeholder="you@example.com" required autocomplete="email" />
          </div>
          <div class="form-group">
            <label class="form-label">Phone (optional)</label>
            <input type="tel" class="form-control" id="reg-phone" placeholder="+20 1xx xxx xxxx" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Password *</label>
              <input type="password" class="form-control" id="reg-password" placeholder="Min 8 characters" required />
            </div>
            <div class="form-group">
              <label class="form-label">Confirm Password *</label>
              <input type="password" class="form-control" id="reg-confirm" placeholder="Repeat password" required />
            </div>
          </div>
          <div id="register-error" class="form-error" style="display:none;"></div>
          <button type="submit" class="btn btn-primary" id="register-submit-btn" style="width:100%;justify-content:center;margin-top:.5rem;">
            <i class="fas fa-user-plus"></i> Create Account
          </button>
        </form>

        <p style="text-align:center;margin-top:1.5rem;font-size:.88rem;color:var(--text-mute);">
          Already have an account?
          <a href="#/login" style="color:var(--cyan);font-weight:600;">Sign in</a>
        </p>
      </div>
    </div>`;

  const form      = document.getElementById('register-form');
  const errorEl   = document.getElementById('register-error');
  const submitBtn = document.getElementById('register-submit-btn');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const firstName = document.getElementById('reg-first-name').value.trim();
    const lastName  = document.getElementById('reg-last-name').value.trim();
    const email     = document.getElementById('reg-email').value.trim();
    const phone     = document.getElementById('reg-phone').value.trim();
    const password  = document.getElementById('reg-password').value;
    const confirm   = document.getElementById('reg-confirm').value;

    // Validation
    if (!firstName || !lastName || !email || !password || !confirm) {
      showError(errorEl, 'Please fill in all required fields.');
      return;
    }
    if (password.length < 8) {
      showError(errorEl, 'Password must be at least 8 characters.');
      return;
    }
    if (password !== confirm) {
      showError(errorEl, 'Passwords do not match.');
      return;
    }

    setLoading(submitBtn, true, 'Creating account…');
    errorEl.style.display = 'none';

    try {
      const result = await apiRegister({
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        confirm_password: confirm,
        phone: phone || undefined,
      });

      if (result.data?.user) saveUser(result.data.user);
      await cart.syncOnLogin();

      renderNavbar();
      showToast('Account created successfully! 🎉', 'success');
      window.location.hash = '#/';
    } catch (err) {
      showError(errorEl, err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(submitBtn, false);
    }
  });
}

function showError(el, msg) {
  el.textContent = msg;
  el.style.display = 'block';
}
