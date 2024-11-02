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
        self.timetoscantk = (today + datetime.timedelta(minutes=1)).strftime("%H:%M")
        # Время отправки сообщений
        self.timetosendmessageresponsible = (today + datetime.timedelta(minutes=2)).strftime("%H:%M")
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
                print("Время сканировать ТК")
                dellin = Thread(target=self.scandatesfromdellin)
                dellin.start()

            # Время для отправки данных отвественному по ТК:
            case self.timetosendmessageresponsible:
                print("Время отправлять данные по ТК")
                sendmessage = Thread(target=self.sendmessageresponsible)
                sendmessage.start()

            # Время которое не выбрано для события
            case default:
                return print("Время сейчас:\t", default)

    # Сканирование данных с ТК "Деловые Линии"
    def scandatesfromdellin(self):
        self.datesformdellin = self.finddataonstite()
        #print(f"\t№\t\t№ накладной\t\t\tСтатус заказа\t\tДата прихода на склад\tДата бесплатного хранения на складе")
        #for element in range(0, 10):
        #    if self.datesformdellin[element]["stateName"] != "Заказ завершен":
        #        print(f"\t{element}\t\t{self.datesformdellin[element]["orderId"]}\t\t{self.datesformdellin[element]["stateName"]}\t\t\t{self.datesformdellin[element]["orderDates"]["arrivalToOspReceiver"]}\t\t\t\t{self.datesformdellin[element]["orderDates"]["warehousing"]}")

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

    # Функция оправки сообщений ответственным лицам
    def sendmessageresponsible(self):
        # Выясняем кому нужно отправить данные

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
            self.bot.send_message(userid.id_6080, text)

        # Достаём данные по ответственным за ТК из базы данных
        '''# Открываем соединение с базой данных
        con = sqlite3.connect(pathdatabase)
        request = ('SELECT TransportCompany.Name, FullName.first_name, FullName.last_name FROM TransportCompany, FullName WHERE TransportCompany.id_responsible=FullName.id UNION SELECT TransportCompany.Name, TransportCompany.id_responsible, TransportCompany.id_responsible FROM TransportCompany WHERE TransportCompany.id_responsible="None"')
            datesfromdatabase = checkdatesfromdatabase(con, request)
            # Закрываем соединение с базой данных
            con.close()
            # Формируем список кнопок с этими ТК, справа должны быть статусы
            # Формируем кнопки
            markup = telebot.types.InlineKeyboardMarkup()
            # Разбираем полученные данные
            for element in datesfromdatabase:
                # Название кнопки отвественного
                name = element[1] + " " + element[2]
                responsiblename = "Отсутствует ответственный"
                btn1 = telebot.types.InlineKeyboardButton(element[0], callback_data="WrongButton")
                # Обработка отсутствие ответственного
                if name == "None None":
                    btn2 = telebot.types.InlineKeyboardButton(responsiblename, callback_data=element[0])
                else:
                    btn2 = telebot.types.InlineKeyboardButton(name, callback_data=element[0])
                markup.row(btn1, btn2)
            # Кнопка выхода в главное меню
            btn3 = telebot.types.InlineKeyboardButton(text="Выйти из меню", callback_data="Break")
            markup.add(btn3)
        '''





        # Получаем данные для отправки
        for element in range(0, 10):
            # Создаём кнопочки и "плитку"
            markup = telebot.types.InlineKeyboardMarkup()
            # Если заказ уже завершён, пропускаем
            if self.datesformdellin[element]["stateName"] != "Заказ завершен":
                text = "📦  " + str(self.datesformdellin[element]["orderId"]) + "\n"
                text += "                 <b>" + str(self.datesformdellin[element]["stateName"]) + "</b>\n"
                text += "                 " + str(self.datesformdellin[element]["orderDates"]["arrivalToOspReceiver"]) + "\n"
                text += "                 " + str(self.datesformdellin[element]["orderDates"]["warehousing"]) + "\n"
                texturl = "https://www.dellin.ru/cabinet/orders/" + self.datesformdellin[element]["orderId"] + "/"
                button = telebot.types.InlineKeyboardButton("Открыть на сайте", url=texturl)
                markup.add(button)
                # Отправляем данные
                self.bot.send_message(userid.id_6080, text, parse_mode="HTML", reply_markup=markup)