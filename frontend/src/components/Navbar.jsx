import { Link } from 'react-router-dom';
import { IconMenu } from './icons.jsx';
import { BrandMark } from './Sidebar.jsx';
import ThemeToggle from './ThemeToggle.jsx';

// Top bar for phones and tablets; the sidebar takes over on wide screens.
export default function Navbar({ onMenu }) {
  return (
    <header className="app-topbar">
      <button type="button" className="icon-btn" onClick={onMenu} aria-label="Open menu">
        <IconMenu />
      </button>
      <Link to="/dashboard" className="brand">
        <BrandMark />
        PlacePrep
      </Link>
      <ThemeToggle />
    </header>
  );
}
