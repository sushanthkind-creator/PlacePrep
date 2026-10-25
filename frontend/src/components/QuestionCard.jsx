import { IconCheck, IconCross } from './icons.jsx';

function DataTable({ table }) {
  return (
    <div className="data-table-wrap">
      <table className="data-table">
        {table.caption && <caption>{table.caption}</caption>}
        <thead>
          <tr>
            {table.columns.map((c) => (
              <th key={c} scope="col">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table.rows.map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) => (j === 0 ? <th key={j} scope="row">{cell}</th> : <td key={j}>{cell}</td>))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/**
 * One multiple-choice question.
 * mode: "answer" (choose freely) or "review" (show the correct answer and explanation).
 */
export default function QuestionCard({
  question,
  number,
  total,
  selectedOptionId,
  onSelect,
  mode = 'answer',
  review = null,
  disabled = false,
  headingLevel = 2,
  children,
}) {
  const Heading = `h${headingLevel}`;
  const reviewing = mode === 'review' && review;
  const groupName = `q-${question.id}`;

  return (
    <article className="question-card" aria-labelledby={`${groupName}-title`}>
      <header className="question-meta">
        <Heading id={`${groupName}-title`} className="question-number">
          Question {number}
          {total ? <span className="muted"> of {total}</span> : null}
        </Heading>
        <span className={`chip chip--${question.difficulty}`}>{question.difficulty}</span>
      </header>

      {question.passage && (
        <details className="passage" open>
          <summary>Passage: {question.passage.title}</summary>
          <div className="passage-body">
            {question.passage.body.split('\n\n').map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>
        </details>
      )}

      {question.table && <DataTable table={question.table} />}

      <p className="question-prompt">{question.prompt}</p>

      <fieldset className="options" disabled={disabled || mode === 'review'}>
        <legend className="sr-only">Choose one answer</legend>
        {question.options.map((option) => {
          const checked = selectedOptionId === option.id;
          const isCorrect = reviewing && option.id === review.correct_option_id;
          const isWrongPick = reviewing && checked && !isCorrect;
          const state = isCorrect ? ' is-correct' : isWrongPick ? ' is-wrong' : checked ? ' is-selected' : '';
          return (
            <label key={option.id} className={`option${state}`}>
              <input
                type="radio"
                name={groupName}
                value={option.id}
                checked={checked}
                onChange={() => onSelect?.(option.id)}
              />
              <span className="option-label" aria-hidden="true">
                {option.label}
              </span>
              <span className="option-text">{option.text}</span>
              {isCorrect && (
                <span className="option-flag">
                  <IconCheck /> Correct answer
                </span>
              )}
              {isWrongPick && (
                <span className="option-flag">
                  <IconCross /> Your answer
                </span>
              )}
            </label>
          );
        })}
      </fieldset>

      {reviewing && (
        <div className={`explanation${review.is_correct ? ' is-correct' : review.selected_option_id ? ' is-wrong' : ''}`}>
          <p className="explanation-verdict">
            {review.is_correct ? 'Correct.' : review.selected_option_id ? 'Not quite.' : 'Not answered.'}
          </p>
          <p>{review.explanation}</p>
        </div>
      )}

      {children}
    </article>
  );
}
