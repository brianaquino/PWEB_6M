#!/usr/bin/env python3
"""
Microservicio de Doctores - Punto de entrada
Puerto: 8002
"""

import uvicorn
import sys
import os

# Agregar la ruta correcta de imports
sys.path.insert(0, os.path.dirname(__file__))

from infrastructure.api.doctor_main import app

if __name__ == "__main__":
    print("=" * 60)
    print("Iniciando Microservicio de Doctores")
    print("=" * 60)
    print("Servidor ejecutándose en: http://0.0.0.0:8002")
    print("Documentación Swagger: http://localhost:8002/docs")
    print("ReDoc: http://localhost:8002/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "infrastructure.api.doctor_main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
