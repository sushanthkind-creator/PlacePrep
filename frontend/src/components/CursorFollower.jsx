import { useEffect, useRef } from 'react';

const INTERACTIVE = 'a, button, input, select, label, summary, [data-tilt], [role="button"]';

/**
 * A soft ring that trails the mouse and grows over clickable things.
 * Decorative only: the normal cursor stays, and it's skipped on touch screens and for reduced motion.
 */
export default function CursorFollower() {
  const ringRef = useRef(null);
  const dotRef = useRef(null);

  useEffect(() => {
    const fine = window.matchMedia('(pointer: fine)').matches;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const ring = ringRef.current;
    const dot = dotRef.current;
    if (!fine || reduced || !ring || !dot) return undefined;

    const target = { x: -100, y: -100 };
    const pos = { x: -100, y: -100 };
    let scale = 1;
    let targetScale = 1;
    let visible = false;
    let rafId = 0;

    function frame() {
      // Ease towards the pointer so the ring lags slightly behind.
      pos.x += (target.x - pos.x) * 0.18;
      pos.y += (target.y - pos.y) * 0.18;
      scale += (targetScale - scale) * 0.2;
      ring.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0) translate(-50%, -50%) scale(${scale})`;
      rafId = requestAnimationFrame(frame);
    }

    function onMove(e) {
      target.x = e.clientX;
      target.y = e.clientY;
      dot.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0) translate(-50%, -50%)`;
      targetScale = e.target.closest?.(INTERACTIVE) ? 1.8 : 1;
      if (!visible) {
        visible = true;
        pos.x = target.x;
        pos.y = target.y;
        ring.classList.add('is-visible');
        dot.classList.add('is-visible');
      }
    }

    function onLeaveWindow() {
      visible = false;
      ring.classList.remove('is-visible');
      dot.classList.remove('is-visible');
    }

    function onDown() {
      targetScale = 0.75;
    }

    window.addEventListener('pointermove', onMove, { passive: true });
    window.addEventListener('pointerdown', onDown);
    document.documentElement.addEventListener('mouseleave', onLeaveWindow);
    rafId = requestAnimationFrame(frame);
    return () => {
      cancelAnimationFrame(rafId);
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerdown', onDown);
      document.documentElement.removeEventListener('mouseleave', onLeaveWindow);
    };
  }, []);

  return (
    <>
      <div ref={ringRef} className="cursor-ring" aria-hidden="true" />
      <div ref={dotRef} className="cursor-dot" aria-hidden="true" />
    </>
  );
}
