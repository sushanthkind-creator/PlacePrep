import { useEffect } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { IconClose, IconGrid, IconHistory, IconLogout, IconTimer, IconUser } from './icons.jsx';
import ThemeToggle from './ThemeToggle.jsx';

const LEARN = [
  { to: '/learn/logical', label: 'Logical Reasoning', tone: 'logical' },
  { to: '/learn/quant', label: 'Quantitative Aptitude', tone: 'quant' },
  { to: '/learn/english', label: 'English / Verbal', tone: 'verbal' },
];

export function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <i />
      <i />
      <i />
      <i />
    </span>
  );
}

export default function Sidebar({ open, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!open) return undefined;
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  async function handleLogout() {
    await logout();
    navigate('/', { replace: true });
  }

  return (
    <>
      <aside className={`sidebar${open ? ' is-open' : ''}`} aria-label="Main navigation">
        <div className="sidebar-head">
          <Link to="/dashboard" className="brand">
            <BrandMark />
            PlacePrep
          </Link>
          <button type="button" className="icon-btn sidebar-close" onClick={onClose} aria-label="Close menu">
            <IconClose />
          </button>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/dashboard" className="nav-item">
            <IconGrid />
            Dashboard
          </NavLink>

          <p className="nav-label">Learn</p>
          {LEARN.map((item) => (
            <NavLink key={item.to} to={item.to} className="nav-item" data-tone={item.tone}>
              <span className="nav-sticker" aria-hidden="true" />
              {item.label}
            </NavLink>
          ))}

          <p className="nav-label">Assess</p>
          <NavLink to="/tests" className="nav-item">
            <IconTimer />
            Tests
          </NavLink>
          <NavLink to="/history" className="nav-item">
            <IconHistory />
            Test history
          </NavLink>

          <p className="nav-label">Account</p>
          <NavLink to="/profile" className="nav-item">
            <IconUser />
            Profile
          </NavLink>
        </nav>

        <div className="sidebar-foot">
          {user && (
            <div className="sidebar-user">
              <span className="sidebar-user-name">{user.full_name}</span>
              <span className="sidebar-user-meta">{user.college_name || user.email}</span>
            </div>
          )}
          <ThemeToggle showLabel />
          <button type="button" className="nav-action" onClick={handleLogout}>
            <IconLogout />
            <span>Log out</span>
          </button>
        </div>
      </aside>
      {open && <div className="sidebar-backdrop" onClick={onClose} aria-hidden="true" />}
    </>
  );
}
