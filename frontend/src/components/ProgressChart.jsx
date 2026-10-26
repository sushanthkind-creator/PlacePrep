import { useMemo } from 'react';
import { Area, CartesianGrid, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useTheme } from '../context/ThemeContext.jsx';
import { formatDate } from '../utils/formatting.js';

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Score trend: the line draws itself in, the area below glows, and the latest score pulses.
 * Green when the last score went up, red when it went down. `points`: [{ id, title, percentage, submitted_at }].
 */
export default function ProgressChart({ points, height = 220 }) {
  const { theme } = useTheme();
  const data = points.map((p, i) => ({ ...p, index: i + 1 }));
  const last = data[data.length - 1]?.percentage ?? 0;
  const previous = data[data.length - 2]?.percentage ?? last;
  const direction = last > previous ? 'up' : last < previous ? 'down' : 'flat';

  // Re-read the palette whenever the theme changes.
  const colors = useMemo(
    () => ({
      up: cssVar('--correct'),
      down: cssVar('--wrong'),
      flat: cssVar('--text'),
      grid: cssVar('--border'),
      muted: cssVar('--muted'),
      surface: cssVar('--surface'),
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [theme],
  );
  const stroke = colors[direction];
  const animate = !prefersReducedMotion();
  // A new key replays the draw-in animation when a new result arrives.
  const chartKey = data.map((p) => p.id).join('-');

  function renderDot({ cx, cy, index }) {
    if (cx === undefined || cy === undefined) return null;
    if (index !== data.length - 1) {
      return <circle key={`dot-${index}`} cx={cx} cy={cy} r={3} fill={colors.surface} stroke={stroke} strokeWidth={1.5} />;
    }
    return (
      <g key={`dot-${index}`}>
        {animate && <circle className="trend-pulse" cx={cx} cy={cy} r={6} fill={stroke} />}
        <circle cx={cx} cy={cy} r={5} fill={stroke} stroke={colors.surface} strokeWidth={2} />
      </g>
    );
  }

  return (
    <figure className="progress-chart" data-direction={direction}>
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart key={chartKey} data={data} margin={{ top: 14, right: 14, bottom: 4, left: -16 }}>
          <defs>
            <linearGradient id="trend-fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={stroke} stopOpacity={0.28} />
              <stop offset="100%" stopColor={stroke} stopOpacity={0} />
            </linearGradient>
            <filter id="trend-glow" x="-20%" y="-50%" width="140%" height="200%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <CartesianGrid stroke={colors.grid} vertical={false} />
          <XAxis dataKey="index" tick={{ fill: colors.muted, fontSize: 12 }} tickLine={false} axisLine={{ stroke: colors.grid }} />
          <YAxis domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tick={{ fill: colors.muted, fontSize: 12 }} tickLine={false} axisLine={false} unit="%" />
          <Tooltip
            cursor={{ stroke: colors.grid }}
            contentStyle={{ background: colors.surface, border: `1px solid ${colors.grid}`, borderRadius: 10, fontSize: 13 }}
            labelFormatter={(index) => data[index - 1]?.title}
            formatter={(value, _name, item) => [`${value}%`, formatDate(item.payload.submitted_at)]}
          />
          <Area
            type="monotone"
            dataKey="percentage"
            stroke="none"
            fill="url(#trend-fill)"
            isAnimationActive={animate}
            animationDuration={1400}
            animationEasing="ease-out"
            tooltipType="none"
          />
          <Line
            type="monotone"
            dataKey="percentage"
            stroke={stroke}
            strokeWidth={2.5}
            filter="url(#trend-glow)"
            dot={renderDot}
            activeDot={{ r: 6, fill: stroke }}
            isAnimationActive={animate}
            animationDuration={1400}
            animationEasing="ease-in-out"
          />
        </ComposedChart>
      </ResponsiveContainer>
      <figcaption className="sr-only">
        Scores of your last {points.length} tests: {points.map((p) => `${p.title} ${p.percentage}%`).join(', ')}.
      </figcaption>
    </figure>
  );
}
