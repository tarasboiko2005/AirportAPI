import api from './axios';

export const authService = {
    login: (username, password) =>
        api.post('/api/auth/login/', { username, password }),

    register: (username, email, password) =>
        api.post('/api/auth/register/', { username, email, password }),

    refreshToken: (refresh) =>
        api.post('/api/token/refresh/', { refresh }),

    saveTokens: (access, refresh) => {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },

    clearTokens: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
    },

    isAuthenticated: () => !!localStorage.getItem('access_token'),

    getUsername: () => localStorage.getItem('username'),

    saveUsername: (username) => localStorage.setItem('username', username),
};
