import { useState } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { getResult } from '../api/tests.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import QuestionCard from '../components/QuestionCard.jsx';
import { formatDateTime, formatDuration, formatPercent } from '../utils/formatting.js';
import useAsync from '../utils/useAsync.js';
import '../styles/test.css';

const FILTERS = [
  { value: 'all', label: 'All' },
  { value: 'incorrect', label: 'Incorrect' },
  { value: 'unanswered', label: 'Unanswered' },
  { value: 'correct', label: 'Correct' },
];

function matches(question, filter) {
  if (filter === 'correct') return question.is_correct === true;
  if (filter === 'incorrect') return question.is_correct === false;
  if (filter === 'unanswered') return question.selected_option_id === null;
  return true;
}

function BreakdownTable({ rows, caption, linkTopics }) {
  return (
    <div className="data-table-wrap">
      <table className="data-table breakdown-table">
        <caption className="sr-only">{caption}</caption>
        <thead>
          <tr>
            <th scope="col">{linkTopics ? 'Topic' : 'Section'}</th>
            <th scope="col">Correct</th>
            <th scope="col">Wrong</th>
            <th scope="col">Skipped</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.slug} data-tone={row.section_slug || row.slug}>
              <th scope="row">
                {linkTopics ? <Link to={`/topics/${row.slug}/practice`}>{row.name}</Link> : row.name}
              </th>
              <td>
                {row.correct}/{row.total}
              </td>
              <td>{row.incorrect}</td>
              <td>{row.unanswered}</td>
              <td>
                <span className="bar" aria-hidden="true">
                  <span style={{ width: `${row.percentage}%` }} />
                </span>
                <span className="mono">{formatPercent(row.percentage)}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function TestResultsPage() {
  const { attemptId } = useParams();
  const location = useLocation();
  const { status, data, error, reload } = useAsync(() => getResult(attemptId).then((r) => r.attempt), [attemptId]);
  const [filter, setFilter] = useState('all');

  if (status === 'loading' && !data) return <Loading label="Loading results…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const attempt = data;
  const shown = attempt.questions.filter((q) => matches(q, filter));
  const { breakdown } = attempt;

  return (
    <div className="page results" data-tone={attempt.test.section_slug || 'mixed'}>
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <Link to="/history">Test history</Link>
        <span aria-hidden="true">/</span>
        <span aria-current="page">Result</span>
      </nav>

      <header className="result-hero">
        <div>
          <p className="eyebrow tone-text">Result · {formatDateTime(attempt.submitted_at)}</p>
          <h1>{attempt.test.title}</h1>
          {(attempt.auto_submitted || location.state?.auto) && (
            <p className="notice">Time ran out, so this test was submitted automatically with the answers saved by then.</p>
          )}
          <div className="header-actions">
            <Link to={`/tests/${attempt.test.id}`} className="btn btn-primary">
              Retake test
            </Link>
            <Link to="/tests" className="btn btn-secondary">
              All tests
            </Link>
          </div>
        </div>
        <div className="score-block">
          <p className="score-value mono">{formatPercent(attempt.percentage, 1)}</p>
          <dl className="score-counts">
            <div className="is-correct">
              <dt>Correct</dt>
              <dd>{attempt.correct}</dd>
            </div>
            <div className="is-wrong">
              <dt>Incorrect</dt>
              <dd>{attempt.incorrect}</dd>
            </div>
            <div>
              <dt>Unanswered</dt>
              <dd>{attempt.unanswered}</dd>
            </div>
            <div>
              <dt>Time taken</dt>
              <dd>
                {formatDuration(attempt.time_taken_seconds)}
                <span className="muted"> / {formatDuration(attempt.duration_seconds)}</span>
              </dd>
            </div>
          </dl>
        </div>
      </header>

      <div className="breakdown-grid">
        <section className="panel" aria-labelledby="sections-heading">
          <h2 id="sections-heading" className="block-title">
            By section
          </h2>
          <BreakdownTable rows={breakdown.sections} caption="Score by section" />
        </section>
        <section className="panel" aria-labelledby="topics-heading">
          <h2 id="topics-heading" className="block-title">
            By topic
          </h2>
          <BreakdownTable rows={breakdown.topics} caption="Score by topic" linkTopics />
          <p className="muted small">Select a topic to practise it.</p>
        </section>
      </div>

      <section aria-labelledby="review-heading">
        <div className="panel-head">
          <h2 id="review-heading" className="block-title">
            Answers and explanations
          </h2>
          <div className="filter-chips" role="group" aria-label="Filter questions">
            {FILTERS.map((f) => (
              <button key={f.value} type="button" className="chip-btn" aria-pressed={filter === f.value} onClick={() => setFilter(f.value)}>
                {f.label}
              </button>
            ))}
          </div>
        </div>
        {shown.length === 0 ? (
          <p className="muted">No questions in this group.</p>
        ) : (
          <div className="question-stack">
            {shown.map((q) => (
              <QuestionCard
                key={q.id}
                question={q}
                number={q.position}
                total={attempt.question_count}
                mode="review"
                selectedOptionId={q.selected_option_id}
                review={q}
                headingLevel={3}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
