import { useEffect, useRef } from 'react';
import { createDrawable, createTimeline, onScroll, stagger } from 'animejs';

// Labels for the three learning sections, joined to the cube by lines that draw in.
// Coordinates are percentages of the stage, so the SVG uses a 100x100 viewBox.
const CALLOUTS = [
  { key: 'logical', title: 'Logical Reasoning', meta: '10 topics', label: [14, 24], line: 'M 27 27 L 35 27 L 43 38' },
  { key: 'quant', title: 'Quantitative Aptitude', meta: '14 topics', label: [86, 30], line: 'M 73 33 L 65 33 L 57 42' },
  { key: 'verbal', title: 'Verbal Ability', meta: '12 topics', label: [80, 76], line: 'M 70 73 L 63 73 L 56 62' },
];

export default function Callouts({ reducedMotion, fadeRef }) {
  const rootRef = useRef(null);

  useEffect(() => {
    if (reducedMotion) return undefined;
    const root = rootRef.current;
    const lines = createDrawable(root.querySelectorAll('.callout-line'));
    const labels = root.querySelectorAll('.callout');
    const dots = root.querySelectorAll('.callout-dot');
    // A scroll observer drives exactly one playable, so the three parts share one timeline.
    const observer = onScroll({ target: root, enter: 'bottom top', repeat: false });
    const timeline = createTimeline({ autoplay: observer })
      .add(lines, { draw: ['0 0', '0 1'], duration: 900, ease: 'inOutQuad', delay: stagger(160) }, 0)
      .add(labels, { opacity: [0, 1], translateY: [10, 0], duration: 700, ease: 'outExpo', delay: stagger(160) }, 500)
      .add(dots, { opacity: [0, 1], scale: [0, 1], duration: 500, ease: 'outBack(2)', delay: stagger(160) }, 800);
    return () => {
      timeline.revert();
      observer.revert();
    };
  }, [reducedMotion]);

  return (
    <div className="callouts" ref={(el) => { rootRef.current = el; if (fadeRef) fadeRef.current = el; }} aria-hidden="true">
      <svg className="callout-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        {CALLOUTS.map((c) => (
          <path key={c.key} className={`callout-line callout-line--${c.key}`} d={c.line} vectorEffect="non-scaling-stroke" />
        ))}
      </svg>
      {CALLOUTS.map((c) => {
        const end = c.line.split(' ').slice(-2).map(Number);
        return (
          <span key={c.key} className={`callout-dot callout-dot--${c.key}`} style={{ left: `${end[0]}%`, top: `${end[1]}%` }} />
        );
      })}
      {CALLOUTS.map((c) => (
        <div key={c.key} className={`callout callout--${c.key}`} style={{ left: `${c.label[0]}%`, top: `${c.label[1]}%` }}>
          <span className="callout-title">{c.title}</span>
          <span className="callout-meta">{c.meta}</span>
        </div>
      ))}
    </div>
  );
}
