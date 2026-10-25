import { useEffect, useRef, useState } from 'react';
import { formatClock } from '../utils/formatting.js';

/**
 * Counts down to `deadline` (a Date.now()-style timestamp) and calls onExpire once at zero.
 * The server enforces the same deadline, so this timer can't be extended from the browser.
 */
export default function TestTimer({ deadline, onExpire }) {
  const [remaining, setRemaining] = useState(() => (deadline - Date.now()) / 1000);
  const [announcement, setAnnouncement] = useState('');
  const expiredRef = useRef(false);
  const announcedRef = useRef(new Set());

  useEffect(() => {
    const tick = () => {
      const left = (deadline - Date.now()) / 1000;
      setRemaining(left);
      for (const mark of [300, 60]) {
        if (left <= mark && left > mark - 2 && !announcedRef.current.has(mark)) {
          announcedRef.current.add(mark);
          setAnnouncement(mark === 300 ? '5 minutes left' : '1 minute left');
        }
      }
      if (left <= 0 && !expiredRef.current) {
        expiredRef.current = true;
        onExpire?.();
      }
    };
    tick();
    const id = setInterval(tick, 250);
    return () => clearInterval(id);
  }, [deadline, onExpire]);

  const tone = remaining <= 60 ? ' is-critical' : remaining <= 300 ? ' is-low' : '';
  return (
    <div className={`test-timer${tone}`}>
      <span className="test-timer-label">Time left</span>
      <span className="test-timer-value" role="timer" aria-label={`Time left ${formatClock(remaining)}`}>
        {formatClock(remaining)}
      </span>
      <span className="sr-only" aria-live="assertive">
        {announcement}
      </span>
    </div>
  );
}
