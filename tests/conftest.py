import pytest
import requests
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier, delete_courier
from data.urls import URLs

@pytest.fixture
def create_and_delete_courier():
    """Фикстура создает курьера перед тестом и удаляет после"""
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data
    #удаляем курьера после теста
    if courier_data:
        login_response = login_courier(courier_data[0], courier_data[1])
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_courier(courier_id)

@pytest.fixture
def get_courier_id(create_and_delete_courier):
    """Фикстура возвращает ID созданного курьера"""
    login = create_and_delete_courier[0]
    password = create_and_delete_courier[1]
    response = login_courier(login, password)
    return response.json()["id"]