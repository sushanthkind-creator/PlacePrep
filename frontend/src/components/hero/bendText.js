/**
 * Makes headline letters bend.
 * - Near the cursor, letters lift and lean around it, like a strip of paper pressed from below.
 * - While scrolling away, each line curls into an arc.
 * Letters ease towards their targets every frame, so the motion stays smooth.
 *
 * `root` contains `.line` elements whose letters are `.char` spans.
 * Returns a cleanup function.
 */

const CURSOR_SPREAD = 150; // px: how wide the bend around the cursor is
const CURSOR_LIFT = 26; // px: how high letters under the cursor rise
const CURSOR_LEAN = 12; // deg: how much letters beside the cursor lean
const SCROLL_CURL = 70; // px: how far line ends drop when fully scrolled
const SCROLL_TILT = 16; // deg: how much line ends rotate when fully scrolled
const EASE = 0.12;

export function measureLetters(root) {
  // Gradient letters need their position within the line so the gradient spans the whole line.
  root.querySelectorAll('.line').forEach((line) => {
    line.style.setProperty('--line-w', `${line.offsetWidth}px`);
    line.querySelectorAll('.char').forEach((char) => char.style.setProperty('--char-x', `${char.offsetLeft}px`));
  });
}

export function startBend(root, { cursor = true } = {}) {
  const lines = [...root.querySelectorAll('.line')];
  const letters = lines.flatMap((line) =>
    [...line.querySelectorAll('.char')].map((el) => ({ el, line, x: 0, y: 0, u: 0, curY: 0, curR: 0 })),
  );
  const pointer = { x: -9999, y: -9999, strength: 0, target: 0 };
  let rafId = 0;

  function measure() {
    letters.forEach((l) => {
      l.el.style.transform = 'none';
    });
    lines.forEach((line) => {
      const rect = line.getBoundingClientRect();
      const mid = rect.left + rect.width / 2;
      letters
        .filter((l) => l.line === line)
        .forEach((l) => {
          const r = l.el.getBoundingClientRect();
          l.x = r.left + r.width / 2 + window.scrollX;
          l.y = r.top + r.height / 2 + window.scrollY;
          // -1 at the line's left end, +1 at its right end.
          l.u = (r.left + r.width / 2 - mid) / (rect.width / 2 || 1);
        });
    });
    measureLetters(root);
  }

  function frame() {
    const heroHeight = root.offsetHeight || window.innerHeight;
    const curl = Math.min(1, Math.max(0, window.scrollY / (heroHeight * 0.7)));
    pointer.strength += (pointer.target - pointer.strength) * 0.08;

    for (const l of letters) {
      let ty = 0;
      let tr = 0;
      if (pointer.strength > 0.001) {
        const dx = l.x - pointer.x;
        const dy = l.y - pointer.y;
        const influence =
          Math.exp(-(dx * dx) / (2 * CURSOR_SPREAD * CURSOR_SPREAD)) *
          Math.exp(-(dy * dy) / (2 * (CURSOR_SPREAD * 1.2) ** 2)) *
          pointer.strength;
        ty -= influence * CURSOR_LIFT;
        tr += Math.max(-1, Math.min(1, dx / CURSOR_SPREAD)) * influence * CURSOR_LEAN;
      }
      ty += curl * SCROLL_CURL * l.u * l.u;
      tr += curl * SCROLL_TILT * l.u;

      l.curY += (ty - l.curY) * EASE;
      l.curR += (tr - l.curR) * EASE;
      l.el.style.transform = `translate3d(0, ${l.curY.toFixed(2)}px, 0) rotate(${l.curR.toFixed(2)}deg)`;
    }
    rafId = requestAnimationFrame(frame);
  }

  function onPointerMove(e) {
    pointer.x = e.clientX + window.scrollX;
    pointer.y = e.clientY + window.scrollY;
    const rect = root.getBoundingClientRect();
    const inside = e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom;
    pointer.target = inside ? 1 : 0;
  }

  function onPointerLeave() {
    pointer.target = 0;
  }

  // Only animate while the headline is on screen.
  const visibility = new IntersectionObserver(([entry]) => {
    cancelAnimationFrame(rafId);
    if (entry.isIntersecting) rafId = requestAnimationFrame(frame);
  });

  const resize = new ResizeObserver(measure);
  measure();
  resize.observe(root);
  visibility.observe(root);
  if (cursor) {
    window.addEventListener('pointermove', onPointerMove, { passive: true });
    document.documentElement.addEventListener('mouseleave', onPointerLeave);
  }

  return () => {
    cancelAnimationFrame(rafId);
    resize.disconnect();
    visibility.disconnect();
    window.removeEventListener('pointermove', onPointerMove);
    document.documentElement.removeEventListener('mouseleave', onPointerLeave);
    letters.forEach((l) => {
      l.el.style.transform = '';
    });
  };
}
