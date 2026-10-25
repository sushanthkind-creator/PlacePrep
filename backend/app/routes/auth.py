from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import create_access_token, current_user, get_jwt, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import RevokedToken, User
from app.schemas.auth import parse_login, parse_register
from app.services import google_auth
from app.utils.errors import ApiError
from app.utils.validation import get_json_body, validate_full_name

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

DUPLICATE_EMAIL = "An account with this email already exists. Log in instead."
DUPLICATE_MOBILE = "An account with this mobile number already exists."


def _session_response(user, status=200):
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": user.to_dict()}), status


def duplicate_fields(email=None, mobile=None, exclude_id=None):
    fields = {}
    if email:
        q = User.query.filter_by(email=email)
        if exclude_id:
            q = q.filter(User.id != exclude_id)
        if q.first():
            fields["email"] = DUPLICATE_EMAIL
    if mobile:
        q = User.query.filter_by(mobile=mobile)
        if exclude_id:
            q = q.filter(User.id != exclude_id)
        if q.first():
            fields["mobile"] = DUPLICATE_MOBILE
    return fields


@bp.post("/register")
def register():
    data = parse_register(get_json_body())
    duplicates = duplicate_fields(email=data["email"], mobile=data["mobile"])
    if duplicates:
        raise ApiError(409, "An account already exists with these details.", "duplicate_account", duplicates)

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        mobile=data["mobile"],
        college_name=data["college_name"],
        auth_provider="password",
    )
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        # Two registrations raced each other.
        db.session.rollback()
        raise ApiError(409, "An account already exists with these details.", "duplicate_account")
    return _session_response(user, 201)


@bp.post("/login")
def login():
    email, password = parse_login(get_json_body())
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        # Same message either way, so the form can't be used to discover registered emails.
        raise ApiError(401, "Invalid email or password.", "invalid_credentials")
    return _session_response(user)


@bp.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    if not RevokedToken.query.filter_by(jti=jti).first():
        db.session.add(RevokedToken(jti=jti))
        db.session.commit()
    return jsonify({"message": "Logged out."})


@bp.get("/me")
@jwt_required()
def me():
    return jsonify({"user": current_user.to_dict()})


@bp.get("/config")
def auth_config():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID")
    return jsonify({"google_enabled": bool(client_id), "google_client_id": client_id})


@bp.post("/google")
def google_sign_in():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID")
    if not client_id:
        raise ApiError(404, "Google sign-in is not enabled on this server.", "google_disabled")

    credential = get_json_body().get("credential")
    if not isinstance(credential, str) or not credential:
        raise ApiError(400, "Missing Google credential.", "validation_error")
    try:
        claims = google_auth.verify_google_credential(credential, client_id)
    except ValueError:
        raise ApiError(401, "Google sign-in could not be verified. Please try again.", "invalid_google_token")

    email = (claims.get("email") or "").strip().lower()
    if not email or not claims.get("email_verified"):
        raise ApiError(401, "Your Google account email is not verified.", "google_email_unverified")

    user = User.query.filter_by(google_sub=claims["sub"]).first()
    status = 200
    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            # Same email, already verified by Google: link the accounts.
            user.google_sub = claims["sub"]
        else:
            name, err = validate_full_name(claims.get("name") or email.split("@")[0])
            user = User(
                full_name=name if not err else "Student",
                email=email,
                google_sub=claims["sub"],
                auth_provider="google",
            )
            db.session.add(user)
            status = 201
        user.email_verified_by_google = True
        db.session.commit()
    return _session_response(user, status)
