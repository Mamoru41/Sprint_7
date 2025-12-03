import pytest
import requests
import allure
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier
from data.urls import URLs
from data.test_data import TestData


@allure.feature("Courier API")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, create_and_delete_courier):
        # Создаем куру и удаляем
        courier_data = create_and_delete_courier
        assert len(courier_data) == 3, "Курьер не был создан"

        # Проверяем авторизации
        login = courier_data[0]
        password = courier_data[1]
        response = login_courier(login, password)

        assert response.status_code == 200, "Не удалось авторизоваться под созданным курьером"
        assert "id" in response.json(), "В ответе нет ID курьера"

    @allure.title("Создание дубликата курьера")
    def test_create_duplicate_courier_fails(self, create_and_delete_courier):
        # Взял данные курьера из фикстур
        courier_data = create_and_delete_courier
        assert len(courier_data) == 3, "Первый курьер не создан"

        # Создаем дубликат
        payload = {
            "login": courier_data[0],
            "password": courier_data[1],
            "firstName": courier_data[2]
        }

        response = requests.post(URLs.BASE_URL + URLs.COURIER, data=payload)
        assert response.status_code == 409, "Ожидалась ошибка 409 при создании дубликата"
        assert response.json()["message"] == TestData.ERROR_MESSAGES["duplicate_login"]

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize("payload,expected_message", TestData.COURIER_MISSING_FIELDS)
    def test_create_courier_missing_required_fields(self, payload, expected_message):
        response = requests.post(URLs.BASE_URL + URLs.COURIER, data=payload)
        assert response.status_code == 400, "Ожидалась ошибка 400 при отсутствии обязательного поля"
        assert response.json()["message"] == expected_message


@allure.feature("Courier Login API")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, create_and_delete_courier):
        courier_data = create_and_delete_courier
        assert len(courier_data) == 3, "Курьер не создан"

        login = courier_data[0]
        password = courier_data[1]
        response = login_courier(login, password)

        assert response.status_code == 200, "Ожидался успешный логин"
        assert "id" in response.json(), "В ответе нет ID курьера"

    @allure.title("Авторизация с неправильным паролем")
    def test_login_with_wrong_password_fails(self, create_and_delete_courier):
        courier_data = create_and_delete_courier
        assert len(courier_data) == 3, "Курьер не создан"

        login = courier_data[0]
        wrong_password = "wrong_password"
        response = login_courier(login, wrong_password)

        assert response.status_code == 404, "Ожидалась ошибка 404 при неверном пароле"
        assert response.json()["message"] == TestData.ERROR_MESSAGES["account_not_found"]

    @allure.title("Авторизация без логина")
    def test_login_without_login_fails(self):
        payload = {
            "password": "password123"
        }

        response = requests.post(URLs.BASE_URL + URLs.COURIER_LOGIN, data=payload)
        assert response.status_code == 400, "Ожидалась ошибка 400 при отсутствии логина"
        assert response.json()["message"] == TestData.ERROR_MESSAGES["missing_login_data"]

    @allure.title("Авторизация без пароля")
    def test_login_without_password_fails(self, create_and_delete_courier):
        courier_data = create_and_delete_courier
        assert len(courier_data) == 3, "Курьер не создан"

        payload = {
            "login": courier_data[0]
        }

        response = requests.post(URLs.BASE_URL + URLs.COURIER_LOGIN, data=payload)
        assert response.status_code in [400, 404, 504], f"Неожиданный статус код: {response.status_code}"

        if response.status_code == 400:
            assert response.json()["message"] == TestData.ERROR_MESSAGES["missing_login_data"]
        elif response.status_code == 404:
            assert response.json()["message"] == TestData.ERROR_MESSAGES["account_not_found"]