import { Suspense, lazy, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { animate, onScroll } from 'animejs';
import HeroHeader from '../components/hero/HeroHeader.jsx';
import ScrollScrubber from '../components/hero/ScrollScrubber.jsx';
import Callouts from '../components/hero/Callouts.jsx';
import LoginCard from '../components/hero/LoginCard.jsx';
import { BrandMark } from '../components/Sidebar.jsx';
import { generateScramble, solutionFor } from '../components/hero/cubeMoves.js';
import { useAuth } from '../context/AuthContext.jsx';
import usePrefersReducedMotion from '../utils/usePrefersReducedMotion.js';

// Three.js only loads on this page.
const CubeScene = lazy(() => import('../components/hero/CubeScene.jsx'));

const MOVE_COUNT = 18;
// Scroll progress through the pinned section: solve first, then reveal the login card.
const SOLVE_END = 0.8;
const REVEAL_START = 0.84;

const clamp01 = (v) => Math.min(1, Math.max(0, v));
const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

export default function LandingPage({ jumpToLogin = false }) {
  const { status } = useAuth();
  const reducedMotion = usePrefersReducedMotion();
  const scramble = useMemo(() => generateScramble(MOVE_COUNT), []);
  const solution = useMemo(() => solutionFor(scramble), [scramble]);

  const sectionRef = useRef(null);
  const loginDockRef = useRef(null);
  const calloutsRef = useRef(null);
  const hintRef = useRef(null);
  const scrubberRef = useRef(null);
  const emailInputRef = useRef(null);
  const wantsFocusRef = useRef(jumpToLogin);
  const sceneStateRef = useRef({ solve: 0, reveal: 0 });

  const [movesDone, setMovesDone] = useState(0);
  const [loginOpen, setLoginOpen] = useState(false);

  const getSceneState = useCallback(() => sceneStateRef.current, []);

  const applyProgress = useCallback(
    (progress) => {
      const p = progress > 0.999 ? 1 : progress;
      const solve = clamp01(p / SOLVE_END);
      const reveal = clamp01((p - REVEAL_START) / (1 - REVEAL_START));
      sceneStateRef.current = { solve, reveal };

      setMovesDone(Math.min(solution.length, Math.floor(solve * solution.length + 1e-6)));
      setLoginOpen(reveal > 0.6);

      const e = easeOutCubic(reveal);
      loginDockRef.current?.style.setProperty('--reveal', e.toFixed(4));
      if (calloutsRef.current) calloutsRef.current.style.opacity = String(clamp01(1 - reveal * 2));
      if (hintRef.current) hintRef.current.style.opacity = String(clamp01(1 - solve * 6));
      if (scrubberRef.current) scrubberRef.current.style.opacity = String(clamp01(1 - reveal * 1.6));
    },
    [solution.length],
  );

  // Scroll → progress. anime.js syncs a 0→1 animation to the pinned section's scroll range.
  useEffect(() => {
    if (reducedMotion) {
      applyProgress(1);
      return undefined;
    }
    const proxy = { p: 0 };
    const observer = onScroll({ target: sectionRef.current, enter: 'top top', leave: 'bottom bottom', sync: 0.5 });
    const animation = animate(proxy, {
      p: [0, 1],
      duration: 1000,
      ease: 'linear',
      autoplay: observer,
      onUpdate: () => applyProgress(proxy.p),
    });
    return () => {
      animation.revert();
      observer.revert();
    };
  }, [reducedMotion, applyProgress]);

  // /login lands directly on the solved cube + login card.
  // The browser restores scroll after load, so take over restoration and jump again once settled.
  useEffect(() => {
    if (!jumpToLogin) return undefined;
    const previous = window.history.scrollRestoration;
    window.history.scrollRestoration = 'manual';
    wantsFocusRef.current = true;
    const jump = () => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' });
    const frame = requestAnimationFrame(jump);
    const timer = setTimeout(jump, 250);
    window.addEventListener('load', jump, { once: true });
    return () => {
      cancelAnimationFrame(frame);
      clearTimeout(timer);
      window.removeEventListener('load', jump);
      window.history.scrollRestoration = previous;
    };
  }, [jumpToLogin]);

  // Keep the hidden card out of the tab order, and focus it once a "skip" reveals it.
  useEffect(() => {
    const dock = loginDockRef.current;
    if (!dock) return;
    if (loginOpen) {
      dock.removeAttribute('inert');
      if (wantsFocusRef.current) {
        wantsFocusRef.current = false;
        emailInputRef.current?.focus({ preventScroll: true });
      }
    } else {
      dock.setAttribute('inert', '');
    }
  }, [loginOpen]);

  function skipToLogin() {
    wantsFocusRef.current = true;
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: reducedMotion ? 'instant' : 'smooth' });
  }

  return (
    <div className={`landing${reducedMotion ? ' is-reduced-motion' : ''}`}>
      <header className="topbar">
        <Link to="/" className="brand" aria-label="PlacePrep home">
          <BrandMark />
          PlacePrep
        </Link>
        <nav className="topbar-actions" aria-label="Account">
          {status === 'authenticated' ? (
            <Link to="/dashboard" className="btn-outline">
              Go to dashboard
            </Link>
          ) : (
            <>
              <button type="button" className="btn-ghost" onClick={skipToLogin}>
                Skip to login
              </button>
              <Link to="/register" className="btn-outline">
                Register
              </Link>
            </>
          )}
        </nav>
      </header>

      <HeroHeader reducedMotion={reducedMotion} />

      <section className="solve" ref={sectionRef} aria-label="Interactive Rubik's cube and login">
        <div className="stage">
          <Suspense fallback={<div className="cube-loading" role="status">Loading 3D cube…</div>}>
            <CubeScene scramble={scramble} getState={getSceneState} reducedMotion={reducedMotion} />
          </Suspense>

          <p className="stage-hint" ref={hintRef}>
            <span>Drag to look around.</span> Keep scrolling to solve it.
          </p>

          <Callouts reducedMotion={reducedMotion} fadeRef={calloutsRef} />

          <div className="scrubber-wrap" ref={scrubberRef}>
            <ScrollScrubber solution={solution} movesDone={movesDone} />
          </div>

          <div className="login-dock" ref={loginDockRef} id="login">
            <LoginCard emailInputRef={emailInputRef} />
          </div>
        </div>
      </section>
    </div>
  );
}
