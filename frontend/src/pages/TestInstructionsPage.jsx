import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { getTest, startAttempt } from '../api/tests.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import { formatPercent } from '../utils/formatting.js';
import { sectionPath } from '../utils/sections.js';
import useAsync from '../utils/useAsync.js';
import '../styles/test.css';

const DURATION_PRESETS = [3, 5, 7, 10, 15, 20, 25, 30, 40, 45, 60, 90, 120, 180];

function countOptions([low, high], preferred) {
  if (high - low <= 12) return Array.from({ length: high - low + 1 }, (_, i) => low + i);
  const steps = new Set([low, high, preferred]);
  for (let n = 5; n < high; n += 5) if (n > low) steps.add(n);
  return [...steps].sort((a, b) => a - b);
}

export default function TestInstructionsPage() {
  const { testId } = useParams();
  const navigate = useNavigate();
  const { status, data, error, reload } = useAsync(() => getTest(testId).then((r) => r.test), [testId]);
  const [count, setCount] = useState(null);
  const [minutes, setMinutes] = useState(null);
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState(null);

  useEffect(() => {
    if (data) {
      setCount(data.default_question_count);
      setMinutes(data.default_duration_minutes);
    }
  }, [data]);

  const counts = useMemo(() => (data ? countOptions(data.question_count_range, data.default_question_count) : []), [data]);
  const durations = useMemo(() => {
    if (!data) return [];
    const [low, high] = data.duration_range;
    return [...new Set([...DURATION_PRESETS, data.default_duration_minutes])].filter((m) => m >= low && m <= high).sort((a, b) => a - b);
  }, [data]);

  if (status === 'loading' && !data) return <Loading label="Loading test…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;
  const test = data;

  async function handleStart(e) {
    e.preventDefault();
    setStarting(true);
    setStartError(null);
    try {
      const res = await startAttempt(test.id, { question_count: count, duration_minutes: minutes });
      navigate(`/attempts/${res.attempt.id}`, { state: { resumed: res.resumed } });
    } catch (err) {
      setStartError(err);
      setStarting(false);
    }
  }

  const backLink = test.section_slug ? sectionPath(test.section_slug) : '/tests';

  return (
    <div className="page instructions" data-tone={test.section_slug || 'mixed'}>
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <Link to="/tests">Tests</Link>
        <span aria-hidden="true">/</span>
        <span aria-current="page">{test.title}</span>
      </nav>

      <header className="page-header">
        <p className="eyebrow tone-text">
          {test.scope === 'mixed' ? 'All sections' : test.scope === 'section' ? `${test.section_name} · section test` : `${test.topic_name} · topic test`}
        </p>
        <h1>{test.title}</h1>
        <p className="lede">{test.description}</p>
        {test.my_stats.attempts > 0 && (
          <p className="muted">
            You've taken this test {test.my_stats.attempts} time{test.my_stats.attempts > 1 ? 's' : ''}. Best score{' '}
            {formatPercent(test.my_stats.best)}, last {formatPercent(test.my_stats.last)}.
          </p>
        )}
      </header>

      <div className="instructions-layout">
        <section className="panel" aria-labelledby="rules-heading">
          <h2 id="rules-heading" className="block-title">
            Before you start
          </h2>
          <ul className="rule-list">
            {test.instructions.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </section>

        <form className="panel settings-form" onSubmit={handleStart} aria-labelledby="settings-heading">
          <h2 id="settings-heading" className="block-title">
            Test settings
          </h2>
          {test.active_attempt_id ? (
            <p className="notice">
              You have an unfinished attempt of this test. Starting continues that attempt with its original settings and timer.
            </p>
          ) : null}
          <div className="field">
            <label htmlFor="question-count">Number of questions</label>
            <select id="question-count" value={count ?? ''} onChange={(e) => setCount(Number(e.target.value))} disabled={!!test.active_attempt_id}>
              {counts.map((n) => (
                <option key={n} value={n}>
                  {n} questions
                </option>
              ))}
            </select>
            <p className="field-hint">{test.available_questions} questions are available for this test.</p>
          </div>
          <div className="field">
            <label htmlFor="duration">Time limit</label>
            <select id="duration" value={minutes ?? ''} onChange={(e) => setMinutes(Number(e.target.value))} disabled={!!test.active_attempt_id}>
              {durations.map((m) => (
                <option key={m} value={m}>
                  {m} minutes
                </option>
              ))}
            </select>
            {count && minutes ? (
              <p className="field-hint">About {Math.round((minutes * 60) / count)} seconds per question.</p>
            ) : null}
          </div>
          <ErrorMessage error={startError} compact />
          <button type="submit" className="btn btn-primary" disabled={starting || !count || !minutes}>
            {starting ? 'Starting…' : test.active_attempt_id ? 'Resume test' : 'Start test'}
          </button>
          <Link to={backLink} className="btn btn-ghost">
            Not now
          </Link>
        </form>
      </div>
    </div>
  );
}
