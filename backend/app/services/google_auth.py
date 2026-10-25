"""Verifies Google Sign-In ID tokens. Kept separate so tests can replace it."""

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

GOOGLE_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}


def verify_google_credential(credential, client_id):
    """Returns the verified token claims, or raises ValueError."""
    claims = id_token.verify_oauth2_token(credential, google_requests.Request(), client_id)
    if claims.get("iss") not in GOOGLE_ISSUERS:
        raise ValueError("Wrong token issuer.")
    return claims
