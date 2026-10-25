export default function ErrorMessage({ error, title = "Couldn't load this page", onRetry, compact = false }) {
  if (!error) return null;
  const message = typeof error === 'string' ? error : error.message;
  return (
    <div className={`error-box${compact ? ' error-box--compact' : ''}`} role="alert">
      {!compact && <p className="error-title">{title}</p>}
      <p className="error-text">{message}</p>
      {onRetry && (
        <button type="button" className="btn btn-secondary btn-sm" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}
