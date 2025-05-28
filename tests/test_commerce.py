from src.commerce import Product, Category
import pytest


def test_private_products_access():
    cat = Category("Тест", "Описание")
    assert not hasattr(cat, '__products'), "Список продуктов должен быть приватным"


def test_add_product_method():
    cat = Category("Тест", "Описание")
    product = Product("Товар", "Описание", 100, 5)

    initial_count = Category.product_count
    cat.add_product(product)

    assert Category.product_count == initial_count + 1
    assert len(cat.products.split('\n')) == 2  # 1 товар + пустая строка


def test_products_getter_format():
    cat = Category("Тест", "Описание")
    product = Product("Телефон", "Смартфон", 50000, 3)
    cat.add_product(product)

    assert "Телефон, 50000 руб. Остаток: 3 шт.\n" in cat.products


def test_new_product_classmethod():
    product = Product.new_product({
        'name': 'Ноутбук',
        'description': 'Игровой',
        'price': 100000,
        'quantity': 5
    })

    assert isinstance(product, Product)
    assert product.name == "Ноутбук"
    assert product.price == 100000


def test_price_property():
    product = Product("Тест", "Тест", 100, 1)

    # Проверка геттера
    assert product.price == 100

    # Проверка сеттера с отрицательной ценой
    product.price = -50
    assert product.price == 100

    # Проверка сеттера с валидной ценой
    product.price = 150
    assert product.price == 150


def test_duplicate_product_handling():
    products = [Product("Телефон", "Смартфон", 50000, 3)]
    updated = Product.new_product({
        'name': 'Телефон',
        'description': 'Новый',
        'price': 60000,
        'quantity': 2
    }, products)

    assert updated.quantity == 5
    assert updated.price == 60000


def test_price_reduction_confirmation(monkeypatch):
    """Тест подтверждения снижения цены через input"""
    product = Product("Тест", "Тест", 100, 1)

    # Тест 1: Пользователь подтверждает снижение
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 80
    assert product.price == 80

    # Тест 2: Пользователь отменяет снижение
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 70
    assert product.price == 80  # Цена не должна измениться

    # Проверка вывода сообщения
    from io import StringIO
    import sys
    captured_output = StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 70
    assert "Изменение цены отменено" in captured_output.getvalue()

    sys.stdout = sys.__stdout__


def test_add_product_type_check():
    """Тест проверки типа добавляемого продукта"""
    cat = Category("Тест", "Тест")
    product = Product("Тест", "Тест", 100, 1)

    # Корректный продукт
    cat.add_product(product)
    assert len(cat.products) > 0

    # Некорректный продукт
    with pytest.raises(TypeError) as excinfo:
        cat.add_product("не продукт")
    assert "Можно добавлять только объекты класса Product" in str(excinfo.value)


def test_category_len():
    """Тест метода __len__ категории"""
    cat = Category("Тест", "Тест")
    assert len(cat) == 0

    product = Product("Тест", "Тест", 100, 1)
    cat.add_product(product)
    assert len(cat) == 1

    # Проверка после нескольких добавлений
    for i in range(2, 5):
        new_product = Product(f"Тест{i}", "Тест", 100 + i, i)
        cat.add_product(new_product)
        assert len(cat) == i