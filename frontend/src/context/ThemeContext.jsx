// ThemeContext.jsx
// Manages the global light/dark theme toggle.
// The selected theme is persisted in localStorage so it survives page refreshes.
// All components read the theme via the useTheme() hook.
// Theme switching works by setting a data-theme attribute on the <html> element,
// which activates the corresponding CSS variable set defined in index.css.

import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
    // Read saved preference from localStorage, defaulting to 'light'
    const [theme, setTheme] = useState(
        () => localStorage.getItem('sv-theme') || 'light'
    );

    useEffect(() => {
        // Apply the theme by setting a data attribute on the root HTML element.
        // CSS variables in index.css respond to [data-theme="dark"].
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('sv-theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    return useContext(ThemeContext);
}