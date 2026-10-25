import { request } from './client.js';

export const register = (payload) => request('/auth/register', { method: 'POST', body: payload, auth: false });
export const login = (email, password) => request('/auth/login', { method: 'POST', body: { email, password }, auth: false });
export const loginWithGoogle = (credential) => request('/auth/google', { method: 'POST', body: { credential }, auth: false });
export const logout = () => request('/auth/logout', { method: 'POST' });
export const getMe = () => request('/auth/me');
export const getAuthConfig = () => request('/auth/config', { auth: false });

export const updateProfile = (changes) => request('/profile', { method: 'PATCH', body: changes });
export const changePassword = (payload) => request('/profile/password', { method: 'POST', body: payload });
