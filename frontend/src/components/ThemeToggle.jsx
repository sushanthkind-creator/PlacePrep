import { useTheme } from '../context/ThemeContext.jsx';
import { IconMoon, IconSun } from './icons.jsx';

export default function ThemeToggle({ showLabel = false }) {
  const { theme, toggleTheme } = useTheme();
  const next = theme === 'dark' ? 'light' : 'dark';
  return (
    <button
      type="button"
      className={showLabel ? 'nav-action' : 'icon-btn'}
      onClick={toggleTheme}
      aria-label={`Switch to ${next} theme`}
      title={`Switch to ${next} theme`}
    >
      {theme === 'dark' ? <IconSun /> : <IconMoon />}
      {showLabel && <span>{next === 'light' ? 'Light theme' : 'Dark theme'}</span>}
    </button>
  );
}
