// VideoUploader.jsx — Drag-and-drop video upload component with progress indication

import React, { useState, useRef } from 'react';
import { translateVideo } from '../services/translationService';
import { useAuth } from '../context/AuthContext';

function VideoUploader({ onResult }) {
    const [isDragging, setIsDragging]   = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [isLoading, setIsLoading]     = useState(false);
    const [error, setError]             = useState('');
    const fileInputRef                  = useRef(null);
    const { token }                     = useAuth();

    const handleFile = (file) => {
        const allowed = ['video/mp4', 'video/quicktime', 'video/avi', 'video/webm'];
        if (!allowed.includes(file.type)) {
            setError('Please upload an MP4, MOV, AVI, or WebM video file.');
            return;
        }
        if (file.size > 50 * 1024 * 1024) {
            setError('File is too large. Maximum size is 50MB.');
            return;
        }
        setError('');
        setSelectedFile(file);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
    };

    const handleTranslate = async () => {
        if (!selectedFile) return;
        setIsLoading(true);
        setError('');
        try {
            const result = await translateVideo(selectedFile, token);
            onResult(result);   // Pass result up to parent (DashboardPage)
        } catch (err) {
            setError(err.response?.data?.detail || 'Translation failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            {/* Drop zone */}
            <div
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current.click()}
                style={{
                    border: `3px dashed ${isDragging ? '#0D7377' : '#BBBBBB'}`,
                    borderRadius: '12px',
                    padding: '3rem',
                    textAlign: 'center',
                    cursor: 'pointer',
                    background: isDragging ? '#E0F4F4' : '#F8F8F8',
                    transition: 'all 0.2s ease'
                }}
            >
                <div style={{ fontSize: '3rem' }}>🎥</div>
                <p style={{ fontWeight: 'bold', color: '#1B3A6B', marginBottom: '0.5rem' }}>
                    {selectedFile ? selectedFile.name : 'Drop your ASL video here'}
                </p>
                <p style={{ color: '#888', fontSize: '0.9rem' }}>
                    {selectedFile
                        ? `${(selectedFile.size / 1024 / 1024).toFixed(1)} MB`
                        : 'MP4, MOV, AVI, or WebM — max 50MB'}
                </p>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    style={{ display: 'none' }}
                    onChange={(e) => e.target.files[0] && handleFile(e.target.files[0])}
                />
            </div>

            {error && (
                <p style={{ color: 'red', marginTop: '0.5rem', textAlign: 'center' }}>
                    {error}
                </p>
            )}

            <button
                onClick={handleTranslate}
                disabled={!selectedFile || isLoading}
                style={{
                    width: '100%', marginTop: '1rem', padding: '0.9rem',
                    background: selectedFile && !isLoading ? '#1B3A6B' : '#AAAAAA',
                    color: 'white', border: 'none', borderRadius: '8px',
                    fontSize: '1rem', cursor: selectedFile && !isLoading ? 'pointer' : 'not-allowed'
                }}
            >
                {isLoading ? '⏳ Processing video... this may take a moment' : '🔄 Translate Video'}
            </button>
        </div>
    );
}

export default VideoUploader;