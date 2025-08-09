import os.path
import time
import requests
import datetime
import json
import pickle
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By

from projectfiles.dates import datesforavito, datesfordrom, class_bot, newusers

# Класс для проверки Авито
class avito:

    # Инициализация класса
    def __init__(self):
        # Авторизация
        self.autorisation_id = datesforavito.autorization_id
        self.autorisation_secret = datesforavito.autorization_secret
        # Сессия
        self.__Session = requests.Session()
        # Токен доступа
        self.__AccessToken = self.autorisation()
        # Id профиля
        self.__ProfileId = self.idProfile()
        # Путь к файлам cookie AVITO
        self.pathfilecookieavito = "projectfiles/cookies/cookies_avito.pki"
        # URL страницы статистики
        self.urlstatistics = "https://www.avito.ru/profile/statistics/spending"
        # URL профиля AVITO
        self.urlprofile = "https://www.avito.ru/tariff/cpa/profile"
        # Время сканирования данных в Авито
        self.timetoscanavito = datetime.time(12, 30).strftime("%H:%M")

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
        #url = "https://api.avito.ru/tariff/info/1"
        Headers = dict()
        Headers["Authorization"] = self.__AccessToken
        response = self.__Session.get(url, headers=Headers)
        print(response.text)
        print("Завершение выяснения баланса")

    # Начало работы с Авито
    def startprocessing(self):
        print("Запуск потока опроса Дром.")
        while True:
            # Время сейчас
            today = datetime.datetime.today()
            todaytime = today.strftime("%H:%M")
            # Запускаем функцию обработки времени
            self.switcher(todaytime)
            # Засыпаем функцию
            time.sleep(60)

    # Функция определения действия
    def switcher(self, argument):
        match argument:

            # Время для сканирования ТК
            case self.timetoscanavito:
                print(
                    f"{argument}\tВремя оповещать ответственных по данным на Авито.")
                self.check()

            # Время которое не выбрано для события
            case default:
                pass

    # Главная функция выяснения баланса
    def check(self):
        # Запускаем браузер GoogleChrome
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        # Открываем веб сайт
        driver.get(self.urlstatistics)
        # Проверяем есть ли сохранённый файл cookie
        if os.path.exists(self.pathfilecookieavito) == True:
            # Загружаем данные файлов cookie
            self.load_session(driver)
            # Перезагружаем страницу браузера
            driver.get(self.urlstatistics)
            #time.sleep(300)
        else:
            # Заполняем данные для входа
            logininput = datesforavito.phone
            passwordinput = datesforavito.password
            time.sleep(10)
            input_field = driver.find_element(By.NAME, "login")
            input_field.clear()
            input_field.send_keys(logininput)
            input_field = driver.find_element(By.NAME, "password")
            input_field.clear()
            input_field.send_keys(passwordinput)
            time.sleep(120)
            # Нажимаем на кнопку входа
            driver.find_element(By.CLASS_NAME, "css-1kdcmzd").click()
            # Сохраняем cookie для дальнейшего использования
            self.save_session(driver)

        # Ищем данные о балансе
        driver.get(self.urlprofile)
        time.sleep(4)
        try:
            balance = driver.find_element(By.CLASS_NAME,
                                      "styles-header-XwbbZ").text
            print("Баланс Авито: ", balance)
            balance2 = balance[-11:-2]
            balance = balance[-11:-2].replace(',', '.').replace(' ', '')
            print("Баланс Авито 2: ", float(balance))
            # Вычисление количества средств до отключения прайс-листа
            countmoney = int(float(balance) - 250)
            print("Денег до снятия объявлений с публикации: ", countmoney)
            averagemoney = self.avaragemonyspent()
            print("Средние траты в день: ", averagemoney)
            countdays = int(countmoney/averagemoney)
            print("Количество дней на которые хватит баланса: ", countdays)

        except Exception as e:
            print(e)
        # Закрываем браузер
        driver.quit()
        # Отправляем данные ответственному лицу
        self.sendmessage(balance2, countdays)

    # Функция вычисления средних трат в день
    def avaragemonyspent(self):
        # Запускаем браузер GoogleChrome
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        # Открываем веб сайт
        driver.get(self.urlstatistics)
        # Загружаем данные файлов cookie
        self.load_session(driver)
        # Перезагружаем страницу браузера
        driver.get(self.urlstatistics)
        expenses = driver.find_element(By.CLASS_NAME,
                                      "styles-spending-header-CfCP5").text
        expenses = int(float(expenses.replace(' ', '').replace(',', '.').replace('₽','')))
        print("Количество средств потраченных за последние 30 дней: ", int(expenses))
        return int(int(expenses)/30)

    # Функция отправки данных ответственному
    def sendmessage(self, balanse, days):
        # Токен для связи с ботом
        bot = telebot.TeleBot(class_bot.botkey)
        textmessage = "Баланс Авито: " + str(balanse) + " ₽\n"
        textmessage += "Баланса кошелька зватит на " + str(days) + " дней.\n\n"
        if days < 3:
            textmessage += "Необходимо пополнить баланс."
        else:
            textmessage += "Нет необходимости пополнять баланс."
        bot.send_message(newusers.administrator.id, text=textmessage)
        bot.send_message(newusers.sekachev.id, text=textmessage)
        print("Оповещение ответственных совершено.")

    # Функция сохранения сессии
    def save_session(self, driver):
        path = self.pathfilecookieavito
        with open(path, 'wb') as file:
            pickle.dump(driver.get_cookies(), file)

    # Функция загрузки сессии
    def load_session(self, driver):
        path = self.pathfilecookieavito
        try:
            with open(path, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except FileNotFoundError:
            print("Файл с cookie не найден.")

# Класс для проверки Дром
class drom:

    # Инициализация класса
    def __init__(self):
        # Путь к файлам cookie DROM
        self.pathfilecookiedrom = "projectfiles/cookies/cookies_drom.pki"
        # URL личного кабинета DROM
        self.url = "https://baza.drom.ru/personal"
        # URL статистики по тратам в день
        self.urlpayments = "https://baza.drom.ru/personal/balance"
        # Время сканирования данных в Дром
        self.timetoscandrom = datetime.time(12, 0).strftime("%H:%M")

    # Начало работы с Дром
    def startprocessing(self):
        print("Запуск потока опроса Дром.")
        while True:
            # Время сейчас
            today = datetime.datetime.today()
            todaytime = today.strftime("%H:%M")
            # Запускаем функцию обработки времени
            self.switcher(todaytime)
            # Засыпаем функцию
            time.sleep(60)

    # Функция определения действия
    def switcher(self, argument):
        match argument:

            # Время для сканирования ТК
            case self.timetoscandrom:
                print(f"{argument}\tВремя оповещать ответственных по данным на Дром.")
                self.check()

            # Время которое не выбрано для события
            case default:
                pass

    # Главная функция выяснения баланса
    def check(self):
        # Запускаем браузер GoogleChrome
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        # Открываем веб сайт
        driver.get(self.url)
        # Проверяем есть ли сохранённый файл cookie
        if os.path.exists(self.pathfilecookiedrom) == True:
            # Загружаем данные файлов cookie
            self.load_session(driver)
            # Перезагружаем страницу браузера
            driver.refresh()
        else:
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
            # Сохраняем cookie для дальнейшего использования
            self.save_session(driver)
        # Ищем данные о балансе
        balance = driver.find_element(By.CLASS_NAME, "personal-balance-info__balance")
        # Отправляем данные ответственному лицу
        self.sendmessage(balance.text)
        # Закрываем браузер
        driver.quit()

    # Функция сохранения сессии
    def save_session(self, driver):
        path = self.pathfilecookiedrom
        with open(path, 'wb') as file:
            pickle.dump(driver.get_cookies(), file)

    # Функция загрузки сессии
    def load_session(self, driver):
        path = self.pathfilecookiedrom
        try:
            with open(path, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except FileNotFoundError:
            print("Файл с cookie не найден.")

    # Функция отправки данных ответственному
    def sendmessage(self, balanse):
        # Токен для связи с ботом
        bot = telebot.TeleBot(class_bot.botkey)
        textmessage = "Баланс Drom: " + str(balanse) + self.replenishmentforecast(balanse)
        bot.send_message(newusers.administrator.id, text=textmessage)
        bot.send_message(newusers.sekachev.id, text=textmessage)
        print("Оповещение ответственных совершено.")

    # Функция прогнозирования пополнения
    def replenishmentforecast(self, balance):
        # Запускаем браузер GoogleChrome
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        # Открываем веб сайт
        driver.get(self.urlpayments)
        # Загружаем данные файлов cookie
        self.load_session(driver)
        # Перезагружаем страницу браузера
        driver.refresh()
        # Ищем данные об тратах за последее время
        dates = driver.find_element(By.CLASS_NAME, "month-details").text.splitlines()
        paymentdats = dict()
        sum = i = 0
        # Разбираем полученные данные на нужные
        for element in dates:
            if element.find('Оплата за просмотры') >= 0:
                i += 1
                element = element.replace(',', '.')
                indexclick = element.find('за клик')
                # Обьединение строк из выборки и подсчёт данных пл дням
                if i % 2 == 0:
                    sum += float(element[indexclick+9:])
                    #print("Второй элемент", i, "\t\t", sum)
                    paymentdats[element[56:66]] = sum
                    sum = 0
                    i = 0
                else:
                    sum += float(element[indexclick+9:])
                    #print("Первый элемент", i, "\t\t", sum)
        # Удаление пробелов из баланса
        balance = balance.replace(' ', '')
        # Вычисляем количество дней, на которых хватит баланса
        countdays = float(balance[:-1])//self.sumavaragepayment(paymentdats)
        # Если количество дней меньше 3, то надо пополнить баланс
        if countdays < 3:
            text = "\nБаланса кошелька хватит меньше чем на "
            text += str(int(countdays))
            text += " дня.\n\nНеобходимо пополнить баланс."
        else:
            text = "\nБаланса кошелька хватит на "
            text += str(int(countdays))
            text += " дней.\n\nНет необходимости пополнять баланс."
        # Закрываем браузер
        driver.quit()
        return text

    # Функция средней суммы трат в день
    def sumavaragepayment(self, data):
        float_values = [value for value in data.values() if
                        isinstance(value, float)]
        if not float_values:
            return None

        return sum(float_values) / len(float_values)