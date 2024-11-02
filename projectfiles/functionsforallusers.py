import os
import sqlite3
from time import sleep

from telebot import *
from urllib3 import request

from projectfiles.dates import *
import datetime
import requests

# Функция отправки нашего расписания работы
def timeworking(message, bot):
    time = ['09:00 - 19:00', '09:00 - 19:00', '09:00 - 16:00', '09:00 - 19:00', '09:00 - 19:00', '10:00 - 17:00',
            '10:00 - 15:00']
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    markup = telebot.types.InlineKeyboardMarkup()
    index = 0
    for i in time:
        btn1 = telebot.types.InlineKeyboardButton(days[index], callback_data = 1)
        btn2 = telebot.types.InlineKeyboardButton(time[index], callback_data = 2)
        index += 1
        markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Наш режим работы", reply_markup=markup)

# Функция отправки наших социальных сетей
def socialntworks(message, bot):
    namessocialnetworks = ['📸   Instagram   📸',
                           '🎥   YouTube   🎥',
                           '📱   Vkontakte   📱',
                           '📽   RuTube   📽',
                           '📡   WebSite   📡']
    socialnetworks = ['https://www.instagram.com/glessgroup/',
                      'https://www.youtube.com/c/GLeSSGroup',
                      'https://vk.com/gless_group_omsk',
                      'https://rutube.ru/channel/25007187/',
                      'https://gless.group/']
    index = 0
    markup = telebot.types.InlineKeyboardMarkup()
    for i in socialnetworks:
        button = telebot.types.InlineKeyboardButton(namessocialnetworks[index], url=socialnetworks[index])
        markup.add(button)
        index += 1
    bot.send_message(message.chat.id, "Наши социальные сети", reply_markup=markup)

# Функция отправки ошибки ввода сообещния
def senderrormessage(message, bot):
    text = "Я что-то ничего не понимаю( Кликните по кнопке, пожалуйста."
    bot.send_message(message.chat.id, text)

# Функция отправки ссылок на наши отзывы
def reviews(message, bot):
    reviewsnetworks = ['📸   Flump   📸',
                       '📍   2GIS   📍',
                       '📨   YandexMaps   📨',
                       '🌎   GoogleMaps   🌎']
    socialnetworks = ['http://omsk.flamp.ru/firm/gless_avtotekhcentr-282003257988334',
                      'https://go.2gis.com/xotto',
                      'https://yandex.ru/maps/-/CCUZ4Lc8kB',
                      'https://goo.gl/maps/4CGmYUNVMuh8Md7P8']
    index = 0
    markup = telebot.types.InlineKeyboardMarkup()
    for i in socialnetworks:
        button = telebot.types.InlineKeyboardButton(reviewsnetworks[index], url=socialnetworks[index])
        markup.add(button)
        index += 1
    #bot.send_message(message.chat.id, "Оставьте о нас мнение!", reply_markup=markup)
    text_caption = "🚗 Добрый день, вы обслуживались у нас в  Mazda Gless🚗\n🏠 Лизы Чайкиной, 7 к3🏠\n🤠Оставьте пожалуйста отзыв о нашей работе!🤠"
    bot.send_photo(message.chat.id, photo=open("images/Картинка для поста с отзывами.png", 'rb'), caption=text_caption, reply_markup=markup)

# Функция отправки ссылки с приглашеним в телеграмм канал и отзывами
def channellinkandreviews(message, bot):
    reviewsnetworks = ['💎   Telegram   💎',
                       '📸   Flump   📸',
                       '📍   2GIS   📍',
                       '📨   YandexMaps   📨',
                       '🌎   GoogleMaps   🌎']
    socialnetworks = ['https://t.me/glessgroup',
                      'http://omsk.flamp.ru/firm/gless_avtotekhcentr-282003257988334',
                      'https://go.2gis.com/xotto',
                      'https://yandex.ru/maps/-/CCUZ4Lc8kB',
                      'https://goo.gl/maps/4CGmYUNVMuh8Md7P8']
    index = 0
    markup = telebot.types.InlineKeyboardMarkup()
    for i in socialnetworks:
        button = telebot.types.InlineKeyboardButton(reviewsnetworks[index], url=socialnetworks[index])
        markup.add(button)
        index += 1
    text_caption = "🚗 Добрый день, вы обслуживались у нас в  Mazda Gless. 🚗\n" \
                   "🏠 Лизы Чайкиной, 7 к3. 🏠\n" \
                   "🤠 Оставьте пожалуйста отзыв о нашей работе! 🤠\n" \
                   "📟 Хотим пригласить вас в наш Telegram канал. 📟\n" \
                   "🎥 Полезные видео от профессионалов ремонта. 🎥\n" \
                   "Вопросы, ответы, консультации.\n" \
                   "📞 +7(965)9836080 📞\n" \
                   "🤠 Починим Mazdу в момент! 🤠\n" \
                   "😁 Кстати и запчасти тоже есть! 😁\n" \
                   "Оставьте отзыв о нашей работе! "

    bot.send_photo(message.chat.id, photo=open("images/Картинка для поста с приглашением в telegram.jpg", 'rb'), caption=text_caption, reply_markup=markup)

# Функция отправки id человека
def youid(message, bot):
    text = "Человек : " + str(message.chat.id) + "\n" + str(message.chat.first_name) + " " + str(
        message.chat.last_name) + "\n" + str(message.chat.username)
    text2 = "Написал следующее: " + message.text
    bot.send_message(userid.id_6080, text)
    bot.send_message(userid.id_6080, text2)
    text3 = "Ваш ID: \n" + str(message.chat.id)
    bot.send_message(message.chat.id, text3)

# Функция создания таблиц
def createtables(con):
    # Создаём таблицы
    with con:
        con.execute(
            """
                CREATE TABLE FullName (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT
                );
            """
        ),
        con.execute(
            """
                CREATE TABLE PathFolder (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    path TEXT,
                    id_full_name INTEGER,
                    FOREIGN KEY (id_full_name) REFERENCES FullName(id)
                );
            """
        ),
        con.execute(
            """
                CREATE TABLE TelegramId (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    idTelegram INTEGER,
                    id_full_name INTEGER,
                    FOREIGN KEY (id_full_name) REFERENCES FullName(id)
                );
            """
        ),
        con.execute(
            """
                CREATE TABLE ShortNumber (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Number INTEGER,
                    id_full_name INTEGER,
                    FOREIGN KEY (id_full_name) REFERENCES FullName(id)
                );
            """
        ),
        con.execute(
            """
                CREATE TABLE TransportCompany (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    id_responsible INTEGER,
                    FOREIGN KEY (id_responsible) REFERENCES FullName(id)
                );
            """
        ),

# Функция заполнения таблиц
def insertdatesintables(con, nametable, data):
    match (nametable):
        case "FullName":
            for element in data:
                mass = element.split()
                request = """ INSERT INTO FullName (first_name, last_name) VALUES (?, ?);"""
                paramsrequest = (mass[0], mass[1])
                # Вставляем данные в таблицы
                with con:
                    con.execute(request, paramsrequest)
            print("\tТаблица FullName заполнена успешно")
        case "PathFolder":
            index = 0
            for element in data:
                index += 1
                request = """ INSERT INTO PathFolder (path, id_full_name) VALUES (?, ?);"""
                paramsrequest = (element, index)
                # Вставляем данные в таблицы
                with con:
                    con.execute(request, paramsrequest)
            print("\tТаблица PathFolder заполнена успешно")
        case "TelegramId":
            index = 0
            for element in data:
                index += 1
                request = """ INSERT INTO TelegramId (idTelegram, id_full_name) VALUES (?, ?);"""
                paramsrequest = (element, index)
                # Вставляем данные в таблицы
                with con:
                    con.execute(request, paramsrequest)
            print("\tТаблица TelegramId заполнена успешно")
        case "ShortNumber":
            index = 0
            for element in data:
                index += 1
                request = """ INSERT INTO ShortNumber (Number, id_full_name) VALUES (?, ?);"""
                paramsrequest = (element, index)
                # Вставляем данные в таблицы
                with con:
                    con.execute(request, paramsrequest)
            print("\tТаблица ShortNumber заполнена успешно")

        case "TransportCompany":
            index = 0
            masstk = [transport_companies.dellin, transport_companies.nrg_tk, transport_companies.pecom, transport_companies.cdek]
            for element in data:
                request = """ INSERT INTO TransportCompany (Name, id_responsible) VALUES (?, ?);"""
                paramsrequest = (element, 'None')
                # Вставляем данные в таблицы
                with con:
                    con.execute(request, paramsrequest)
            print("\tТаблица TransportCompany заполнена успешно")
        case _:
            print("Неверное имя таблицы")

# Функция проверки данных в таблице
def checkdatesfromdatabase(con, request):
    #print("Проверка вводимых значений")
    with con:
        cursor = con.cursor()
        cursor.execute(request)
        result = cursor.fetchall()
        #for element in result:
        #    print(element)
    return result

# Функция вставки первичных данных в базу
def insertfirstdatesintables(con):
    # Функция заполнения таблицы FullName
    insertdatesintables(con, 'FullName', Workers)
    # Функция заполнения таблицы PathFolder
    insertdatesintables(con, 'PathFolder', [class_pathmanagers.admin, class_pathmanagers.fleysner,
                                            class_pathmanagers.beregovoy, class_pathmanagers.konovalov,
                                            class_pathmanagers.zagravskiy, class_pathmanagers.pushkar,
                                            class_pathmanagers.peshkov])
    # Функция заполнения таблицы TelegramId
    insertdatesintables(con, 'TelegramId', [userid.id_6080, userid.id_fleysner, userid.id_beregovoy,
                                            userid.id_konovalov, userid.id_zagravskiy,
                                            userid.id_pushkar, userid.id_pushkar])
    # Функция заполнения таблицы ShortNumber
    insertdatesintables(con, 'ShortNumber', [class_shortnumbersworkers.admin, class_shortnumbersworkers.fleysner,
                                             class_shortnumbersworkers.beregovoy, class_shortnumbersworkers.konovalov,
                                             class_shortnumbersworkers.zagravskiy, class_shortnumbersworkers.pushkar,
                                             class_shortnumbersworkers.peshkov])
    # Функция заполнения таблицы TransportCompany
    insertdatesintables(con, 'TransportCompany', [transport_companies.dellin, transport_companies.nrg_tk,
                                             transport_companies.pecom, transport_companies.cdek])

# Функция записи на обслуживание
def serviserecord(message, bot):
    # Выяснение даты и времени обращения
    today = datetime.datetime.today()
    todaytime = today.strftime("%H:%M:%S")

    print(f"Дата и время обращения: {todaytime}")

    if os.path.exists(pathdatabase) == True:
        os.remove(pathdatabase)

    # Создаём таблицы
    # Открываем соединение с базой данных
    con = sqlite3.connect(pathdatabase)
    # Функция создания таблиц
    createtables(con)
    # Закрываем соединение с базой данных
    con.close()

    # Заполняем таблицы
    # Открываем соединение с базой данных
    con = sqlite3.connect(pathdatabase)
    # Функция вставки первичных данных в базу
    insertfirstdatesintables(con)

    # Функция проверки данных на вставку
    request = 'SELECT FullName.id, FullName.first_name, FullName.last_name, PathFolder.path, ShortNumber.Number, TelegramId.idTelegram FROM FullName, PathFolder, ShortNumber, TelegramId WHERE FullName.id = PathFolder.id_full_name AND FullName.id = ShortNumber.id_full_name AND FullName.id = TelegramId.id_full_name'
    massdates = checkdatesfromdatabase(con, request)
    # Закрываем соединение с базой данных
    con.close()

    # Количество менеджеров онлайн
    countonlinemanagers = 0
    # Выбираем рандомного менеджера, которому упадёт заявка
    for element in massdates:
        statusget = requests.get(urlapi + str(element[4]) + '/agent', headers=headers).text
        if statusget == '"ONLINE"':
            countonlinemanagers += 1

        print(f"====>{element[1]} {element[2]}\t{statusget}\t{countonlinemanagers}")
    numbermanagerforrequest = random.randint(0, countonlinemanagers)
    print(f"{numbermanagerforrequest}")
    print("Вашей заявкой займётся: ", massdates[numbermanagerforrequest][1])


    #msg = bot.send_message(message.chat.id, "Выберите тему обращения.")
    #markup = telebot.types.InlineKeyboardMarkup()
    #listid = [userid.id_beregovoy, userid.id_konovalov, userid.id_zagravskiy]
    #listnames = [class_namesmanagers.second, class_namesmanagers.third, class_namesmanagers.first]
    #randommanager = random.randint(0, len(listid) - 1)
    #textmessage = todaytime + " [" + message.chat.first_name + " " + message.chat.last_name + "] нажал на кнопку [📝Записаться📝]  перевожу заявку на " + listnames[randommanager] + " ( " + str(listid[randommanager]) + " )"
    #print(textmessage)
    #bot.send_message(userid.id_6080, textmessage)

# Функция скачивания файлов в папки менеджеров
def savefileinfolder2(message, bot, path):
    # Информация о фаиле
    file_id_info = bot.get_file(message.document.file_id)
    #print(file_id_info)
    # Сохраняем фаил
    downloaded_file = bot.download_file(file_id_info.file_path)
    #print(downloaded_file)
    # Название фаила
    file_name = message.document.file_name
    #print(file_name)
    mass = file_name.split(".")
    # Генерируем новое название фаила
    today = datetime.datetime.today().strftime("%d.%m.%Y.") + mass[1]
    #print(today)
    # Путь по которому сохраняем фаил
    src = path + today
    #print(src)
    # Скачиваем фаил
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        # Создаём кнопочки и "плитку"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/start"))
    text = "Фаил сохранён в папку:\n!папка для фаилов из telegram\n В твоей личной папке на сетевом диске"
    bot.send_message(message.chat.id, text, reply_markup=markup)

# Функция подписки на транспортные компании
def subscribetotransportcompany(message, bot):
    print(f"Функция подписки на ТК")

    # Выяснием id человека
    id_sotr = message.chat.id
    print(f"Сотрудник с id: {id_sotr}")

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
        con = sqlite3.connect(pathdatabase)
        # Функция создания таблиц
        createtables(con)
        # Функция наполнения её первичными данными
        insertfirstdatesintables(con)
        # Закрываем соединение с базой данных
        con.close()

    # Достаём данные по всем доступным ТК из базы данных
    # Открываем соединение с базой данных
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
    btn3 = telebot.types.InlineKeyboardButton(text = "Выйти из меню", callback_data = "Break")
    markup.add(btn3)

    old_message = bot.send_message(message.chat.id, "Список ТК", reply_markup=markup)
    print(f"ID old message: {old_message.message_id}")
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        match (call.data):
            case transport_companies.dellin:
                bot.send_message(call.message.chat.id, 'Обновляем данные по ' + transport_companies.dellin + ".")
                changedatesindatabase(id_sotr, transport_companies.dellin, bot, message)
            case transport_companies.nrg_tk:
                bot.send_message(call.message.chat.id, 'Обновляем данные по ' + transport_companies.nrg_tk + ".")
                changedatesindatabase(id_sotr, transport_companies.nrg_tk, bot, message)
            case transport_companies.pecom:
                bot.send_message(call.message.chat.id, 'Обновляем данные по ' + transport_companies.pecom + ".")
                changedatesindatabase(id_sotr, transport_companies.pecom, bot, message)
            case transport_companies.cdek:
                bot.send_message(call.message.chat.id, 'Обновляем данные по ' + transport_companies.cdek + ".")
                changedatesindatabase(id_sotr, transport_companies.cdek, bot, message)
            # Обработка кнопки удаления таблички
            case "Break":
                bot.delete_message(old_message.chat.id, old_message.message_id)
            # Обработка неверной кнопочки
            case _:
                print("На кнопочку справа!")
                bot.answer_callback_query(call.id, "На кнопочку справа!")

# Функция изменения данных в базе данных
def changedatesindatabase(id_responsible, tk_name, bot, message):
    try:
        # Открываем соединение с базой данных
        con = sqlite3.connect(pathdatabase)
        # Выясняем id человека в базе данных
        request = 'SELECT id FROM TelegramId WHERE idTelegram = ' + str(id_responsible)
        id_responsible_in_database = checkdatesfromdatabase(con, request)[0][0]
        #print(f"{id_responsible}\t\t{tk_name}\n{request}\n{id_responsible_in_database}")

        # Выясняем id транспортной компании
        request = 'SELECT id FROM TransportCompany WHERE Name = "' + str(tk_name) + '"'
        id_tk_in_database = checkdatesfromdatabase(con, request)[0][0]
        #print(f"{id_responsible}\t\t{tk_name}\n{request}\n{id_tk_in_database}")

        # Проверка на подписку на эту ТК
        request = 'SELECT id_responsible FROM TransportCompany WHERE Name = "' + str(tk_name) + '"'
        id_oldresponsible_in_database = checkdatesfromdatabase(con, request)[0][0]
        #print(f"{id_responsible}\t\t{tk_name}\n{request}\n{id_responsible_in_database}\t{id_tk_in_database}\t{id_oldresponsible_in_database}")
        if id_oldresponsible_in_database == id_responsible_in_database:
            bot.send_message(message.chat.id, "Ты уже и так отвественный по этой ТК")
            #print(f"\t\t{id_responsible_in_database} равен {id_oldresponsible_in_database}. Зачем будем обновлять?")
        else:
            # Обновляем данные по транспортной компании
            request = 'UPDATE TransportCompany SET id_responsible = ' + str(id_responsible_in_database) + ' WHERE id = ' + str(id_tk_in_database)
            checkdatesfromdatabase(con, request)
            bot.send_message(message.chat.id, "Вроде всё получилось")

        # Закрываем соединение с базой данных
        con.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Чот сломалось(\nПерешли это сообщение, пожалуйста.\n{e}")