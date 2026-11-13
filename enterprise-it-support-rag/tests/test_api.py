
from fastapi.testclient import TestClient

from backend.main import app
from backend.dependencies import require_api_key

# Bypass authentication for these isolated endpoint tests.
app.dependency_overrides[require_api_key] = lambda: True

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_retrieve_validation():
    response = client.post(
        "/retrieve",
        json={"question": "Hi"}
    )

    assert response.status_code == 422


def test_chat_validation():
    response = client.post(
        "/chat",
        json={"question": "Hi"}
    )

    assert response.status_code == 422


def test_feedback_validation():
    response = client.post(
        "/feedback",
        json={
            "question": "How do I reset my password?",
            "answer": "Use the approved password reset portal.",
            "rating": "invalid"
        }
    )

    assert response.status_code == 422

def test_retrieve_success(monkeypatch):
    from backend.api import routes

    class FakePipeline:
        def retrieve(self, question, top_k):
            return [
                {
                    "text": "Open the company sign-in page and select Forgot password.",
                    "title": "Password Reset Guide",
                    "metadata": {
                        "filename": "password_reset.txt"
                    }
                }
            ]

    monkeypatch.setattr(
        routes,
        "pipeline",
        lambda: FakePipeline()
    )

    response = client.post(
        "/retrieve",
        json={
            "question": "How can I reset my forgotten password?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "How can I reset my forgotten password?"
    assert len(data["results"]) == 1
    assert "Forgot password" in data["results"][0]["text"]


def test_chat_success(monkeypatch):
    from backend.api import routes

    class FakePipeline:
        def retrieve(self, question, top_k):
            return [
                {
                    "text": "Select Forgot password on the company sign-in page.",
                    "title": "Password Reset Guide",
                    "metadata": {
                        "filename": "password_reset.txt"
                    }
                }
            ]

    def fake_generate_answer(question, hits, history=None):
        return {
            "answer": "Select Forgot password on the company sign-in page.",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 30,
                "total_tokens": 130
            },
            "model": "gpt-5-mini",
            "provider": "foundry"
        }

    monkeypatch.setattr(routes, "pipeline", lambda: FakePipeline())
    monkeypatch.setattr(routes, "generate_answer", fake_generate_answer)

    response = client.post(
        "/chat",
        json={
            "question": "How can I reset my forgotten password?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "Forgot password" in data["answer"]
    assert len(data["sources"]) == 1
    assert data["sources"][0]["filename"] == "Password Reset Guide"

def test_missing_api_key_rejected():
    from backend.api import routes

    # Restore the real authentication dependency.
    app.dependency_overrides.pop(require_api_key, None)

    response = client.post(
        "/retrieve",
        json={
            "question": "How can I reset my password?"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"

    # Restore the test override for other tests.
    app.dependency_overrides[require_api_key] = lambda: True

