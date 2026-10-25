import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHistory } from '../api/tests.js';
import EmptyState from '../components/EmptyState.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import ProgressChart from '../components/ProgressChart.jsx';
import { formatChange, formatDateTime, formatDuration, formatPercent } from '../utils/formatting.js';
import '../styles/test.css';

const PER_PAGE = 20;

export default function TestHistoryPage() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    setStatus('loading');
    getHistory(page, PER_PAGE)
      .then((res) => {
        if (!active) return;
        setItems((prev) => (page === 1 ? res.attempts : [...prev, ...res.attempts]));
        setTotal(res.total);
        setStatus('success');
      })
      .catch((err) => {
        if (!active) return;
        setError(err);
        setStatus('error');
      });
    return () => {
      active = false;
    };
  }, [page]);

  if (status === 'loading' && items.length === 0) return <Loading label="Loading your test history…" />;
  if (status === 'error' && items.length === 0) return <ErrorMessage error={error} onRetry={() => setPage(1)} />;

  const chronological = [...items].reverse().map((a) => ({
    id: a.id,
    title: a.test.title,
    percentage: a.percentage,
    submitted_at: a.submitted_at,
  }));

  return (
    <div className="page history">
      <header className="page-header">
        <h1>Test history</h1>
        <p className="lede">Every test you've submitted, newest first, with the change since your previous attempt of the same test.</p>
      </header>

      {total === 0 ? (
        <EmptyState title="No submitted tests yet" action={<Link to="/tests" className="btn btn-primary">Take your first test</Link>}>
          Your results will be saved here after you submit a test.
        </EmptyState>
      ) : (
        <>
          {chronological.length >= 2 && (
            <section className="panel" aria-labelledby="history-chart-heading">
              <h2 id="history-chart-heading" className="block-title">
                Scores over time
              </h2>
              <ProgressChart points={chronological} />
            </section>
          )}

          <section aria-labelledby="attempts-heading">
            <h2 id="attempts-heading" className="block-title">
              Attempts <span className="muted">({total})</span>
            </h2>
            <div className="data-table-wrap">
              <table className="data-table history-table">
                <thead>
                  <tr>
                    <th scope="col">Test</th>
                    <th scope="col">Submitted</th>
                    <th scope="col">Score</th>
                    <th scope="col">Correct</th>
                    <th scope="col">Time</th>
                    <th scope="col">Change</th>
                    <th scope="col">
                      <span className="sr-only">Details</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((a) => {
                    const change = formatChange(a.change);
                    return (
                      <tr key={a.id} data-tone={a.test.section_slug || 'mixed'}>
                        <th scope="row">
                          <span className="sticker sticker--static is-done" aria-hidden="true" /> {a.test.title}
                        </th>
                        <td>{formatDateTime(a.submitted_at)}</td>
                        <td className="mono">{formatPercent(a.percentage, 1)}</td>
                        <td>
                          {a.correct}/{a.question_count}
                        </td>
                        <td>{formatDuration(a.time_taken_seconds)}</td>
                        <td>
                          <span className={`change change--${change.tone}`}>{change.label}</span>
                        </td>
                        <td>
                          <Link to={`/attempts/${a.id}/result`} className="text-link" aria-label={`View result of ${a.test.title}`}>
                            View
                          </Link>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            {items.length < total && (
              <button type="button" className="btn btn-secondary load-more" onClick={() => setPage((p) => p + 1)} disabled={status === 'loading'}>
                {status === 'loading' ? 'Loading…' : 'Load more'}
              </button>
            )}
            {status === 'error' && <ErrorMessage error={error} compact />}
          </section>
        </>
      )}
    </div>
  );
}
