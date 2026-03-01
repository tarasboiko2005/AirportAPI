import api from './axios';

export const userService = {
    getProfile: () => api.get('/api/me/'),
};
