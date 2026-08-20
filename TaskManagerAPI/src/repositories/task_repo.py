from src.models import Task
from src.repositories.base_repo import BaseRepository
from sqlalchemy.orm import Session
from typing import List, Optional

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> List[Task]:
        query = self.db.query(Task).filter(Task.owner_id == user_id)
        if completed is not None:
            query = query.filter(Task.completed == (1 if completed else 0))
        return query.offset(skip).limit(limit).all()
