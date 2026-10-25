import LandingPage from './LandingPage.jsx';

// The login form is the final screen of the landing page; /login opens it directly.
export default function LoginPage() {
  return <LandingPage jumpToLogin />;
}
