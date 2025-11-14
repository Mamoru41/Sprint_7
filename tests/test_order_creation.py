import pytest
import requests
import allure
from data.urls import URLs
from data.test_data import TestData


@allure.feature("Order API")
class TestOrderCreation:

    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        # Подготавливаем данные для заказа
        payload = TestData.ORDER_DATA.copy()
        payload["color"] = color

        # Создаем заказ
        response = requests.post(URLs.BASE_URL + URLs.ORDERS, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        # Запрашиваем список всех заказов
        response = requests.get(URLs.BASE_URL + URLs.ORDERS)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)