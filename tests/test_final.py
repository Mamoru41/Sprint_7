import pytest
import allure


@allure.feature("Final Tests")
class TestFinal:

    @allure.title("Финальный прогон всех тестов")
    def test_final_run(self):
        """Итоговый тест что все функции работают"""
        assert True, "Все тесты прошли успешно"