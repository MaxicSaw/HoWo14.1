from src.base_class import BaseContainer
from src.commerce import Product


class Order(BaseContainer):
    def __init__(self, name, description, product, quantity):
        super().__init__(name, description)
        if not isinstance(product, Product):
            raise TypeError("Можно заказать только объекты класса Product")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self):
        return (f"Заказ '{self.name}': {self.product.name} - "
                f"{self.quantity} шт. на сумму {self.total_price} руб.")