from fastapi import FastAPI, HTTPException, status
import uvicorn
from typing import List

# Importaciones de tus capas
from domain.user import User, UserCreate, UserUpdate
from application.services.user_services import UserService
from infrastructure.adapters.user_repository import InMemoryUserRepository

app = FastAPI(
    title="Microservicio de Usuarios",
    description="API CRUD para gestión de usuarios con arquitectura hexagonal",
    version="1.0.0"
)

# --- INYECCIÓN DE DEPENDENCIAS ---
# Instanciamos el adaptador (Repositorio)
user_repository = InMemoryUserRepository()
# Inyectamos el repositorio al servicio
user_service = UserService(user_repository)

# --- ENDPOINTS ---

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def create_user(user: UserCreate):
    try:
        return user_service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=User, tags=["Usuarios"])
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.get("/users", response_model=List[User], tags=["Usuarios"])
def get_all_users():
    return user_service.get_all_users()

@app.put("/users/{user_id}", response_model=User, tags=["Usuarios"])
def update_user(user_id: str, user_update: UserUpdate):
    try:
        updated_user = user_service.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def delete_user(user_id: str):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None

# Endpoints adicionales (Lógica de negocio extra)
@app.post("/users/{user_id}/activate", response_model=User, tags=["Operaciones"])
def activate_user(user_id: str):
    user = user_service.activate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.post("/users/{user_id}/deactivate", response_model=User, tags=["Operaciones"])
def deactivate_user(user_id: str):
    user = user_service.deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.get("/stats", tags=["Estadísticas"])
def get_stats():
    return user_service.get_user_stats()

if __name__ == "__main__":
    # Se configura el puerto 8001 como pide el requisito
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)