import { createContext, useContext, useState, useCallback } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('mm_user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const [token, setToken] = useState(() => localStorage.getItem('mm_token') || null);

  const persist = useCallback((tokenVal, userVal) => {
    setToken(tokenVal);
    setUser(userVal);
    localStorage.setItem('mm_token', tokenVal);
    localStorage.setItem('mm_user', JSON.stringify(userVal));
    axios.defaults.headers.common['Authorization'] = `Bearer ${tokenVal}`;
  }, []);

  const register = useCallback(async (username, email, password) => {
    const res = await axios.post(`${API_BASE}/register`, { username, email, password });
    persist(res.data.access_token, res.data.user);
    return res.data;
  }, [persist]);

  const login = useCallback(async (email, password) => {
    const res = await axios.post(`${API_BASE}/login`, { email, password });
    persist(res.data.access_token, res.data.user);
    return res.data;
  }, [persist]);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('mm_token');
    localStorage.removeItem('mm_user');
    delete axios.defaults.headers.common['Authorization'];
  }, []);

  // Set axios header on initial load if token exists
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
