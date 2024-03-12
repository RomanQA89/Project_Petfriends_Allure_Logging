import functools
from datetime import datetime


# Декоратор создания логов для записи в файл log.txt
def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a') as f:
            f.write(f'{datetime.now()} | {args[1]} {args[2]}\n')
            f.write(f'{datetime.now()} | Request headers: {args[0].headers}\n')
            response = func(*args, **kwargs)
            f.write(f'{datetime.now()} | Request body: {response.request.body}\n')
            f.write(f'{datetime.now()} | Response status code: {response.status_code}\n')
            f.write(f'{datetime.now()} | Response headers: {response.headers}\n')
            f.write(f'{datetime.now()} | Response body: {response.text}\n\n')
        return response
    return wrapper
