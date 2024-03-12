import os
import string
from dotenv import load_dotenv

load_dotenv()

"""Валидные данные"""
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
BASE_URL = 'https://petfriends.skillfactory.ru/api'


def generate_string(n):
    return 's' * n


def russian_chars():
    return 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'


def chinese_chars():    # 20 популярных китайских иероглифов
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return f'{string.punctuation}'
