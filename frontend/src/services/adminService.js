import axios from 'axios';
const API_URL = 'http://localhost:8000';

const authHeaders = (token) => ({ Authorization: `Bearer ${token}` });

export const getStats = (token) =>
    axios.get(`${API_URL}/admin/stats`, { headers: authHeaders(token) })
         .then(r => r.data);

export const getUsers = (token) =>
    axios.get(`${API_URL}/admin/users`, { headers: authHeaders(token) })
         .then(r => r.data);

export const deactivateUser = (userId, token) =>
    axios.patch(`${API_URL}/admin/users/${userId}/deactivate`,
                {}, { headers: authHeaders(token) }).then(r => r.data);

export const activateUser = (userId, token) =>
    axios.patch(`${API_URL}/admin/users/${userId}/activate`,
                {}, { headers: authHeaders(token) }).then(r => r.data);

export const deleteUser = (userId, token) =>
    axios.delete(`${API_URL}/admin/users/${userId}`,
                 { headers: authHeaders(token) }).then(r => r.data);