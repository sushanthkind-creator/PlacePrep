from datetime import timedelta

from app.extensions import db
from app.models import STATUS_SUBMITTED, TestAttempt
from tests.conftest import correct_option_id, find_test_id, wrong_option_id

SECRET_KEYS = {"is_correct", "correct_option_id", "explanation"}


def start(client, headers, slug, **settings):
    test_id = find_test_id(client, headers, slug)
    return client.post(f"/api/tests/{test_id}/attempts", headers=headers, json=settings)


def test_list_tests_covers_every_scope(client, student):
    tests = client.get("/api/tests", headers=student).get_json()["tests"]
    scopes = {t["scope"] for t in tests}
    assert scopes == {"mixed", "section", "topic"}
    assert len([t for t in tests if t["scope"] == "topic"]) == 36
    filtered = client.get("/api/tests?scope=section", headers=student).get_json()["tests"]
    assert len(filtered) == 3
    assert client.get("/api/tests?scope=bogus", headers=student).status_code == 400


def test_instructions(client, student):
    test_id = find_test_id(client, student, "topic-percentages")
    test = client.get(f"/api/tests/{test_id}", headers=student).get_json()["test"]
    assert test["instructions"]
    assert test["question_count_range"] == [3, 6]
    assert client.get("/api/tests/99999", headers=student).status_code == 404


def test_start_attempt_hides_answer_key(client, student):
    res = start(client, student, "topic-percentages", question_count=5, duration_minutes=5)
    assert res.status_code == 201
    attempt = res.get_json()["attempt"]
    assert attempt["question_count"] == 5
    assert attempt["remaining_seconds"] > 290
    for question in attempt["questions"]:
        assert len(question["options"]) == 4
        assert SECRET_KEYS.isdisjoint(question)
        assert all(set(o) == {"id", "label", "text"} for o in question["options"])


def test_start_attempt_validates_settings(client, student):
    assert start(client, student, "topic-percentages", question_count=50).status_code == 400
    assert start(client, student, "topic-percentages", question_count=2).status_code == 400
    assert start(client, student, "topic-percentages", duration_minutes=0).status_code == 400
    assert start(client, student, "topic-percentages", duration_minutes=500).status_code == 400
    assert start(client, student, "topic-percentages", question_count="5").status_code == 400


def test_unfinished_attempt_is_resumed_not_duplicated(client, student):
    first = start(client, student, "topic-tenses", question_count=4, duration_minutes=5)
    second = start(client, student, "topic-tenses", question_count=6, duration_minutes=9)
    assert first.status_code == 201 and second.status_code == 200
    assert second.get_json()["resumed"] is True
    assert first.get_json()["attempt"]["id"] == second.get_json()["attempt"]["id"]
    assert TestAttempt.query.count() == 1


def test_section_test_spreads_questions_across_topics(client, student):
    attempt = start(client, student, "section-quant", question_count=14, duration_minutes=20).get_json()["attempt"]
    topics = {q["topic"]["slug"] for q in attempt["questions"]}
    assert len(topics) == 14


def test_scoring_is_done_on_the_server(client, student):
    attempt = start(client, student, "topic-percentages", question_count=5, duration_minutes=5).get_json()["attempt"]
    qs = attempt["questions"]
    answers = [
        {"question_id": qs[0]["id"], "option_id": correct_option_id(qs[0]["id"])},
        {"question_id": qs[1]["id"], "option_id": correct_option_id(qs[1]["id"])},
        {"question_id": qs[2]["id"], "option_id": wrong_option_id(qs[2]["id"])},
        {"question_id": qs[3]["id"], "option_id": None},
    ]
    # Extra fields such as a client-side score are ignored.
    res = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={"answers": answers, "percentage": 100})
    assert res.status_code == 200
    result = res.get_json()["attempt"]
    assert (result["correct"], result["incorrect"], result["unanswered"]) == (2, 1, 2)
    assert result["percentage"] == 40.0
    assert result["status"] == "submitted"
    assert result["time_taken_seconds"] is not None
    review = {q["id"]: q for q in result["questions"]}
    assert review[qs[2]["id"]]["is_correct"] is False
    assert review[qs[2]["id"]]["explanation"]
    assert result["breakdown"]["topics"][0]["slug"] == "percentages"
    assert result["breakdown"]["sections"][0]["total"] == 5


def test_saved_answers_count_when_submitting_without_payload(client, student):
    attempt = start(client, student, "topic-analogies", question_count=3, duration_minutes=5).get_json()["attempt"]
    for q in attempt["questions"]:
        res = client.put(
            f"/api/attempts/{attempt['id']}/answers",
            headers=student,
            json={"question_id": q["id"], "option_id": correct_option_id(q["id"])},
        )
        assert res.status_code == 200
    result = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={}).get_json()["attempt"]
    assert result["correct"] == 3 and result["percentage"] == 100.0


def test_submission_validates_question_and_option_ids(client, student):
    attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=5).get_json()["attempt"]
    qs = attempt["questions"]
    foreign = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student,
                          json={"answers": [{"question_id": 999999, "option_id": None}]})
    assert foreign.status_code == 400
    mismatched = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student,
                             json={"answers": [{"question_id": qs[0]["id"], "option_id": qs[1]["options"][0]["id"]}]})
    assert mismatched.status_code == 400
    duplicate = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student,
                            json={"answers": [{"question_id": qs[0]["id"], "option_id": None}] * 2})
    assert duplicate.status_code == 400
    # Rejected submissions leave the attempt open.
    assert db.session.get(TestAttempt, attempt["id"]).status == "in_progress"


def test_duplicate_submission_is_rejected(client, student):
    attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=5).get_json()["attempt"]
    first = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={})
    second = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={})
    assert first.status_code == 200
    assert second.status_code == 409
    assert TestAttempt.query.filter_by(status=STATUS_SUBMITTED).count() == 1
    saving = client.put(f"/api/attempts/{attempt['id']}/answers", headers=student,
                        json={"question_id": attempt["questions"][0]["id"], "option_id": None})
    assert saving.status_code == 409


def _expire(attempt_id, seconds_ago):
    row = db.session.get(TestAttempt, attempt_id)
    row.expires_at = row.started_at - timedelta(seconds=seconds_ago) + timedelta(seconds=0)
    row.started_at = row.expires_at - timedelta(seconds=row.duration_seconds)
    db.session.commit()


def test_late_submission_uses_only_answers_saved_in_time(client, student):
    attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=1).get_json()["attempt"]
    q0 = attempt["questions"][0]
    client.put(f"/api/attempts/{attempt['id']}/answers", headers=student,
               json={"question_id": q0["id"], "option_id": correct_option_id(q0["id"])})
    _expire(attempt["id"], seconds_ago=120)  # well past the grace period

    late_answers = [{"question_id": q["id"], "option_id": correct_option_id(q["id"])} for q in attempt["questions"]]
    res = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={"answers": late_answers})
    result = res.get_json()["attempt"]
    assert res.status_code == 200
    assert result["auto_submitted"] is True
    assert result["correct"] == 1
    assert result["time_taken_seconds"] == 60


def test_submission_within_grace_period_is_accepted(client, student):
    attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=1).get_json()["attempt"]
    _expire(attempt["id"], seconds_ago=5)  # timer hit zero 5 s ago; grace is 15 s
    answers = [{"question_id": q["id"], "option_id": correct_option_id(q["id"])} for q in attempt["questions"]]
    result = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={"answers": answers}).get_json()["attempt"]
    assert result["correct"] == 3
    assert result["auto_submitted"] is False


def test_expired_attempt_is_auto_submitted_on_next_request(client, student):
    attempt = start(client, student, "topic-tenses", question_count=3, duration_minutes=1).get_json()["attempt"]
    _expire(attempt["id"], seconds_ago=120)
    view = client.get(f"/api/attempts/{attempt['id']}", headers=student).get_json()["attempt"]
    assert view["status"] == "submitted"
    assert view["auto_submitted"] is True
    assert "questions" not in view
    result = client.get(f"/api/attempts/{attempt['id']}/result", headers=student)
    assert result.status_code == 200


def test_results_unavailable_before_submission(client, student):
    attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=5).get_json()["attempt"]
    res = client.get(f"/api/attempts/{attempt['id']}/result", headers=student)
    assert res.status_code == 409


def test_history_lists_attempts_with_change(client, student):
    for answer_correctly in (False, True):
        attempt = start(client, student, "topic-percentages", question_count=3, duration_minutes=5).get_json()["attempt"]
        answers = [
            {"question_id": q["id"], "option_id": (correct_option_id if answer_correctly else wrong_option_id)(q["id"])}
            for q in attempt["questions"]
        ]
        client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={"answers": answers})

    history = client.get("/api/attempts", headers=student).get_json()
    assert history["total"] == 2
    latest, earlier = history["attempts"]
    assert latest["percentage"] == 100.0 and earlier["percentage"] == 0.0
    assert latest["change"] == 100.0 and earlier["change"] is None


def test_mixed_mock_covers_all_sections(client, student):
    attempt = start(client, student, "placement-mock", question_count=12, duration_minutes=15).get_json()["attempt"]
    result = client.post(f"/api/attempts/{attempt['id']}/submit", headers=student, json={}).get_json()["attempt"]
    sections = {s["slug"] for s in result["breakdown"]["sections"]}
    assert sections == {"logical", "quant", "verbal"}
    assert result["unanswered"] == 12
