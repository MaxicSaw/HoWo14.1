import pytest

from src.base_class import BaseProduct, LoggingMixin, BaseContainer
from src.commerce import Product, Category
from src.order import Order


def test_base_product_abc():
    """Тест, что BaseProduct действительно абстрактный"""
    with pytest.raises(TypeError):
        BaseProduct("Test", "Test", 100, 1)


def test_product_inherits_base_product():
    """Тест наследования от BaseProduct"""
    assert issubclass(Product, BaseProduct)
    product = Product("Test", "Test", 100, 1)
    assert isinstance(product, BaseProduct)


def test_logging_mixin(capsys):
    """Тест миксина логирования"""

    class Test(LoggingMixin):
        def __init__(self, x):
            super().__init__(x=x)
            self.x = x

    test = Test(10)
    captured = capsys.readouterr()
    assert "Создан объект Test с параметрами:" in captured.out
    assert "x=10" in str(test)

def test_base_container_abc():
    """Тест, что BaseContainer действительно абстрактный"""
    with pytest.raises(TypeError):
        BaseContainer("Test", "Test")

def test_category_and_order_inheritance():
    """Тест наследования от BaseContainer"""
    assert issubclass(Category, BaseContainer)