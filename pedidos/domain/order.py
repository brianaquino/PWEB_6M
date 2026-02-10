from pydantic import BaseModel
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pendiente"
    COMPLETED = "completado"
    CANCELLED = "cancelado"

class Order(BaseModel):
    id: str
    user_id: str          # Relación con el usuario
    item_description: str # Qué pidió (Ej: "Hamburguesa")
    quantity: int
    total_price: float
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(BaseModel):
    user_id: str
    item_description: str
    quantity: int
    total_price: float

class OrderUpdate(BaseModel):
    item_description: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[OrderStatus] = None