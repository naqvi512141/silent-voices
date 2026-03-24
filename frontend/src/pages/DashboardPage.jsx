import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function DashboardPage() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div style={{ padding: '2rem' }}>
            <h1>Welcome to Silent Voices</h1>
            {user && <p>Logged in as: <strong>{user.full_name}</strong> ({user.role})</p>}
            <p>Video translation features coming in Sprint 2.</p>
            <button onClick={handleLogout}
                style={{ padding: '0.5rem 1rem', background: '#cc0000',
                         color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                Log Out
            </button>
        </div>
    );
}

export default DashboardPage;