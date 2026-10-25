import { useMemo } from 'react';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useTheme } from '../context/ThemeContext.jsx';
import { formatDate } from '../utils/formatting.js';

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

/** Line chart of test scores over time. `points`: [{ id, title, percentage, submitted_at }]. */
export default function ProgressChart({ points, height = 220 }) {
  const { theme } = useTheme();
  // Re-read the palette whenever the theme changes.
  const colors = useMemo(
    () => ({ line: cssVar('--text'), grid: cssVar('--border'), muted: cssVar('--muted'), surface: cssVar('--surface') }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [theme],
  );
  const data = points.map((p, i) => ({ ...p, index: i + 1 }));

  return (
    <figure className="progress-chart">
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data} margin={{ top: 12, right: 12, bottom: 4, left: -16 }}>
          <CartesianGrid stroke={colors.grid} vertical={false} />
          <XAxis dataKey="index" tick={{ fill: colors.muted, fontSize: 12 }} tickLine={false} axisLine={{ stroke: colors.grid }} />
          <YAxis domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tick={{ fill: colors.muted, fontSize: 12 }} tickLine={false} axisLine={false} unit="%" />
          <Tooltip
            cursor={{ stroke: colors.grid }}
            contentStyle={{ background: colors.surface, border: `1px solid ${colors.grid}`, borderRadius: 10, fontSize: 13 }}
            labelFormatter={(index) => data[index - 1]?.title}
            formatter={(value, _name, item) => [`${value}%`, formatDate(item.payload.submitted_at)]}
          />
          <Line type="monotone" dataKey="percentage" stroke={colors.line} strokeWidth={2} dot={{ r: 3.5, fill: colors.line }} activeDot={{ r: 5 }} />
        </LineChart>
      </ResponsiveContainer>
      <figcaption className="sr-only">
        Scores of your last {points.length} tests: {points.map((p) => `${p.title} ${p.percentage}%`).join(', ')}.
      </figcaption>
    </figure>
  );
}
