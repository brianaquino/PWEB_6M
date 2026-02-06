from typing import List, Optional
import uuid
from datetime import datetime
from domain.user import User, UserCreate, UserUpdate, UserStatus
from application.ports.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = []

    def save(self, user_create: UserCreate) -> User:
        new_user = User(
            id=str(uuid.uuid4()),
            username=user_create.username,
            email=user_create.email,
            status=UserStatus.ACTIVE,
            created_at=datetime.now()
        )
        self.users.append(new_user)
        return new_user

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def find_by_id(self, user_id: str) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def find_all(self) -> List[User]:
        return self.users

    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        for i, user in enumerate(self.users):
            if user.id == user_id:
                # Actualizamos solo los campos que vienen (no son None)
                updated_data = user.dict()
                update_data = user_update.dict(exclude_unset=True)
                updated_data.update(update_data)
                
                # Creamos la nueva instancia actualizada
                self.users[i] = User(**updated_data)
                return self.users[i]
        return None

    def delete(self, user_id: str) -> bool:
        initial_count = len(self.users)
        self.users = [u for u in self.users if u.id != user_id]
        return len(self.users) < initial_count