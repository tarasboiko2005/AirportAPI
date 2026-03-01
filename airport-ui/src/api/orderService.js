import api from './axios';

export const orderService = {
    getOrders: (params) => api.get('/api/orders/', { params }),
    getOrder: (id) => api.get(`/api/orders/${id}/`),
    createOrder: (data) => api.post('/api/orders/', data),
};
