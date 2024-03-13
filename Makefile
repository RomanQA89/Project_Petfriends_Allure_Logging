result:
	allure serve allure-results

report:
	allure generate -c ./allure-results -o ./allure-report

tests_pos:
	pytest -v tests/test.py -k positive --alluredir allure-results

tests_neg:
	pytest -v tests/test.py -k negative --alluredir allure-results

tests_all:
	pytest -v tests/test.py --alluredir allure-results
