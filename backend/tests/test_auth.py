from app.extensions import db
from app.models import User
from app.services import google_auth
from tests.conftest import PASSWORD, auth_headers, register


def test_register_creates_account_and_hashes_password(client):
    res = register(client)
    assert res.status_code == 201
    body = res.get_json()
    assert body["access_token"]
    assert body["user"]["email"] == "asha@college.edu"

    user = User.query.filter_by(email="asha@college.edu").one()
    # Neither the password nor its hash is ever sent back.
    assert "password_hash" not in body["user"]
    assert PASSWORD not in res.get_data(as_text=True)
    assert user.password_hash not in res.get_data(as_text=True)
    assert user.password_hash != PASSWORD
    assert user.check_password(PASSWORD)


def test_register_normalises_email_and_indian_mobile(client):
    res = register(client, email="  Asha@College.EDU ", mobile="+91 98765-43210")
    assert res.status_code == 201
    user = res.get_json()["user"]
    assert user["email"] == "asha@college.edu"
    assert user["mobile"] == "9876543210"


def test_register_rejects_invalid_input(client):
    res = client.post(
        "/api/auth/register",
        json={
            "full_name": "",
            "mobile": "12345",
            "email": "not-an-email",
            "college_name": "",
            "password": "short",
            "confirm_password": "different",
        },
    )
    assert res.status_code == 400
    fields = res.get_json()["error"]["fields"]
    assert set(fields) == {"full_name", "mobile", "email", "college_name", "password"}


def test_register_rejects_password_mismatch_and_bad_mobile_prefix(client):
    res = register(client, mobile="5123456789", confirm_password="Placement2025")
    assert res.status_code == 400
    fields = res.get_json()["error"]["fields"]
    assert "mobile" in fields and "confirm_password" in fields


def test_register_requires_json_object(client):
    res = client.post("/api/auth/register", data="nope", content_type="text/plain")
    assert res.status_code == 400


def test_duplicate_email_is_rejected_case_insensitively(client):
    assert register(client).status_code == 201
    res = register(client, email="ASHA@college.edu", mobile="9000000001")
    assert res.status_code == 409
    assert "email" in res.get_json()["error"]["fields"]
    assert User.query.count() == 1


def test_duplicate_mobile_is_rejected(client):
    assert register(client).status_code == 201
    res = register(client, email="other@college.edu", mobile="09876543210")
    assert res.status_code == 409
    assert "mobile" in res.get_json()["error"]["fields"]


def test_login_success_and_failures_share_one_message(client):
    register(client)
    ok = client.post("/api/auth/login", json={"email": "ASHA@college.edu", "password": PASSWORD})
    assert ok.status_code == 200
    assert ok.get_json()["access_token"]

    wrong = client.post("/api/auth/login", json={"email": "asha@college.edu", "password": "Wrong12345"})
    unknown = client.post("/api/auth/login", json={"email": "nobody@college.edu", "password": PASSWORD})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.get_json()["error"]["message"] == unknown.get_json()["error"]["message"]


def test_login_validates_missing_fields(client):
    res = client.post("/api/auth/login", json={})
    assert res.status_code == 400
    assert set(res.get_json()["error"]["fields"]) == {"email", "password"}


def test_me_requires_token(client, student):
    assert client.get("/api/auth/me").status_code == 401
    res = client.get("/api/auth/me", headers=student)
    assert res.status_code == 200
    assert "password_hash" not in res.get_json()["user"]


def test_invalid_token_is_rejected(client):
    res = client.get("/api/auth/me", headers=auth_headers("not.a.token"))
    assert res.status_code == 401


def test_logout_revokes_token(client, student):
    assert client.post("/api/auth/logout", headers=student).status_code == 200
    res = client.get("/api/auth/me", headers=student)
    assert res.status_code == 401
    assert res.get_json()["error"]["code"] == "token_revoked"


def test_profile_update_and_email_is_read_only(client, student):
    res = client.patch("/api/profile", headers=student, json={"full_name": "Asha V", "college_name": "NIT Trichy"})
    assert res.status_code == 200
    assert res.get_json()["user"]["college_name"] == "NIT Trichy"

    res = client.patch("/api/profile", headers=student, json={"email": "new@college.edu"})
    assert res.status_code == 400


def test_profile_mobile_must_stay_unique(client, student, other_student):
    res = client.patch("/api/profile", headers=other_student, json={"mobile": "9876543210"})
    assert res.status_code == 409


def test_change_password_requires_current_password(client, student):
    bad = client.post(
        "/api/profile/password",
        headers=student,
        json={"current_password": "Wrong12345", "new_password": "NewPass2025", "confirm_password": "NewPass2025"},
    )
    assert bad.status_code == 400
    ok = client.post(
        "/api/profile/password",
        headers=student,
        json={"current_password": PASSWORD, "new_password": "NewPass2025", "confirm_password": "NewPass2025"},
    )
    assert ok.status_code == 200
    login = client.post("/api/auth/login", json={"email": "asha@college.edu", "password": "NewPass2025"})
    assert login.status_code == 200


def test_google_sign_in_disabled_without_client_id(client):
    config = client.get("/api/auth/config").get_json()
    assert config["google_enabled"] is False
    assert client.post("/api/auth/google", json={"credential": "x"}).status_code == 404


def test_google_sign_in_creates_then_links_accounts(app, client, monkeypatch):
    app.config["GOOGLE_CLIENT_ID"] = "test-client-id"
    claims = {"sub": "google-123", "email": "Ravi@College.edu", "email_verified": True, "name": "Ravi Kumar", "iss": "accounts.google.com"}
    monkeypatch.setattr(google_auth, "verify_google_credential", lambda token, cid: claims)

    res = client.post("/api/auth/google", json={"credential": "token"})
    assert res.status_code == 201
    user = res.get_json()["user"]
    assert user["profile_complete"] is False
    assert user["email_verified_by_google"] is True
    assert user["has_password"] is False

    again = client.post("/api/auth/google", json={"credential": "token"})
    assert again.status_code == 200
    assert User.query.count() == 1

    # An existing password account with the same email gets linked, not duplicated.
    register(client, email="meena@college.edu", mobile="9111111111")
    claims.update({"sub": "google-456", "email": "meena@college.edu"})
    linked = client.post("/api/auth/google", json={"credential": "token"})
    assert linked.status_code == 200
    assert linked.get_json()["user"]["has_password"] is True
    assert User.query.count() == 2


def test_google_sign_in_rejects_unverified_email(app, client, monkeypatch):
    app.config["GOOGLE_CLIENT_ID"] = "test-client-id"
    monkeypatch.setattr(
        google_auth,
        "verify_google_credential",
        lambda token, cid: {"sub": "g-1", "email": "x@college.edu", "email_verified": False},
    )
    assert client.post("/api/auth/google", json={"credential": "token"}).status_code == 401
    assert db.session.query(User).count() == 0
