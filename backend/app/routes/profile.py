from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.routes.auth import duplicate_fields
from app.schemas.auth import parse_password_change, parse_profile_update
from app.utils.errors import ApiError
from app.utils.validation import get_json_body

bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@bp.get("")
@jwt_required()
def get_profile():
    return jsonify({"user": current_user.to_dict()})


@bp.patch("")
@jwt_required()
def update_profile():
    updates = parse_profile_update(get_json_body())
    if "mobile" in updates:
        duplicates = duplicate_fields(mobile=updates["mobile"], exclude_id=current_user.id)
        if duplicates:
            raise ApiError(409, "That mobile number is already registered.", "duplicate_account", duplicates)
    for field, value in updates.items():
        setattr(current_user, field, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ApiError(409, "That mobile number is already registered.", "duplicate_account")
    return jsonify({"user": current_user.to_dict()})


@bp.post("/password")
@jwt_required()
def change_password():
    current, new = parse_password_change(get_json_body(), current_user)
    if current_user.password_hash and not current_user.check_password(current):
        raise ApiError(400, "Please fix the highlighted fields.", "validation_error",
                       {"current_password": "Current password is incorrect."})
    current_user.set_password(new)
    db.session.commit()
    return jsonify({"message": "Password updated.", "user": current_user.to_dict()})
