from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func

from app.extensions import db
from app.models import POOL_PRACTICE, AnswerOption, PracticeAnswer, Question
from app.routes.learning import get_topic_or_404
from app.utils.errors import ApiError
from app.utils.validation import get_json_body, require_int

bp = Blueprint("practice", __name__, url_prefix="/api")


def _review(question, answer):
    """Feedback for a practice answer: only ever sent after the student has answered."""
    key = question.correct_option
    return {
        "selected_option_id": answer.selected_option_id,
        "is_correct": answer.is_correct,
        "correct_option_id": key.id if key else None,
        "explanation": question.explanation,
    }


@bp.get("/topics/<slug>/practice")
@jwt_required()
def get_practice(slug):
    topic = get_topic_or_404(slug)
    questions = (
        Question.query.filter_by(topic_id=topic.id, pool=POOL_PRACTICE).order_by(Question.position).all()
    )
    latest_ids = (
        db.session.query(func.max(PracticeAnswer.id))
        .filter(PracticeAnswer.user_id == current_user.id, PracticeAnswer.question_id.in_([q.id for q in questions]))
        .group_by(PracticeAnswer.question_id)
    )
    latest = {a.question_id: a for a in PracticeAnswer.query.filter(PracticeAnswer.id.in_(latest_ids)).all()}
    return jsonify(
        {
            "topic": {**topic.to_dict(), "section": topic.section.to_dict()},
            "questions": [
                {**q.to_public_dict(), "review": _review(q, latest[q.id]) if q.id in latest else None}
                for q in questions
            ],
        }
    )


@bp.post("/practice/answers")
@jwt_required()
def answer_practice():
    data = get_json_body()
    question_id = require_int(data.get("question_id"), "question_id")
    option_id = require_int(data.get("option_id"), "option_id")

    # Only practice questions can be checked here, so test answer keys never leak.
    question = Question.query.filter_by(id=question_id, pool=POOL_PRACTICE).first()
    if not question:
        raise ApiError(404, "Practice question not found.", "not_found")
    option = AnswerOption.query.filter_by(id=option_id, question_id=question.id).first()
    if not option:
        raise ApiError(400, "That option does not belong to this question.", "invalid_option")

    answer = PracticeAnswer(
        user_id=current_user.id,
        question_id=question.id,
        selected_option_id=option.id,
        is_correct=option.is_correct,
    )
    db.session.add(answer)
    db.session.commit()
    return jsonify({"question_id": question.id, "review": _review(question, answer)})
