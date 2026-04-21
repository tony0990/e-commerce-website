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
                
                // Extract detailed error message if available
                let errorMessage = 'An error occurred';
                if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        errorMessage = data.detail.map(err => `${err.loc[err.loc.length - 1]}: ${err.msg}`).join(', ');
                    } else {
                        errorMessage = data.detail;
                    }
                } else if (data.message) {
                    errorMessage = data.message;
                }
                
                throw new Error(errorMessage);
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
                this.token = data.tokens.access_token;
                this.refreshToken = data.tokens.refresh_token;
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
        this.token = result.tokens.access_token;
        this.refreshToken = result.tokens.refresh_token;
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

    // --- Product Endpoints ---

    async getProducts(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/products/?${query}`);
    }

    async getCategories() {
        return this.request('/products/categories');
    }

    // --- Order Endpoints ---

    async createOrder(orderData) {
        return this.request('/orders/', {
            method: 'POST',
            body: JSON.stringify(orderData),
        });
    }

    async getMyOrders() {
        return this.request('/orders/me');
    }

    async getAllOrders() {
        return this.request('/orders/');
    }

    async getAdminStats() {
        return this.request('/orders/admin/stats');
    }

    // --- Wishlist Endpoints ---

    async getWishlist() {
        return this.request('/wishlist/');
    }

    async addToWishlist(productId) {
        return this.request('/wishlist/', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId }),
        });
    }

    async removeFromWishlist(productId) {
        return this.request(`/wishlist/${productId}`, {
            method: 'DELETE',
        });
    }
}

const api = new API();
export default api;
