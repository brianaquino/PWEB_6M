"""Capa de Infraestructura - Adaptadores e implementaciones"""

from .adapters.user_repository import InMemoryUserRepository

__all__ = ["InMemoryUserRepository"]
