import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

load_dotenv(BASE_DIR / ".env")


def _split_origins(value):
    return [origin.strip() for origin in value.split(",") if origin.strip()]


def _database_url():
    url = os.getenv("DATABASE_URL", "sqlite:///placeprep.db").strip()
    # Hosts like Render hand out postgres:// URLs; SQLAlchemy needs the psycopg (v3) driver named.
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    # Relative SQLite paths are stored in backend/instance/ so the location doesn't depend on the cwd.
    if url.startswith("sqlite:///") and ":memory:" not in url:
        name = url[len("sqlite:///"):]
        if not os.path.isabs(name):
            INSTANCE_DIR.mkdir(exist_ok=True)
            url = f"sqlite:///{(INSTANCE_DIR / name).as_posix()}"
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "8")))
    CORS_ORIGINS = _split_origins(os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"))
    GOOGLE_CLIENT_ID = (os.getenv("GOOGLE_CLIENT_ID") or "").strip() or None

    # Extra seconds accepted after a test's timer ends, to absorb network delay on auto-submit.
    SUBMISSION_GRACE_SECONDS = 15


class TestingConfig(Config):
    __test__ = False  # not a pytest test class

    TESTING = True
    SECRET_KEY = "testing-secret-key-not-for-production-use-0123456789"
    JWT_SECRET_KEY = "testing-jwt-secret-key-not-for-production-use-0123456789"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    GOOGLE_CLIENT_ID = None
