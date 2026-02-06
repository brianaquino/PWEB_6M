from typing import List, Optional
from domain.user import User, UserCreate, UserUpdate,UserStatus
from application.ports.user_repository import UserRepository

class UserService:

    #Servicio de aplicacion - Implementa casos de uso#
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserCreate) -> User:
        #Caso de uso: Registrar nuevo usuario#
        if not user_data.username or not user_data.email:
            raise ValueError("Username and email are required")


        existing_user = self.repository.find_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"Email {user_data.email} is already registered")

        return self.repository.save(user_data)
    
    def get_user(self, user_id: str) -> Optional[User]:
        #Caso de uso: Obtener usuario por ID#
        return self.repository.find_by_id(user_id)


    def get_all_users(self) -> List[User]:
        #Caso de uso: Obtener todos los usuarios#
        return self.repository.find_all()

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        #Caso de uso: Actualizar datos de usuario#
        user = self.repository.find_by_id(user_id)
        if not user:
            return None

        if user_update.email != user.email:
            existing_user = self.repository.find_by_email(user_update.email)
            if existing_user:
                raise ValueError(f"Email {user_update.email} is already registered")

        return self.repository.update(user_id, user_update)
    

    def delete_user(self, user_id: str) -> bool:
        #Caso de uso: Eliminar usuario#
        return self.repository.delete(user_id)
    
    def deactivate_user(self, user_id: str) -> Optional[User]:
        #Caso de uso: Desactivar usuario#
        user = self.repository.find_by_id(user_id)
        if not user:
            return None

        user.deactivate()
        return self.repository.update(user_id, UserUpdate(status=UserStatus.INACTIVE))
    
    def activate_user(self, user_id: str) -> Optional[User]:
        
        #Caso de uso: Activar usuario#
        user = self.repository.find_by_id(user_id)
        if not user:
            return None

        user.activate()
        return self.repository.update(user_id, UserUpdate(status=UserStatus.ACTIVE))
    
    def get_user_stats(self) -> dict:
        #Caso de uso: Obtener estadisticas de usuarios#
        users = self.repository.find_all()
        total = len(users)
        active = len([u for u in users if u.is_active()])

        return {
            "total_users": total,
            "active_users": active,
            "inactive_users": total - active
        }