from netology.unit_test_s.web_driver import open_url, ya_passport_login, driver_quit, is_logged_in
from netology.unit_test_s.conftest import ValueStorage


class TestClass:

    def test_open_url_11(self):
        url = 'https://passport.yandex.ru/auth/'
        ValueStorage.driver = open_url(url)
        assert ValueStorage.driver != False

    def test_ya_passport_login_11(self):
        driver = ValueStorage.driver
        ya_login = 'test'
        ya_password = 'test'
        result = ya_passport_login(ya_login, ya_password, driver)
        assert result == True

    def test_is_logged_in_11(self):
        driver = ValueStorage.driver
        result = is_logged_in(driver)
        assert result == True

    def test_driver_quit_11(self):
        driver = ValueStorage.driver
        result = driver_quit(driver)
        assert result == True

