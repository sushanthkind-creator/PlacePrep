import { Suspense, lazy } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './components/AppLayout.jsx';
import Loading from './components/Loading.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import LandingPage from './pages/LandingPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';

// Pages behind login load on demand, so the landing page stays light.
const CompleteProfilePage = lazy(() => import('./pages/CompleteProfilePage.jsx'));
const DashboardPage = lazy(() => import('./pages/DashboardPage.jsx'));
const QualitativePage = lazy(() => import('./pages/QualitativePage.jsx'));
const QuantitativePage = lazy(() => import('./pages/QuantitativePage.jsx'));
const EnglishPage = lazy(() => import('./pages/EnglishPage.jsx'));
const LessonPage = lazy(() => import('./pages/LessonPage.jsx'));
const PracticePage = lazy(() => import('./pages/PracticePage.jsx'));
const TestsPage = lazy(() => import('./pages/TestsPage.jsx'));
const TestInstructionsPage = lazy(() => import('./pages/TestInstructionsPage.jsx'));
const TestPage = lazy(() => import('./pages/TestPage.jsx'));
const TestResultsPage = lazy(() => import('./pages/TestResultsPage.jsx'));
const TestHistoryPage = lazy(() => import('./pages/TestHistoryPage.jsx'));
const ProfilePage = lazy(() => import('./pages/ProfilePage.jsx'));

export default function App() {
  return (
    <Suspense fallback={<Loading fullPage />}>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route element={<ProtectedRoute allowIncompleteProfile />}>
          <Route path="/complete-profile" element={<CompleteProfilePage />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          {/* The active test is a focused screen without the sidebar. */}
          <Route path="/attempts/:attemptId" element={<TestPage />} />

          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/learn/logical" element={<QualitativePage />} />
            <Route path="/learn/quant" element={<QuantitativePage />} />
            <Route path="/learn/english" element={<EnglishPage />} />
            <Route path="/topics/:slug" element={<LessonPage />} />
            <Route path="/topics/:slug/practice" element={<PracticePage />} />
            <Route path="/tests" element={<TestsPage />} />
            <Route path="/tests/:testId" element={<TestInstructionsPage />} />
            <Route path="/attempts/:attemptId/result" element={<TestResultsPage />} />
            <Route path="/history" element={<TestHistoryPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
