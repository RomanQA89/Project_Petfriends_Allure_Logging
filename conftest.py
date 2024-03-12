import allure
import pytest
import requests
from settings import valid_email, valid_password, BASE_URL
from api import api_request


# Фикстура для запроса API ключа через метод GET.
@allure.step("Авторизация в сервисе Petfriends через API.")
@pytest.fixture(scope='module')
def api_client():
    session = requests.Session()
    response = api_request(session, 'GET', f'{BASE_URL}/key',
                           headers_update={
                               'email': valid_email,
                               'password': valid_password
                           })
    access_token = response.json().get('key')
    assert access_token
    session.headers.update({
        'auth_key': access_token,
        'accept': 'application/json'
    })
    yield session
    print('logout')


# Фикстура для создания и обновления данных питомца и последующего его удаления.
@allure.step("Создание и обновление данных питомца и последующее его удаление.")
@pytest.fixture(scope='function')
def create_pet(api_client, name, animal_type, age):
    data = {
        'name': name,
        'age': age,
        'animal_type': animal_type
    }
    response = api_request(api_client, 'POST', f'{BASE_URL}/create_pet_simple', json=data)
    pet_id = response.json().get('id')
    assert pet_id
    yield pet_id
    api_request(api_client, 'DELETE', f'{BASE_URL}/pets/{pet_id}')


# Фикстура для создания питомца с фото и для добавления фото к питомцу с последующим его удалением.
@allure.step("Создание питомца с фото и добавление фото к питомцу у которого нет фото и последующее их удаление.")
@pytest.fixture(scope='function')
def create_pet_with_photo(api_client):
    data = {
            'name': 'Tom',
            'age': 9,
            'animal_type': 'cat'
    }
    files = {
        "pet_photo": ("cat1.jpg", open("tests/images/cat1.jpg", "rb"), "image/jpeg"),
    }
    response = api_request(api_client, 'POST', f'{BASE_URL}/pets', data=data, files=files)
    pet_id = response.json().get('id')
    assert pet_id
    yield pet_id
    api_request(api_client, 'DELETE', f'{BASE_URL}/pets/{pet_id}')
