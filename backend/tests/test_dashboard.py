from tests.conftest import correct_option_id, find_test_id, wrong_option_id


def take_test(client, headers, slug, count, correct):
    """Start a test and answer the first `correct` questions right and the rest wrong."""
    test_id = find_test_id(client, headers, slug)
    attempt = client.post(f"/api/tests/{test_id}/attempts", headers=headers,
                          json={"question_count": count, "duration_minutes": 10}).get_json()["attempt"]
    answers = [
        {"question_id": q["id"], "option_id": (correct_option_id if i < correct else wrong_option_id)(q["id"])}
        for i, q in enumerate(attempt["questions"])
    ]
    return client.post(f"/api/attempts/{attempt['id']}/submit", headers=headers, json={"answers": answers}).get_json()["attempt"]


def test_new_student_sees_empty_state_not_fake_numbers(client, student):
    data = client.get("/api/dashboard", headers=student).get_json()
    assert data["user"]["full_name"] == "Asha Verma"
    assert data["tests_attempted"] == 0
    assert data["average_percentage"] is None
    assert data["strongest_section"] is None
    assert data["weak_topics"] == []
    assert data["recent_results"] == []
    assert data["trend"] == []
    assert data["progress"] == {"topics_completed": 0, "topics_total": 36, "practice_attempted": 0, "practice_total": 144, "percent": 0}


def test_dashboard_reflects_recorded_results(client, student):
    take_test(client, student, "topic-percentages", count=5, correct=5)    # quant 100%
    take_test(client, student, "topic-syllogisms", count=5, correct=1)     # logical 20%
    client.post("/api/topics/percentages/progress", headers=student, json={"completed": True})

    data = client.get("/api/dashboard", headers=student).get_json()
    assert data["tests_attempted"] == 2
    assert data["average_percentage"] == 60.0
    assert data["strongest_section"]["slug"] == "quant"
    assert data["strongest_section"]["percentage"] == 100.0
    assert [t["slug"] for t in data["weak_topics"]] == ["syllogisms"]
    assert data["weak_topics"][0]["percentage"] == 20.0
    assert data["recent_results"][0]["test"]["slug"] == "topic-syllogisms"
    assert [p["percentage"] for p in data["trend"]] == [100.0, 20.0]
    assert data["progress"]["topics_completed"] == 1
    assert data["progress"]["percent"] == 3


def test_section_and_topic_performance_endpoints(client, student):
    take_test(client, student, "topic-tenses", count=4, correct=3)
    sections = client.get("/api/dashboard/sections", headers=student).get_json()["sections"]
    verbal = next(s for s in sections if s["slug"] == "verbal")
    assert (verbal["test_questions"], verbal["test_correct"], verbal["test_percentage"]) == (4, 3, 75.0)

    topics = client.get("/api/dashboard/topics", headers=student).get_json()["topics"]
    tenses = next(t for t in topics if t["slug"] == "tenses")
    assert tenses["tests"] == {"total": 4, "correct": 3, "percentage": 75.0}
    assert tenses["best_topic_test"] == 75.0


def test_practice_counts_latest_answer_per_question(client, student):
    question = client.get("/api/topics/averages/practice", headers=student).get_json()["questions"][0]
    for option in (wrong_option_id(question["id"]), correct_option_id(question["id"])):
        client.post("/api/practice/answers", headers=student, json={"question_id": question["id"], "option_id": option})
    progress = client.get("/api/dashboard", headers=student).get_json()["progress"]
    assert progress["practice_attempted"] == 1
    topic = next(t for t in client.get("/api/progress/topics", headers=student).get_json()["topics"] if t["slug"] == "averages")
    assert topic["practice"] == {"attempted": 1, "correct": 1, "total": 4}
