"""Idempotent content seeding: every record is matched by a stable key and updated in place."""

from app.extensions import db
from app.models import (
    POOL_PRACTICE,
    POOL_TEST,
    SCOPE_MIXED,
    SCOPE_SECTION,
    SCOPE_TOPIC,
    AnswerOption,
    Lesson,
    Passage,
    Question,
    Section,
    SolvedExample,
    TestDefinition,
    Topic,
)
from app.seed.builders import LABELS
from app.seed.seed_data import CONTENT, PASSAGES, SECTIONS

TOPIC_TEST_QUESTIONS = 5
TOPIC_TEST_MINUTES = 7
SECTION_TEST_QUESTIONS = 20
SECTION_TEST_MINUTES = 25
MOCK_TEST_QUESTIONS = 30
MOCK_TEST_MINUTES = 40


def _upsert(model, lookup, values):
    row = model.query.filter_by(**lookup).first()
    if row is None:
        row = model(**lookup)
        db.session.add(row)
    for key, value in values.items():
        setattr(row, key, value)
    return row


def _seed_questions(topic_row, items, pool, passage_ids):
    for position, item in enumerate(items, start=1):
        seed_key = f"{topic_row.slug}-{pool}-{position}"
        question = _upsert(
            Question,
            {"seed_key": seed_key},
            {
                "topic_id": topic_row.id,
                "pool": pool,
                "position": position,
                "prompt": item["prompt"],
                "table": item["table"],
                "explanation": item["explanation"],
                "difficulty": item["difficulty"],
                "passage_id": passage_ids[item["passage"]] if item["passage"] else None,
            },
        )
        db.session.flush()
        for label, text in zip(LABELS, item["options"]):
            _upsert(
                AnswerOption,
                {"question_id": question.id, "label": label},
                {"text": text, "is_correct": label == item["answer"]},
            )


def run_seed():
    sections = {}
    for position, data in enumerate(SECTIONS, start=1):
        sections[data["slug"]] = _upsert(
            Section,
            {"slug": data["slug"]},
            {
                "name": data["name"],
                "short_name": data["short_name"],
                "description": data["description"],
                "color": data["color"],
                "position": position,
            },
        )
    db.session.flush()

    topic_rows = []
    question_count = 0
    for section_slug, topics in CONTENT.items():
        section = sections[section_slug]
        for position, data in enumerate(topics, start=1):
            topic_row = _upsert(
                Topic,
                {"slug": data["slug"]},
                {"section_id": section.id, "name": data["name"], "summary": data["summary"], "position": position},
            )
            db.session.flush()
            topic_rows.append((section, topic_row))

            _upsert(
                Lesson,
                {"topic_id": topic_row.id},
                {
                    "concept": data["concept"],
                    "key_points": data["key_points"],
                    "formulas": data["formulas"],
                    "tips": data["tips"],
                },
            )
            for ex_pos, example in enumerate(data["examples"], start=1):
                _upsert(
                    SolvedExample,
                    {"topic_id": topic_row.id, "position": ex_pos},
                    {"problem": example["problem"], "steps": example["steps"], "answer": example["answer"]},
                )
            SolvedExample.query.filter(
                SolvedExample.topic_id == topic_row.id, SolvedExample.position > len(data["examples"])
            ).delete()

            passage_ids = {}
            used = {item["passage"] for item in data["practice"] + data["test"] if item["passage"]}
            for key in sorted(used):
                passage = PASSAGES[key]
                row = _upsert(
                    Passage, {"key": key}, {"topic_id": topic_row.id, "title": passage["title"], "body": passage["body"]}
                )
                db.session.flush()
                passage_ids[key] = row.id

            _seed_questions(topic_row, data["practice"], POOL_PRACTICE, passage_ids)
            _seed_questions(topic_row, data["test"], POOL_TEST, passage_ids)
            question_count += len(data["practice"]) + len(data["test"])

    _seed_tests(sections, topic_rows)
    db.session.commit()
    return {
        "sections": len(sections),
        "topics": len(topic_rows),
        "questions": question_count,
        "tests": TestDefinition.query.count(),
    }


def _seed_tests(sections, topic_rows):
    position = 0
    _upsert(
        TestDefinition,
        {"slug": "placement-mock"},
        {
            "title": "Full placement mock",
            "description": "Questions from all three sections, like a real campus aptitude round.",
            "scope": SCOPE_MIXED,
            "section_id": None,
            "topic_id": None,
            "default_question_count": MOCK_TEST_QUESTIONS,
            "default_duration_minutes": MOCK_TEST_MINUTES,
            "position": position,
        },
    )
    for section in sections.values():
        position += 1
        _upsert(
            TestDefinition,
            {"slug": f"section-{section.slug}"},
            {
                "title": f"{section.short_name} section test",
                "description": f"Mixed questions from every {section.short_name} topic.",
                "scope": SCOPE_SECTION,
                "section_id": section.id,
                "topic_id": None,
                "default_question_count": SECTION_TEST_QUESTIONS,
                "default_duration_minutes": SECTION_TEST_MINUTES,
                "position": position,
            },
        )
    for section, topic_row in topic_rows:
        position += 1
        _upsert(
            TestDefinition,
            {"slug": f"topic-{topic_row.slug}"},
            {
                "title": f"{topic_row.name} test",
                "description": f"Test questions on {topic_row.name}.",
                "scope": SCOPE_TOPIC,
                "section_id": section.id,
                "topic_id": topic_row.id,
                "default_question_count": TOPIC_TEST_QUESTIONS,
                "default_duration_minutes": TOPIC_TEST_MINUTES,
                "position": position,
            },
        )
