from abc import ABC, abstractmethod
from typing import List, Optional
from domain.user import Paciente, PacienteCreate, PacienteUpdate

class UserRepository(ABC):
    """Puerto de repositorio para operaciones de Paciente"""
    
    @abstractmethod
    def save(self, paciente: PacienteCreate) -> Paciente:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Paciente]:
        pass

    @abstractmethod
    def find_by_id(self, paciente_id: str) -> Optional[Paciente]:
        pass

    @abstractmethod
    def find_all(self) -> List[Paciente]:
        pass

    @abstractmethod
    def delete(self, paciente_id: str) -> bool:
        pass

    @abstractmethod
    def update(self, paciente_id: str, paciente_update: PacienteUpdate) -> Optional[Paciente]:
        pass
