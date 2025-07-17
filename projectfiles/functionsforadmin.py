from projectfiles.dates import *
from telebot import *


import requests
import datetime
import gspread
import subprocess

global oldmessage


# Функция редактирования call-центра
def changecallcener(message, bot):
    # Функция для получения
    def GETrequest(manager, headers):
        request = urlapi + str(manager) + '/agent'
        result = requests.get(request, headers=headers)
        return result
    today = datetime.datetime.today()
    todaytime = today.strftime("%H:%M:%S")
    firstname = message.chat.first_name
    lastname = message.chat.last_name
    print(todaytime, "[", firstname, lastname, "] нажал на кнопку [☎Отредактировать call-центр☎]")
    status = []
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(newusers.names_managers)):
        statusget = GETrequest(newusers.shortnumbers_managers[i], headers)
        # Добавляем статус каждого менеджера в список
        status.append(str(statusget.text)[1:-1])
        # Создаём кнопку имени менеджера
        buttonname = types.InlineKeyboardButton(newusers.names_managers[i], callback_data = "wrongCallBack")
        # Создаём кнопку статуса менеджера
        textfornutton = "🟢 ONLINE 🟢" if (status[i] == "ONLINE") else "🔴 OFFLINE 🔴"
        buttonstatus = types.InlineKeyboardButton(text = textfornutton, callback_data = newusers.names_managers[i])
        # Добавляем кнопки в меню
        markup.add(buttonname, buttonstatus)
    oldmessage = bot.send_message(message.chat.id, "Менеджеры онлайн", reply_markup = markup)
    # Функция изменения в коллцентре
    def callback_change_call_center(usershortnumber, username, bot, call, firstname, lastname, oldmessage, message):
        statusget = str(GETrequest(usershortnumber, headers).text)[1:-1]
        print("Статус менеджера", username, '(', statusget, ") инвертируем")
        test_for_callback = changestatus(statusget, usershortnumber)
        bot.answer_callback_query(call.id, test_for_callback)
        statusget = str(GETrequest(usershortnumber, headers).text)[1:-1]
        logger(firstname, lastname, username, statusget)
        try:
            bot.edit_message_text("Более не актуально", oldmessage.chat.id, oldmessage.message_id)
        except:
            bot.send_message(message.chat.id, "Что то пошло не так( Выберите команду ещё раз")
        finally:
            bot.send_message(message.chat.id, "Выберите команду ещё раз")
    # Фунция отбработки нажания на кнопку
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        match(call.data):
            case newusers.konovalov.name:
                callback_change_call_center(newusers.konovalov.shortnumber, newusers.konovalov.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case newusers.zagravskiy.name:
                callback_change_call_center(newusers.zagravskiy.shortnumber, newusers.zagravskiy.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case newusers.beregovoy.name:
                callback_change_call_center(newusers.beregovoy.shortnumber, newusers.beregovoy.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case newusers.peshkov.name:
                callback_change_call_center(newusers.peshkov.shortnumber, newusers.peshkov.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case newusers.sekachev.name:
                callback_change_call_center(newusers.sekachev.shortnumber, newusers.sekachev.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case newusers.reserved.name:
                callback_change_call_center(newusers.reserved.shortnumber, newusers.reserved.name, bot, call,
                                            firstname, lastname, oldmessage, message)
            case _:
                print("На кнопочку справа!")
                bot.answer_callback_query(call.id, "На кнопочку справа!")

# Функция логгирования действий
def logger(firstname, lastname, name, status):
    # Подключаемся к сервисному аккаунту
    gc = gspread.service_account(CREDENTIALS_FILE)
    # Подключаемся к таблице по ключу таблицы
    table = gc.open_by_key(sheetkey)
    # Открываем нужный лист
    worksheet = table.worksheet("LogsCallCenterBot")
    # Получаем данные с листа
    dates = worksheet.get_values()
    # Получаем номер самой последней строки
    newstr = len(worksheet.col_values(1)) + 1
    # Вычисляем номер строки
    newnumber = newstr - 1
    # Определяем время выполения операции
    today = datetime.datetime.today().strftime("%d.%m.%Y | %H:%M:%S")
    # Формираем данные человека который нажал кнопку
    resultname = firstname + " " + lastname
    # Добавляем строку в конец фаила логгирования
    worksheet.update_cell(newstr, 1, newnumber)
    worksheet.update_cell(newstr, 2, today)
    worksheet.update_cell(newstr, 3, resultname)
    worksheet.update_cell(newstr, 4, name)
    worksheet.update_cell(newstr, 5, status)

# Функция инверсии статуса
def changestatus(statusnow, numbermanager):
    if (statusnow == "OFFLINE"):
        text_for_callback = "Статус " + str(numbermanager) + " изменён на ONLINE"
        urlforapi = urlapi + str(numbermanager) + '/agent'
        requests.put(urlforapi, params = paramsonline, headers = headers)
    else:
        text_for_callback = "Статус " + str(numbermanager) + " изменён на OFFLINE"
        urlforapi = urlapi + str(numbermanager) + '/agent'
        requests.put(urlforapi, params = paramoffline, headers = headers)
    return text_for_callback

# Функция отключения всех в Call центре
def offcallcenter(message, bot):
    today = datetime.datetime.today()
    todaytime = today.strftime("%H:%M:%S")
    print(todaytime, "[", message.chat.first_name, message.chat.last_name, "] нажал на кнопку [Выключить Call-центр]")
    for element in newusers.shortnumbers_managers:
        urlforapi = urlapi + str(element) + '/agent'
        requests.put(urlforapi, params = paramoffline, headers=headers)
    text = "Все телефоны выключены"
    bot.send_message(message.chat.id, text)
    # Подключаемся к сервисному аккаунту
    gc = gspread.service_account(CREDENTIALS_FILE)
    # Подключаемся к таблице по ключу таблицы
    table = gc.open_by_key(sheetkey)
    # Открываем нужный лист
    worksheet = table.worksheet("LogsCallCenterBot")
    # Получаем данные с листа
    dates = worksheet.get_values()
    # Получаем номер самой последней строки
    newstr = len(worksheet.col_values(1)) + 1
    # Вычисляем номер строки
    newnumber = newstr - 1
    # Определяем время выполения операции
    today = datetime.datetime.today().strftime("%d.%m.%Y | %H:%M:%S")
    # Формираем данные человека который нажал кнопку
    resultname = message.chat.first_name + " " + message.chat.last_name
    # Добавляем строку в конец фаила логгирования
    worksheet.update_cell(newstr, 1, newnumber)
    worksheet.update_cell(newstr, 2, today)
    worksheet.update_cell(newstr, 3, resultname)
    worksheet.update_cell(newstr, 4, "ALL")
    worksheet.update_cell(newstr, 5, "OFFLINE")

# Функция перезапуска скрипта uploadfilesonserverglessgroup
def reloadscriptuploadfilesonserverglessgroup(message, bot):
    try:
        subprocess.Popen('Синхронизация файлов GlessGroup и настройка Call-центра.bat')
        text = "Перезапуск программы завершён"
        bot.send_message(message.chat.id, text=text)
    except Exception as e:
        text = "Перезапуск не удался(\nКод ошибки[" + str(e) + "]"
        print(text)
        bot.send_message(message.chat.id, text=text)