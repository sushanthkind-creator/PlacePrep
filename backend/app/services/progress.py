"""Per-student progress and performance, computed from recorded activity only."""

from sqlalchemy import case, func

from app.extensions import db
from app.models import (
    POOL_PRACTICE,
    SCOPE_TOPIC,
    STATUS_SUBMITTED,
    AttemptQuestion,
    PracticeAnswer,
    Question,
    Section,
    TestAttempt,
    TestDefinition,
    Topic,
    TopicProgress,
)
from app.utils.time import iso

# Minimum graded questions before a section or topic is judged strong or weak.
MIN_SECTION_QUESTIONS = 5
MIN_TOPIC_QUESTIONS = 3
WEAK_TOPIC_THRESHOLD = 70.0


def _pct(correct, total):
    return round(correct * 100 / total, 1) if total else None


def practice_totals_by_topic():
    rows = (
        db.session.query(Question.topic_id, func.count(Question.id))
        .filter(Question.pool == POOL_PRACTICE)
        .group_by(Question.topic_id)
        .all()
    )
    return dict(rows)


def practice_by_topic(user_id):
    """Distinct practice questions attempted per topic, and how many the latest answer got right."""
    latest_ids = (
        db.session.query(func.max(PracticeAnswer.id))
        .filter(PracticeAnswer.user_id == user_id)
        .group_by(PracticeAnswer.question_id)
    )
    rows = (
        db.session.query(
            Question.topic_id,
            func.count(PracticeAnswer.id),
            func.sum(case((PracticeAnswer.is_correct.is_(True), 1), else_=0)),
        )
        .join(Question, Question.id == PracticeAnswer.question_id)
        .filter(PracticeAnswer.id.in_(latest_ids))
        .group_by(Question.topic_id)
        .all()
    )
    return {topic_id: {"attempted": n, "correct": int(c or 0)} for topic_id, n, c in rows}


def tests_by_topic(user_id):
    """Questions seen in submitted tests per topic, and how many were answered correctly."""
    rows = (
        db.session.query(
            Question.topic_id,
            func.count(AttemptQuestion.id),
            func.sum(case((AttemptQuestion.is_correct.is_(True), 1), else_=0)),
        )
        .join(TestAttempt, TestAttempt.id == AttemptQuestion.attempt_id)
        .join(Question, Question.id == AttemptQuestion.question_id)
        .filter(TestAttempt.user_id == user_id, TestAttempt.status == STATUS_SUBMITTED)
        .group_by(Question.topic_id)
        .all()
    )
    return {topic_id: {"total": n, "correct": int(c or 0)} for topic_id, n, c in rows}


def best_topic_test_scores(user_id):
    rows = (
        db.session.query(TestDefinition.topic_id, func.max(TestAttempt.percentage))
        .join(TestDefinition, TestDefinition.id == TestAttempt.test_id)
        .filter(
            TestAttempt.user_id == user_id,
            TestAttempt.status == STATUS_SUBMITTED,
            TestDefinition.scope == SCOPE_TOPIC,
        )
        .group_by(TestDefinition.topic_id)
        .all()
    )
    return dict(rows)


def topic_progress_map(user_id):
    rows = TopicProgress.query.filter_by(user_id=user_id).all()
    return {row.topic_id: row for row in rows}


def topic_rows(user_id, topics=None):
    """Progress for each topic (all topics when `topics` is None)."""
    topics = topics if topics is not None else Topic.query.order_by(Topic.section_id, Topic.position).all()
    progress = topic_progress_map(user_id)
    practice = practice_by_topic(user_id)
    practice_totals = practice_totals_by_topic()
    tests = tests_by_topic(user_id)
    best = best_topic_test_scores(user_id)

    rows = []
    for topic in topics:
        p = progress.get(topic.id)
        pr = practice.get(topic.id, {"attempted": 0, "correct": 0})
        ts = tests.get(topic.id, {"total": 0, "correct": 0})
        rows.append(
            {
                "slug": topic.slug,
                "name": topic.name,
                "summary": topic.summary,
                "section_slug": topic.section.slug,
                "completed": bool(p and p.completed),
                "completed_at": iso(p.completed_at) if p else None,
                "practice": {**pr, "total": practice_totals.get(topic.id, 0)},
                "tests": {**ts, "percentage": _pct(ts["correct"], ts["total"])},
                "best_topic_test": best.get(topic.id),
            }
        )
    return rows


def section_rows(user_id):
    rows_by_section = {}
    for row in topic_rows(user_id):
        rows_by_section.setdefault(row["section_slug"], []).append(row)

    result = []
    for section in Section.query.order_by(Section.position).all():
        rows = rows_by_section.get(section.slug, [])
        test_total = sum(r["tests"]["total"] for r in rows)
        test_correct = sum(r["tests"]["correct"] for r in rows)
        result.append(
            {
                **section.to_dict(),
                "topics_total": len(rows),
                "topics_completed": sum(r["completed"] for r in rows),
                "practice_attempted": sum(r["practice"]["attempted"] for r in rows),
                "practice_correct": sum(r["practice"]["correct"] for r in rows),
                "practice_total": sum(r["practice"]["total"] for r in rows),
                "test_questions": test_total,
                "test_correct": test_correct,
                "test_percentage": _pct(test_correct, test_total),
                "topics": [{"slug": r["slug"], "name": r["name"], "completed": r["completed"]} for r in rows],
            }
        )
    return result


def submitted_attempts(user_id):
    return (
        TestAttempt.query.filter_by(user_id=user_id, status=STATUS_SUBMITTED)
        .order_by(TestAttempt.submitted_at, TestAttempt.id)
        .all()
    )


def with_change(attempts):
    """Pairs each attempt with the change in score since the previous attempt of the same test."""
    last_by_test, changes = {}, {}
    for attempt in attempts:
        previous = last_by_test.get(attempt.test_id)
        changes[attempt.id] = round(attempt.percentage - previous, 1) if previous is not None else None
        last_by_test[attempt.test_id] = attempt.percentage
    return changes


def dashboard(user):
    from app.services.attempts import attempt_summary

    attempts = submitted_attempts(user.id)
    changes = with_change(attempts)
    sections = section_rows(user.id)
    topics = topic_rows(user.id)

    strongest = None
    eligible = [s for s in sections if s["test_questions"] >= MIN_SECTION_QUESTIONS]
    if eligible:
        best = max(eligible, key=lambda s: (s["test_percentage"], s["test_questions"]))
        strongest = {"slug": best["slug"], "name": best["name"], "percentage": best["test_percentage"]}

    weak = sorted(
        (
            t
            for t in topics
            if t["tests"]["total"] >= MIN_TOPIC_QUESTIONS and t["tests"]["percentage"] < WEAK_TOPIC_THRESHOLD
        ),
        key=lambda t: (t["tests"]["percentage"], -t["tests"]["total"]),
    )[:5]

    completed = sum(t["completed"] for t in topics)
    practice_attempted = sum(t["practice"]["attempted"] for t in topics)
    practice_total = sum(t["practice"]["total"] for t in topics)

    recent = [{**attempt_summary(a), "change": changes[a.id]} for a in reversed(attempts[-5:])]
    trend = [
        {"id": a.id, "title": a.test.title, "percentage": a.percentage, "submitted_at": iso(a.submitted_at)}
        for a in attempts[-12:]
    ]

    return {
        "user": {"full_name": user.full_name, "college_name": user.college_name},
        "tests_attempted": len(attempts),
        "average_percentage": round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else None,
        "progress": {
            "topics_completed": completed,
            "topics_total": len(topics),
            "practice_attempted": practice_attempted,
            "practice_total": practice_total,
            "percent": round(completed * 100 / len(topics)) if topics else 0,
        },
        "strongest_section": strongest,
        "weak_topics": [
            {
                "slug": t["slug"],
                "name": t["name"],
                "section_slug": t["section_slug"],
                "percentage": t["tests"]["percentage"],
                "questions": t["tests"]["total"],
            }
            for t in weak
        ],
        "recent_results": recent,
        "trend": trend,
        "sections": sections,
        "thresholds": {
            "min_section_questions": MIN_SECTION_QUESTIONS,
            "min_topic_questions": MIN_TOPIC_QUESTIONS,
            "weak_below": WEAK_TOPIC_THRESHOLD,
        },
    }
