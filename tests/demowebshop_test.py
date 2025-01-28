import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have

LOGIN = 'Coluchy@yandex.ru'
PASSWORD = '123456789'
URL = 'https://demowebshop.tricentis.com/'


def clear_cart():
    with allure.step('Очистить корзину'):
        browser.element('.qty-input').set_value('0').press_enter()


def test_add_one_item():
    with allure.step('Авторизоваться через API'):
        login = requests.post(url=URL + 'login',
                              data={'email': LOGIN, 'password': PASSWORD, 'RememberMe': False},
                              allow_redirects=False)
        allure.attach(body=login.text,
                      name='response',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Получить cookie через API'):
        cookie = login.cookies.get('NOPCOMMERCE.AUTH')
        browser.open(URL)
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.open(URL)

    with allure.step('Проверить прохождение авторизации'):
        browser.element('.account').should(have.text('Coluchy@yandex.ru'))

    with allure.step('Добавить товар в корзину через API'):
        response1 = requests.post(url=URL + 'addproducttocart/catalog/31/1/1',
                                  cookies={'NOPCOMMERCE.AUTH': cookie})
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Проверить добавление товара в корзину'):
        assert response1.status_code == 200
        browser.open(URL + 'cart')
        browser.element('.product-name').should(have.text('14.1-inch Laptop'))

    with allure.step('Очистить корзину'):
        browser.open(URL + 'cart')
        clear_cart()
        browser.quit()


def test_add_some_item():
    with allure.step('Авторизоваться через API'):
        login = requests.post(url=URL + 'login',
                              data={'email': LOGIN, 'password': PASSWORD, 'RememberMe': False},
                              allow_redirects=False)
        allure.attach(body=login.text,
                      name='response',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Получить cookie через API'):
        cookie = login.cookies.get('NOPCOMMERCE.AUTH')
        browser.open(URL)
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.open(URL)

    with allure.step('Проверить прохождение авторизации'):
        browser.element('.account').should(have.text('Coluchy@yandex.ru'))

    with allure.step('Добавить 2 товара в корзину через API'):
        response2 = requests.post(url=URL + 'addproducttocart/catalog/40/1/1',
                                  cookies={'NOPCOMMERCE.AUTH': cookie})
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')
        response3 = requests.post(url=URL + 'addproducttocart/catalog/14/1/1',
                                  cookies={'NOPCOMMERCE.AUTH': cookie})
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Проверить добавление 2 товаров в корзину'):
        assert response2.status_code == 200
        assert response3.status_code == 200
        browser.open(URL + 'cart')
        browser.element('.cart').should(have.text('Black & White Diamond Heart'))
        browser.element('.cart').should(have.text('Casual Golf Belt'))

    with allure.step('Чистим корзину'):
        browser.open(URL + 'cart')
        clear_cart()

    with allure.step('Чистим корзину'):
        browser.open(URL + 'cart')
        clear_cart()
        browser.quit()


def test_add_item_unauth_user():
    with allure.step("Добавить товар в корзину через API"):
        response4 = requests.post(URL + 'addproducttocart/catalog/31/1/1')
        allure.attach(
            body=response4.text,
            name="Response",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        allure.attach(
            body=str(response4.cookies),
            name="Cookies",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        allure.attach(
            body=str(response4.request.headers),
            name="Request headers",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        cookie = response4.cookies.get_dict()

    with allure.step('Проверить добавление товара в корзину'):
        assert response4.status_code == 200
        browser.open(URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie["Nop.customer"]})
        browser.open(URL + "cart")
        browser.element('.product-name').should(have.text('14.1-inch Laptop'))

    with allure.step('Очистить корзину'):
        browser.open(URL + 'cart')
        clear_cart()
        browser.quit()
