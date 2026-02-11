from typing import List, Optional
import uuid
from datetime import datetime
from domain.user import Paciente, PacienteCreate, PacienteUpdate, PacienteStatus
from application.ports.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    """Adaptador de repositorio en memoria para Paciente"""
    
    def __init__(self):
        self.pacientes = []

    def save(self, paciente_create: PacienteCreate) -> Paciente:
        new_paciente = Paciente(
            id=str(uuid.uuid4()),
            nombre=paciente_create.nombre,
            email=paciente_create.email,
            status=PacienteStatus.ACTIVE,
            created_at=datetime.now()
        )
        self.pacientes.append(new_paciente)
        return new_paciente

    def find_by_email(self, email: str) -> Optional[Paciente]:
        for paciente in self.pacientes:
            if paciente.email == email:
                return paciente
        return None

    def find_by_id(self, paciente_id: str) -> Optional[Paciente]:
        for paciente in self.pacientes:
            if paciente.id == paciente_id:
                return paciente
        return None

    def find_all(self) -> List[Paciente]:
        return self.pacientes

    def update(self, paciente_id: str, paciente_update: PacienteUpdate) -> Optional[Paciente]:
        for i, paciente in enumerate(self.pacientes):
            if paciente.id == paciente_id:
                # Actualizamos solo los campos que vienen (no son None)
                updated_data = paciente.dict()
                update_data = paciente_update.dict(exclude_unset=True)
                updated_data.update(update_data)
                
                # Creamos la nueva instancia actualizada
                self.pacientes[i] = Paciente(**updated_data)
                return self.pacientes[i]
        return None

    def delete(self, paciente_id: str) -> bool:
        initial_count = len(self.pacientes)
        self.pacientes = [p for p in self.pacientes if p.id != paciente_id]
        return len(self.pacientes) < initial_count