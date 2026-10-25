from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required

from app.services.progress import dashboard, section_rows, topic_rows

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@bp.get("")
@jwt_required()
def get_dashboard():
    return jsonify(dashboard(current_user))


@bp.get("/sections")
@jwt_required()
def section_performance():
    return jsonify({"sections": section_rows(current_user.id)})


@bp.get("/topics")
@jwt_required()
def topic_performance():
    return jsonify({"topics": topic_rows(current_user.id)})
