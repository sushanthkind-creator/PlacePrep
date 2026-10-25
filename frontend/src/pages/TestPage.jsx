import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { getAttempt, saveAnswer, submitAttempt } from '../api/tests.js';
import ConfirmDialog from '../components/ConfirmDialog.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';
import { IconArrowLeft, IconArrowRight } from '../components/icons.jsx';
import Loading from '../components/Loading.jsx';
import QuestionCard from '../components/QuestionCard.jsx';
import { BrandMark } from '../components/Sidebar.jsx';
import TestTimer from '../components/TestTimer.jsx';
import useAsync from '../utils/useAsync.js';
import '../styles/test.css';

export default function TestPage() {
  const { attemptId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { status, data, error, reload } = useAsync(() => getAttempt(attemptId).then((r) => r.attempt), [attemptId]);

  const [answers, setAnswers] = useState({});
  const [index, setIndex] = useState(0);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [timeUp, setTimeUp] = useState(false);
  const [saveWarning, setSaveWarning] = useState(false);
  const answersRef = useRef(answers);
  const submittingRef = useRef(false);
  answersRef.current = answers;

  // Already-submitted attempts go straight to their results.
  useEffect(() => {
    if (data?.status === 'submitted') navigate(`/attempts/${attemptId}/result`, { replace: true });
  }, [data, attemptId, navigate]);

  useEffect(() => {
    if (data?.questions) {
      setAnswers(Object.fromEntries(data.questions.map((q) => [q.id, q.selected_option_id])));
    }
  }, [data]);

  // The deadline comes from the server's remaining time, so reloading never resets the clock.
  const deadline = useMemo(() => (data?.remaining_seconds !== undefined ? Date.now() + data.remaining_seconds * 1000 : null), [data]);

  const submit = useCallback(
    async (auto = false) => {
      if (submittingRef.current || !data?.questions) return;
      submittingRef.current = true;
      setSubmitting(true);
      setSubmitError(null);
      const payload = data.questions.map((q) => ({ question_id: q.id, option_id: answersRef.current[q.id] ?? null }));
      try {
        await submitAttempt(attemptId, payload);
        navigate(`/attempts/${attemptId}/result`, { replace: true, state: { auto } });
      } catch (err) {
        if (err.status === 409) {
          navigate(`/attempts/${attemptId}/result`, { replace: true });
          return;
        }
        submittingRef.current = false;
        setSubmitting(false);
        setConfirmOpen(false);
        setSubmitError(err);
      }
    },
    [attemptId, data, navigate],
  );

  const handleExpire = useCallback(() => {
    setTimeUp(true);
    submit(true);
  }, [submit]);

  // Warn before leaving mid-test (the timer keeps running on the server).
  useEffect(() => {
    if (!data || data.status !== 'in_progress') return undefined;
    const onBeforeUnload = (e) => {
      if (!submittingRef.current) {
        e.preventDefault();
        e.returnValue = '';
      }
    };
    window.addEventListener('beforeunload', onBeforeUnload);
    return () => window.removeEventListener('beforeunload', onBeforeUnload);
  }, [data]);

  if (status === 'loading' && !data) return <Loading fullPage label="Loading your test…" />;
  if (status === 'error') {
    return (
      <div className="page-center">
        <ErrorMessage error={error} onRetry={reload} />
        <Link to="/tests" className="btn btn-ghost">
          Back to tests
        </Link>
      </div>
    );
  }
  if (!data.questions) return <Loading fullPage label="Opening results…" />;

  const questions = data.questions;
  const question = questions[index];
  const answeredCount = questions.filter((q) => answers[q.id]).length;

  function choose(optionId) {
    setAnswers((a) => ({ ...a, [question.id]: optionId }));
    saveAnswer(attemptId, question.id, optionId).catch(() => setSaveWarning(true));
  }

  function clearChoice() {
    setAnswers((a) => ({ ...a, [question.id]: null }));
    saveAnswer(attemptId, question.id, null).catch(() => setSaveWarning(true));
  }

  return (
    <div className="test-shell" data-tone={data.test.section_slug || 'mixed'}>
      <header className="test-bar">
        <div className="test-bar-title">
          <BrandMark />
          <div>
            <p className="test-bar-name">{data.test.title}</p>
            <p className="muted small">
              {answeredCount} of {questions.length} answered
            </p>
          </div>
        </div>
        {deadline && <TestTimer deadline={deadline} onExpire={handleExpire} />}
        <button type="button" className="btn btn-primary" onClick={() => setConfirmOpen(true)} disabled={submitting}>
          Submit test
        </button>
      </header>

      {location.state?.resumed && (
        <p className="notice test-notice">You're continuing an unfinished attempt. Your saved answers and timer are restored.</p>
      )}
      {saveWarning && (
        <p className="notice test-notice" role="status">
          Some answers couldn't be saved just now. They'll still be sent when you submit.
        </p>
      )}
      {submitError && (
        <div className="test-notice">
          <ErrorMessage title="Your test wasn't submitted" error={submitError} onRetry={() => submit(timeUp)} />
        </div>
      )}

      <div className="test-body">
        <main className="test-main" id="main">
          <QuestionCard
            key={question.id}
            question={question}
            number={index + 1}
            total={questions.length}
            selectedOptionId={answers[question.id]}
            onSelect={choose}
            disabled={submitting}
          />
          <div className="test-nav">
            <button type="button" className="btn btn-secondary" onClick={() => setIndex((i) => i - 1)} disabled={index === 0}>
              <IconArrowLeft /> Previous
            </button>
            <button type="button" className="btn btn-ghost" onClick={clearChoice} disabled={!answers[question.id] || submitting}>
              Clear answer
            </button>
            {index < questions.length - 1 ? (
              <button type="button" className="btn btn-secondary" onClick={() => setIndex((i) => i + 1)}>
                Next <IconArrowRight />
              </button>
            ) : (
              <button type="button" className="btn btn-primary" onClick={() => setConfirmOpen(true)} disabled={submitting}>
                Review and submit
              </button>
            )}
          </div>
        </main>

        <aside className="question-grid-panel" aria-labelledby="grid-heading">
          <h2 id="grid-heading" className="sub-title">
            Questions
          </h2>
          <ol className="question-grid">
            {questions.map((q, i) => {
              const answered = Boolean(answers[q.id]);
              return (
                <li key={q.id}>
                  <button
                    type="button"
                    className={`grid-cell${answered ? ' is-answered' : ''}${i === index ? ' is-current' : ''}`}
                    onClick={() => setIndex(i)}
                    aria-current={i === index ? 'step' : undefined}
                    aria-label={`Question ${i + 1}, ${answered ? 'answered' : 'not answered'}`}
                  >
                    {i + 1}
                  </button>
                </li>
              );
            })}
          </ol>
          <ul className="grid-legend">
            <li>
              <span className="grid-cell is-answered" aria-hidden="true" /> Answered ({answeredCount})
            </li>
            <li>
              <span className="grid-cell" aria-hidden="true" /> Not answered ({questions.length - answeredCount})
            </li>
          </ul>
        </aside>
      </div>

      <ConfirmDialog
        open={confirmOpen && !timeUp}
        title="Submit this test?"
        confirmLabel="Submit test"
        cancelLabel="Keep working"
        busy={submitting}
        onConfirm={() => submit(false)}
        onCancel={() => setConfirmOpen(false)}
      >
        <p>
          You've answered <strong>{answeredCount}</strong> of <strong>{questions.length}</strong> questions.
          {answeredCount < questions.length && ' Unanswered questions score zero.'}
        </p>
        <p className="muted">You can't change your answers after submitting.</p>
      </ConfirmDialog>

      {timeUp && !submitError && (
        <div className="time-up" role="alertdialog" aria-live="assertive" aria-label="Time is up">
          <p className="time-up-title">Time's up</p>
          <p className="muted">Submitting your answers…</p>
        </div>
      )}
    </div>
  );
}
