import json
import pytest
from src.loader import loader_data


def test_loader_with_valid_data(tmp_path):
    """Тест загрузки корректных данных"""
    test_data = [
        {
            "name": "Телефоны",
            "description": "Смартфоны",
            "products": [{"name": "iPhone 13", "description": "128GB", "price": 80000, "quantity": 10}],
        }
    ]

    file = tmp_path / "test.json"
    file.write_text(json.dumps(test_data))

    categories = loader_data(str(file))

    assert len(categories) == 1
    assert categories[0].name == "Телефоны"
    assert "iPhone 13, 80000 руб. Остаток: 10 шт.\n" in categories[0].products


def test_file_not_found():
    """Проверка обработки отсутствия файла"""
    with pytest.raises(FileNotFoundError):
        loader_data("missing.json")


def test_invalid_json(tmp_path):
    """Проверка обработки невалидного JSON"""
    file = tmp_path / "bad.json"
    file.write_text("{invalid}")
    with pytest.raises(json.JSONDecodeError):
        loader_data(str(file))