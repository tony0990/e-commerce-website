// js/session.js — JWT session management (access + refresh tokens)

const ACCESS_KEY  = 'ps_access_token';
const REFRESH_KEY = 'ps_refresh_token';
const USER_KEY    = 'ps_user';

// ── Token Storage ───────────────────────────────────────────────
export function saveTokens(accessToken, refreshToken) {
  localStorage.setItem(ACCESS_KEY, accessToken);
  if (refreshToken) localStorage.setItem(REFRESH_KEY, refreshToken);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function removeTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(USER_KEY);
}

// ── User Cache ──────────────────────────────────────────────────
export function saveUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function getCachedUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch { return null; }
}

// ── JWT Parsing ─────────────────────────────────────────────────
function parseJwtPayload(token) {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const json = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(json);
  } catch { return null; }
}

// ── Auth State ──────────────────────────────────────────────────
export function isLoggedIn() {
  const token = getAccessToken();
  if (!token) return false;
  const payload = parseJwtPayload(token);
  if (!payload || !payload.exp) return false;
  return Date.now() / 1000 < payload.exp;
}

export function getCurrentUser() {
  const token = getAccessToken();
  if (!token) return null;
  const payload = parseJwtPayload(token);
  if (!payload) return null;
  return {
    id:    parseInt(payload.sub),
    email: payload.email,
    role:  payload.role || 'user',
  };
}

export function getUserRole() {
  const user = getCurrentUser();
  return user ? user.role : null;
}
