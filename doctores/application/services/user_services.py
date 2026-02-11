from typing import List, Optional
from domain.user import Paciente, PacienteCreate, PacienteUpdate, PacienteStatus
from application.ports.user_repository import UserRepository

class UserService:
    """Servicio de aplicación - Implementa casos de uso para Paciente"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, paciente_data: PacienteCreate) -> Paciente:
        """Caso de uso: Registrar nuevo paciente"""
        if not paciente_data.nombre or not paciente_data.email:
            raise ValueError("Nombre y email son requeridos")

        existing_paciente = self.repository.find_by_email(paciente_data.email)
        if existing_paciente:
            raise ValueError(f"Email {paciente_data.email} ya está registrado")

        return self.repository.save(paciente_data)
    
    def get_user(self, paciente_id: str) -> Optional[Paciente]:
        """Caso de uso: Obtener paciente por ID"""
        return self.repository.find_by_id(paciente_id)

    def get_all_users(self) -> List[Paciente]:
        """Caso de uso: Obtener todos los pacientes"""
        return self.repository.find_all()

    def delete_user(self, paciente_id: str) -> bool:
        """Caso de uso: Eliminar paciente"""
        return self.repository.delete(paciente_id)
    
    def deactivate_user(self, paciente_id: str) -> Optional[Paciente]:
        """Caso de uso: Desactivar paciente"""
        paciente = self.repository.find_by_id(paciente_id)
        if not paciente:
            return None

        paciente.deactivate()
        return self.repository.update(paciente_id, PacienteUpdate(status=PacienteStatus.INACTIVE))
    
    def activate_user(self, paciente_id: str) -> Optional[Paciente]:
        """Caso de uso: Activar paciente"""
        paciente = self.repository.find_by_id(paciente_id)
        if not paciente:
            return None

        paciente.activate()
        return self.repository.update(paciente_id, PacienteUpdate(status=PacienteStatus.ACTIVE))
    
    def update_user(self, paciente_id: str, paciente_update: PacienteUpdate) -> Optional[Paciente]:
        """Caso de uso: Actualizar paciente"""
        return self.repository.update(paciente_id, paciente_update)
    
    def get_user_stats(self) -> dict:
        """Caso de uso: Obtener estadísticas de pacientes"""
        pacientes = self.repository.find_all()
        total = len(pacientes)
        active = len([p for p in pacientes if p.is_active()])

        return {
            "total_pacientes": total,
            "active_pacientes": active,
            "inactive_pacientes": total - active
        }