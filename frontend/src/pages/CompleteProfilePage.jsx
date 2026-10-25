import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { updateProfile } from '../api/auth.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { validateCollegeName, validateMobile } from '../utils/validation.js';
import '../styles/auth.css';

// Google sign-ups don't include a mobile number or college, so we ask once before the dashboard.
export default function CompleteProfilePage() {
  const { user, setUser, logout } = useAuth();
  const navigate = useNavigate();
  const [values, setValues] = useState({ mobile: user.mobile || '', college_name: user.college_name || '' });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState(null);
  const [saving, setSaving] = useState(false);

  if (user.profile_complete) return <Navigate to="/dashboard" replace />;

  async function handleSubmit(e) {
    e.preventDefault();
    const found = { mobile: validateMobile(values.mobile), college_name: validateCollegeName(values.college_name) };
    const clean = Object.fromEntries(Object.entries(found).filter(([, m]) => m));
    setErrors(clean);
    if (Object.keys(clean).length) return;
    setSaving(true);
    setFormError(null);
    try {
      const res = await updateProfile(values);
      setUser(res.user);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setSaving(false);
      if (err.fields) setErrors(err.fields);
      setFormError(err);
    }
  }

  return (
    <div className="auth-page">
      <main className="auth-main auth-main--single">
        <div className="auth-card">
          <h1 className="auth-title">One more step, {user.full_name.split(' ')[0]}</h1>
          <p className="auth-sub">
            You signed in as <strong>{user.email}</strong>
            {user.email_verified_by_google ? ' (email verified by Google)' : ''}. Add your mobile number and college to finish setting up.
          </p>
          <form onSubmit={handleSubmit} noValidate>
            <div className="field">
              <label htmlFor="cp-mobile">Mobile number</label>
              <input
                id="cp-mobile"
                type="tel"
                inputMode="tel"
                autoComplete="tel-national"
                value={values.mobile}
                onChange={(e) => setValues((v) => ({ ...v, mobile: e.target.value }))}
                aria-invalid={Boolean(errors.mobile)}
                aria-describedby={errors.mobile ? 'cp-mobile-error' : undefined}
              />
              {errors.mobile && <p className="field-error" id="cp-mobile-error">{errors.mobile}</p>}
            </div>
            <div className="field">
              <label htmlFor="cp-college">College name</label>
              <input
                id="cp-college"
                autoComplete="organization"
                value={values.college_name}
                onChange={(e) => setValues((v) => ({ ...v, college_name: e.target.value }))}
                aria-invalid={Boolean(errors.college_name)}
                aria-describedby={errors.college_name ? 'cp-college-error' : undefined}
              />
              {errors.college_name && <p className="field-error" id="cp-college-error">{errors.college_name}</p>}
            </div>
            {formError && !formError.fields && <ErrorMessage error={formError} compact />}
            <button type="submit" className="btn-primary auth-submit" disabled={saving}>
              {saving ? 'Saving…' : 'Save and continue'}
            </button>
          </form>
          <p className="login-footer">
            Not you?{' '}
            <button type="button" className="link-button" onClick={() => logout().then(() => navigate('/', { replace: true }))}>
              Log out
            </button>
          </p>
        </div>
      </main>
    </div>
  );
}
