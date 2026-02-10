from abc import ABC, abstractmethod
from typing import List, Optional
from domain.order import Order, OrderCreate, OrderUpdate

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order_id: str, order_update: OrderUpdate) -> Optional[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: str) -> bool:
        pass