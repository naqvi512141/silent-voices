import axios from 'axios';
const API_URL = 'http://localhost:8000';

const authHeaders = (token) => ({ Authorization: `Bearer ${token}` });

export const getHistory = (token) =>
    axios.get(`${API_URL}/history/`, { headers: authHeaders(token) })
         .then(r => r.data);

export const getSessionDetail = (id, token) =>
    axios.get(`${API_URL}/history/${id}`, { headers: authHeaders(token) })
         .then(r => r.data);

// Export functions return Blob objects so the browser can create download links
export const exportTxt = (id, token) =>
    axios.get(`${API_URL}/history/${id}/export/txt`,
              { headers: authHeaders(token), responseType: 'blob' })
         .then(r => r.data);

export const exportPdf = (id, token) =>
    axios.get(`${API_URL}/history/${id}/export/pdf`,
              { headers: authHeaders(token), responseType: 'blob' })
         .then(r => r.data);

export const submitFeedback = (sessionId, rating, correction, token) =>
    axios.post(`${API_URL}/feedback/${sessionId}`,
               { rating, correction },
               { headers: authHeaders(token) })
         .then(r => r.data);