import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import GoogleSignInButton from '../components/GoogleSignInButton.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';
import { BrandMark } from '../components/Sidebar.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import {
  validateCollegeName,
  validateConfirmPassword,
  validateEmail,
  validateFullName,
  validateMobile,
  validateNewPassword,
  validateRegistration,
} from '../utils/validation.js';
import '../styles/auth.css';

const FIELDS = [
  { name: 'full_name', label: 'Full name', autoComplete: 'name', validate: validateFullName },
  {
    name: 'mobile',
    label: 'Mobile number',
    type: 'tel',
    autoComplete: 'tel-national',
    inputMode: 'tel',
    placeholder: '98765 43210',
    hint: '10-digit Indian mobile number. It is stored with your account, not verified.',
    validate: validateMobile,
  },
  {
    name: 'email',
    label: 'College email ID',
    type: 'email',
    autoComplete: 'email',
    placeholder: 'name@college.edu',
    hint: 'You will use this to log in.',
    validate: validateEmail,
  },
  { name: 'college_name', label: 'College name', autoComplete: 'organization', validate: validateCollegeName },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    autoComplete: 'new-password',
    hint: 'At least 8 characters, including a letter and a number.',
    validate: validateNewPassword,
  },
  { name: 'confirm_password', label: 'Confirm password', type: 'password', autoComplete: 'new-password' },
];

const EMPTY = Object.fromEntries(FIELDS.map((f) => [f.name, '']));

export default function RegisterPage() {
  const { status, register, loginWithGoogle } = useAuth();
  const navigate = useNavigate();
  const [values, setValues] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  if (status === 'authenticated') return <Navigate to="/dashboard" replace />;

  function fieldError(name, nextValues) {
    if (name === 'confirm_password') return validateConfirmPassword(nextValues.password, nextValues.confirm_password);
    return FIELDS.find((f) => f.name === name).validate(nextValues[name]);
  }

  function handleChange(e) {
    const { name, value } = e.target;
    const next = { ...values, [name]: value };
    setValues(next);
    if (errors[name]) setErrors((err) => ({ ...err, [name]: fieldError(name, next) }));
  }

  function handleBlur(e) {
    const { name } = e.target;
    if (values[name]) setErrors((err) => ({ ...err, [name]: fieldError(name, values) }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setFormError(null);
    const found = validateRegistration(values);
    setErrors(found);
    if (Object.keys(found).length) {
      document.getElementById(`reg-${Object.keys(found)[0]}`)?.focus();
      return;
    }
    setSubmitting(true);
    try {
      await register(values);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setSubmitting(false);
      if (err.fields) setErrors(err.fields);
      setFormError(err);
    }
  }

  async function handleGoogle(credential) {
    setFormError(null);
    try {
      const user = await loginWithGoogle(credential);
      navigate(user.profile_complete ? '/dashboard' : '/complete-profile', { replace: true });
    } catch (err) {
      setFormError(err);
    }
  }

  return (
    <div className="auth-page">
      <header className="auth-topbar">
        <Link to="/" className="brand">
          <BrandMark />
          PlacePrep
        </Link>
        <Link to="/login" className="btn-outline">
          Log in
        </Link>
      </header>

      <main className="auth-main">
        <section className="auth-intro" aria-hidden="true">
          <p className="auth-kicker">New here</p>
          <p className="auth-headline">Three sections. Thirty-six topics. One cube to solve.</p>
          <div className="auth-faces">
            {['logical', 'quant', 'verbal'].map((tone) => (
              <span key={tone} data-tone={tone}>
                {Array.from({ length: 9 }, (_, i) => (
                  <i key={i} />
                ))}
              </span>
            ))}
          </div>
        </section>

        <div className="auth-card">
          <h1 className="auth-title">Create your account</h1>
          <p className="auth-sub">Your lessons, practice and test results are saved to this account.</p>

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-grid">
              {FIELDS.map((field) => {
                const id = `reg-${field.name}`;
                const hintId = field.hint ? `${id}-hint` : undefined;
                const errorId = errors[field.name] ? `${id}-error` : undefined;
                return (
                  <div key={field.name} className={`field${field.name === 'email' || field.name === 'college_name' ? ' field--wide' : ''}`}>
                    <label htmlFor={id}>{field.label}</label>
                    <input
                      id={id}
                      name={field.name}
                      type={field.type || 'text'}
                      autoComplete={field.autoComplete}
                      inputMode={field.inputMode}
                      placeholder={field.placeholder}
                      value={values[field.name]}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      aria-invalid={Boolean(errors[field.name])}
                      aria-describedby={[hintId, errorId].filter(Boolean).join(' ') || undefined}
                    />
                    {field.hint && !errors[field.name] && (
                      <p className="field-hint" id={hintId}>
                        {field.hint}
                      </p>
                    )}
                    {errors[field.name] && (
                      <p className="field-error" id={errorId}>
                        {errors[field.name]}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>

            {formError && !formError.fields && <ErrorMessage error={formError} compact />}
            {formError?.fields && <p className="field-error" role="alert">{formError.message}</p>}

            <button type="submit" className="btn-primary auth-submit" disabled={submitting}>
              {submitting ? 'Creating account…' : 'Create account'}
            </button>
          </form>

          <GoogleSignInButton onCredential={handleGoogle} onError={(message) => setFormError(message)} />

          <p className="login-footer">
            Already registered? <Link to="/login">Log in</Link>
          </p>
        </div>
      </main>
    </div>
  );
}
