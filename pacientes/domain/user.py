from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class PacienteStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Paciente(BaseModel):
    """Modelo de dominio para Paciente"""
    id: str
    nombre: str
    email: str
    status: PacienteStatus = PacienteStatus.ACTIVE
    created_at: datetime

    def deactivate(self):
        self.status = PacienteStatus.INACTIVE

    def activate(self):
        self.status = PacienteStatus.ACTIVE

    def is_active(self) -> bool:
        return self.status == PacienteStatus.ACTIVE

class PacienteUpdate(BaseModel):
    """Modelo para actualizar Paciente"""
    nombre: Optional[str] = None
    email: Optional[str] = None
    status: Optional[PacienteStatus] = None

class PacienteCreate(BaseModel):
    """Modelo para crear Paciente"""
    nombre: str
    email: str


# Mantener alias para compatibilidad
User = Paciente
UserCreate = PacienteCreate
UserUpdate = PacienteUpdate
UserStatus = PacienteStatus

