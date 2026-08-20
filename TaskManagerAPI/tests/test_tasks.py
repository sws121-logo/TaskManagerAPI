import pytest
from src.models import Task

def test_create_task(authenticated_client):
    response = authenticated_client.post(
        "/api/tasks/",
        json={"title": "Test Task", "description": "Description", "priority": 2}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False
    assert data["owner_id"] == 1  # from fixture user (id=1)

def test_list_tasks(authenticated_client):
    # Create 3 tasks
    for i in range(3):
        authenticated_client.post("/api/tasks/", json={"title": f"Task {i}"})
    response = authenticated_client.get("/api/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_pagination(authenticated_client):
    for i in range(5):
        authenticated_client.post("/api/tasks/", json={"title": f"Task {i}"})
    response = authenticated_client.get("/api/tasks/?skip=1&limit=2")
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"

def test_update_task(authenticated_client):
    create_resp = authenticated_client.post("/api/tasks/", json={"title": "Old"})
    task_id = create_resp.json()["id"]
    update_resp = authenticated_client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "completed": True}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated"
    assert update_resp.json()["completed"] is True

def test_delete_task(authenticated_client):
    create_resp = authenticated_client.post("/api/tasks/", json={"title": "To delete"})
    task_id = create_resp.json()["id"]
    delete_resp = authenticated_client.delete(f"/api/tasks/{task_id}")
    assert delete_resp.status_code == 204
    # Verify not found
    get_resp = authenticated_client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404

def test_unauthorized_access(client):
    # No token
    response = client.get("/api/tasks/")
    assert response.status_code == 401