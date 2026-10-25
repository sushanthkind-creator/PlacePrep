import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getTopic, setTopicCompleted } from '../api/learning.js';
import { listTests } from '../api/tests.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import { IconArrowLeft, IconArrowRight, IconCheck } from '../components/icons.jsx';
import Loading from '../components/Loading.jsx';
import { formatPercent } from '../utils/formatting.js';
import { sectionPath, topicStatus } from '../utils/sections.js';
import useAsync from '../utils/useAsync.js';
import '../styles/learning.css';

const RULES_HEADING = { quant: 'Formulas', verbal: 'Rules', logical: 'Rules and patterns' };

export default function LessonPage() {
  const { slug } = useParams();
  const { status, data, error, reload, setData } = useAsync(
    () => Promise.all([getTopic(slug), listTests({ topic: slug })]).then(([t, l]) => ({ topic: t.topic, test: l.tests[0] })),
    [slug],
  );
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  if (status === 'loading' && !data) return <Loading label="Loading lesson…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const { topic, test } = data;
  const { lesson, section, progress } = topic;

  async function toggleCompleted() {
    setSaving(true);
    setSaveError(null);
    try {
      const res = await setTopicCompleted(slug, !progress.completed);
      setData((d) => ({ ...d, topic: { ...d.topic, progress: res.progress } }));
    } catch (err) {
      setSaveError(err);
    } finally {
      setSaving(false);
    }
  }

  const state = topicStatus(progress);

  return (
    <div className="page lesson" data-tone={section.slug}>
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <Link to={sectionPath(section.slug)}>{section.short_name}</Link>
        <span aria-hidden="true">/</span>
        <span aria-current="page">{topic.name}</span>
      </nav>

      <header className="lesson-header">
        <p className="eyebrow tone-text">{section.short_name} · Lesson</p>
        <h1>{topic.name}</h1>
        <p className="lede">{topic.summary}</p>
        <span className={`status status--${state.tone}`}>{state.label}</span>
      </header>

      <div className="lesson-layout">
        <article className="lesson-body">
          <section aria-labelledby="concept-heading" className="lesson-section reading">
            <h2 id="concept-heading">The idea</h2>
            {lesson.concept.split(/\n\s*\n/).map((para, i) => (
              <p key={i}>{para.trim()}</p>
            ))}
          </section>

          <section aria-labelledby="remember-heading" className="lesson-section">
            <h2 id="remember-heading">Remember</h2>
            <ul className="key-points reading">
              {lesson.key_points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
          </section>

          {lesson.formulas.length > 0 && (
            <section aria-labelledby="rules-heading" className="lesson-section">
              <h2 id="rules-heading">{RULES_HEADING[section.slug]}</h2>
              <div className="formula-grid">
                {lesson.formulas.map((f) => (
                  <div key={f.label} className="formula-card">
                    <p className="formula-label">{f.label}</p>
                    <p className="formula">{f.formula}</p>
                    {f.note && <p className="formula-note">{f.note}</p>}
                  </div>
                ))}
              </div>
            </section>
          )}

          {lesson.tips.length > 0 && (
            <section aria-labelledby="tips-heading" className="lesson-section">
              <h2 id="tips-heading">Shortcuts and traps</h2>
              <ul className="tips reading">
                {lesson.tips.map((tip) => (
                  <li key={tip}>{tip}</li>
                ))}
              </ul>
            </section>
          )}

          <section aria-labelledby="examples-heading" className="lesson-section">
            <h2 id="examples-heading">Solved examples</h2>
            {topic.examples.map((example, i) => (
              <div key={example.id} className="example">
                <p className="example-label">Example {i + 1}</p>
                <p className="example-problem reading">{example.problem}</p>
                <ol className="example-steps reading">
                  {example.steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ol>
                <p className="example-answer">
                  <span>Answer</span>
                  {example.answer}
                </p>
              </div>
            ))}
          </section>
        </article>

        <aside className="lesson-aside" aria-label="Lesson actions">
          <div className="panel lesson-actions">
            <h2 className="sub-title">After this lesson</h2>
            <button
              type="button"
              className={`btn ${progress.completed ? 'btn-done' : 'btn-primary'}`}
              onClick={toggleCompleted}
              disabled={saving}
              aria-pressed={progress.completed}
            >
              {progress.completed ? (
                <>
                  <IconCheck /> Completed
                </>
              ) : (
                'Mark as completed'
              )}
            </button>
            {progress.completed && <p className="muted small">Select again to mark it as not completed.</p>}
            <ErrorMessage error={saveError} compact />
            <Link to={`/topics/${slug}/practice`} className="btn btn-secondary">
              Practice questions
            </Link>
            {test && (
              <Link to={`/tests/${test.id}`} className="btn btn-ghost">
                Take the topic test
              </Link>
            )}
            <dl className="mini-stats">
              <div>
                <dt>Practice</dt>
                <dd>
                  {progress.practice.correct}/{progress.practice.total} correct
                </dd>
              </div>
              <div>
                <dt>Best test</dt>
                <dd>{progress.best_topic_test === null ? 'Not taken' : formatPercent(progress.best_topic_test)}</dd>
              </div>
            </dl>
          </div>
        </aside>
      </div>

      <nav className="pager" aria-label="Other topics">
        {topic.previous ? (
          <Link to={`/topics/${topic.previous.slug}`} className="pager-link">
            <IconArrowLeft />
            <span>
              <span className="muted">Previous</span>
              {topic.previous.name}
            </span>
          </Link>
        ) : (
          <span />
        )}
        {topic.next && (
          <Link to={`/topics/${topic.next.slug}`} className="pager-link pager-link--next">
            <span>
              <span className="muted">Next</span>
              {topic.next.name}
            </span>
            <IconArrowRight />
          </Link>
        )}
      </nav>
    </div>
  );
}
