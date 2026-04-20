from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_todos_crud():
    r = client.get("/todos")
    assert r.status_code == 200
    assert r.json() == []

    r = client.post("/todos", json={"title": "Learn FastAPI"})
    assert r.status_code == 201
    todo = r.json()
    assert todo["title"] == "Learn FastAPI"
    assert todo["done"] is False
    tid = todo["id"]

    r = client.patch(f"/todos/{tid}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True

    r = client.delete(f"/todos/{tid}")
    assert r.status_code == 204
