import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List

from domain.order import Order, OrderCreate, OrderUpdate
from application.services.order_service import OrderService
from infrastructure.adapters.in_memory_order_repository import InMemoryOrderRepository

app = FastAPI(title="Microservicio de Pedidos", version="1.0.0")

# Inyección de dependencias
repo = InMemoryOrderRepository()
service = OrderService(repo)

@app.post("/orders", response_model=Order, status_code=201)
def create_order(order: OrderCreate):
    return service.create_order(order)

@app.get("/orders", response_model=List[Order])
def list_orders():
    return service.list_orders()

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: str, order_update: OrderUpdate):
    order = service.update_order(order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: str):
    success = service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return None

if __name__ == "__main__":
    # REQUISITO: Puerto 8002
    uvicorn.run(app, host="0.0.0.0", port=8002)