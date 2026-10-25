import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { checkPracticeAnswer, getPractice } from '../api/learning.js';
import { listTests } from '../api/tests.js';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import QuestionCard from '../components/QuestionCard.jsx';
import { sectionPath } from '../utils/sections.js';
import useAsync from '../utils/useAsync.js';
import '../styles/learning.css';
import '../styles/test.css';

export default function PracticePage() {
  const { slug } = useParams();
  const { status, data, error, reload, setData } = useAsync(
    () => Promise.all([getPractice(slug), listTests({ topic: slug })]).then(([p, l]) => ({ ...p, test: l.tests[0] })),
    [slug],
  );
  const [selected, setSelected] = useState({});
  const [retrying, setRetrying] = useState({});
  const [checking, setChecking] = useState({});
  const [checkErrors, setCheckErrors] = useState({});

  if (status === 'loading' && !data) return <Loading label="Loading practice questions…" />;
  if (status === 'error') return <ErrorMessage error={error} onRetry={reload} />;

  const { topic, questions, test } = data;
  const answered = questions.filter((q) => q.review).length;
  const correct = questions.filter((q) => q.review?.is_correct).length;

  async function check(question) {
    const optionId = selected[question.id];
    if (!optionId) return;
    setChecking((c) => ({ ...c, [question.id]: true }));
    setCheckErrors((e) => ({ ...e, [question.id]: null }));
    try {
      const res = await checkPracticeAnswer(question.id, optionId);
      setData((d) => ({ ...d, questions: d.questions.map((q) => (q.id === question.id ? { ...q, review: res.review } : q)) }));
      setRetrying((r) => ({ ...r, [question.id]: false }));
    } catch (err) {
      setCheckErrors((e) => ({ ...e, [question.id]: err }));
    } finally {
      setChecking((c) => ({ ...c, [question.id]: false }));
    }
  }

  function tryAgain(questionId) {
    setRetrying((r) => ({ ...r, [questionId]: true }));
    setSelected((s) => ({ ...s, [questionId]: undefined }));
  }

  return (
    <div className="page practice" data-tone={topic.section.slug}>
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <Link to={sectionPath(topic.section.slug)}>{topic.section.short_name}</Link>
        <span aria-hidden="true">/</span>
        <Link to={`/topics/${slug}`}>{topic.name}</Link>
        <span aria-hidden="true">/</span>
        <span aria-current="page">Practice</span>
      </nav>

      <header className="practice-header">
        <div>
          <p className="eyebrow tone-text">Practice</p>
          <h1>{topic.name}</h1>
          <p className="lede">Choose an answer and check it. You'll see the correct answer and an explanation straight away.</p>
        </div>
        <p className="practice-score" aria-live="polite">
          <span className="mono">
            {correct}/{questions.length}
          </span>{' '}
          correct
          <span className="muted"> · {answered} checked</span>
        </p>
      </header>

      <div className="question-stack">
        {questions.map((question, i) => {
          const showReview = question.review && !retrying[question.id];
          return (
            <QuestionCard
              key={question.id}
              question={question}
              number={i + 1}
              total={questions.length}
              mode={showReview ? 'review' : 'answer'}
              review={showReview ? question.review : null}
              selectedOptionId={showReview ? question.review.selected_option_id : selected[question.id]}
              onSelect={(optionId) => setSelected((s) => ({ ...s, [question.id]: optionId }))}
            >
              <div className="question-actions">
                {showReview ? (
                  <button type="button" className="btn btn-ghost btn-sm" onClick={() => tryAgain(question.id)}>
                    Try again
                  </button>
                ) : (
                  <button
                    type="button"
                    className="btn btn-primary btn-sm"
                    onClick={() => check(question)}
                    disabled={!selected[question.id] || checking[question.id]}
                  >
                    {checking[question.id] ? 'Checking…' : 'Check answer'}
                  </button>
                )}
              </div>
              <ErrorMessage error={checkErrors[question.id]} compact />
            </QuestionCard>
          );
        })}
      </div>

      <div className="panel practice-next">
        <p>
          {answered === questions.length
            ? 'All practice questions checked. Ready to test yourself?'
            : 'When you feel confident, take the timed topic test.'}
        </p>
        <div className="header-actions">
          <Link to={`/topics/${slug}`} className="btn btn-ghost">
            Back to lesson
          </Link>
          {test && (
            <Link to={`/tests/${test.id}`} className="btn btn-secondary">
              Take the topic test
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
