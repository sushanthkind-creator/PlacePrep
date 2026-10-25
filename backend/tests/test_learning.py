from app.extensions import db
from app.models import POOL_TEST, Question
from tests.conftest import correct_option_id, wrong_option_id

SECRET_KEYS = {"is_correct", "correct_option_id", "explanation"}


def _contains_key(value, keys):
    if isinstance(value, dict):
        return any(k in keys and v is not None for k, v in value.items()) or any(_contains_key(v, keys) for v in value.values())
    if isinstance(value, list):
        return any(_contains_key(v, keys) for v in value)
    return False


def test_learning_requires_login(client):
    assert client.get("/api/sections").status_code == 401
    assert client.get("/api/topics/percentages").status_code == 401


def test_three_sections_with_all_topics(client, student):
    sections = client.get("/api/sections", headers=student).get_json()["sections"]
    assert [s["slug"] for s in sections] == ["logical", "quant", "verbal"]
    assert [s["topics_total"] for s in sections] == [10, 14, 12]
    assert all(s["topics_completed"] == 0 for s in sections)


def test_section_detail_and_unknown_section(client, student):
    res = client.get("/api/sections/quant", headers=student)
    assert res.status_code == 200
    topics = res.get_json()["section"]["topics"]
    assert len(topics) == 14 and topics[0]["slug"] == "percentages"
    assert client.get("/api/sections/history", headers=student).status_code == 404


def test_every_topic_has_full_lesson_content(client, student):
    for section in client.get("/api/sections", headers=student).get_json()["sections"]:
        detail = client.get(f"/api/sections/{section['slug']}", headers=student).get_json()["section"]
        for t in detail["topics"]:
            topic = client.get(f"/api/topics/{t['slug']}", headers=student).get_json()["topic"]
            assert topic["lesson"]["concept"], t["slug"]
            assert topic["lesson"]["key_points"], t["slug"]
            assert len(topic["examples"]) >= 2, t["slug"]
            assert all(e["steps"] for e in topic["examples"]), t["slug"]
            practice = client.get(f"/api/topics/{t['slug']}/practice", headers=student).get_json()["questions"]
            assert len(practice) >= 4, t["slug"]


def test_examples_endpoint(client, student):
    res = client.get("/api/topics/blood-relations/examples", headers=student)
    assert res.status_code == 200
    assert len(res.get_json()["examples"]) == 2


def test_practice_questions_hide_answers_until_checked(client, student):
    questions = client.get("/api/topics/syllogisms/practice", headers=student).get_json()["questions"]
    assert all(q["review"] is None for q in questions)
    assert not _contains_key(questions, SECRET_KEYS)
    assert all(len(q["options"]) == 4 for q in questions)


def test_practice_answer_evaluation(client, student):
    question = client.get("/api/topics/percentages/practice", headers=student).get_json()["questions"][0]
    right = correct_option_id(question["id"])
    wrong = wrong_option_id(question["id"])

    res = client.post("/api/practice/answers", headers=student, json={"question_id": question["id"], "option_id": wrong})
    review = res.get_json()["review"]
    assert res.status_code == 200
    assert review["is_correct"] is False
    assert review["correct_option_id"] == right
    assert review["explanation"]

    res = client.post("/api/practice/answers", headers=student, json={"question_id": question["id"], "option_id": right})
    assert res.get_json()["review"]["is_correct"] is True

    # The latest answer is shown when the page is reloaded.
    reloaded = client.get("/api/topics/percentages/practice", headers=student).get_json()["questions"][0]
    assert reloaded["review"]["is_correct"] is True


def test_practice_cannot_reveal_test_answers(client, student):
    test_question = Question.query.filter_by(pool=POOL_TEST).first()
    res = client.post(
        "/api/practice/answers",
        headers=student,
        json={"question_id": test_question.id, "option_id": test_question.options[0].id},
    )
    assert res.status_code == 404


def test_practice_rejects_option_from_another_question(client, student):
    questions = client.get("/api/topics/analogies/practice", headers=student).get_json()["questions"]
    res = client.post(
        "/api/practice/answers",
        headers=student,
        json={"question_id": questions[0]["id"], "option_id": questions[1]["options"][0]["id"]},
    )
    assert res.status_code == 400


def test_practice_rejects_non_integer_ids(client, student):
    res = client.post("/api/practice/answers", headers=student, json={"question_id": "1", "option_id": True})
    assert res.status_code == 400


def test_mark_topic_completed_updates_progress(client, student):
    res = client.post("/api/topics/tenses/progress", headers=student, json={"completed": True})
    assert res.status_code == 200
    assert res.get_json()["progress"]["completed"] is True

    sections = client.get("/api/sections", headers=student).get_json()["sections"]
    verbal = next(s for s in sections if s["slug"] == "verbal")
    assert verbal["topics_completed"] == 1

    assert client.post("/api/topics/tenses/progress", headers=student, json={"completed": "yes"}).status_code == 400
    undo = client.post("/api/topics/tenses/progress", headers=student, json={"completed": False})
    assert undo.get_json()["progress"]["completed"] is False


def test_topic_neighbours(client, student):
    topic = client.get("/api/topics/percentages", headers=student).get_json()["topic"]
    assert topic["previous"] is None
    assert topic["next"]["slug"] == "profit-and-loss"
    assert db.session is not None
