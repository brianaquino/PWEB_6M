from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class DoctorEspecialidad(str, Enum):
    CARDIOLOGIA = "cardiología"
    NEUROLOGIA = "neurología"
    PEDIATRIA = "pediatría"
    CIRUGIA = "cirugía"
    DERMATOLOGIA = "dermatología"
    OFTALMOLOGIA = "oftalmología"
    ONCOLOGIA = "oncología"
    PSICOLOGIA = "psicología"


class Doctor(BaseModel):
    """Modelo de dominio para Doctor"""
    id: str
    nombre: str
    especialidad: DoctorEspecialidad
    created_at: datetime

    def __str__(self) -> str:
        return f"Dr(a). {self.nombre} - {self.especialidad.value}"


class DoctorCreate(BaseModel):
    """Modelo para crear Doctor"""
    nombre: str
    especialidad: DoctorEspecialidad


class DoctorUpdate(BaseModel):
    """Modelo para actualizar Doctor"""
    nombre: Optional[str] = None
    especialidad: Optional[DoctorEspecialidad] = None
