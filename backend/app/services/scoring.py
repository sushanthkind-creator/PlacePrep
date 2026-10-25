"""Server-side grading. Scores are always computed here from stored answers and the answer key."""


def grade_attempt(attempt):
    correct = incorrect = unanswered = 0
    for item in attempt.questions:
        if item.selected_option_id is None:
            item.is_correct = None
            unanswered += 1
            continue
        key = item.question.correct_option
        item.is_correct = key is not None and item.selected_option_id == key.id
        if item.is_correct:
            correct += 1
        else:
            incorrect += 1

    total = len(attempt.questions)
    attempt.correct_count = correct
    attempt.incorrect_count = incorrect
    attempt.unanswered_count = unanswered
    attempt.percentage = round(correct * 100 / total, 1) if total else 0.0


def _empty_bucket(ref):
    return {**ref, "total": 0, "correct": 0, "incorrect": 0, "unanswered": 0}


def _finish(buckets):
    rows = list(buckets.values())
    for row in rows:
        row["percentage"] = round(row["correct"] * 100 / row["total"], 1) if row["total"] else 0.0
    return rows


def breakdown(attempt):
    """Per-section and per-topic results for a graded attempt."""
    sections, topics = {}, {}
    for item in attempt.questions:
        topic = item.question.topic
        section = topic.section
        s = sections.setdefault(
            section.id, _empty_bucket({"slug": section.slug, "name": section.name, "color": section.color})
        )
        t = topics.setdefault(
            topic.id, _empty_bucket({"slug": topic.slug, "name": topic.name, "section_slug": section.slug})
        )
        outcome = "unanswered" if item.is_correct is None else ("correct" if item.is_correct else "incorrect")
        for bucket in (s, t):
            bucket["total"] += 1
            bucket[outcome] += 1
    return {"sections": _finish(sections), "topics": _finish(topics)}
