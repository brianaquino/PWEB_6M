from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.utils import get_openapi
from typing import List
import sys
import os

# Agregar la ruta correcta de imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain.user import Paciente, PacienteCreate, PacienteUpdate
from application.services.user_services import UserService
from infrastructure.adapters.user_repository import InMemoryUserRepository

# --- CONFIGURACIÓN DE FASTAPI CON SWAGGER ---
app = FastAPI(
    title="Microservicio de Pacientes",
    description="API CRUD para registro y gestión de pacientes con arquitectura hexagonal. Permite crear, leer, actualizar y eliminar registros de pacientes.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "info@pacientes.local"
    },
    license_info={
        "name": "MIT",
    },
)

# --- INYECCIÓN DE DEPENDENCIAS ---
# Instanciamos el adaptador (Repositorio)
paciente_repository = InMemoryUserRepository()
# Inyectamos el repositorio al servicio
paciente_service = UserService(paciente_repository)

# --- ENDPOINTS ---

@app.post(
    "/pacientes",
    response_model=Paciente,
    status_code=status.HTTP_201_CREATED,
    tags=["Pacientes"],
    summary="Registrar nuevo paciente",
    description="Crea un nuevo registro de paciente en el sistema. El email debe ser único.",
    responses={
        201: {"description": "Paciente creado exitosamente"},
        400: {"description": "Error de validación - Email duplicado o campos requeridos faltantes"}
    }
)
def registrar_paciente(paciente: PacienteCreate):
    """
    Registra un nuevo paciente en el sistema.
    
    - **nombre**: Nombre completo del paciente (requerido)
    - **email**: Correo electrónico del paciente, debe ser único (requerido)
    
    Retorna el paciente creado con su ID asignado automáticamente.
    """
    try:
        return paciente_service.register_user(paciente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/pacientes/{paciente_id}",
    response_model=Paciente,
    tags=["Pacientes"],
    summary="Obtener paciente por ID",
    description="Recupera la información de un paciente específico usando su ID.",
    responses={
        200: {"description": "Paciente encontrado"},
        404: {"description": "Paciente no encontrado"}
    }
)
def obtener_paciente(paciente_id: str):
    """
    Obtiene los detalles de un paciente específico.
    
    - **paciente_id**: ID único del paciente (requerido)
    """
    paciente = paciente_service.get_user(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@app.get(
    "/pacientes",
    response_model=List[Paciente],
    tags=["Pacientes"],
    summary="Listar todos los pacientes",
    description="Recupera la lista completa de todos los pacientes registrados en el sistema.",
    responses={
        200: {"description": "Lista de pacientes"}
    }
)
def listar_pacientes():
    """
    Obtiene la lista de todos los pacientes registrados.
    """
    return paciente_service.get_all_users()


@app.delete(
    "/pacientes/{paciente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Pacientes"],
    summary="Eliminar paciente",
    description="Elimina permanentemente un paciente del sistema.",
    responses={
        204: {"description": "Paciente eliminado exitosamente"},
        404: {"description": "Paciente no encontrado"}
    }
)
def eliminar_paciente(paciente_id: str):
    """
    Elimina un paciente del sistema.
    
    - **paciente_id**: ID único del paciente a eliminar (requerido)
    """
    deleted = paciente_service.delete_user(paciente_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return None


@app.get(
    "/pacientes/estadisticas/resumen",
    tags=["Estadísticas"],
    summary="Obtener estadísticas de pacientes",
    description="Retorna un resumen de estadísticas de los pacientes registrados.",
    responses={
        200: {"description": "Estadísticas obtenidas"}
    }
)
def obtener_estadisticas():
    """
    Obtiene estadísticas sobre los pacientes registrados.
    
    Retorna:
    - total_pacientes: Número total de pacientes
    - active_pacientes: Número de pacientes activos
    - inactive_pacientes: Número de pacientes inactivos
    """
    return paciente_service.get_user_stats()


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Verifica que el servicio esté funcionando correctamente."
)
def health_check():
    """
    Endpoint de salud para verificar que el servicio está activo.
    """
    return {
        "status": "healthy",
        "service": "Microservicio de Pacientes",
        "version": "1.0.0"
    }


# Personalizar el esquema OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Microservicio de Pacientes",
        version="1.0.0",
        description="API REST para la gestión de pacientes con Swagger UI integrada",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
