import api from './axios';

export const paymentService = {
    getPayments: (params) => api.get('/payments/payments/', { params }),
    createCheckoutSession: (orderId) =>
        api.post('/payments/checkout-session/', { order_id: String(orderId) }),
};
