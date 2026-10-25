import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import ErrorMessage from './ErrorMessage.jsx';
import Loading from './Loading.jsx';

export default function ProtectedRoute({ allowIncompleteProfile = false }) {
  const { status, user, retry } = useAuth();
  const location = useLocation();

  if (status === 'loading') return <Loading fullPage label="Checking your session…" />;

  if (status === 'offline') {
    return (
      <div className="page-center">
        <ErrorMessage
          title="Can't reach the server"
          error="PlacePrep couldn't contact its server. Check that the backend is running, then try again."
          onRetry={retry}
        />
      </div>
    );
  }

  if (status !== 'authenticated') {
    return <Navigate to="/login" replace state={{ from: location.pathname + location.search }} />;
  }

  if (!user.profile_complete && !allowIncompleteProfile) {
    return <Navigate to="/complete-profile" replace />;
  }

  return <Outlet />;
}
