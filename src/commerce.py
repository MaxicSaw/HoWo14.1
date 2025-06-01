from src.base_class import BaseProduct, BaseContainer, LoggingMixin, CreationInfoMixin
from src.class_error import ZeroQuantityError


class Product(LoggingMixin, BaseProduct, CreationInfoMixin):
    total_products = 0

    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        Product.total_products += 1

    @classmethod
    def new_product(cls, product_data, products=None):
        """Создает новый товар или обновляет существующий"""
        if products:
            for prod in products:
                if prod.name.lower() == product_data["name"].lower():
                    prod.quantity += product_data["quantity"]
                    prod.price = max(prod.price, product_data["price"])
                    return prod
        return cls(**product_data)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self._price:
            confirm = input(f"Цена снижается с {self._price} до {new_price}. Подтвердите (y/n): ")

            if confirm.lower() != "y":
                print("Изменение цены отменено")
                return
        self._price = new_price

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать продукты разных типов")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category(BaseContainer):
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []
        if products:
            for product in products:
                try:
                    self.add_product(product)
                except ZeroQuantityError as e:
                    print(e)
                finally:
                    print("Обработка добавления товара завершена")
        Category.category_count += 1

    def add_product(self, product):
        """Добавляет товар в категорию"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        if product.quantity <= 0:
            raise ZeroQuantityError(f"Товар {product.name} имеет недопустимое количество: {product.quantity}")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Возвращает строку со списком товаров"""
        return "".join(str(product) for product in self.__products)

    def __len__(self):
        return len(self.__products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def middle_price(self):
        """Возвращает среднюю цену товаров в категории"""
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            print("В категории нет товаров")
            return 0