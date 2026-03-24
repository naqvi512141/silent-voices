// authService.js — All functions that call the backend auth endpoints
// This file is the only place that knows the backend URL
// All components call these functions; none of them do fetch/axios directly

import axios from 'axios';

// The base URL of your backend — centralised here so changing it is one edit
const API_URL = 'http://localhost:8000';

export async function registerUser(fullName, email, password) {
    // axios.post sends a POST request with JSON body
    // If the response status is 4xx or 5xx, axios throws an error automatically
    const response = await axios.post(`${API_URL}/auth/register`, {
        full_name: fullName,
        email: email,
        password: password
    });
    return response.data;  // Returns the user object from the backend
}

export async function loginUser(email, password) {
    const response = await axios.post(`${API_URL}/auth/login`, {
        email: email,
        password: password
    });
    return response.data;  // Returns { access_token: "...", token_type: "bearer" }
}

export async function fetchProfile(token) {
    // The Authorization header is how we send the JWT token to protected endpoints
    const response = await axios.get(`${API_URL}/auth/profile`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
}