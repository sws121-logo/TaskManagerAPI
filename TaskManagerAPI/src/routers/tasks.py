from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from src.dependencies import get_db, get_current_active_user
from src.schemas import TaskCreate, TaskUpdate, TaskOut
from src.services.task_service import TaskService
from src.models import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    task = service.create_task(task_data, current_user)
    logger.info(f"Task created by user {current_user.id}: {task.title}")
    return task

@router.get("/", response_model=List[TaskOut])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    tasks = service.get_user_tasks(current_user.id, skip, limit, completed)
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    task = service.get_task_for_user(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    task = service.update_task(task_id, task_data, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task_id} updated by user {current_user.id}")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    deleted = service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task_id} deleted by user {current_user.id}")
    return
