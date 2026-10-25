import { moveNotation } from './cubeMoves.js';

export default function ScrollScrubber({ solution, movesDone }) {
  const total = solution.length;
  const solved = movesDone >= total;
  const next = solved ? null : solution[movesDone];

  return (
    <div className="scrubber" aria-live="polite">
      <span className="scrubber-label">{solved ? 'Solved' : movesDone === 0 ? 'Scrambled' : 'Solving'}</span>
      <span className="scrubber-ticks" aria-hidden="true">
        {solution.map((move, i) => (
          <span key={i} className={`tick${i < movesDone ? ' is-done' : ''}${i === movesDone ? ' is-current' : ''}`} />
        ))}
      </span>
      <span className="scrubber-count">
        {String(movesDone).padStart(2, '0')}/{String(total).padStart(2, '0')}
      </span>
      <span className="scrubber-next">
        {solved ? (
          <>in {total} moves</>
        ) : (
          <>
            next <b>{moveNotation(next)}</b>
          </>
        )}
      </span>
    </div>
  );
}
