from abc import ABC, abstractmethod
from datetime import datetime


class BaseProduct(ABC): #pragma: no cover
    """Абстрактный базовый класс для продуктов"""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass


class BaseContainer(ABC): #pragma: no cover
    """Абстрактный класс для контейнеров (Категория и Заказ)"""

    @abstractmethod
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    @abstractmethod
    def __str__(self):
        pass


class LoggingMixin:
    """Миксин для логирования создания объектов"""
    def __init__(self, *args, **kwargs):
        print(f"Создан объект {self.__class__.__name__} с параметрами:")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        super().__init__(*args)

    def __repr__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class CreationInfoMixin:
    """Миксин для вывода информации о создании объектов"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._print_creation_info()

    def _print_creation_info(self):
        """Альтернативный подход с возвратом строки вместо печати"""
        info = (
            f"[CREATION INFO] Создан объект {self.__class__.__name__}\n"
            f"Параметры: name={getattr(self, 'name', '')}\n"
        )
        import sys
        sys.stdout.write(info)
        sys.stdout.flush()