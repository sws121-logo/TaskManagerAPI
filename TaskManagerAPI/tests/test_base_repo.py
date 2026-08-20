import pytest
from src.repositories.base_repo import BaseRepository
from src.models import User
from sqlalchemy.orm import Session

def test_base_repo_create(db_session):
    repo = BaseRepository(User, db_session)
    user = repo.create(email="base@example.com", hashed_password="hash")
    assert user.id is not None
    assert user.email == "base@example.com"

def test_base_repo_update(db_session):
    repo = BaseRepository(User, db_session)
    user = repo.create(email="old@example.com", hashed_password="hash")
    updated = repo.update(user, email="new@example.com")
    assert updated.email == "new@example.com"

def test_base_repo_delete(db_session):
    repo = BaseRepository(User, db_session)
    user = repo.create(email="delete@example.com", hashed_password="hash")
    repo.delete(user)
    assert repo.get_by_id(user.id) is None

def test_base_repo_get_all(db_session):
    repo = BaseRepository(User, db_session)
    repo.create(email="a@example.com", hashed_password="hash")
    repo.create(email="b@example.com", hashed_password="hash")
    all_users = repo.get_all()
    assert len(all_users) >= 2