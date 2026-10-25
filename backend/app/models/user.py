from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.utils.time import iso, utcnow


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    # Nullable only for Google sign-ups that haven't completed their profile yet.
    mobile = db.Column(db.String(10), unique=True, nullable=True)
    college_name = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    google_sub = db.Column(db.String(255), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), nullable=False, default="password")
    email_verified_by_google = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)

    @property
    def profile_complete(self):
        return bool(self.mobile and self.college_name)

    def to_dict(self):
        # Never include password_hash or google_sub.
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "mobile": self.mobile,
            "college_name": self.college_name,
            "auth_provider": self.auth_provider,
            "has_password": bool(self.password_hash),
            "email_verified_by_google": self.email_verified_by_google,
            "profile_complete": self.profile_complete,
            "created_at": iso(self.created_at),
        }


class RevokedToken(db.Model):
    """JWT IDs invalidated by logout."""

    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), nullable=False, unique=True, index=True)
    revoked_at = db.Column(db.DateTime, nullable=False, default=utcnow)
