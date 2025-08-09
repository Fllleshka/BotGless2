from projectfiles.dates import *

from threading import Thread
import datetime
import requests
import time
import os
import telebot
import sqlite3

class class_tk:

    # Инициализация класса
    def __init__(self, bot):
        # Переменная бота telegram
        self.bot = bot
        # Время сейчас
        today = datetime.datetime.today()
        todaytime = today.strftime("%H:%M:%S")
        # Время сканирования данных в ТК
        # timetoscantk = today.time().strftime("%H:%M")
        #self.timetoscantk = (today + datetime.timedelta(minutes=1)).strftime("%H:%M")
        self.timetoscantk = datetime.time(7, 30).strftime("%H:%M")
        # Время отправки сообщений
        #self.timetosendmessageresponsible = (today + datetime.timedelta(minutes=2)).strftime("%H:%M")
        self.timetosendmessageresponsible = datetime.time(9, 5).strftime("%H:%M")

        # Данных по ТК
        self.datesformdellin = []

    # Функция старта процессов
    def startprocessing(self):
        print("Запуск потока опроса ТК.")
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
            case self.timetoscantk:
                print(f"{argument}\tВремя сканировать ТК")
                dellin = Thread(target=self.scandatesfromdellin)
                dellin.start()

            # Время для отправки данных ответственному по ТК:
            case self.timetosendmessageresponsible:
                print(f"{argument}\tВремя отправлять данные по ТК")
                sendmessage = Thread(target=self.sendmessageresponsible)
                sendmessage.start()

            # Время которое не выбрано для события
            case default:
                pass

    # Сканирование данных с ТК "Деловые Линии"
    def scandatesfromdellin(self):
        self.datesformdellin = self.finddataonstite()
        print(f"\t№\t\t№ накладной\t\t\tСтатус заказа\t\tДата прихода на склад\tДата бесплатного хранения на складе")
        for element in range(0, 10):
            if self.datesformdellin[element]["stateName"] != "Заказ завершен":
                print(f"\t{element}\t\t{self.datesformdellin[element]["orderId"]}\t\t{self.datesformdellin[element]["stateName"]}\t\t\t{self.datesformdellin[element]["orderDates"]["arrivalToOspReceiver"]}\t\t\t\t{self.datesformdellin[element]["orderDates"]["warehousing"]}")

    # Функция получения данных с серверов ТК "Деловые Линии"
    def finddataonstite(self):
        address = datesfromdellin.addressautorisation
        datesjson = {
            "appkey": datesfromdellin.apikey,
            "login": datesfromdellin.login,
            "password": datesfromdellin.password
        }
        result = requests.post(address, json=datesjson)
        dates = result.json()
        sessionid = dates['data']['sessionID']
        datesjson2 = {
            "appkey": datesfromdellin.apikey,
            "sessionID": sessionid,
        }
        result = requests.post(datesfromdellin.addresmethod2, json=datesjson2)
        resultjson = result.json()["orders"]
        return resultjson

    # Функция проверки данных в таблице
    def checkdatesfromdatabase(self, con, request):
        #print("Проверка вводимых значений")
        with con:
            cursor = con.cursor()
            cursor.execute(request)
            result = cursor.fetchall()
            #for element in result:
            #    print(element)
        return result

    # Функция оправки сообщений ответственным лицам
    def sendmessageresponsible(self):
        # Обработка утери базы данных
        if os.path.exists(pathdatabase) == True:
            print("Файл базы данных существует!")
            # Открываем соединение с базой данных
            con = sqlite3.connect(pathdatabase)
            # Закрываем соединение с базой данных
            con.close()
        else:
            print("Файл базы данных отсутствует!\tСоздаём базу и наполняем данными")
            # Открываем соединение с базой данных
            text = "При отправке сообщения о ТК база данных не найдена("
            self.bot.send_message(newusers.administrator.id, text)
            return

        # Выясняем кому нужно отправить данные
        # Достаём данные по ответственным за ТК из базы данных
        # Открываем соединение с базой данных
        con = sqlite3.connect(pathdatabase)
        request = ('SELECT TransportCompany.Name, TelegramId.idTelegram FROM TransportCompany, TelegramId WHERE TransportCompany.id_responsible=TelegramId.id')
        datesfromdatabase = self.checkdatesfromdatabase(con, request)
        for elem in datesfromdatabase:
            print(f"{type(datesfromdatabase)}{elem}\t{type(elem)}")
        # Закрываем соединение с базой данных
        con.close()

        # Получаем данные для отправки
        for element in range(0, 10):
            # Создаём кнопочки и "плитку"
            markup = telebot.types.InlineKeyboardMarkup()
            # Если заказ уже завершён, пропускаем
            if self.datesformdellin[element]["stateName"] != "Заказ завершен":
                text = "<b>" + str(datesfromdatabase[0][0]) + "\t" + "</b>\n"
                text += "📦  " + str(self.datesformdellin[element]["orderId"]) + "\n"
                text += "                 <b>" + str(self.datesformdellin[element]["stateName"]) + "</b>\n"
                text += "                 " + str(self.datesformdellin[element]["orderDates"]["arrivalToOspReceiver"]) + "\n"
                text += "                 " + str(self.datesformdellin[element]["orderDates"]["warehousing"]) + "\n"
                texturl = "https://www.dellin.ru/cabinet/orders/" + self.datesformdellin[element]["orderId"] + "/"
                button = telebot.types.InlineKeyboardButton("Открыть на сайте", url=texturl)
                markup.add(button)
                # Отправляем данные
                self.bot.send_message(datesfromdatabase[0][1], text, parse_mode="HTML", reply_markup=markup)