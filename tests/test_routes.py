import json


def post_task(client, title="Buy milk", description=""):
    return client.post(
        "/api/tasks",
        data=json.dumps({"title": title, "description": description}),
        content_type="application/json",
    )


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_create_task(client):
    r = post_task(client, "Write Dockerfile")
    assert r.status_code == 201
    data = r.get_json()
    assert data["title"] == "Write Dockerfile"
    assert data["done"] is False
    assert "id" in data

def test_create_task_missing_title(client):
    r = client.post("/api/tasks", json={})
    assert r.status_code == 400

def test_list_tasks_empty(client):
    r = client.get("/api/tasks")
    assert r.status_code == 200
    assert r.get_json() == []

def test_list_tasks(client):
    post_task(client, "Task A")
    post_task(client, "Task B")
    r = client.get("/api/tasks")
    assert len(r.get_json()) == 2

def test_get_task(client):
    task_id = post_task(client, "Specific task").get_json()["id"]
    r = client.get(f"/api/tasks/{task_id}")
    assert r.status_code == 200

def test_get_task_not_found(client):
    r = client.get("/api/tasks/does-not-exist")
    assert r.status_code == 404

def test_update_task_done(client):
    task_id = post_task(client, "Deploy to K8s").get_json()["id"]
    r = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert r.status_code == 200
    assert r.get_json()["done"] is True

def test_update_task_title(client):
    task_id = post_task(client, "Old title").get_json()["id"]
    r = client.patch(f"/api/tasks/{task_id}", json={"title": "New title"})
    assert r.get_json()["title"] == "New title"

def test_update_task_not_found(client):
    r = client.patch("/api/tasks/nope", json={"done": True})
    assert r.status_code == 404

def test_delete_task(client):
    task_id = post_task(client, "To be deleted").get_json()["id"]
    r = client.delete(f"/api/tasks/{task_id}")
    assert r.status_code == 200
    assert client.get(f"/api/tasks/{task_id}").status_code == 404

def test_delete_task_not_found(client):
    r = client.delete("/api/tasks/ghost")
    assert r.status_code == 404
