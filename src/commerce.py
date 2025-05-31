from src.base_class import BaseProduct, BaseContainer, LoggingMixin, CreationInfoMixin


class Product(BaseProduct, LoggingMixin, CreationInfoMixin):
    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self.__price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if hasattr(self, '_Product__price') and new_price < self.__price:
            confirmation = input("Подтвердите снижение цены (y/n): ")
            if confirmation.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data, products=None):
        if products is None:
            products = []

        for prod in products:
            if prod.name == product_data["name"]:
                prod.price = max(prod.price, product_data["price"])
                prod.quantity += product_data["quantity"]
                return prod

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category(BaseContainer, LoggingMixin, CreationInfoMixin):
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        super().__init__(name, description)
        self.__products = products if products else []
        Category.category_count += 1

    def __len__(self):
        return len(self.__products)

    @property
    def products(self):
        return "".join(str(product) for product in self.__products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."