from selenium import webdriver
import time


def open_url(url):
    try:
        driver = webdriver.Firefox(executable_path=r'c:/ProgFiles/geckodriver/geckodriver.exe')
        driver.get(url)
        driver.implicitly_wait(10)
    except Exception as e:
        return False
    return driver


def ya_passport_login(login, password, driver):
    try:
        input_field_login_xpath = '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[1]/span/input'
        input_field = driver.find_element_by_xpath(input_field_login_xpath)
        input_field.send_keys(login)
        input_field.submit()
        driver.implicitly_wait(10)
    except Exception as e:
        return False, 'cannot find input_field_login'

    try:
        input_field_password_xpath = '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[2]/span/input'
        input_field = driver.find_element_by_xpath(input_field_password_xpath)
        input_field.send_keys(password)
        input_field.submit()
        driver.implicitly_wait(10)
    except Exception as e:
        return False, 'cannot find input_field_password'

    time.sleep(5)
    return True


def is_logged_in(driver):
    page_text = driver.find_element_by_tag_name('body').text

    if page_text.find('Неверный пароль'):
        return False

    return True


def driver_quit(driver):
    try:
        driver.quit()
    except Exception as e:
        return False

    return True


if __name__ == '__main__':
    url = 'https://passport.yandex.ru/auth/'
    ya_login = 'test'
    ya_password = 'test'

    driver = open_url(url)
    print(ya_passport_login(ya_login, ya_password, driver))
    print(is_logged_in(driver))
    driver_quit(driver)
