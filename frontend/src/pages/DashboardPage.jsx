import { Link } from 'react-router-dom';
import { getDashboard } from '../api/dashboard.js';
import EmptyState from '../components/EmptyState.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';
import TiltPanel from '../components/TiltPanel.jsx';
import LearningCard from '../components/LearningCard.jsx';
import Loading from '../components/Loading.jsx';
import ProgressChart from '../components/ProgressChart.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { firstName, formatChange, formatDateTime, formatPercent, plural } from '../utils/formatting.js';
import { sectionPath } from '../utils/sections.js';
import useAsync from '../utils/useAsync.js';
import '../styles/dashboard.css';

function nextTopic(sections) {
  for (const section of sections) {
    const topic = section.topics.find((t) => !t.completed);
    if (topic) return topic;
  }
  return null;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const { status, data, error, reload } = useAsync(getDashboard, []);

  if (status === 'loading' && !data) return <Loading label="Loading your dashboard…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const { progress, sections, recent_results: recent, trend, strongest_section: strongest, weak_topics: weak, thresholds } = data;
  const isNew = data.tests_attempted === 0 && progress.topics_completed === 0 && progress.practice_attempted === 0;
  const upNext = nextTopic(sections);

  return (
    <div className="page dashboard">
      <header className="dash-header">
        <div>
          <h1>
            {isNew ? 'Welcome' : 'Welcome back'}, {firstName(data.user.full_name)}.
          </h1>
          <p className="lede">
            {isNew
              ? 'Pick a section and start with its first topic. Your progress and scores will appear here as you go.'
              : `You've completed ${progress.topics_completed} of ${progress.topics_total} topics and taken ${plural(data.tests_attempted, 'test')}.`}
          </p>
        </div>
        <div className="header-actions">
          <Link to={upNext ? `/topics/${upNext.slug}` : sectionPath('logical')} className="btn btn-primary">
            {isNew ? 'Start learning' : upNext ? `Continue: ${upNext.name}` : 'Review topics'}
          </Link>
          <Link to="/tests" className="btn btn-secondary">
            Take a test
          </Link>
        </div>
      </header>

      <section className="cube-panel" aria-labelledby="cube-heading">
        <div className="cube-panel-head">
          <div>
            <h2 id="cube-heading" className="block-title">
              Your cube
            </h2>
            <p className="muted">Each sticker is a topic. Finish its lesson to fill it in.</p>
          </div>
          <p className="cube-progress">
            <span className="mono">
              {progress.topics_completed}/{progress.topics_total}
            </span>{' '}
            topics · <span className="mono">{progress.percent}%</span>
          </p>
        </div>
        <div className="learning-grid">
          {sections.map((section) => (
            <LearningCard key={section.slug} section={section} />
          ))}
        </div>
      </section>

      <dl className="stat-strip" aria-label="Your numbers">
        <div>
          <dt>Tests taken</dt>
          <dd>{data.tests_attempted}</dd>
        </div>
        <div>
          <dt>Average score</dt>
          <dd>{data.average_percentage === null ? '—' : formatPercent(data.average_percentage, 1)}</dd>
        </div>
        <div>
          <dt>Learning progress</dt>
          <dd>{progress.percent}%</dd>
        </div>
        <div>
          <dt>Practice answered</dt>
          <dd>
            {progress.practice_attempted}
            <span className="muted">/{progress.practice_total}</span>
          </dd>
        </div>
      </dl>

      <div className="dash-grid">
        <TiltPanel className="panel" aria-labelledby="recent-heading">
          <div className="panel-head">
            <h2 id="recent-heading" className="block-title">
              Recent results
            </h2>
            {recent.length > 0 && (
              <Link to="/history" className="text-link">
                View history
              </Link>
            )}
          </div>
          {recent.length === 0 ? (
            <EmptyState title="No tests yet" action={<Link to="/tests" className="btn btn-secondary btn-sm">Browse tests</Link>}>
              Take a topic test after studying a lesson. Your scores will show up here.
            </EmptyState>
          ) : (
            <ul className="result-list">
              {recent.map((attempt) => {
                const change = formatChange(attempt.change);
                return (
                  <li key={attempt.id}>
                    <Link to={`/attempts/${attempt.id}/result`} className="result-row">
                      <span className="result-title">
                        {attempt.test.title}
                        <span className="muted">{formatDateTime(attempt.submitted_at)}</span>
                      </span>
                      <span className="result-score mono">{formatPercent(attempt.percentage)}</span>
                      <span className={`change change--${change.tone}`}>{change.label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          )}
        </TiltPanel>

        <TiltPanel className="panel" aria-labelledby="trend-heading">
          <h2 id="trend-heading" className="block-title">
            Score trend
          </h2>
          {trend.length < 2 ? (
            <EmptyState title="Not enough tests yet">
              Your scores over time appear here after two or more tests.
            </EmptyState>
          ) : (
            <ProgressChart points={trend} />
          )}
        </TiltPanel>

        <TiltPanel className="panel" aria-labelledby="strength-heading" tone={strongest?.slug}>
          <h2 id="strength-heading" className="block-title">
            Strengths and gaps
          </h2>
          {strongest ? (
            <p className="strength" data-tone={strongest.slug}>
              <span className="muted">Strongest section</span>
              <Link to={sectionPath(strongest.slug)} className="strength-name tone-text">
                {strongest.name}
              </Link>
              <span className="mono">{formatPercent(strongest.percentage)} correct in tests</span>
            </p>
          ) : (
            <p className="muted small">
              Your strongest section appears once you've answered at least {thresholds.min_section_questions} test questions in a section.
            </p>
          )}

          <h3 className="sub-title">Needs improvement</h3>
          {weak.length ? (
            <ul className="weak-list">
              {weak.map((topic) => (
                <li key={topic.slug} data-tone={topic.section_slug}>
                  <span className="sticker sticker--static" aria-hidden="true" />
                  <span className="weak-name">
                    {topic.name}
                    <span className="muted">
                      {formatPercent(topic.percentage)} of {topic.questions} test questions
                    </span>
                  </span>
                  <Link to={`/topics/${topic.slug}`} className="btn btn-sm btn-ghost" aria-label={`Revise ${topic.name}`}>
                    Revise
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted small">
              {data.tests_attempted
                ? `Nothing flagged. Every topic you've been tested on (with ${thresholds.min_topic_questions}+ questions) is at ${thresholds.weak_below}% or above.`
                : 'Topics where your test accuracy is below 70% will be listed here.'}
            </p>
          )}
        </TiltPanel>

        <TiltPanel className="panel" aria-labelledby="profile-heading">
          <div className="panel-head">
            <h2 id="profile-heading" className="block-title">
              Profile
            </h2>
            <Link to="/profile" className="text-link">
              Edit
            </Link>
          </div>
          <dl className="profile-summary">
            <div>
              <dt>Name</dt>
              <dd>{user.full_name}</dd>
            </div>
            <div>
              <dt>College</dt>
              <dd>{user.college_name}</dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd>{user.email}</dd>
            </div>
            <div>
              <dt>Mobile</dt>
              <dd>{user.mobile}</dd>
            </div>
          </dl>
        </TiltPanel>
      </div>
    </div>
  );
}
