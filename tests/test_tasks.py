import pytest

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_task(client):
    response = await client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] is None
    assert data["status"] == "todo"
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_create_task_with_description(client):
    response = await client.post(
        "/tasks",
        json={"title": "With desc", "description": "Some test."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Some test."

@pytest.mark.asyncio
async def test_create_task_with_status(client):
    response = await client.post(
        "/tasks",
        json={"title": "In progress", "status": "in_progress"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_create_task_with_empty_title(client):
    response = await client.post("/tasks", json={"title": ""})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_task_with_invalid_status(client):
    response = await client.post("/tasks", json={"title": "Some title", "status": "invalid"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_tasks_empty(client):
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_tasks(client):
    await client.post("/tasks", json={"title": "First"})
    await client.post("/tasks", json={"title": "Second"})
    response = await client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "First"
    assert tasks[1]["title"] == "Second"

@pytest.mark.asyncio
async def test_get_task(client):
    create = await client.post("/tasks", json={"title": "To get"})
    task_id = create.json()["id"]

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "To get"

@pytest.mark.asyncio
async def test_get_task_not_found(client):
    response = await client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_update_task(client):
    create = await client.post("/tasks", json={"title": "Old"})
    task_id = create.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "New", "description": "Updated", "status": "done"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["description"] == "Updated"
    assert data["status"] == "done"

@pytest.mark.asyncio
async def test_update_task_not_found(client):
    response = await client.put(
        "/tasks/999",
        json={"title": "New", "description": None, "status": "done"}
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_task(client):
    create = await client.post("/tasks", json={"title": "To delete"})
    task_id = create.json()["id"]

    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_task_not_found(client):
    response = await client.delete("/tasks/9999")
    assert response.status_code == 404