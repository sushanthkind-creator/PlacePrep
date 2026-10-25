export default function EmptyState({ title, children, action }) {
  return (
    <div className="empty-state">
      <span className="empty-stickers" aria-hidden="true">
        <i />
        <i />
        <i />
      </span>
      <p className="empty-title">{title}</p>
      {children && <p className="empty-text">{children}</p>}
      {action && <div className="empty-action">{action}</div>}
    </div>
  );
}
