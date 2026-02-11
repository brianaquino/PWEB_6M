from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.utils import get_openapi
from typing import List
import sys
import os

# Agregar la ruta correcta de imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain.doctor import Doctor, DoctorCreate, DoctorEspecialidad
from application.services.doctor_services import DoctorService
from infrastructure.adapters.doctor_repository import InMemoryDoctorRepository

# --- CONFIGURACIÓN DE FASTAPI CON SWAGGER ---
app = FastAPI(
    title="Microservicio de Doctores",
    description="API para gestión de Doctores. Permite crear, consultar y eliminar registros de médicos especializados con arquitectura hexagonal. Solo soporta operaciones GET, POST y DELETE.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "info@doctores.local"
    },
    license_info={
        "name": "MIT",
    },
)

# --- INYECCIÓN DE DEPENDENCIAS ---
# Instanciamos el adaptador (Repositorio)
doctor_repository = InMemoryDoctorRepository()
# Inyectamos el repositorio al servicio
doctor_service = DoctorService(doctor_repository)

# --- ENDPOINTS ---

@app.post(
    "/doctores",
    response_model=Doctor,
    status_code=status.HTTP_201_CREATED,
    tags=["Doctores"],
    summary="Registrar nuevo doctor",
    description="Crea un nuevo registro de doctor en el sistema.",
    responses={
        201: {"description": "Doctor creado exitosamente"},
        400: {"description": "Error de validación - Datos incompletos o inválidos"}
    }
)
def create_doctor(doctor_data: DoctorCreate):
    """
    Registra un nuevo doctor en el sistema.
    
    **Parámetros:**
    - **nombre**: Nombre completo del doctor (requerido)
    - **especialidad**: Especialidad médica del doctor (requerida)
    
    **Especialidades disponibles:**
    - cardiología
    - neurología
    - pediatría
    - cirugía
    - dermatología
    - oftalmología
    - oncología
    - psicología
    """
    try:
        new_doctor = doctor_service.create_doctor(doctor_data)
        return new_doctor
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get(
    "/doctores",
    response_model=List[Doctor],
    status_code=status.HTTP_200_OK,
    tags=["Doctores"],
    summary="Obtener todos los doctores",
    description="Retorna la lista completa de doctores registrados en el sistema.",
)
def list_all_doctors():
    """
    Obtiene la lista completa de todos los doctores registrados.
    
    **Respuesta:** Lista de doctores con sus datos: id, nombre, especialidad y fecha de creación.
    """
    return doctor_service.get_all_doctors()


@app.get(
    "/doctores/{doctor_id}",
    response_model=Doctor,
    status_code=status.HTTP_200_OK,
    tags=["Doctores"],
    summary="Obtener doctor por ID",
    description="Retorna los datos de un doctor específico identificado por su ID.",
    responses={
        200: {"description": "Doctor encontrado"},
        404: {"description": "Doctor no encontrado"}
    }
)
def get_doctor_by_id(doctor_id: str):
    """
    Obtiene los datos de un doctor específico por su ID.
    
    **Parámetros:**
    - **doctor_id**: ID único del doctor (UUID)
    
    **Respuesta:** Datos completos del doctor si existe.
    """
    doctor = doctor_service.get_doctor(doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor con ID {doctor_id} no encontrado"
        )
    return doctor


@app.get(
    "/doctores/especialidad/{especialidad}",
    response_model=List[Doctor],
    status_code=status.HTTP_200_OK,
    tags=["Doctores"],
    summary="Buscar doctores por especialidad",
    description="Retorna la lista de doctores que tienen una especialidad específica.",
)
def get_doctors_by_especialidad(especialidad: str):
    """
    Busca todos los doctores que tienen una especialidad específica.
    
    **Parámetros:**
    - **especialidad**: Nombre de la especialidad a buscar (ej: cardiología, neurología)
    
    **Respuesta:** Lista de doctores con la especialidad especificada.
    """
    doctors = doctor_service.get_doctors_by_especialidad(especialidad)
    return doctors


@app.delete(
    "/doctores/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Doctores"],
    summary="Eliminar doctor",
    description="Elimina un doctor específico del sistema por su ID.",
    responses={
        204: {"description": "Doctor eliminado exitosamente"},
        404: {"description": "Doctor no encontrado"}
    }
)
def delete_doctor(doctor_id: str):
    """
    Elimina un doctor del sistema.
    
    **Parámetros:**
    - **doctor_id**: ID único del doctor a eliminar
    
    **Respuesta:** Sin contenido (204) si se elimina exitosamente.
    """
    deleted = doctor_service.delete_doctor(doctor_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor con ID {doctor_id} no encontrado"
        )
    return None


# --- INFORMACIÓN DE LA API ---
@app.get(
    "/info",
    tags=["Info"],
    summary="Información de la API",
)
def api_info():
    """Retorna información sobre la API de Doctores"""
    return {
        "nombre": "Microservicio de Doctores",
        "versión": "1.0.0",
        "descripción": "API CRUD para gestión de doctores",
        "métodos_disponibles": ["GET", "POST", "DELETE"],
        "especialidades": [e.value for e in DoctorEspecialidad],
    }


# --- HEALTH CHECK ---
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
def health_check():
    """Verifica que el servicio está disponible"""
    return {"status": "ok", "service": "doctores"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
