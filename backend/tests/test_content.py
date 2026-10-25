"""Checks on the seeded learning content itself."""

import math
import re

import pytest

from app.models import AnswerOption, Question, Section, TestDefinition, Topic
from app.seed import run_seed
from app.seed.builders import LABELS
from app.seed.content_quant import QUANT_TOPICS
from app.seed.seed_data import CONTENT

NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")


def parse_number(text):
    match = NUMBER.search(text.replace(",", ""))
    assert match, f"No number in option text: {text!r}"
    value = match.group()
    if "/" in value:
        num, den = value.split("/")
        return float(num) / float(den)
    return float(value)


def test_every_question_has_four_options_and_one_answer(app):
    for question in Question.query.all():
        assert len(question.options) == 4, question.seed_key
        assert sum(o.is_correct for o in question.options) == 1, question.seed_key
        assert question.explanation.strip(), question.seed_key
        assert len({o.text for o in question.options}) == 4, f"duplicate options in {question.seed_key}"


def test_every_topic_has_practice_and_test_pools():
    for section, topics in CONTENT.items():
        for t in topics:
            assert len(t["practice"]) >= 4, t["slug"]
            assert len(t["test"]) >= 6, t["slug"]
            assert len(t["examples"]) >= 2, t["slug"]


def test_answer_letters_are_spread_out():
    """Guards against lazily putting every correct answer in the same position."""
    counts = {label: 0 for label in LABELS}
    for topics in CONTENT.values():
        for t in topics:
            for item in t["practice"] + t["test"]:
                counts[item["answer"]] += 1
    total = sum(counts.values())
    assert all(count / total > 0.12 for count in counts.values()), counts


QUANT_CHECKS = [
    pytest.param(item, id=f"{t['slug']}-{pool}-{i + 1}")
    for t in QUANT_TOPICS
    for pool in ("practice", "test")
    for i, item in enumerate(t[pool])
    if item["check"]
]


@pytest.mark.parametrize("item", QUANT_CHECKS)
def test_quant_answer_keys_match_computed_values(item):
    correct_text = item["options"][LABELS.index(item["answer"])]
    expected = item["check"]()
    assert math.isclose(parse_number(correct_text), expected, rel_tol=1e-9, abs_tol=1e-6), (
        f"{item['prompt']!r}: option {correct_text!r} but computed {expected}"
    )


def test_most_quant_questions_are_machine_checked():
    total = sum(len(t["practice"]) + len(t["test"]) for t in QUANT_TOPICS)
    assert len(QUANT_CHECKS) / total > 0.85


def test_seed_is_idempotent(app):
    before = (Section.query.count(), Topic.query.count(), Question.query.count(),
              AnswerOption.query.count(), TestDefinition.query.count())
    run_seed()
    run_seed()
    after = (Section.query.count(), Topic.query.count(), Question.query.count(),
             AnswerOption.query.count(), TestDefinition.query.count())
    assert before == after == (3, 36, 360, 1440, 40)
