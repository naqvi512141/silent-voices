// AuthContext.jsx — Global state for authentication
// Any component in the app can "subscribe" to this context and read/update
// the current user's login state

import React, { createContext, useContext, useState } from 'react';

// Create the context object
const AuthContext = createContext(null);

// AuthProvider is a wrapper component that provides the context value
// to all components inside it. It goes in App.jsx wrapping everything.
export function AuthProvider({ children }) {
    // 'token' is the JWT we receive after login
    // useState(null) means it starts as null (no one is logged in)
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);

    const login = (newToken, userData) => {
        // Save the token to localStorage so it persists when the page is refreshed
        localStorage.setItem('token', newToken);
        setToken(newToken);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    // The value object is what all child components can access
    return (
        <AuthContext.Provider value={{ token, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook — a shortcut so any component can write:
// const { token, login, logout } = useAuth();
// instead of the more verbose React.useContext(AuthContext)
export function useAuth() {
    return useContext(AuthContext);
}