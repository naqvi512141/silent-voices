// AdminPage.jsx
// Admin dashboard with user management table and analytics summary.
// Only accessible to users with role='admin' via AdminRoute guard in App.jsx.

import React, { useState, useEffect, useCallback } from 'react'; 
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { 
    getStats, 
    getUsers, 
    deactivateUser, 
    activateUser, 
    deleteUser 
} from '../services/adminService';

function StatCard({ label, value, icon, color }) {
    return (
        <div className="card" style={{ textAlign: 'center', flex: '1', minWidth: '140px' }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.25rem' }}>{icon}</div>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color }}>
                {value}
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                {label}
            </div>
        </div>
    );
}

function AdminPage() {
    const { token } = useAuth();
    const [stats, setStats]     = useState(null);
    const [users, setUsers]     = useState([]);
    const [tab, setTab]         = useState('stats');   // 'stats' or 'users'
    const [loading, setLoading] = useState(true);
    const [msg, setMsg]         = useState('');

    /**
     * loadData is wrapped in useCallback to ensure the function identity 
     * remains stable between renders unless the token changes.
     */
    const loadData = useCallback(async () => {
        setLoading(true);
        try {
            const [s, u] = await Promise.all([getStats(token), getUsers(token)]);
            setStats(s);
            setUsers(u);
        } catch (e) { 
            console.error("Failed to load admin data:", e); 
        }
        setLoading(false);
    }, [token]);

    // Triggers initial data load on component mount
    useEffect(() => { 
        loadData(); 
    }, [loadData]);

    const showMsg = (text) => { 
        setMsg(text); 
        setTimeout(() => setMsg(''), 3000); 
    };

    const handleDeactivate = async (userId) => {
        if (!window.confirm('Deactivate this user?')) return;
        await deactivateUser(userId, token);
        showMsg('User deactivated.');
        loadData();
    };

    const handleActivate = async (userId) => {
        await activateUser(userId, token);
        showMsg('User reactivated.');
        loadData();
    };

    const handleDelete = async (userId) => {
        if (!window.confirm('Permanently delete this user and all their data? This cannot be undone.')) return;
        await deleteUser(userId, token);
        showMsg('User deleted.');
        loadData();
    };

    const tabStyle = (t) => ({
        padding: '0.5rem 1.2rem',
        border: 'none',
        background: tab === t ? 'var(--accent-navy)' : 'var(--bg-secondary)',
        color: tab === t ? 'white' : 'var(--text-secondary)',
        borderRadius: '8px',
        cursor: 'pointer',
        fontWeight: tab === t ? '700' : '500',
    });

    return (
        <>
            <Navbar />
            <a href="#main-content" className="skip-link">Skip to content</a>

            <main id="main-content" style={{ maxWidth: '1000px', margin: '2rem auto', padding: '0 1rem' }}>
                <h1 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                    Admin Dashboard
                </h1>
                
                {msg && (
                    <div className="badge badge-green"
                         style={{ marginBottom: '1rem', padding: '0.5rem 1rem', borderRadius: '8px', display: 'block' }}>
                        ✓ {msg}
                    </div>
                )}

                {/* Tab navigation */}
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }} role="tablist">
                    <button style={tabStyle('stats')} onClick={() => setTab('stats')}
                            role="tab" aria-selected={tab === 'stats'}>
                        📊 Analytics
                    </button>
                    <button style={tabStyle('users')} onClick={() => setTab('users')}
                            role="tab" aria-selected={tab === 'users'}>
                        👥 Users ({users.length})
                    </button>
                </div>

                {loading && <p style={{ color: 'var(--text-muted)' }}>Loading...</p>}

                {/* Analytics Tab */}
                {!loading && tab === 'stats' && stats && (
                    <div>
                        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '2rem' }}>
                            <StatCard label="Total Users" value={stats.total_users}
                                      icon="👤" color="var(--accent-navy)" />
                            <StatCard label="Total Sessions" value={stats.total_sessions}
                                      icon="🎬" color="var(--accent-teal)" />
                            <StatCard label="Avg. Confidence" value={`${stats.avg_confidence}%`}
                                      icon="🎯" color="var(--success)" />
                            <StatCard label="Sessions (7 days)" value={stats.sessions_last_7days}
                                      icon="📅" color="var(--accent-navy)" />
                        </div>

                        <div className="card">
                            <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
                                System Information
                            </h3>
                            <p style={{ color: 'var(--text-secondary)' }}>
                                <strong>Model:</strong> Random Forest Classifier (gesture_model.pkl) &nbsp;·&nbsp;
                                <strong>Pipeline:</strong> OpenCV + MediaPipe Hands + Scikit-learn &nbsp;·&nbsp;
                                <strong>Version:</strong> Sprint 3 Release
                            </p>
                        </div>
                    </div>
                )}

                {/* Users Tab */}
                {!loading && tab === 'users' && (
                    <div style={{ overflowX: 'auto' }}>
                        <table style={{ 
                            width: '100%', 
                            borderCollapse: 'collapse',
                            background: 'var(--bg-card)',
                            borderRadius: '12px', 
                            overflow: 'hidden',
                            boxShadow: 'var(--shadow)' 
                        }} aria-label="User management table">
                            <thead>
                                <tr style={{ background: 'var(--accent-navy)', color: 'white' }}>
                                    {['ID','Name','Email','Role','Status','Joined','Actions'].map(h => (
                                        <th key={h} scope="col"
                                            style={{ padding: '0.75rem 1rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '700' }}>
                                            {h}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((u, i) => (
                                    <tr key={u.id}
                                        style={{ 
                                            background: i % 2 === 0 ? 'var(--bg-card)' : 'var(--bg-secondary)',
                                            borderBottom: '1px solid var(--border-color)' 
                                        }}>
                                        <td style={{ padding: '0.65rem 1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                            {u.id}
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem', color: 'var(--text-primary)', fontWeight: '600' }}>
                                            {u.full_name}
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                                            {u.email}
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem' }}>
                                            <span className={`badge ${u.role === 'admin' ? 'badge-teal' : 'badge-navy'}`}>
                                                {u.role}
                                            </span>
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem' }}>
                                            <span className={`badge ${u.is_active ? 'badge-green' : 'badge-red'}`}>
                                                {u.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                                            {new Date(u.created_at).toLocaleDateString()}
                                        </td>
                                        <td style={{ padding: '0.65rem 1rem' }}>
                                            <div style={{ display: 'flex', gap: '0.4rem' }}>
                                                {u.is_active ? (
                                                    <button className="btn btn-ghost"
                                                            onClick={() => handleDeactivate(u.id)}
                                                            style={{ fontSize:'0.78rem', padding:'0.3rem 0.6rem' }}
                                                            aria-label={`Deactivate ${u.full_name}`}>
                                                        Deactivate
                                                    </button>
                                                ) : (
                                                    <button className="btn btn-teal"
                                                            onClick={() => handleActivate(u.id)}
                                                            style={{ fontSize:'0.78rem', padding:'0.3rem 0.6rem' }}
                                                            aria-label={`Reactivate ${u.full_name}`}>
                                                        Activate
                                                    </button>
                                                )}
                                                <button className="btn btn-danger"
                                                        onClick={() => handleDelete(u.id)}
                                                        style={{ fontSize:'0.78rem', padding:'0.3rem 0.6rem' }}
                                                        aria-label={`Delete ${u.full_name}`}>
                                                    Delete
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>
        </>
    );
}

export default AdminPage;