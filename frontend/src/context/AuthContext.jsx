import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import * as authApi from '../api/auth.js';
import { getToken, onUnauthorized, setToken } from '../api/client.js';

const AuthContext = createContext(null);
const EXPIRED_KEY = 'placeprep-session-ended';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState(getToken() ? 'loading' : 'anonymous');

  const clearSession = useCallback((reason) => {
    setToken(null);
    setUser(null);
    setStatus('anonymous');
    if (reason) {
      try {
        sessionStorage.setItem(EXPIRED_KEY, reason);
      } catch {
        // ignore
      }
    }
  }, []);

  useEffect(() => {
    onUnauthorized((code) => clearSession(code === 'token_expired' ? 'expired' : 'invalid'));
  }, [clearSession]);

  // Restore the session from a stored token.
  const restore = useCallback(() => {
    if (!getToken()) return undefined;
    let active = true;
    setStatus('loading');
    authApi
      .getMe()
      .then(({ user: me }) => {
        if (!active) return;
        setUser(me);
        setStatus('authenticated');
      })
      .catch((err) => {
        if (!active) return;
        // Network errors keep the token so the student can retry once the server is up.
        if (err.status === 0) setStatus('offline');
        else clearSession();
      });
    return () => {
      active = false;
    };
  }, [clearSession]);

  useEffect(() => restore(), [restore]);

  const startSession = useCallback(({ access_token: token, user: me }) => {
    setToken(token);
    setUser(me);
    setStatus('authenticated');
    return me;
  }, []);

  const login = useCallback((email, password) => authApi.login(email, password).then(startSession), [startSession]);
  const register = useCallback((payload) => authApi.register(payload).then(startSession), [startSession]);
  const loginWithGoogle = useCallback((credential) => authApi.loginWithGoogle(credential).then(startSession), [startSession]);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } catch {
      // The token is discarded locally either way.
    }
    clearSession();
  }, [clearSession]);

  const value = useMemo(
    () => ({ user, status, login, register, loginWithGoogle, logout, setUser, retry: restore }),
    [user, status, login, register, loginWithGoogle, logout, restore],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside <AuthProvider>');
  return context;
}

/** Returns (and clears) why the last session ended, for a one-time notice on the login card. */
export function takeSessionEndedReason() {
  try {
    const reason = sessionStorage.getItem(EXPIRED_KEY);
    sessionStorage.removeItem(EXPIRED_KEY);
    return reason;
  } catch {
    return null;
  }
}
