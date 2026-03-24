// RegisterPage.jsx — The user registration form

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../services/authService';

function RegisterPage() {
    // Form state — each field has its own piece of state
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    // UI state — for showing errors and loading indicator
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    // useNavigate lets us redirect the user to another page programmatically
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        // e.preventDefault() stops the browser from refreshing the page
        // (default form behaviour) — in React, we handle form submission ourselves
        e.preventDefault();
        
        setError('');     // Clear any previous error
        setLoading(true); // Show a loading state on the button
        
        try {
            await registerUser(fullName, email, password);
            // If registration succeeds, redirect to the login page
            navigate('/login');
        } catch (err) {
            // The backend sends error details in err.response.data.detail
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false); // Always remove loading state, whether success or failure
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '80px auto', padding: '2rem', 
                      border: '1px solid #ddd', borderRadius: '8px' }}>
            <h2>Create Account</h2>
            
            {/* Only show the error message if there is one */}
            {error && (
                <p style={{ color: 'red', background: '#fff0f0', padding: '0.5rem', 
                            borderRadius: '4px' }}>
                    {error}
                </p>
            )}
            
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Full Name</label>
                    <input
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        required
                        style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
                    />
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
                    />
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
                    />
                </div>
                
                <button 
                    type="submit" 
                    disabled={loading}
                    style={{ width: '100%', padding: '0.75rem', background: '#1B3A6B', 
                             color: 'white', border: 'none', borderRadius: '4px', 
                             cursor: loading ? 'not-allowed' : 'pointer' }}
                >
                    {loading ? 'Creating account...' : 'Register'}
                </button>
                
                <p style={{ textAlign: 'center', marginTop: '1rem' }}>
                    Already have an account? <a href="/login">Log in</a>
                </p>
            </form>
        </div>
    );
}

export default RegisterPage;