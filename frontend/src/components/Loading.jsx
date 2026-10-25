export default function Loading({ label = 'Loading…', fullPage = false }) {
  return (
    <div className={`loading${fullPage ? ' loading--page' : ''}`} role="status" aria-live="polite">
      <span className="loading-cube" aria-hidden="true">
        <i />
        <i />
        <i />
        <i />
      </span>
      <span>{label}</span>
    </div>
  );
}
