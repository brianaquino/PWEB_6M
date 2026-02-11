#!/usr/bin/env python3
"""
Microservicio de Pacientes - Punto de entrada
Puerto: 8001
"""

import uvicorn
import sys
import os

# Agregar la ruta correcta de imports
sys.path.insert(0, os.path.dirname(__file__))

from infrastructure.api.main import app

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 Iniciando Microservicio de Pacientes")
    print("=" * 60)
    print("📍 Servidor ejecutándose en: http://0.0.0.0:8001")
    print("📚 Documentación Swagger: http://localhost:8001/docs")
    print("📖 ReDoc: http://localhost:8001/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "infrastructure.api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )

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