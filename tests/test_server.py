from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_review_type_map():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "response": "ok",
        "status": "success",
    }
