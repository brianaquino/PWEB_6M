from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserStatus(str,Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(BaseModel):
    id: str
    username: str
    email: str
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime

    def deactivate(self):
        self.status = UserStatus.INACTIVE

    def activate(self):
        self.status = UserStatus.ACTIVE

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    status: Optional[UserStatus] = None

class UserCreate(BaseModel):
    username: str
    email: str

