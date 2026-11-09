from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_services_lists_required_documents():
    body = client.get("/services").json()
    assert body["ownership_transfer"] == ["registration", "id_card", "driving_licence"]
    assert "unknown" not in body
