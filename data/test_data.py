class TestData:
    # Данные для создания курьера без обязательных полей
    COURIER_MISSING_FIELDS = [
        ({"password": "password123", "firstName": "Ilya"}, "Недостаточно данных для создания учетной записи"),
        ({"login": "testlogin123", "firstName": "Ilya"}, "Недостаточно данных для создания учетной записи")
    ]

    # Данные для создания заказа
    ORDER_DATA = {
        "firstName": "Ilya",
        "lastName": "Ivanov",
        "address": "Moscow, Red Square 1",
        "metroStation": 5,
        "phone": "+79991112233",
        "rentTime": 3,
        "deliveryDate": "2025-10-25",
        "comment": "Test order"
    }

    # Сообщения об ошибках
    ERROR_MESSAGES = {
        "missing_data": "Недостаточно данных для создания учетной записи",
        "missing_login_data": "Недостаточно данных для входа",
        "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
        "account_not_found": "Учетная запись не найдена"
    }