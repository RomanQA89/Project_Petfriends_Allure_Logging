# Проект по автоматизации тестирования API сайта https://petfriends.skillfactory.ru/.

При проектирований автотестов были применены фреймворки Pytest и Allure Report.
После запуска автотестов автоматически создается файл log.txt, где записываются все HTTP запросы и ответы.
Представлено 725 тестов в проекте, 6 позитивных и 719 негативных, в некоторых тестах применена параметризация через декоратор pytest.mark.parametrize.

Основная директория проекта содержит файлы:

- api.py - API библиотека;
- conftest.py - фикстуры для работы с тестами;
- pytest.ini - маркеры для параметризации;
- requirements.txt - используемые при тестировании библиотеки PyCharm;
- settings.py - учетные данные, используемые в процессе тестов.

Папка tests содержит:

- папка images с фотографиями питомцев в формате jpg;
- log_decorator.py - декоратор для записи логов в файл log.txt;
- test.py - файл с тестами.

  Для подготовки к запуску автотестов необходимо установить необходимые библиотеки PyCharm с помощью вводимой команды в консоли терминала:

       pip install -r requirements.txt

  Также необходимо ввести валидные данные уже авторизованного пользователя на сайте в файл .env и установить Allure Report для успешного прохождения автотестов.
  

  Для простого запуска автотестов с логированием необходимо вводить команды в консоли терминала.
  

1. Для всех позитивных API тестов:

       pytest -v tests/test.py -k positive

2. Для всех негативных API тестов:

       pytest -v tests/test.py -k negative

3. Для запуска всех тестов:

       pytest -v tests/test.py


Для запуска автотестов с логированием и создания отчетности Allure необходимо вводить команды в консоли терминала.


1. Для всех позитивных API тестов:

       pytest -v tests/test.py -k positive --alluredir allure-results

2. Для всех негативных API тестов:

       pytest -v tests/test.py -k negative --alluredir allure-results

3. Для запуска всех тестов:

       pytest -v tests/test.py --alluredir allure-results
   
4. Для генерации локального Allure сервера и просмотра отчетности Allure Report:

       allure serve allure-results

5. Для экспорта Allure отчетов проведенных тестов:

       allure generate -c ./allure-results -o ./allure-report

Окружение: Google Chrome Версия 122, Python 3.11, Windows 11 Home (64 бит)
