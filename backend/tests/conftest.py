import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.seed import run_seed

PASSWORD = "Placement2024"


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        run_seed()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, **overrides):
    payload = {
        "full_name": "Asha Verma",
        "mobile": "9876543210",
        "email": "asha@college.edu",
        "college_name": "Govt Engineering College",
        "password": PASSWORD,
        "confirm_password": PASSWORD,
    }
    payload.update(overrides)
    return client.post("/api/auth/register", json=payload)


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def student(client):
    """A registered student: returns auth headers."""
    res = register(client)
    assert res.status_code == 201, res.get_json()
    return auth_headers(res.get_json()["access_token"])


@pytest.fixture
def other_student(client):
    res = register(client, full_name="Bilal Khan", mobile="9123456780", email="bilal@college.edu")
    assert res.status_code == 201, res.get_json()
    return auth_headers(res.get_json()["access_token"])


def find_test_id(client, headers, slug):
    tests = client.get("/api/tests", headers=headers).get_json()["tests"]
    return next(t["id"] for t in tests if t["slug"] == slug)


def correct_option_id(question_id):
    from app.models import Question

    return db.session.get(Question, question_id).correct_option.id


def wrong_option_id(question_id):
    from app.models import Question

    return next(o.id for o in db.session.get(Question, question_id).options if not o.is_correct)
