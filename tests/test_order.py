import pytest

from src.base_class import BaseContainer
from src.commerce import Product
from src.order import Order


def test_order_creation():
    """Тест создания заказа"""
    product = Product("Тест", "Тест", 100, 5)
    order = Order("Мой заказ", "Описание", product, 3)
    assert order.total_price == 300
    assert "Заказ 'Мой заказ'" in str(order)

def test_order_invalid_product():
    """Тест заказа с неверным продуктом"""
    with pytest.raises(TypeError):
        Order("Тест", "Тест", "не продукт", 1)


def test_category_and_order_inheritance():
    """Тест наследования от BaseContainer"""
    assert issubclass(Order, BaseContainer)