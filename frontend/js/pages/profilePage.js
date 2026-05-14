// js/pages/profilePage.js — User profile + change password

import { apiGetProfile, apiUpdateProfile, apiChangePassword } from '../api.js';
import { escapeHtml, setLoading } from '../utils.js';
import { showToast } from '../toast.js';

export async function renderProfilePage(container) {
  container.innerHTML = `<div class="page-header"><h1>My Profile</h1></div><div style="max-width:600px;"><div style="text-align:center;padding:3rem;"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--cyan);"></i></div></div>`;

  try {
    const res = await apiGetProfile();
    const u = res.data || res;

    container.innerHTML = `
      <div class="page-header"><h1>My Profile</h1><p>${escapeHtml(u.email)}</p></div>
      <div style="max-width:600px;">
        <div class="form-section">
          <h3><i class="fas fa-user"></i> Personal Information</h3>
          <form id="profile-form">
            <div class="form-row">
              <div class="form-group"><label class="form-label">First Name</label><input class="form-control" id="pf-first" value="${escapeHtml(u.first_name||'')}"></div>
              <div class="form-group"><label class="form-label">Last Name</label><input class="form-control" id="pf-last" value="${escapeHtml(u.last_name||'')}"></div>
            </div>
            <div class="form-group"><label class="form-label">Phone</label><input class="form-control" id="pf-phone" value="${escapeHtml(u.phone||'')}"></div>
            <div class="form-group"><label class="form-label">Address</label><input class="form-control" id="pf-address" value="${escapeHtml(u.address||'')}"></div>
            <div class="form-row">
              <div class="form-group"><label class="form-label">City</label><input class="form-control" id="pf-city" value="${escapeHtml(u.city||'')}"></div>
              <div class="form-group"><label class="form-label">State</label><input class="form-control" id="pf-state" value="${escapeHtml(u.state||'')}"></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label class="form-label">ZIP Code</label><input class="form-control" id="pf-zip" value="${escapeHtml(u.zip_code||'')}"></div>
              <div class="form-group"><label class="form-label">Country</label><input class="form-control" id="pf-country" value="${escapeHtml(u.country||'')}"></div>
            </div>
            <button type="submit" class="btn btn-primary" id="save-profile-btn"><i class="fas fa-save"></i> Save Changes</button>
          </form>
        </div>

        <div class="form-section" style="margin-top:1.5rem;">
          <h3><i class="fas fa-lock"></i> Change Password</h3>
          <form id="password-form">
            <div class="form-group"><label class="form-label">Current Password</label><input type="password" class="form-control" id="pw-current"></div>
            <div class="form-row">
              <div class="form-group"><label class="form-label">New Password</label><input type="password" class="form-control" id="pw-new"></div>
              <div class="form-group"><label class="form-label">Confirm New</label><input type="password" class="form-control" id="pw-confirm"></div>
            </div>
            <div id="pw-error" class="form-error" style="display:none;"></div>
            <button type="submit" class="btn btn-outline" id="change-pw-btn"><i class="fas fa-key"></i> Change Password</button>
          </form>
        </div>
      </div>`;

    // Save profile
    document.getElementById('profile-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('save-profile-btn');
      setLoading(btn, true, 'Saving…');
      try {
        await apiUpdateProfile({
          first_name: document.getElementById('pf-first').value.trim(),
          last_name: document.getElementById('pf-last').value.trim(),
          phone: document.getElementById('pf-phone').value.trim() || undefined,
          address: document.getElementById('pf-address').value.trim() || undefined,
          city: document.getElementById('pf-city').value.trim() || undefined,
          state: document.getElementById('pf-state').value.trim() || undefined,
          zip_code: document.getElementById('pf-zip').value.trim() || undefined,
          country: document.getElementById('pf-country').value.trim() || undefined,
        });
        showToast('Profile updated!', 'success');
      } catch (err) { showToast(err.message, 'error'); }
      setLoading(btn, false);
    });

    // Change password
    document.getElementById('password-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const errEl = document.getElementById('pw-error');
      const cur = document.getElementById('pw-current').value;
      const nw = document.getElementById('pw-new').value;
      const conf = document.getElementById('pw-confirm').value;
      if (!cur || !nw || !conf) { errEl.textContent = 'Fill in all fields'; errEl.style.display = 'block'; return; }
      if (nw !== conf) { errEl.textContent = 'Passwords do not match'; errEl.style.display = 'block'; return; }
      if (nw.length < 8) { errEl.textContent = 'Password must be at least 8 characters'; errEl.style.display = 'block'; return; }

      const btn = document.getElementById('change-pw-btn');
      setLoading(btn, true, 'Changing…');
      errEl.style.display = 'none';
      try {
        await apiChangePassword(cur, nw, conf);
        showToast('Password changed!', 'success');
        document.getElementById('pw-current').value = '';
        document.getElementById('pw-new').value = '';
        document.getElementById('pw-confirm').value = '';
      } catch (err) { errEl.textContent = err.message; errEl.style.display = 'block'; }
      setLoading(btn, false);
    });
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><h2>Failed to load profile</h2><p>${escapeHtml(err.message)}</p></div>`;
  }
}
