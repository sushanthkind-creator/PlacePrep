import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { changePassword, updateProfile } from '../api/auth.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { formatDate } from '../utils/formatting.js';
import {
  validateCollegeName,
  validateConfirmPassword,
  validateFullName,
  validateMobile,
  validateNewPassword,
} from '../utils/validation.js';
import '../styles/dashboard.css';

function Field({ id, label, error, hint, ...props }) {
  const describedBy = [hint && `${id}-hint`, error && `${id}-error`].filter(Boolean).join(' ') || undefined;
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input id={id} aria-invalid={Boolean(error)} aria-describedby={describedBy} {...props} />
      {hint && !error && <p className="field-hint" id={`${id}-hint`}>{hint}</p>}
      {error && <p className="field-error" id={`${id}-error`}>{error}</p>}
    </div>
  );
}

function clean(errors) {
  return Object.fromEntries(Object.entries(errors).filter(([, m]) => m));
}

export default function ProfilePage() {
  const { user, setUser, logout } = useAuth();
  const navigate = useNavigate();

  const [details, setDetails] = useState({ full_name: user.full_name, mobile: user.mobile || '', college_name: user.college_name || '' });
  const [detailErrors, setDetailErrors] = useState({});
  const [detailStatus, setDetailStatus] = useState({ saving: false, message: '', error: null });

  const [passwords, setPasswords] = useState({ current_password: '', new_password: '', confirm_password: '' });
  const [passwordErrors, setPasswordErrors] = useState({});
  const [passwordStatus, setPasswordStatus] = useState({ saving: false, message: '', error: null });

  async function saveDetails(e) {
    e.preventDefault();
    const found = clean({
      full_name: validateFullName(details.full_name),
      mobile: validateMobile(details.mobile),
      college_name: validateCollegeName(details.college_name),
    });
    setDetailErrors(found);
    if (Object.keys(found).length) return;
    setDetailStatus({ saving: true, message: '', error: null });
    try {
      const res = await updateProfile(details);
      setUser(res.user);
      setDetailStatus({ saving: false, message: 'Profile saved.', error: null });
    } catch (err) {
      if (err.fields) setDetailErrors(err.fields);
      setDetailStatus({ saving: false, message: '', error: err.fields ? null : err });
    }
  }

  async function savePassword(e) {
    e.preventDefault();
    const found = clean({
      current_password: user.has_password && !passwords.current_password ? 'Enter your current password.' : '',
      new_password: validateNewPassword(passwords.new_password),
      confirm_password: validateConfirmPassword(passwords.new_password, passwords.confirm_password),
    });
    setPasswordErrors(found);
    if (Object.keys(found).length) return;
    setPasswordStatus({ saving: true, message: '', error: null });
    try {
      const res = await changePassword(passwords);
      setUser(res.user);
      setPasswords({ current_password: '', new_password: '', confirm_password: '' });
      setPasswordStatus({ saving: false, message: user.has_password ? 'Password changed.' : 'Password set.', error: null });
    } catch (err) {
      if (err.fields) setPasswordErrors(err.fields);
      setPasswordStatus({ saving: false, message: '', error: err.fields ? null : err });
    }
  }

  async function handleLogout() {
    await logout();
    navigate('/', { replace: true });
  }

  const onDetail = (e) => {
    setDetails((d) => ({ ...d, [e.target.name]: e.target.value }));
    setDetailStatus((s) => ({ ...s, message: '' }));
  };
  const onPassword = (e) => {
    setPasswords((p) => ({ ...p, [e.target.name]: e.target.value }));
    setPasswordStatus((s) => ({ ...s, message: '' }));
  };

  return (
    <div className="page profile">
      <header className="page-header">
        <h1>Profile</h1>
        <p className="lede">Member since {formatDate(user.created_at)}.</p>
      </header>

      <div className="profile-grid">
        <form className="panel" onSubmit={saveDetails} noValidate aria-labelledby="details-heading">
          <h2 id="details-heading" className="block-title">
            Your details
          </h2>
          <div className="field">
            <label htmlFor="pf-email">College email ID</label>
            <input id="pf-email" value={user.email} readOnly aria-describedby="pf-email-hint" />
            <p className="field-hint" id="pf-email-hint">
              Your login ID, so it can't be changed.
              {user.email_verified_by_google ? ' Verified by Google.' : ''}
            </p>
          </div>
          <Field id="pf-name" name="full_name" label="Full name" autoComplete="name" value={details.full_name} onChange={onDetail} error={detailErrors.full_name} />
          <Field
            id="pf-mobile"
            name="mobile"
            label="Mobile number"
            type="tel"
            inputMode="tel"
            autoComplete="tel-national"
            value={details.mobile}
            onChange={onDetail}
            error={detailErrors.mobile}
            hint="Stored with your account. Not verified."
          />
          <Field id="pf-college" name="college_name" label="College name" autoComplete="organization" value={details.college_name} onChange={onDetail} error={detailErrors.college_name} />
          <ErrorMessage error={detailStatus.error} compact />
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={detailStatus.saving}>
              {detailStatus.saving ? 'Saving…' : 'Save changes'}
            </button>
            <p className="form-success" role="status">
              {detailStatus.message}
            </p>
          </div>
        </form>

        <form className="panel" onSubmit={savePassword} noValidate aria-labelledby="password-heading">
          <h2 id="password-heading" className="block-title">
            {user.has_password ? 'Change password' : 'Set a password'}
          </h2>
          {!user.has_password && (
            <p className="muted small">You signed up with Google. Set a password to also log in with your email.</p>
          )}
          {user.has_password && (
            <Field
              id="pf-current"
              name="current_password"
              label="Current password"
              type="password"
              autoComplete="current-password"
              value={passwords.current_password}
              onChange={onPassword}
              error={passwordErrors.current_password}
            />
          )}
          <Field
            id="pf-new"
            name="new_password"
            label="New password"
            type="password"
            autoComplete="new-password"
            value={passwords.new_password}
            onChange={onPassword}
            error={passwordErrors.new_password}
            hint="At least 8 characters, including a letter and a number."
          />
          <Field
            id="pf-confirm"
            name="confirm_password"
            label="Confirm new password"
            type="password"
            autoComplete="new-password"
            value={passwords.confirm_password}
            onChange={onPassword}
            error={passwordErrors.confirm_password}
          />
          <ErrorMessage error={passwordStatus.error} compact />
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={passwordStatus.saving}>
              {passwordStatus.saving ? 'Saving…' : user.has_password ? 'Change password' : 'Set password'}
            </button>
            <p className="form-success" role="status">
              {passwordStatus.message}
            </p>
          </div>
        </form>

        <section className="panel" aria-labelledby="session-heading">
          <h2 id="session-heading" className="block-title">
            Session
          </h2>
          <p className="muted small">Logging out ends this session on the server too.</p>
          <button type="button" className="btn btn-secondary" onClick={handleLogout}>
            Log out
          </button>
        </section>
      </div>
    </div>
  );
}
