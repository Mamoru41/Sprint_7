import requests
import random
import string
from data.urls import URLs


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''
    for i in range(length):
        random_string += random.choice(letters)
    return random_string


def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(URLs.BASE_URL + URLs.COURIER, data=payload)

    if response.status_code == 201:
        if response.text:
            response_data = response.json()
            if 'ok' in response_data:
                assert response_data['ok'] == True
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }

    response = requests.post(URLs.BASE_URL + URLs.COURIER_LOGIN, data=payload)
    return response


def delete_courier(courier_id):
    response = requests.delete(URLs.BASE_URL + URLs.COURIER_BY_ID.format(id=courier_id))
    return response.status_code == 200
