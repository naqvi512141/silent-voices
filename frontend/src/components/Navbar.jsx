// Navbar.jsx
// The persistent top navigation bar shown on all authenticated pages.
// Includes: logo, navigation links, dark mode toggle, and logout button.
// WCAG 2.1: uses <nav> landmark, aria-label, and keyboard-accessible controls.

import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

function Navbar() {
    const { user, logout } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navStyle = {
        background: 'var(--nav-bg)',
        color: 'var(--nav-text)',
        padding: '0 1.5rem',
        height: '60px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
    };

    const linkStyle = ({ isActive }) => ({
        color: isActive ? '#7EC8E3' : 'var(--nav-text)',
        textDecoration: 'none',
        fontWeight: isActive ? '700' : '500',
        fontSize: '0.95rem',
        padding: '0.3rem 0.6rem',
        borderRadius: '6px',
        transition: 'background 0.2s',
    });

    return (
        // role="navigation" and aria-label make this a recognizable landmark for screen readers
        <nav role="navigation" aria-label="Main navigation" style={navStyle}>
            {/* Logo / Brand */}
            <NavLink to="/dashboard" style={{ textDecoration: 'none' }}>
                <span style={{ color: 'white', fontWeight: '800', fontSize: '1.2rem',
                               letterSpacing: '0.5px' }}>
                    🤟 Silent Voices
                </span>
            </NavLink>

            {/* Navigation links */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <NavLink to="/dashboard" style={linkStyle}>Translate</NavLink>
                <NavLink to="/history"   style={linkStyle}>History</NavLink>
                <NavLink to="/vocabulary" style={linkStyle}>Vocabulary</NavLink>
                {user?.role === 'admin' && (
                    <NavLink to="/admin" style={linkStyle}>Admin</NavLink>
                )}
            </div>

            {/* Right side: theme toggle + user info + logout */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                {/* Dark mode toggle — aria-label explains the button's purpose */}
                <button
                    onClick={toggleTheme}
                    aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                    title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                    style={{
                        background: 'rgba(255,255,255,0.15)',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '0.4rem 0.7rem',
                        cursor: 'pointer',
                        fontSize: '1.1rem',
                        color: 'white',
                    }}
                >
                    {theme === 'light' ? '🌙' : '☀️'}
                </button>

                <span style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.7)' }}>
                    {user?.full_name}
                </span>

                <button onClick={handleLogout} className="btn"
                    style={{ background: 'rgba(255,255,255,0.15)', color: 'white',
                             border: '1px solid rgba(255,255,255,0.3)',
                             padding: '0.35rem 0.75rem', fontSize: '0.85rem' }}>
                    Log Out
                </button>
            </div>
        </nav>
    );
}

export default Navbar;