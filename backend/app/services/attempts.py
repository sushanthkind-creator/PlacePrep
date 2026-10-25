"""Test attempts: drawing questions, timing, saving answers and one-time submission."""

import random
from datetime import timedelta

from flask import current_app
from sqlalchemy import update

from app.extensions import db
from app.models import (
    POOL_TEST,
    SCOPE_SECTION,
    SCOPE_TOPIC,
    STATUS_IN_PROGRESS,
    STATUS_SUBMITTED,
    AnswerOption,
    AttemptQuestion,
    Question,
    TestAttempt,
    Topic,
)
from app.services.scoring import breakdown, grade_attempt
from app.utils.errors import ApiError
from app.utils.time import iso, utcnow


def pool_query(test):
    query = Question.query.filter(Question.pool == POOL_TEST)
    if test.scope == SCOPE_TOPIC:
        query = query.filter(Question.topic_id == test.topic_id)
    elif test.scope == SCOPE_SECTION:
        query = query.join(Topic).filter(Topic.section_id == test.section_id)
    return query


def available_count(test):
    return pool_query(test).count()


def select_questions(test, count, rng=random):
    """Pick `count` questions, spreading them evenly across the topics in the pool."""
    by_topic = {}
    for question in pool_query(test).all():
        by_topic.setdefault(question.topic_id, []).append(question)
    groups = list(by_topic.values())
    for group in groups:
        rng.shuffle(group)
    rng.shuffle(groups)

    picked = []
    while len(picked) < count and any(groups):
        for group in groups:
            if group and len(picked) < count:
                picked.append(group.pop())
    rng.shuffle(picked)
    return picked


def grace_seconds():
    return current_app.config["SUBMISSION_GRACE_SECONDS"]


def is_past_grace(attempt, now):
    return now > attempt.expires_at + timedelta(seconds=grace_seconds())


def find_active_attempt(user_id, test_id):
    return TestAttempt.query.filter_by(user_id=user_id, test_id=test_id, status=STATUS_IN_PROGRESS).first()


def start_attempt(user, test, question_count, duration_minutes):
    """Returns (attempt, created). An unfinished attempt of the same test is resumed instead of duplicated."""
    now = utcnow()
    existing = find_active_attempt(user.id, test.id)
    if existing:
        if not is_past_grace(existing, now):
            return existing, False
        finalize_attempt(existing, auto=True, now=now)

    questions = select_questions(test, question_count)
    if not questions:
        raise ApiError(409, "This test has no questions available yet.", "no_questions")

    duration_seconds = duration_minutes * 60
    attempt = TestAttempt(
        user_id=user.id,
        test_id=test.id,
        status=STATUS_IN_PROGRESS,
        question_count=len(questions),
        duration_seconds=duration_seconds,
        started_at=now,
        expires_at=now + timedelta(seconds=duration_seconds),
    )
    attempt.questions = [AttemptQuestion(question=q, position=i + 1) for i, q in enumerate(questions)]
    db.session.add(attempt)
    db.session.commit()
    return attempt, True


def get_owned_attempt(attempt_id, user_id):
    # Other students' attempts look exactly like missing ones.
    attempt = TestAttempt.query.filter_by(id=attempt_id, user_id=user_id).first()
    if not attempt:
        raise ApiError(404, "Test attempt not found.", "not_found")
    return attempt


def validate_option(attempt, question_id, option_id):
    """Returns the AttemptQuestion; raises 400 if the question or option don't belong to this attempt."""
    item = next((q for q in attempt.questions if q.question_id == question_id), None)
    if item is None:
        raise ApiError(400, f"Question {question_id} is not part of this test.", "invalid_question")
    if option_id is not None:
        valid = db.session.query(AnswerOption.id).filter_by(id=option_id, question_id=question_id).first()
        if not valid:
            raise ApiError(400, f"Option {option_id} does not belong to question {question_id}.", "invalid_option")
    return item


def finalize_attempt(attempt, answers=None, auto=False, now=None):
    """Grade and close an attempt exactly once. A second submission gets 409, never a second result."""
    now = now or utcnow()
    claimed = db.session.execute(
        update(TestAttempt)
        .where(TestAttempt.id == attempt.id, TestAttempt.status == STATUS_IN_PROGRESS)
        .values(status=STATUS_SUBMITTED, submitted_at=now)
        .execution_options(synchronize_session=False)
    )
    if claimed.rowcount != 1:
        db.session.rollback()
        raise ApiError(409, "This test has already been submitted.", "already_submitted")

    if answers:
        for item in attempt.questions:
            if item.question_id in answers:
                item.selected_option_id = answers[item.question_id]

    attempt.status = STATUS_SUBMITTED
    attempt.submitted_at = now
    attempt.auto_submitted = auto
    attempt.time_taken_seconds = max(0, int((min(now, attempt.expires_at) - attempt.started_at).total_seconds()))
    grade_attempt(attempt)
    db.session.commit()
    return attempt


def close_if_overdue(attempt, now=None):
    """Auto-submit an attempt whose timer (plus grace) has run out, using the answers saved so far."""
    now = now or utcnow()
    if attempt.status == STATUS_IN_PROGRESS and is_past_grace(attempt, now):
        try:
            finalize_attempt(attempt, auto=True, now=now)
        except ApiError:
            db.session.refresh(attempt)
    return attempt


# ---- Serialisers ---------------------------------------------------------------

def test_ref(test):
    return {
        "id": test.id,
        "slug": test.slug,
        "title": test.title,
        "scope": test.scope,
        "section_slug": test.section.slug if test.section else None,
        "topic_slug": test.topic.slug if test.topic else None,
    }


def attempt_summary(attempt):
    return {
        "id": attempt.id,
        "test": test_ref(attempt.test),
        "status": attempt.status,
        "question_count": attempt.question_count,
        "duration_seconds": attempt.duration_seconds,
        "started_at": iso(attempt.started_at),
        "submitted_at": iso(attempt.submitted_at),
        "auto_submitted": attempt.auto_submitted,
        "correct": attempt.correct_count,
        "incorrect": attempt.incorrect_count,
        "unanswered": attempt.unanswered_count,
        "percentage": attempt.percentage,
        "time_taken_seconds": attempt.time_taken_seconds,
    }


def attempt_for_taking(attempt, now=None):
    """The in-progress view: questions without answer keys, plus the student's saved choices."""
    now = now or utcnow()
    data = attempt_summary(attempt)
    data.update(
        {
            "expires_at": iso(attempt.expires_at),
            "server_time": iso(now),
            "remaining_seconds": max(0, int((attempt.expires_at - now).total_seconds())),
            "questions": [
                {**item.question.to_public_dict(), "position": item.position, "selected_option_id": item.selected_option_id}
                for item in attempt.questions
            ],
        }
    )
    return data


def attempt_result(attempt):
    data = attempt_summary(attempt)
    review = []
    for item in attempt.questions:
        question = item.question
        key = question.correct_option
        review.append(
            {
                **question.to_public_dict(),
                "position": item.position,
                "selected_option_id": item.selected_option_id,
                "correct_option_id": key.id if key else None,
                "is_correct": item.is_correct,
                "explanation": question.explanation,
            }
        )
    data["questions"] = review
    data["breakdown"] = breakdown(attempt)
    return data
