import importlib

import app.config as config


def _url_for(monkeypatch, value):
    monkeypatch.setenv("DATABASE_URL", value)
    return importlib.reload(config).Config.SQLALCHEMY_DATABASE_URI


def test_render_postgres_urls_use_psycopg_driver(monkeypatch):
    assert _url_for(monkeypatch, "postgres://u:p@host:5432/db") == "postgresql+psycopg://u:p@host:5432/db"
    assert _url_for(monkeypatch, "postgresql://u:p@host/db") == "postgresql+psycopg://u:p@host/db"


def test_relative_sqlite_path_goes_to_instance_folder(monkeypatch):
    url = _url_for(monkeypatch, "sqlite:///placeprep.db")
    assert url.startswith("sqlite:///") and url.endswith("instance/placeprep.db")


def teardown_module():
    importlib.reload(config)
