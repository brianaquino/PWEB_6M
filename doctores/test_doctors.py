"""
Test examples for Doctor microservice
Ejecutar con: pytest test_doctors.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from domain.doctor import Doctor, DoctorCreate, DoctorEspecialidad
from application.services.doctor_services import DoctorService
from infrastructure.adapters.doctor_repository import InMemoryDoctorRepository
from datetime import datetime


def test_create_doctor():
    """Test: Crear un nuevo doctor"""
    print("\n📝 Test: Crear Doctor")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Ejecutar
    doctor_data = DoctorCreate(
        nombre="Dr. Juan García",
        especialidad=DoctorEspecialidad.CARDIOLOGIA
    )
    doctor = service.create_doctor(doctor_data)
    
    # Validar
    assert doctor is not None
    assert doctor.nombre == "Dr. Juan García"
    assert doctor.especialidad == DoctorEspecialidad.CARDIOLOGIA
    assert doctor.id is not None
    assert doctor.created_at is not None
    
    print(f"✅ Doctor creado: {doctor.nombre} - {doctor.especialidad.value}")
    print(f"   ID: {doctor.id}")
    return doctor


def test_get_doctor():
    """Test: Obtener doctor por ID"""
    print("\n📋 Test: Obtener Doctor por ID")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Crear un doctor primero
    doctor_data = DoctorCreate(
        nombre="Dra. María López",
        especialidad=DoctorEspecialidad.NEUROLOGIA
    )
    created_doctor = service.create_doctor(doctor_data)
    
    # Ejecutar
    retrieved_doctor = service.get_doctor(created_doctor.id)
    
    # Validar
    assert retrieved_doctor is not None
    assert retrieved_doctor.id == created_doctor.id
    assert retrieved_doctor.nombre == "Dra. María López"
    
    print(f"✅ Doctor recuperado: {retrieved_doctor.nombre}")


def test_get_all_doctors():
    """Test: Obtener todos los doctores"""
    print("\n📚 Test: Obtener Todos los Doctores")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Crear múltiples doctores
    doctors_data = [
        DoctorCreate(nombre="Dr. Pedro Sánchez", especialidad=DoctorEspecialidad.CARDIOLOGIA),
        DoctorCreate(nombre="Dra. Ana Martínez", especialidad=DoctorEspecialidad.PEDIATRIA),
        DoctorCreate(nombre="Dr. Luis García", especialidad=DoctorEspecialidad.CIRUGIA),
    ]
    
    for doctor_data in doctors_data:
        service.create_doctor(doctor_data)
    
    # Ejecutar
    all_doctors = service.get_all_doctors()
    
    # Validar
    assert len(all_doctors) == 3
    print(f"✅ Total de doctores: {len(all_doctors)}")
    for doctor in all_doctors:
        print(f"   - {doctor.nombre} ({doctor.especialidad.value})")


def test_search_by_especialidad():
    """Test: Buscar doctores por especialidad"""
    print("\n🔍 Test: Buscar por Especialidad")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Crear doctores con diferentes especialidades
    doctors_data = [
        DoctorCreate(nombre="Dr. Carlos Torres", especialidad=DoctorEspecialidad.CARDIOLOGIA),
        DoctorCreate(nombre="Dra. Elena Ruiz", especialidad=DoctorEspecialidad.CARDIOLOGIA),
        DoctorCreate(nombre="Dr. Javier Díaz", especialidad=DoctorEspecialidad.NEUROLOGIA),
    ]
    
    for doctor_data in doctors_data:
        service.create_doctor(doctor_data)
    
    # Ejecutar
    cardiologists = service.get_doctors_by_especialidad("cardiología")
    
    # Validar
    assert len(cardiologists) == 2
    assert all(d.especialidad == DoctorEspecialidad.CARDIOLOGIA for d in cardiologists)
    
    print(f"✅ Cardiólogos encontrados: {len(cardiologists)}")
    for doctor in cardiologists:
        print(f"   - {doctor.nombre}")


def test_update_doctor():
    """Test: Actualizar información del doctor"""
    print("\n✏️ Test: Actualizar Doctor")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Crear doctor
    doctor_data = DoctorCreate(
        nombre="Dr. Roberto Flores",
        especialidad=DoctorEspecialidad.DERMATOLOGIA
    )
    doctor = service.create_doctor(doctor_data)
    original_id = doctor.id
    
    # Ejecutar actualización
    from domain.doctor import DoctorUpdate
    update_data = DoctorUpdate(especialidad=DoctorEspecialidad.OFTALMOLOGIA)
    updated_doctor = service.update_doctor(original_id, update_data)
    
    # Validar
    assert updated_doctor is not None
    assert updated_doctor.id == original_id
    assert updated_doctor.especialidad == DoctorEspecialidad.OFTALMOLOGIA
    assert updated_doctor.nombre == "Dr. Roberto Flores"
    
    print(f"✅ Doctor actualizado: {updated_doctor.nombre}")
    print(f"   Nueva especialidad: {updated_doctor.especialidad.value}")


def test_delete_doctor():
    """Test: Eliminar doctor"""
    print("\n🗑️ Test: Eliminar Doctor")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Crear doctor
    doctor_data = DoctorCreate(
        nombre="Dr. Gonzalo Méndez",
        especialidad=DoctorEspecialidad.ONCOLOGIA
    )
    doctor = service.create_doctor(doctor_data)
    doctor_id = doctor.id
    
    # Verificar que existe
    assert service.get_doctor(doctor_id) is not None
    
    # Ejecutar eliminación
    deleted = service.delete_doctor(doctor_id)
    
    # Validar
    assert deleted is True
    assert service.get_doctor(doctor_id) is None
    
    print(f"✅ Doctor eliminado: {doctor.nombre}")


def test_validation_errors():
    """Test: Validaciones de error"""
    print("\n⚠️ Test: Validaciones")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    # Test 1: Nombre vacío
    try:
        doctor_data = DoctorCreate(nombre="", especialidad=DoctorEspecialidad.PSICOLOGIA)
        service.create_doctor(doctor_data)
        print("❌ Debería haber levantado un error para nombre vacío")
    except ValueError as e:
        print(f"✅ Validación correcta: {str(e)}")
    
    # Test 2: Actualizar doctor inexistente
    updated = service.update_doctor("doctor-inexistente-id", {})
    assert updated is None
    print(f"✅ Actualización correcta para doctor inexistente: retorna None")
    
    # Test 3: Eliminar doctor inexistente
    deleted = service.delete_doctor("doctor-inexistente-id")
    assert deleted is False
    print(f"✅ Eliminación correcta para doctor inexistente: retorna False")


def test_complete_workflow():
    """Test: Workflow completo"""
    print("\n🔄 Test: Workflow Completo")
    
    # Configurar
    repository = InMemoryDoctorRepository()
    service = DoctorService(repository)
    
    print("\n1️⃣ Creando 3 doctores...")
    doctors = []
    for nombre, especialidad in [
        ("Dr. Rafael García", DoctorEspecialidad.CARDIOLOGIA),
        ("Dra. Sofía López", DoctorEspecialidad.NEUROLOGIA),
        ("Dr. Marcos Ruiz", DoctorEspecialidad.CIRUGIA),
    ]:
        doctor_data = DoctorCreate(nombre=nombre, especialidad=especialidad)
        doctor = service.create_doctor(doctor_data)
        doctors.append(doctor)
        print(f"   ✓ {nombre}")
    
    print("\n2️⃣ Consultando todos los doctores...")
    all_doctors = service.get_all_doctors()
    print(f"   ✓ Total registrado: {len(all_doctors)} doctores")
    
    print("\n3️⃣ Buscando por especialidad...")
    cardio_doctors = service.get_doctors_by_especialidad("cardiología")
    print(f"   ✓ Cardiólogos encontrados: {len(cardio_doctors)}")
    
    print("\n4️⃣ Obteniendo doctor específico...")
    doctor = service.get_doctor(doctors[0].id)
    print(f"   ✓ {doctor.nombre}")
    
    print("\n5️⃣ Eliminando un doctor...")
    service.delete_doctor(doctors[1].id)
    remaining = service.get_all_doctors()
    print(f"   ✓ Doctores restantes: {len(remaining)}")
    
    print("\n✅ Workflow completado exitosamente!")


if __name__ == "__main__":
    print("=" * 60)
    print("👨‍⚕️ TESTS DEL MICROSERVICIO DE DOCTORES")
    print("=" * 60)
    
    try:
        test_create_doctor()
        test_get_doctor()
        test_get_all_doctors()
        test_search_by_especialidad()
        test_update_doctor()
        test_delete_doctor()
        test_validation_errors()
        test_complete_workflow()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Error en test: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)
