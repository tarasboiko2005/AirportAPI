import api from './axios';

export const ticketService = {
    getTickets: (params) => api.get('/api/tickets/', { params }),
    getTicket: (id) => api.get(`/api/tickets/${id}/`),
};
