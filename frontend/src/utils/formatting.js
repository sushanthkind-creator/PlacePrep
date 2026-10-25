export function firstName(fullName = '') {
  return fullName.trim().split(/\s+/)[0] || 'there';
}

export function formatPercent(value, digits = 0) {
  if (value === null || value === undefined) return '—';
  return `${Number(value).toFixed(digits).replace(/\.0+$/, '')}%`;
}

export function formatDuration(totalSeconds) {
  if (totalSeconds === null || totalSeconds === undefined) return '—';
  const seconds = Math.max(0, Math.round(totalSeconds));
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h) return `${h}h ${String(m).padStart(2, '0')}m`;
  if (m) return `${m}m ${String(s).padStart(2, '0')}s`;
  return `${s}s`;
}

export function formatClock(totalSeconds) {
  const seconds = Math.max(0, Math.ceil(totalSeconds));
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const mm = String(m).padStart(2, '0');
  const ss = String(s).padStart(2, '0');
  return h ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}

const dateFormatter = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
const dateTimeFormatter = new Intl.DateTimeFormat('en-IN', {
  day: 'numeric',
  month: 'short',
  hour: 'numeric',
  minute: '2-digit',
});

export function formatDate(iso) {
  return iso ? dateFormatter.format(new Date(iso)) : '—';
}

export function formatDateTime(iso) {
  return iso ? dateTimeFormatter.format(new Date(iso)) : '—';
}

export function formatChange(change) {
  if (change === null || change === undefined) return { label: 'First attempt', tone: 'neutral' };
  if (change > 0) return { label: `▲ ${formatPercent(change, 1)}`, tone: 'up' };
  if (change < 0) return { label: `▼ ${formatPercent(Math.abs(change), 1)}`, tone: 'down' };
  return { label: 'No change', tone: 'neutral' };
}

export function plural(count, word, pluralWord = `${word}s`) {
  return `${count} ${count === 1 ? word : pluralWord}`;
}
