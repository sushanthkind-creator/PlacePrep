import { GoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';
import { useEffect, useState } from 'react';
import { getAuthConfig } from '../api/auth.js';

let configRequest = null;

/**
 * "Continue with Google". Renders nothing unless the backend has GOOGLE_CLIENT_ID configured,
 * so there is never a button that can't work.
 */
export default function GoogleSignInButton({ onCredential, onError }) {
  const [clientId, setClientId] = useState(null);

  useEffect(() => {
    configRequest ||= getAuthConfig().catch(() => ({ google_enabled: false }));
    let active = true;
    configRequest.then((config) => active && setClientId(config.google_enabled ? config.google_client_id : null));
    return () => {
      active = false;
    };
  }, []);

  if (!clientId) return null;

  return (
    <div className="google-signin">
      <p className="divider">
        <span>or</span>
      </p>
      <GoogleOAuthProvider clientId={clientId}>
        <GoogleLogin
          onSuccess={(response) => onCredential(response.credential)}
          onError={() => onError('Google sign-in was cancelled or failed. Please try again.')}
          theme="filled_black"
          shape="pill"
          text="continue_with"
          width="320"
        />
      </GoogleOAuthProvider>
    </div>
  );
}
