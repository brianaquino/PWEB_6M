from typing import List, Optional
import uuid
from datetime import datetime
from domain.doctor import Doctor, DoctorCreate, DoctorUpdate
from application.ports.doctor_repository import DoctorRepository


class InMemoryDoctorRepository(DoctorRepository):
    """Adaptador de repositorio en memoria para Doctor"""
    
    def __init__(self):
        self.doctores = []

    def save(self, doctor_create: DoctorCreate) -> Doctor:
        """Guardar un nuevo doctor en memoria"""
        new_doctor = Doctor(
            id=str(uuid.uuid4()),
            nombre=doctor_create.nombre,
            especialidad=doctor_create.especialidad,
            created_at=datetime.now()
        )
        self.doctores.append(new_doctor)
        return new_doctor

    def find_by_id(self, doctor_id: str) -> Optional[Doctor]:
        """Buscar doctor por ID"""
        for doctor in self.doctores:
            if doctor.id == doctor_id:
                return doctor
        return None

    def find_all(self) -> List[Doctor]:
        """Obtener todos los doctores"""
        return self.doctores

    def find_by_especialidad(self, especialidad: str) -> List[Doctor]:
        """Buscar doctores por especialidad"""
        return [doctor for doctor in self.doctores if doctor.especialidad.value.lower() == especialidad.lower()]

    def delete(self, doctor_id: str) -> bool:
        """Eliminar un doctor por ID"""
        for i, doctor in enumerate(self.doctores):
            if doctor.id == doctor_id:
                self.doctores.pop(i)
                return True
        return False

    def update(self, doctor_id: str, doctor_update: DoctorUpdate) -> Optional[Doctor]:
        """Actualizar información de un doctor"""
        for i, doctor in enumerate(self.doctores):
            if doctor.id == doctor_id:
                # Actualizamos solo los campos que vienen (no son None)
                updated_data = doctor.dict()
                update_data = doctor_update.dict(exclude_unset=True)
                updated_data.update(update_data)
                
                # Creamos la nueva instancia actualizada
                self.doctores[i] = Doctor(**updated_data)
                return self.doctores[i]
        return None
