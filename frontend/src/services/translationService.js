// translationService.js — API calls for the translation feature

import axios from 'axios';
const API_URL = 'http://localhost:8000';

export async function translateVideo(videoFile, token) {
    // For file uploads, we use FormData instead of JSON.
    // FormData is the correct way to send files over HTTP.
    const formData = new FormData();
    formData.append('file', videoFile);
    
    const response = await axios.post(`${API_URL}/translate/upload`, formData, {
        headers: {
            Authorization: `Bearer ${token}`,
            // Do NOT set Content-Type manually for FormData —
            // axios sets it automatically with the correct boundary parameter
        },
        // onUploadProgress lets us track upload progress (future enhancement)
        timeout: 300000  // 5 minute timeout — large videos take time to process
    });
    return response.data;
}