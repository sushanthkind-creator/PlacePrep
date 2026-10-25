import { useEffect, useRef } from 'react';
import { animate, scrambleText, stagger } from 'animejs';

const TITLE_LINES = ['Every placement', 'is a puzzle.'];

export default function HeroHeader({ reducedMotion }) {
  const rootRef = useRef(null);

  useEffect(() => {
    if (reducedMotion) return undefined;
    const root = rootRef.current;
    const lines = root.querySelectorAll('.hero-title .line');
    const fades = root.querySelectorAll('[data-fade]');
    const dot = root.querySelector('.scroll-dot');

    const animations = [
      animate(lines, {
        innerHTML: scrambleText({ chars: 'A-Z!%#_', perturbation: 0.4 }),
        delay: stagger(260, { start: 150 }),
      }),
      animate(fades, {
        opacity: [0, 1],
        translateY: [18, 0],
        duration: 900,
        ease: 'outExpo',
        delay: stagger(120, { start: 700 }),
      }),
      animate(dot, {
        translateY: [0, 34],
        opacity: [{ to: 1, duration: 200 }, { to: 0, duration: 400, delay: 800 }],
        duration: 1400,
        ease: 'inOutSine',
        loop: true,
      }),
    ];
    return () => animations.forEach((a) => a.revert());
  }, [reducedMotion]);

  return (
    <section className="hero" ref={rootRef}>
      <p className="hero-eyebrow" data-fade>
        Placement training <span aria-hidden="true">·</span> Logical <span aria-hidden="true">·</span> Quant{' '}
        <span aria-hidden="true">·</span> Verbal
      </p>
      <h1 className="hero-title" aria-label={TITLE_LINES.join(' ')}>
        {TITLE_LINES.map((line) => (
          <span className="line" aria-hidden="true" key={line}>
            {line}
          </span>
        ))}
      </h1>
      <p className="hero-sub" data-fade>
        Scroll down and solve it, one concept, one question, one test at a time.
      </p>
      <div className="scroll-cue" data-fade aria-hidden="true">
        <span>Scroll to start solving</span>
        <span className="scroll-track">
          <span className="scroll-dot" />
        </span>
      </div>
    </section>
  );
}
