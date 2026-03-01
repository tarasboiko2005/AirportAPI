import api from './axios';

export const airportService = {
  getAirports: (params) => api.get('/api/airports-generic/', { params }),
  getAirport: (id) => api.get(`/api/airports-generic/${id}/`),
  getCountries: (params) => api.get('/api/countries-generic/', { params }),
  getAirlines: (params) => api.get('/api/airlines/', { params }),
  getAirline: (id) => api.get(`/api/airlines/${id}/`),
  getAirplanes: (params) => api.get('/api/airplanes/', { params }),
};