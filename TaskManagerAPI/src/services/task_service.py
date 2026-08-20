from sqlalchemy.orm import Session
from src.repositories.task_repo import TaskRepository
from src.models import Task, User
from src.schemas import TaskCreate, TaskUpdate
from typing import List, Optional

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, task_data: TaskCreate, owner: User) -> Task:
        return self.repo.create(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            owner_id=owner.id
        )

    def get_user_tasks(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> List[Task]:
        return self.repo.get_by_user(user_id, skip, limit, completed)

    def get_task_for_user(self, task_id: int, user_id: int) -> Optional[Task]:
        task = self.repo.get_by_id(task_id)
        if not task or task.owner_id != user_id:
            return None
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int) -> Optional[Task]:
        task = self.get_task_for_user(task_id, user_id)
        if not task:
            return None
        update_data = task_data.dict(exclude_unset=True)
        if "completed" in update_data:
            update_data["completed"] = 1 if update_data["completed"] else 0
        return self.repo.update(task, **update_data)

    def delete_task(self, task_id: int, user_id: int) -> bool:
        task = self.get_task_for_user(task_id, user_id)
        if not task:
            return False
        self.repo.delete(task)
        return True
