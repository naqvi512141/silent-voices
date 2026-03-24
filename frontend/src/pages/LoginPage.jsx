import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, fetchProfile } from '../services/authService';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const navigate = useNavigate();
    const { login } = useAuth();  // Get the login function from global state

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        
        try {
            // Step 1: Get the JWT token
            const tokenData = await loginUser(email, password);
            
            // Step 2: Use the token to fetch the user's profile
            const userData = await fetchProfile(tokenData.access_token);
            
            // Step 3: Store both in global AuthContext
            login(tokenData.access_token, userData);
            
            // Step 4: Redirect to the dashboard
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '80px auto', padding: '2rem',
                      border: '1px solid #ddd', borderRadius: '8px' }}>
            <h2>Sign In to Silent Voices</h2>
            
            {error && (
                <p style={{ color: 'red', background: '#fff0f0', padding: '0.5rem',
                            borderRadius: '4px' }}>
                    {error}
                </p>
            )}
            
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Email</label>
                    <input type="email" value={email}
                        onChange={(e) => setEmail(e.target.value)} required
                        style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }} />
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label>Password</label>
                    <input type="password" value={password}
                        onChange={(e) => setPassword(e.target.value)} required
                        style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }} />
                </div>
                
                <button type="submit" disabled={loading}
                    style={{ width: '100%', padding: '0.75rem', background: '#1B3A6B',
                             color: 'white', border: 'none', borderRadius: '4px',
                             cursor: loading ? 'not-allowed' : 'pointer' }}>
                    {loading ? 'Signing in...' : 'Log In'}
                </button>
                
                <p style={{ textAlign: 'center', marginTop: '1rem' }}>
                    No account? <a href="/register">Register here</a>
                </p>
            </form>
        </div>
    );
}

export default LoginPage;