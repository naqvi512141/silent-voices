// App.jsx — Final Sprint 3 version with all routes and guards.

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import LoginPage      from './pages/LoginPage';
import RegisterPage   from './pages/RegisterPage';
import DashboardPage  from './pages/DashboardPage';
import HistoryPage    from './pages/HistoryPage';
import VocabGuidePage from './pages/VocabGuidePage';
import AdminPage      from './pages/AdminPage';

// Redirects to /login if the user has no valid token
function ProtectedRoute({ children }) {
    const { token } = useAuth();
    return token ? children : <Navigate to="/login" replace />;
}

// Redirects to /dashboard if the user is not an admin
// The role is read from the user object stored in AuthContext
function AdminRoute({ children }) {
    const { token, user } = useAuth();
    if (!token)               return <Navigate to="/login" replace />;
    if (user?.role !== 'admin') return <Navigate to="/dashboard" replace />;
    return children;
}

function AppRoutes() {
    return (
        <Routes>
            {/* Public routes */}
            <Route path="/login"    element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Authenticated routes */}
            <Route path="/dashboard" element={
                <ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/history"   element={
                <ProtectedRoute><HistoryPage /></ProtectedRoute>} />
            <Route path="/vocabulary" element={
                <ProtectedRoute><VocabGuidePage /></ProtectedRoute>} />

            {/* Admin-only route */}
            <Route path="/admin" element={
                <AdminRoute><AdminPage /></AdminRoute>} />

            {/* Default */}
            <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
    );
}

function App() {
    return (
        <BrowserRouter>
            {/* ThemeProvider wraps everything so any component can read/toggle theme */}
            <ThemeProvider>
                <AuthProvider>
                    <AppRoutes />
                </AuthProvider>
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;