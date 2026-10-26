import { useEffect, useRef } from 'react';
import { animate, scrambleText, stagger } from 'animejs';
import { measureLetters, startBend } from './bendText.js';

const TITLE_LINES = ['Every placement', 'is a puzzle.'];

function Letters({ text }) {
  return [...text].map((char, i) =>
    char === ' ' ? (
      <span key={i} className="char space">
        {' '}
      </span>
    ) : (
      <span key={i} className="char">
        {char}
      </span>
    ),
  );
}

export default function HeroHeader({ reducedMotion }) {
  const rootRef = useRef(null);

  useEffect(() => {
    const root = rootRef.current;
    if (reducedMotion) {
      // Still place the gradient correctly on the static headline.
      measureLetters(root);
      return undefined;
    }

    const letters = root.querySelectorAll('.hero-title .char:not(.space)');
    const fades = root.querySelectorAll('[data-fade]');
    const dot = root.querySelector('.scroll-dot');
    const finePointer = window.matchMedia('(pointer: fine)').matches;

    const animations = [
      // Each letter scrambles and settles, left to right.
      animate(letters, {
        innerHTML: scrambleText({ chars: 'A-Z!%#_' }),
        delay: stagger(32, { start: 150 }),
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
    const stopBend = startBend(root, { cursor: finePointer });

    return () => {
      stopBend();
      animations.forEach((a) => a.revert());
    };
  }, [reducedMotion]);

  return (
    <section className="hero" ref={rootRef}>
      <p className="hero-eyebrow" data-fade>
        Placement training <span aria-hidden="true">·</span> Logical <span aria-hidden="true">·</span> Quant{' '}
        <span aria-hidden="true">·</span> Verbal
      </p>
      <h1 className="hero-title" aria-label={TITLE_LINES.join(' ')}>
        {TITLE_LINES.map((line, i) => (
          <span className={`line${i === TITLE_LINES.length - 1 ? ' line--accent' : ''}`} aria-hidden="true" key={line}>
            <Letters text={line} />
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
