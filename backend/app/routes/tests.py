from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required

from app.extensions import db
from app.models import (
    SCOPE_MIXED,
    SCOPE_SECTION,
    SCOPE_TOPIC,
    STATUS_IN_PROGRESS,
    STATUS_SUBMITTED,
    Section,
    TestAttempt,
    TestDefinition,
    Topic,
)
from app.schemas.tests import (
    MAX_DURATION_MINUTES,
    MIN_DURATION_MINUTES,
    parse_single_answer,
    parse_start_attempt,
    parse_submit,
    question_count_limits,
)
from app.services import attempts as engine
from app.services.progress import submitted_attempts, with_change
from app.utils.errors import ApiError
from app.utils.time import utcnow
from app.utils.validation import get_json_body

bp = Blueprint("tests", __name__, url_prefix="/api")


def get_test_or_404(test_id):
    test = db.session.get(TestDefinition, test_id)
    if not test:
        raise ApiError(404, "Test not found.", "not_found")
    return test


def _user_stats_by_test(user_id):
    stats = {}
    for attempt in submitted_attempts(user_id):
        s = stats.setdefault(attempt.test_id, {"attempts": 0, "best": None, "last": None})
        s["attempts"] += 1
        s["best"] = attempt.percentage if s["best"] is None else max(s["best"], attempt.percentage)
        s["last"] = attempt.percentage
    return stats


def _test_card(test, stats, active_ids):
    available = engine.available_count(test)
    low, high = question_count_limits(test, available)
    return {
        **engine.test_ref(test),
        "description": test.description,
        "section_name": test.section.name if test.section else None,
        "topic_name": test.topic.name if test.topic else None,
        "default_question_count": min(test.default_question_count, high),
        "default_duration_minutes": test.default_duration_minutes,
        "available_questions": available,
        "question_count_range": [low, high],
        "my_stats": stats.get(test.id, {"attempts": 0, "best": None, "last": None}),
        "active_attempt_id": active_ids.get(test.id),
    }


def _active_attempts(user_id):
    rows = TestAttempt.query.filter_by(user_id=user_id, status=STATUS_IN_PROGRESS).all()
    now = utcnow()
    active = {}
    for attempt in rows:
        engine.close_if_overdue(attempt, now)
        if attempt.status == STATUS_IN_PROGRESS:
            active[attempt.test_id] = attempt.id
    return active


@bp.get("/tests")
@jwt_required()
def list_tests():
    query = TestDefinition.query
    scope = request.args.get("scope")
    if scope:
        if scope not in (SCOPE_TOPIC, SCOPE_SECTION, SCOPE_MIXED):
            raise ApiError(400, "scope must be topic, section or mixed.", "validation_error")
        query = query.filter_by(scope=scope)
    if request.args.get("section"):
        section = Section.query.filter_by(slug=request.args["section"]).first()
        query = query.filter_by(section_id=section.id if section else -1)
    if request.args.get("topic"):
        topic = Topic.query.filter_by(slug=request.args["topic"]).first()
        query = query.filter_by(topic_id=topic.id if topic else -1)

    stats = _user_stats_by_test(current_user.id)
    active = _active_attempts(current_user.id)
    tests = query.order_by(TestDefinition.position).all()
    return jsonify({"tests": [_test_card(t, stats, active) for t in tests]})


@bp.get("/tests/<int:test_id>")
@jwt_required()
def get_test(test_id):
    test = get_test_or_404(test_id)
    card = _test_card(test, _user_stats_by_test(current_user.id), _active_attempts(current_user.id))
    card["duration_range"] = [MIN_DURATION_MINUTES, MAX_DURATION_MINUTES]
    card["instructions"] = [
        "Each question has four options and exactly one correct answer.",
        "There is no negative marking. Unanswered questions score zero.",
        "Use Next, Previous or the question grid to move around. You can change answers until you submit.",
        "Your answers are saved as you go. If you reload the page, you can continue where you left off.",
        "The timer keeps running even if you leave the page. When it reaches zero, the test is submitted automatically.",
        "Scores are calculated on the server after you submit, and answers with explanations are shown on the results page.",
    ]
    return jsonify({"test": card})


@bp.post("/tests/<int:test_id>/attempts")
@jwt_required()
def start_test(test_id):
    test = get_test_or_404(test_id)
    count, minutes = parse_start_attempt(get_json_body(), test, engine.available_count(test))
    attempt, created = engine.start_attempt(current_user, test, count, minutes)
    return jsonify({"attempt": engine.attempt_for_taking(attempt), "resumed": not created}), 201 if created else 200


@bp.get("/attempts")
@jwt_required()
def history():
    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(50, max(1, int(request.args.get("per_page", 20))))
    except ValueError:
        raise ApiError(400, "page and per_page must be whole numbers.", "validation_error")

    attempts = submitted_attempts(current_user.id)
    changes = with_change(attempts)
    newest_first = list(reversed(attempts))
    start = (page - 1) * per_page
    items = [{**engine.attempt_summary(a), "change": changes[a.id]} for a in newest_first[start:start + per_page]]
    return jsonify({"attempts": items, "page": page, "per_page": per_page, "total": len(attempts)})


@bp.get("/attempts/<int:attempt_id>")
@jwt_required()
def get_attempt(attempt_id):
    attempt = engine.close_if_overdue(engine.get_owned_attempt(attempt_id, current_user.id))
    if attempt.status == STATUS_SUBMITTED:
        return jsonify({"attempt": engine.attempt_summary(attempt)})
    return jsonify({"attempt": engine.attempt_for_taking(attempt)})


@bp.put("/attempts/<int:attempt_id>/answers")
@jwt_required()
def save_answer(attempt_id):
    attempt = engine.close_if_overdue(engine.get_owned_attempt(attempt_id, current_user.id))
    if attempt.status == STATUS_SUBMITTED:
        raise ApiError(409, "This test has already been submitted.", "already_submitted")
    question_id, option_id = parse_single_answer(get_json_body())
    item = engine.validate_option(attempt, question_id, option_id)
    item.selected_option_id = option_id
    db.session.commit()
    return jsonify({"question_id": question_id, "selected_option_id": option_id})


@bp.post("/attempts/<int:attempt_id>/submit")
@jwt_required()
def submit(attempt_id):
    attempt = engine.get_owned_attempt(attempt_id, current_user.id)
    if attempt.status == STATUS_SUBMITTED:
        raise ApiError(409, "This test has already been submitted.", "already_submitted")

    answers = parse_submit(get_json_body())
    for question_id, option_id in answers.items():
        engine.validate_option(attempt, question_id, option_id)

    now = utcnow()
    late = engine.is_past_grace(attempt, now)
    # After the timer (plus grace) ends, only answers saved in time count.
    engine.finalize_attempt(attempt, answers=None if late else answers, auto=late, now=now)
    return jsonify({"attempt": engine.attempt_result(attempt)})


@bp.get("/attempts/<int:attempt_id>/result")
@jwt_required()
def result(attempt_id):
    attempt = engine.close_if_overdue(engine.get_owned_attempt(attempt_id, current_user.id))
    if attempt.status != STATUS_SUBMITTED:
        raise ApiError(409, "Results are available after the test is submitted.", "not_submitted")
    return jsonify({"attempt": engine.attempt_result(attempt)})
