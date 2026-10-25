import { Link } from 'react-router-dom';
import { getSection } from '../api/learning.js';
import { listTests } from '../api/tests.js';
import { formatPercent } from '../utils/formatting.js';
import { topicStatus } from '../utils/sections.js';
import useAsync from '../utils/useAsync.js';
import ErrorMessage from './ErrorMessage.jsx';
import Loading from './Loading.jsx';
import StickerFace from './StickerFace.jsx';
import '../styles/learning.css';

export default function SectionView({ slug }) {
  const { status, data, error, reload } = useAsync(
    () => Promise.all([getSection(slug), listTests({ section: slug })]),
    [slug],
  );

  if (status === 'loading' && !data) return <Loading label="Loading topics…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const [{ section }, { tests }] = data;
  const sectionTest = tests.find((t) => t.scope === 'section');
  const topicTests = Object.fromEntries(tests.filter((t) => t.scope === 'topic').map((t) => [t.topic_slug, t]));
  const nextTopic = section.topics.find((t) => !t.completed);

  return (
    <div className="page" data-tone={slug}>
      <header className="section-hero">
        <div className="section-hero-text">
          <p className="eyebrow tone-text">{section.short_name} section</p>
          <h1>{section.name}</h1>
          <p className="lede">{section.description}</p>
          <div className="header-actions">
            {nextTopic ? (
              <Link to={`/topics/${nextTopic.slug}`} className="btn btn-primary">
                {section.topics_completed ? 'Continue' : 'Start'}: {nextTopic.name}
              </Link>
            ) : (
              <span className="status status--done">All topics completed</span>
            )}
            {sectionTest && (
              <Link to={`/tests/${sectionTest.id}`} className="btn btn-secondary">
                Take section test
              </Link>
            )}
          </div>
        </div>
        <div className="section-hero-face">
          <StickerFace tone={slug} topics={section.topics} size="lg" />
          <p className="muted">
            {section.topics_completed} of {section.topics_total} topics completed
            {section.test_questions ? ` · ${formatPercent(section.test_percentage)} test accuracy` : ''}
          </p>
        </div>
      </header>

      <section aria-labelledby="topics-heading">
        <h2 id="topics-heading" className="block-title">
          Topics <span className="muted">in suggested order</span>
        </h2>
        <ol className="topic-list">
          {section.topics.map((topic) => {
            const state = topicStatus(topic);
            const test = topicTests[topic.slug];
            return (
              <li key={topic.slug} className="topic-row">
                <span className={`sticker sticker--static${topic.completed ? ' is-done' : ''}`} aria-hidden="true" />
                <div className="topic-row-main">
                  <h3>
                    <Link to={`/topics/${topic.slug}`}>{topic.name}</Link>
                  </h3>
                  <p className="topic-row-summary">{topic.summary}</p>
                  <p className="topic-row-meta">
                    <span className={`status status--${state.tone}`}>{state.label}</span>
                    <span>
                      Practice {topic.practice.attempted}/{topic.practice.total}
                    </span>
                    {topic.best_topic_test !== null && <span>Best test {formatPercent(topic.best_topic_test)}</span>}
                  </p>
                </div>
                <div className="topic-row-actions">
                  <Link to={`/topics/${topic.slug}`} className="btn btn-sm btn-secondary" aria-label={`Study ${topic.name}`}>
                    Study
                  </Link>
                  <Link to={`/topics/${topic.slug}/practice`} className="btn btn-sm btn-ghost" aria-label={`Practice ${topic.name}`}>
                    Practice
                  </Link>
                  {test && (
                    <Link to={`/tests/${test.id}`} className="btn btn-sm btn-ghost" aria-label={`Take the ${topic.name} test`}>
                      Test
                    </Link>
                  )}
                </div>
              </li>
            );
          })}
        </ol>
      </section>
    </div>
  );
}
