import api from './axios';

export const flightService = {
    getFlights: (params) => api.get('/api/flights/', { params }),
    getFlight: (id) => api.get(`/api/flights/${id}/`),
};
