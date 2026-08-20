import pytest
from src.services.task_service import TaskService
from src.schemas import TaskCreate, TaskUpdate
from src.models import User

def test_update_task_not_found(db_session, test_user):
    service = TaskService(db_session)
    result = service.update_task(999, TaskUpdate(title="New"), test_user.id)
    assert result is None

def test_delete_task_not_found(db_session, test_user):
    service = TaskService(db_session)
    assert service.delete_task(999, test_user.id) is False

def test_update_task_ownership_mismatch(db_session, test_user):
    # Create a task for another user (simulate)
    other_user = User(email="other@example.com", hashed_password="hash")
    db_session.add(other_user)
    db_session.commit()
    task = TaskService(db_session).create_task(TaskCreate(title="Owner task"), other_user)
    service = TaskService(db_session)
    result = service.update_task(task.id, TaskUpdate(title="Hijack"), test_user.id)
    assert result is None