from abc import ABC, abstractmethod
from typing import List, Optional
from domain.doctor import Doctor, DoctorCreate, DoctorUpdate


class DoctorRepository(ABC):
    """Puerto de repositorio para operaciones de Doctor"""
    
    @abstractmethod
    def save(self, doctor: DoctorCreate) -> Doctor:
        """Guardar un nuevo doctor"""
        pass

    @abstractmethod
    def find_by_id(self, doctor_id: str) -> Optional[Doctor]:
        """Buscar doctor por ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Doctor]:
        """Obtener todos los doctores"""
        pass

    @abstractmethod
    def find_by_especialidad(self, especialidad: str) -> List[Doctor]:
        """Buscar doctores por especialidad"""
        pass

    @abstractmethod
    def delete(self, doctor_id: str) -> bool:
        """Eliminar un doctor por ID"""
        pass

    @abstractmethod
    def update(self, doctor_id: str, doctor_update: DoctorUpdate) -> Optional[Doctor]:
        """Actualizar información de un doctor"""
        pass
