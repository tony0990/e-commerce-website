/**
 * E-Commerce Frontend API Wrapper
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

class API {
    constructor() {
        this.token = localStorage.getItem('token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, { ...options, headers });
            const data = await response.json();

            if (!response.ok) {
                // Handle token expiration
                if (response.status === 401 && this.refreshToken) {
                    const refreshed = await this.refreshTokens();
                    if (refreshed) {
                        return this.request(endpoint, options);
                    }
                }
                throw new Error(data.detail || 'An error occurred');
            }

            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    async refreshTokens() {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: this.refreshToken }),
            });
            const data = await response.json();

            if (response.ok) {
                this.token = data.data.access_token;
                this.refreshToken = data.data.refresh_token;
                localStorage.setItem('token', this.token);
                localStorage.setItem('refresh_token', this.refreshToken);
                return true;
            }
        } catch (error) {
            localStorage.clear();
            window.location.href = 'auth.html';
        }
        return false;
    }

    // --- Auth Endpoints ---

    async login(email, password) {
        const result = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        this.token = result.data.access_token;
        this.refreshToken = result.data.refresh_token;
        localStorage.setItem('token', this.token);
        localStorage.setItem('refresh_token', this.refreshToken);
        return result;
    }

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    }

    async getMe() {
        return this.request('/auth/me');
    }

    logout() {
        localStorage.clear();
        this.token = null;
        this.refreshToken = null;
        window.location.href = 'index.html';
    }

    // --- User Endpoints ---

    async getProfile() {
        return this.request('/users/me/profile');
    }

    async updateProfile(profileData) {
        return this.request('/users/me/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData),
        });
    }

    // --- Admin Endpoints ---
    
    async getAllUsers() {
        return this.request('/users');
    }
}

const api = new API();
export default api;
