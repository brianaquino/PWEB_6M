from typing import List, Optional
from domain.doctor import Doctor, DoctorCreate, DoctorUpdate
from application.ports.doctor_repository import DoctorRepository


class DoctorService:
    """Servicio de aplicación - Implementa casos de uso para Doctor"""
    
    def __init__(self, repository: DoctorRepository):
        self.repository = repository

    def create_doctor(self, doctor_data: DoctorCreate) -> Doctor:
        """Caso de uso: Crear nuevo doctor"""
        if not doctor_data.nombre:
            raise ValueError("Nombre del doctor es requerido")
        
        if not doctor_data.especialidad:
            raise ValueError("Especialidad del doctor es requerida")

        return self.repository.save(doctor_data)
    
    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Caso de uso: Obtener doctor por ID"""
        return self.repository.find_by_id(doctor_id)

    def get_all_doctors(self) -> List[Doctor]:
        """Caso de uso: Obtener todos los doctores"""
        return self.repository.find_all()

    def get_doctors_by_especialidad(self, especialidad: str) -> List[Doctor]:
        """Caso de uso: Obtener doctores por especialidad"""
        return self.repository.find_by_especialidad(especialidad)

    def delete_doctor(self, doctor_id: str) -> bool:
        """Caso de uso: Eliminar doctor"""
        return self.repository.delete(doctor_id)
    
    def update_doctor(self, doctor_id: str, doctor_update: DoctorUpdate) -> Optional[Doctor]:
        """Caso de uso: Actualizar información del doctor"""
        if not self.repository.find_by_id(doctor_id):
            return None
        
        return self.repository.update(doctor_id, doctor_update)
