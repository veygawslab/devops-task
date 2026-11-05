from fastapi.testclient import TestClient

from src.main import app
from src.shared.settings import Settings

client = TestClient(app)


def test_index_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/html")
    assert "app: helloapp" in resp.text
    assert "background-color: gray" in resp.text  # default when BACKGROUND_COLOR is unset


def test_json():
    body = client.get("/json").json()
    assert body["app"] == "helloapp"
    assert body["color"] == "gray"


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("BACKGROUND_COLOR", "blue")
    monkeypatch.setenv("ENVIRONMENT", "dev")
    monkeypatch.setenv("APP_VERSION", "abc1234")
    settings = Settings()
    assert (settings.COLOR, settings.ENVIRONMENT, settings.VERSION) == ("blue", "dev", "abc1234")


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_unknown_path():
    assert client.get("/nope").status_code == 404
