from json import dumps
import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from api import api_request
from settings import *


@allure.feature("Получение списка питомцев через метод API: '/api/pets'")
@allure.title("Метод GET. Проверка возможности получения списка всех питомцев и что он не пустой.")
@pytest.mark.parametrize('filter', ['', 'my_pets'], ids=['filter_all_pets', 'filter_my_pets'])
@pytest.mark.positive
def test_get_list_of_pets(api_client, filter):
    """Метод GET. Проверяем что запрос списка питомцев возвращает не пустой список."""

    response = api_request(api_client, 'GET', f'{BASE_URL}/pets?filter={filter}')
    allure.attach(
        body=dumps(response.json(), ensure_ascii=False, indent=4),
        name="Response JSON",
        attachment_type=AttachmentType.JSON
    )
    assert response.status_code == 200
    assert len(response.json().get('pets')) > 0


@allure.feature("Создание и удаление питомца через методы API: '/api/create_pet_simple' и '/api/pets/{pet_id}'")
@allure.title("Методы POST и DELETE. Проверка возможности создания питомца и его удаления.")
@pytest.mark.parametrize('name', ['Jip'])
@pytest.mark.parametrize('animal_type', ['cat'])
@pytest.mark.parametrize('age', ['5'])
@pytest.mark.positive
def test_create_pet(create_pet, name, animal_type, age):
    """Создание и удаление питомца через методы POST и DELETE с помощью фикстуры 'create_pet'."""
    assert create_pet


@allure.feature("Обновление данных питомца через метод API: '/api/pets/{pet_id}'")
@allure.title("Метод PUT. Проверка возможности обновления данных питомца и последующее его удаление.")
@pytest.mark.parametrize('name', ['Jip'])
@pytest.mark.parametrize('animal_type', ['cat'])
@pytest.mark.parametrize('age', ['5'])
@pytest.mark.positive
def test_update_pet(create_pet, api_client, name, animal_type, age):
    """Обновление данных питомца через фикстуры create_pet и api_client """
    data_update = {
        'name': 'Pusssss'
    }
    response = api_request(api_client, 'PUT', f'{BASE_URL}/pets/{create_pet}', json=data_update)
    assert response.status_code == 200
    assert response.json().get('name') == data_update['name']


@allure.feature("Создание и удаление питомца с фото через методы API: '/api/pets' и '/api/pets/{pet_id}'")
@allure.title("Методы POST и DELETE. Проверка возможности создания питомца с фото и его удаления.")
@pytest.mark.positive
def test_create_pet_with_photo(create_pet_with_photo):
    """Создание и удаление питомца с фото через методы POST и DELETE с помощью фикстуры 'create_pet_with_photo'."""
    assert create_pet_with_photo


@allure.feature("Добавление фото питомца через метод API: '/api/pets/set_photo/{pet_id}'")
@allure.title("Методы POST и DELETE. Проверка возможности добавления фото к уже созданному питомцу "
              "и последующее его удаление.")
@pytest.mark.parametrize('name', ['Jip'])
@pytest.mark.parametrize('animal_type', ['cat'])
@pytest.mark.parametrize('age', ['5'])
@pytest.mark.positive
def test_add_photo_of_pet(create_pet, api_client, name, animal_type, age):
    """Добавление фото питомца через метод POST."""
    files = {
        "pet_photo": ("cat1.jpg", open("tests/images/cat1.jpg", "rb"), "image/jpeg"),
    }
    response = api_request(api_client, 'POST', f'{BASE_URL}/pets/set_photo/{create_pet}', files=files)
    allure.attach(
        body=dumps(response.json(), ensure_ascii=False, indent=4),
        name="Response JSON",
        attachment_type=AttachmentType.JSON
    )
    assert response.status_code == 200


# Негативные тесты.


@allure.feature("Негативная проверка на получение API ключа через метод API: '/api/key'")
@allure.title("Метод GET. Проверка на 403 статус-код при вводе невалидных электронной почты и пароля.")
@pytest.mark.parametrize('email', ['', 'pv.romdex.ru', 'pv.rom@dex.', '123', 'pvrom@dexcom'],
                         ids=['empty', 'without_at', 'without_domain', 'digits', 'without_dot'])
@pytest.mark.parametrize('password', ['', 's', 'gh'], ids=['empty', 'one_char', 'two_chars'])
@pytest.mark.negative
def test_get_api_key_negative(email, password):
    """Проверяем что запросы api ключа с невалидными email и password возвращают статус 403"""
    session = requests.Session()
    response = api_request(session, 'GET', f'{BASE_URL}/key',
                           headers_update={
                               'email': email,
                               'password': password
                           })
    status = response.status_code
    assert status == 403


@pytest.mark.parametrize("name", ['', generate_string(255), generate_string(1001), russian_chars(),
                                  russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                         ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese',
                              'specials', 'digit'])
@pytest.mark.parametrize("animal_type", ['', generate_string(255), generate_string(1001), russian_chars(),
                                         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                         ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese',
                              'specials', 'digit'])
@pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                                 special_chars(), russian_chars(), russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float',
                              'int_max', 'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
@pytest.mark.negative
def test_create_pet_negative(create_pet, name, animal_type, age):
    """Создание и удаление питомца через методы POST и DELETE с помощью фикстуры 'create_pet'.
    Тестирование негативных сценариев с невалидными параметрами name, animal_type, age."""
    assert create_pet
