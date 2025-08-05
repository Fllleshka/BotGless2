import time

from projectfiles.dates import datesforavito, datesfordrom

import requests
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
class avito:

    def __init__(self):
        # Авторизация
        self.autorisation_id = datesforavito.autorization_id
        self.autorisation_secret = datesforavito.autorization_secret
        # Приложение
        self.app_id = datesforavito.app_id
        self.pp_secret = datesforavito.app_secret
        # Сессия
        self.__Session = requests.Session()
        # Токен доступа
        self.__AccessToken = self.autorisation()
        # Id профиля
        self.__ProfileId = self.idProfile()

    def autorisation(self):
        print("Запуск авторизации")
        autourl = "https://api.avito.ru/token/"
        # Параметры запроса.
        Params = {
            "grant_type": "client_credentials",
            "client_id": self.autorisation_id,
            "client_secret": self.autorisation_secret
        }
        # Заголовки запроса
        Headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # Запрос нового токена доступа.
        Response = self.__Session.post(autourl, headers=Headers, params=Params)
        jsonresp = dict(json.loads(Response.text))
        result = jsonresp["token_type"] + " " + jsonresp['access_token']
        print("Авторизация пройдена")
        return result

    def idProfile(self):
        print("Запрос id")
        url = "https://api.avito.ru/core/v1/accounts/self"
        # Заголовки запроса
        Headers = dict()
        Headers["Authorization"] = self.__AccessToken
        response = self.__Session.get(url, headers = Headers)
        profileid = dict(json.loads(response.text))
        print(profileid["id"])
        print("Окончание запроса id")
        return profileid["id"]

    def balance(self):
        print("Выяснение баланса")
        url = "https://api.avito.ru/core/v1/accounts/" + str(self.__ProfileId) +"/balance/"
        Headers = dict()
        Headers["Authorization"] = self.__AccessToken
        response = self.__Session.get(url, headers=Headers)
        print(response.text)
        print("Завершение выяснения баланса")

class drom:
    def check(self):
        url = "https://baza.drom.ru/personal"
        # Используем Генерируем настройки для GoogleChrome
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        # Открываем веб сайт
        driver.get(url)

        # Заполняем данные для входа
        logininput = datesfordrom.login
        passwordinput = datesfordrom.password
        input_field = driver.find_element(By.ID, "sign")
        input_field.clear()
        input_field.send_keys(logininput)
        input_field = driver.find_element(By.ID, "password")
        input_field.clear()
        input_field.send_keys(passwordinput)
        # Нажимаем на кнопку входа
        driver.find_element(By.ID, "signbutton").click()
        # Ищем данные о балансе
        balance = driver.find_element(By.CLASS_NAME, "personal-balance-info__balance")
        print("Баланс Дром: ", balance.text)
        self.save_session(driver)
        # Закрываем браузер
        driver.quit()

    def save_session(self, driver, path="projectfiles/cookies.pkl"):
        with open(path, 'wb') as file:
            pickle.dump(driver.get_cookies(), file)