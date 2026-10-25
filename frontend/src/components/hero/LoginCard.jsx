import { forwardRef, useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { takeSessionEndedReason, useAuth } from '../../context/AuthContext.jsx';
import { validateEmail, validateLoginPassword } from '../../utils/validation.js';
import GoogleSignInButton from '../GoogleSignInButton.jsx';

const SESSION_NOTICES = {
  expired: 'Your session expired. Please log in again.',
  invalid: 'You were logged out. Please log in again.',
};

const LoginCard = forwardRef(function LoginCard({ emailInputRef }, ref) {
  const { status, user, login, loginWithGoogle, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [values, setValues] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [formError, setFormError] = useState('');
  const [notice, setNotice] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const reason = takeSessionEndedReason();
    if (reason) setNotice(SESSION_NOTICES[reason] || SESSION_NOTICES.invalid);
  }, []);

  const destination = location.state?.from || '/dashboard';

  function update(field) {
    return (e) => {
      setValues((v) => ({ ...v, [field]: e.target.value }));
      if (errors[field]) setErrors((err) => ({ ...err, [field]: '' }));
      setFormError('');
    };
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const next = { email: validateEmail(values.email), password: validateLoginPassword(values.password) };
    setErrors(next);
    if (next.email || next.password) return;
    setSubmitting(true);
    setFormError('');
    try {
      const me = await login(values.email.trim(), values.password);
      navigate(me.profile_complete ? destination : '/complete-profile', { replace: true });
    } catch (err) {
      setSubmitting(false);
      if (err.fields) setErrors(err.fields);
      setFormError(err.message);
    }
  }

  async function handleGoogle(credential) {
    setFormError('');
    try {
      const me = await loginWithGoogle(credential);
      navigate(me.profile_complete ? destination : '/complete-profile', { replace: true });
    } catch (err) {
      setFormError(err.message);
    }
  }

  if (status === 'authenticated' && user) {
    return (
      <div className="login-card" ref={ref}>
        <p className="login-kicker">Puzzle solved</p>
        <h2 className="login-title">Welcome back, {user.full_name.split(' ')[0]}.</h2>
        <p className="login-sub">You're logged in as {user.email}.</p>
        <Link to="/dashboard" className="btn-primary login-submit" ref={emailInputRef}>
          Go to dashboard
        </Link>
        <p className="login-footer">
          Not you?{' '}
          <button type="button" className="link-button" onClick={logout}>
            Log out
          </button>
        </p>
      </div>
    );
  }

  return (
    <div className="login-card" ref={ref}>
      <p className="login-kicker">Puzzle solved</p>
      <h2 className="login-title">Now let&apos;s get you placed.</h2>
      <p className="login-sub">Log in with your college email ID to continue your preparation.</p>
      {notice && (
        <p className="login-notice" role="status">
          {notice}
        </p>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div className="field">
          <label htmlFor="login-email">College email ID</label>
          <input
            id="login-email"
            ref={emailInputRef}
            type="email"
            autoComplete="email"
            placeholder="name@college.edu"
            value={values.email}
            onChange={update('email')}
            aria-invalid={Boolean(errors.email)}
            aria-describedby={errors.email ? 'login-email-error' : undefined}
          />
          {errors.email && (
            <p className="field-error" id="login-email-error">
              {errors.email}
            </p>
          )}
        </div>

        <div className="field">
          <label htmlFor="login-password">Password</label>
          <div className="password-wrap">
            <input
              id="login-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              value={values.password}
              onChange={update('password')}
              aria-invalid={Boolean(errors.password)}
              aria-describedby={errors.password ? 'login-password-error' : undefined}
            />
            <button type="button" className="password-toggle" onClick={() => setShowPassword((s) => !s)} aria-pressed={showPassword}>
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          {errors.password && (
            <p className="field-error" id="login-password-error">
              {errors.password}
            </p>
          )}
        </div>

        <button type="submit" className="btn-primary login-submit" disabled={submitting}>
          {submitting ? 'Logging in…' : 'Log in'}
        </button>

        <p className="form-notice form-notice--error" role="alert">
          {formError}
        </p>
      </form>

      <GoogleSignInButton onCredential={handleGoogle} onError={setFormError} />

      <p className="login-footer">
        New to PlacePrep? <Link to="/register">Create an account</Link>
      </p>
    </div>
  );
});

export default LoginCard;
