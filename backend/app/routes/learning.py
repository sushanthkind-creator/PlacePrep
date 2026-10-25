from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required

from app.extensions import db
from app.models import Section, Topic, TopicProgress
from app.services.progress import section_rows, topic_rows
from app.utils.errors import ApiError
from app.utils.time import utcnow
from app.utils.validation import get_json_body

bp = Blueprint("learning", __name__, url_prefix="/api")


def get_topic_or_404(slug):
    topic = Topic.query.filter_by(slug=slug).first()
    if not topic:
        raise ApiError(404, "Topic not found.", "not_found")
    return topic


def get_or_create_progress(user_id, topic_id):
    row = TopicProgress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    if not row:
        row = TopicProgress(user_id=user_id, topic_id=topic_id)
        db.session.add(row)
    return row


@bp.get("/sections")
@jwt_required()
def list_sections():
    return jsonify({"sections": section_rows(current_user.id)})


@bp.get("/sections/<slug>")
@jwt_required()
def get_section(slug):
    section = Section.query.filter_by(slug=slug).first()
    if not section:
        raise ApiError(404, "Section not found.", "not_found")
    summary = next(s for s in section_rows(current_user.id) if s["slug"] == slug)
    summary["topics"] = topic_rows(current_user.id, section.topics)
    return jsonify({"section": summary})


@bp.get("/topics/<slug>")
@jwt_required()
def get_topic(slug):
    topic = get_topic_or_404(slug)
    progress = get_or_create_progress(current_user.id, topic.id)
    progress.last_viewed_at = utcnow()
    db.session.commit()

    siblings = topic.section.topics
    index = siblings.index(topic)
    neighbour = lambda t: {"slug": t.slug, "name": t.name} if t else None  # noqa: E731
    return jsonify(
        {
            "topic": {
                **topic.to_dict(),
                "section": topic.section.to_dict(),
                "lesson": topic.lesson.to_dict() if topic.lesson else None,
                "examples": [e.to_dict() for e in topic.examples],
                "progress": topic_rows(current_user.id, [topic])[0],
                "previous": neighbour(siblings[index - 1] if index > 0 else None),
                "next": neighbour(siblings[index + 1] if index + 1 < len(siblings) else None),
            }
        }
    )


@bp.get("/topics/<slug>/examples")
@jwt_required()
def get_examples(slug):
    topic = get_topic_or_404(slug)
    return jsonify({"examples": [e.to_dict() for e in topic.examples]})


@bp.post("/topics/<slug>/progress")
@jwt_required()
def set_topic_progress(slug):
    topic = get_topic_or_404(slug)
    completed = get_json_body().get("completed")
    if not isinstance(completed, bool):
        raise ApiError(400, "'completed' must be true or false.", "validation_error")
    row = get_or_create_progress(current_user.id, topic.id)
    row.completed = completed
    row.completed_at = utcnow() if completed else None
    db.session.commit()
    return jsonify({"progress": topic_rows(current_user.id, [topic])[0]})


@bp.get("/progress/topics")
@jwt_required()
def list_topic_progress():
    return jsonify({"topics": topic_rows(current_user.id)})
