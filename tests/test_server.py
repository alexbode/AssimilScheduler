from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_review_type_map():
    response = client.get("/api/v1/review_type_map")
    assert response.status_code == 200
    assert response.json() == {
        "response": {
            "1": "LISTEN",
            "2": "SHADOW",
            "3": "SHADOW_BLIND",
            "4": "READ",
            "5": "SCRIPTORIUM",
            "6": "TRANSLATE",
            "7": "REVERSE_TRANSLATE",
            "8": "TRANSCRIBE",
            "9": "GRAMMAR_POINTS",
        },
        "status": "success",
    }
