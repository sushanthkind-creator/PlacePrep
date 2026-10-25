// Client-side checks mirror the backend rules for instant feedback. The server re-validates everything.

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$/;
const MOBILE_PATTERN = /^(?:\+?91|0)?([6-9]\d{9})$/;
const NAME_PATTERN = /^[A-Za-z][A-Za-z .'-]*$/;

export function validateEmail(value) {
  const email = value.trim();
  if (!email) return 'Enter your college email ID.';
  if (email.length > 254 || !EMAIL_PATTERN.test(email)) return 'Enter a valid email address, like name@college.edu.';
  return '';
}

export function validateLoginPassword(value) {
  if (!value) return 'Enter your password.';
  return '';
}

export function validateFullName(value) {
  const name = value.trim().replace(/\s+/g, ' ');
  if (!name) return 'Enter your full name.';
  if (name.length < 2 || name.length > 100) return 'Name must be between 2 and 100 characters.';
  if (!NAME_PATTERN.test(name)) return 'Name can contain only letters, spaces, dots, hyphens and apostrophes.';
  return '';
}

export function validateMobile(value) {
  const raw = value.replace(/[\s\-()]/g, '');
  if (!raw) return 'Enter your mobile number.';
  if (!MOBILE_PATTERN.test(raw)) return 'Enter a valid 10-digit Indian mobile number starting with 6, 7, 8 or 9.';
  return '';
}

export function validateCollegeName(value) {
  const college = value.trim();
  if (!college) return 'Enter your college name.';
  if (college.length < 2 || college.length > 150) return 'College name must be between 2 and 150 characters.';
  return '';
}

export function validateNewPassword(value) {
  if (!value) return 'Enter a password.';
  if (value.length < 8) return 'Password must be at least 8 characters.';
  if (value.length > 128) return 'Password must be at most 128 characters.';
  if (!/[A-Za-z]/.test(value) || !/\d/.test(value)) return 'Password must contain at least one letter and one number.';
  return '';
}

export function validateConfirmPassword(password, confirm) {
  if (!confirm) return 'Confirm your password.';
  if (password !== confirm) return 'Passwords do not match.';
  return '';
}

export function validateRegistration(values) {
  const errors = {
    full_name: validateFullName(values.full_name),
    mobile: validateMobile(values.mobile),
    email: validateEmail(values.email),
    college_name: validateCollegeName(values.college_name),
    password: validateNewPassword(values.password),
    confirm_password: validateConfirmPassword(values.password, values.confirm_password),
  };
  return Object.fromEntries(Object.entries(errors).filter(([, message]) => message));
}
