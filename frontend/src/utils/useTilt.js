import { useEffect } from 'react';

/**
 * Tilts an element in 3D towards the cursor and moves a light spot under it.
 * Writes CSS variables (--rx, --ry, --mx, --my, --glow) that styles in app.css use.
 * Does nothing on touch screens or when the user prefers reduced motion.
 */
export default function useTilt(ref, { max = 7 } = {}) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const fine = window.matchMedia('(pointer: fine)').matches;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!fine || reduced) return undefined;

    const target = { x: 0.5, y: 0.5, glow: 0 };
    const now = { x: 0.5, y: 0.5, glow: 0 };
    let rafId = 0;

    function frame() {
      now.x += (target.x - now.x) * 0.14;
      now.y += (target.y - now.y) * 0.14;
      now.glow += (target.glow - now.glow) * 0.14;
      el.style.setProperty('--ry', `${((now.x - 0.5) * 2 * max).toFixed(2)}deg`);
      el.style.setProperty('--rx', `${((0.5 - now.y) * 2 * max).toFixed(2)}deg`);
      el.style.setProperty('--mx', `${(now.x * 100).toFixed(1)}%`);
      el.style.setProperty('--my', `${(now.y * 100).toFixed(1)}%`);
      el.style.setProperty('--glow', now.glow.toFixed(3));
      const settled =
        Math.abs(target.x - now.x) < 0.001 && Math.abs(target.y - now.y) < 0.001 && Math.abs(target.glow - now.glow) < 0.002;
      rafId = settled ? 0 : requestAnimationFrame(frame);
    }

    function kick() {
      if (!rafId) rafId = requestAnimationFrame(frame);
    }

    function onMove(e) {
      const rect = el.getBoundingClientRect();
      target.x = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width));
      target.y = Math.min(1, Math.max(0, (e.clientY - rect.top) / rect.height));
      target.glow = 1;
      kick();
    }

    function onLeave() {
      target.x = 0.5;
      target.y = 0.5;
      target.glow = 0;
      kick();
    }

    el.addEventListener('pointermove', onMove);
    el.addEventListener('pointerleave', onLeave);
    return () => {
      cancelAnimationFrame(rafId);
      el.removeEventListener('pointermove', onMove);
      el.removeEventListener('pointerleave', onLeave);
    };
  }, [ref, max]);
}
