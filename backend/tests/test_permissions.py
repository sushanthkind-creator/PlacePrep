import pytest

from tests.conftest import find_test_id

PROTECTED = [
    ("get", "/api/auth/me"),
    ("post", "/api/auth/logout"),
    ("get", "/api/profile"),
    ("patch", "/api/profile"),
    ("post", "/api/profile/password"),
    ("get", "/api/sections"),
    ("get", "/api/sections/quant"),
    ("get", "/api/topics/percentages"),
    ("get", "/api/topics/percentages/examples"),
    ("get", "/api/topics/percentages/practice"),
    ("post", "/api/topics/percentages/progress"),
    ("get", "/api/progress/topics"),
    ("post", "/api/practice/answers"),
    ("get", "/api/tests"),
    ("get", "/api/tests/1"),
    ("post", "/api/tests/1/attempts"),
    ("get", "/api/attempts"),
    ("get", "/api/attempts/1"),
    ("put", "/api/attempts/1/answers"),
    ("post", "/api/attempts/1/submit"),
    ("get", "/api/attempts/1/result"),
    ("get", "/api/dashboard"),
    ("get", "/api/dashboard/sections"),
    ("get", "/api/dashboard/topics"),
]


@pytest.mark.parametrize("method,url", PROTECTED)
def test_private_endpoints_require_login(client, method, url):
    res = getattr(client, method)(url, json={})
    assert res.status_code == 401
    assert res.get_json()["error"]["code"] == "auth_required"


def test_students_cannot_touch_each_others_attempts(client, student, other_student):
    test_id = find_test_id(client, student, "topic-percentages")
    attempt = client.post(f"/api/tests/{test_id}/attempts", headers=student,
                          json={"question_count": 3, "duration_minutes": 5}).get_json()["attempt"]
    aid = attempt["id"]
    question = attempt["questions"][0]

    assert client.get(f"/api/attempts/{aid}", headers=other_student).status_code == 404
    assert client.put(f"/api/attempts/{aid}/answers", headers=other_student,
                      json={"question_id": question["id"], "option_id": None}).status_code == 404
    assert client.post(f"/api/attempts/{aid}/submit", headers=other_student, json={}).status_code == 404

    client.post(f"/api/attempts/{aid}/submit", headers=student, json={})
    assert client.get(f"/api/attempts/{aid}/result", headers=other_student).status_code == 404
    assert client.get(f"/api/attempts/{aid}/result", headers=student).status_code == 200

    assert client.get("/api/attempts", headers=other_student).get_json()["total"] == 0
    assert client.get("/api/dashboard", headers=other_student).get_json()["tests_attempted"] == 0
    assert client.get("/api/dashboard", headers=student).get_json()["tests_attempted"] == 1


def test_progress_is_per_student(client, student, other_student):
    client.post("/api/topics/percentages/progress", headers=student, json={"completed": True})
    mine = client.get("/api/dashboard", headers=student).get_json()["progress"]["topics_completed"]
    theirs = client.get("/api/dashboard", headers=other_student).get_json()["progress"]["topics_completed"]
    assert (mine, theirs) == (1, 0)


def test_cors_allows_only_configured_origin(client):
    allowed = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    blocked = client.get("/api/health", headers={"Origin": "http://evil.example"})
    assert allowed.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"
    assert "Access-Control-Allow-Origin" not in blocked.headers
