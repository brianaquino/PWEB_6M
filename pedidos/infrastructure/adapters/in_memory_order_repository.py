from typing import List, Optional, Dict
from domain.order import Order, OrderUpdate
from application.ports.order_repository import OrderRepository

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.db: Dict[str, Order] = {}

    def save(self, order: Order) -> Order:
        self.db[order.id] = order
        return order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.db.get(order_id)

    def get_all(self) -> List[Order]:
        return list(self.db.values())

    def update(self, order_id: str, order_update: OrderUpdate) -> Optional[Order]:
        order = self.db.get(order_id)
        if not order:
            return None
        
        # Actualizamos solo lo que venga
        updated_data = order_update.model_dump(exclude_unset=True)
        updated_order = order.model_copy(update=updated_data)
        
        self.db[order_id] = updated_order
        return updated_order

    def delete(self, order_id: str) -> bool:
        if order_id in self.db:
            del self.db[order_id]
            return True
        return False