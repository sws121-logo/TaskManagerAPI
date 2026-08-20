from sqlalchemy.orm import Session
from src.repositories.user_repo import UserRepository
from src.security import verify_password, create_access_token
from src.schemas import UserCreate
from src.models import User

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user(self, user_data: UserCreate) -> User:
        # Check if email already exists
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        return self.user_repo.create(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name
        )