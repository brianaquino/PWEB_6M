import uuid
from typing import List, Optional
from domain.order import Order, OrderCreate, OrderUpdate, OrderStatus
from application.ports.order_repository import OrderRepository

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, order_in: OrderCreate) -> Order:
        # Lógica: Crear el objeto Order con ID nuevo
        new_order = Order(
            id=str(uuid.uuid4()),
            user_id=order_in.user_id,
            item_description=order_in.item_description,
            quantity=order_in.quantity,
            total_price=order_in.total_price,
            status=OrderStatus.PENDING
        )
        return self.repository.save(new_order)

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.repository.get_by_id(order_id)

    def list_orders(self) -> List[Order]:
        return self.repository.get_all()

    def update_order(self, order_id: str, order_in: OrderUpdate) -> Optional[Order]:
        return self.repository.update(order_id, order_in)

    def delete_order(self, order_id: str) -> bool:
        return self.repository.delete(order_id)