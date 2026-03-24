// App.jsx — The root component that defines routing and wraps everything in context

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';

// ProtectedRoute is a guard — if the user is not logged in,
// redirect them to /login instead of showing the protected page
function ProtectedRoute({ children }) {
    const { token } = useAuth();
    return token ? children : <Navigate to="/login" />;
}

function AppRoutes() {
    return (
        <Routes>
            {/* Public routes — anyone can access */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* Protected routes — only logged-in users can access */}
            <Route path="/dashboard" element={
                <ProtectedRoute>
                    <DashboardPage />
                </ProtectedRoute>
            } />
            
            {/* Default redirect — going to "/" sends you to /login */}
            <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
    );
}

function App() {
    return (
        // BrowserRouter enables URL-based navigation
        // AuthProvider makes auth state available to all child components
        <BrowserRouter>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;