import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { listTests } from '../api/tests.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import { formatPercent } from '../utils/formatting.js';
import useAsync from '../utils/useAsync.js';
import useTilt from '../utils/useTilt.js';
import '../styles/test.css';

const FILTERS = [
  { value: 'all', label: 'All' },
  { value: 'logical', label: 'Logical' },
  { value: 'quant', label: 'Quant' },
  { value: 'verbal', label: 'Verbal' },
];

function TestAction({ test }) {
  if (test.active_attempt_id) {
    return (
      <Link to={`/attempts/${test.active_attempt_id}`} className="btn btn-primary btn-sm">
        Resume
      </Link>
    );
  }
  return (
    <Link to={`/tests/${test.id}`} className="btn btn-secondary btn-sm" aria-label={`Start ${test.title}`}>
      Start
    </Link>
  );
}

function Stats({ stats }) {
  if (!stats.attempts) return <span className="muted">Not attempted</span>;
  return (
    <span>
      Best <span className="mono">{formatPercent(stats.best)}</span>
      <span className="muted"> · {stats.attempts}×</span>
    </span>
  );
}

function TestCard({ test }) {
  const ref = useRef(null);
  useTilt(ref);
  return (
    <article ref={ref} className="test-card tilt-card" data-tone={test.section_slug || 'mixed'} data-tilt>
      <p className="eyebrow tone-text">{test.scope === 'mixed' ? 'All sections' : test.section_name}</p>
      <h3>{test.title}</h3>
      <p className="muted">{test.description}</p>
      <p className="test-card-meta mono">
        {test.default_question_count} Q · {test.default_duration_minutes} min
      </p>
      <div className="test-card-foot">
        <Stats stats={test.my_stats} />
        <TestAction test={test} />
      </div>
    </article>
  );
}

export default function TestsPage() {
  const { status, data, error, reload } = useAsync(() => listTests(), []);
  const [filter, setFilter] = useState('all');

  if (status === 'loading' && !data) return <Loading label="Loading tests…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const tests = data.tests;
  const featured = tests.filter((t) => t.scope !== 'topic');
  const topicTests = tests.filter((t) => t.scope === 'topic' && (filter === 'all' || t.section_slug === filter));

  return (
    <div className="page tests-page">
      <header className="page-header">
        <h1>Tests</h1>
        <p className="lede">
          Timed multiple-choice tests, scored on the server. Choose how many questions and how long you want before you start.
        </p>
      </header>

      <section aria-labelledby="full-heading">
        <h2 id="full-heading" className="block-title">
          Mock and section tests
        </h2>
        <div className="test-card-grid">
          {featured.map((test) => (
            <TestCard key={test.id} test={test} />
          ))}
        </div>
      </section>

      <section aria-labelledby="topic-tests-heading">
        <div className="panel-head">
          <h2 id="topic-tests-heading" className="block-title">
            Topic tests
          </h2>
          <div className="filter-chips" role="group" aria-label="Filter topic tests by section">
            {FILTERS.map((f) => (
              <button
                key={f.value}
                type="button"
                className="chip-btn"
                aria-pressed={filter === f.value}
                onClick={() => setFilter(f.value)}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>
        <ul className="topic-test-list">
          {topicTests.map((test) => (
            <li key={test.id} className="topic-test-row" data-tone={test.section_slug}>
              <span className="sticker sticker--static is-done" aria-hidden="true" />
              <span className="topic-test-name">
                {test.topic_name}
                <span className="muted mono">
                  {test.default_question_count} Q · {test.default_duration_minutes} min
                </span>
              </span>
              <Stats stats={test.my_stats} />
              <TestAction test={test} />
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
