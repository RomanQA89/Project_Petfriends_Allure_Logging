import json
import allure
import requests
from settings import BASE_URL
from tests.log_decorator import log_request


# Апи библиотека.
@log_request
def api_request(session, method, url,
                headers_update='',
                data='',
                json='',
                files=None):  # Добавил аргумент files по умолчанию None
    if headers_update:
        session.headers.update(headers_update)
    if method in ['GET', 'POST', 'PUT', 'DELETE']:
        if files:
            response = session.request(method, url, data=data, json=json, files=files)
        else:
            response = session.request(method, url, data=data, json=json)
    else:
        response = ''
    return response


# @allure.step("HTTP запрос типа GET с ресурсом '/api/key' с API")
# def get_api_key(valid_email, valid_password):
#     """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
#     JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
#
#     headers = {
#         'email': valid_email,
#         'password': valid_password,
#     }
#     res = requests.get(f'{BASE_URL}/key', headers=headers)
#     status = res.status_code
#     result = ""
#     try:
#         result = res.json()
#     except json.decoder.JSONDecodeError:
#         result = res.text
#     return status, result
