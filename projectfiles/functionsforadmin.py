from projectfiles.dates import *
from telebot import *


import requests
import datetime
import gspread
import subprocess


# Функция редактирования call-центра
def changecallcener(message, bot):
    today = datetime.datetime.today()
    todaytime = today.strftime("%H:%M:%S")
    firstname = message.chat.first_name
    lastname = message.chat.last_name
    print(todaytime, "[", firstname, lastname, "] нажал на кнопку [☎Отредактировать call-центр☎]")
    index = 0
    status = []
    markup = telebot.types.InlineKeyboardMarkup()
    for i in namesmanagers:
        statusget = requests.get(urlapi + numbermanagers[index] + '/agent', headers=headers)
        # Добавляем статус каждого менеджера в список
        status.append(str(statusget.text)[1:-1])
        # Создаём кнопку имени менеджера
        buttonname = types.InlineKeyboardButton(namesmanagers[index], callback_data = "123")
        # Создаём кнопку статуса менеджера
        buttonstatus = types.InlineKeyboardButton(text = status[index], callback_data = namesmanagers[index])
        # Добавляем кнопки в меню
        markup.add(buttonname, buttonstatus)
        index += 1
    id_message = bot.send_message(message.chat.id, "Менеджеры онлайн", reply_markup = markup)
    print(status)

    # Фунция отбработки нажания на кнопку
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        match(call.data):
            case class_namesmanagers.first:
                statusget = str(requests.get(urlapi + numbermanagers[0] + '/agent', headers=headers).text)[1:-1]
                print("Статус менеджера", class_namesmanagers.first, '(', statusget, ") инвертируем")
                test_for_callback = changestatus(statusget, numbermanagers[0])
                bot.answer_callback_query(call.id, test_for_callback)
                statusget = str(requests.get(urlapi + numbermanagers[0] + '/agent', headers=headers).text)[1:-1]
                logger(firstname, lastname, class_namesmanagers.first, statusget)
            case class_namesmanagers.second:
                statusget = str(requests.get(urlapi + numbermanagers[1] + '/agent', headers=headers).text)[1:-1]
                print("Статус менеджера", class_namesmanagers.second, '(', statusget, ") инвертируем")
                test_for_callback = changestatus(statusget, numbermanagers[1])
                bot.answer_callback_query(call.id, test_for_callback)
                statusget = str(requests.get(urlapi + numbermanagers[1] + '/agent', headers=headers).text)[1:-1]
                logger(firstname, lastname, class_namesmanagers.second, statusget)
            case class_namesmanagers.third:
                statusget = str(requests.get(urlapi + numbermanagers[2] + '/agent', headers=headers).text)[1:-1]
                print("Статус менеджера", class_namesmanagers.third, '(', statusget, ") инвертируем")
                test_for_callback = changestatus(statusget, numbermanagers[2])
                bot.answer_callback_query(call.id, test_for_callback)
                statusget = str(requests.get(urlapi + numbermanagers[2] + '/agent', headers=headers).text)[1:-1]
                logger(firstname, lastname, class_namesmanagers.third, statusget)
            case class_namesmanagers.fourth:
                statusget = str(requests.get(urlapi + numbermanagers[3] + '/agent', headers=headers).text)[1:-1]
                print("Статус менеджера", class_namesmanagers.fourth, '(', statusget, ") инвертируем")
                test_for_callback = changestatus(statusget, numbermanagers[3])
                bot.answer_callback_query(call.id, test_for_callback)
                statusget = str(requests.get(urlapi + numbermanagers[3] + '/agent', headers=headers).text)[1:-1]
                logger(firstname, lastname, class_namesmanagers.fourth, statusget)
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
        text_for_callback = "Статус " + numbermanager + " изменён на ONLINE"
        urlforapi = urlapi + numbermanager + '/agent'
        result = requests.put(urlforapi, params = paramsonline, headers = headers)
    else:
        text_for_callback = "Статус " + numbermanager + " изменён на OFFLINE"
        urlforapi = urlapi + numbermanager + '/agent'
        result = requests.put(urlforapi, params = paramoffline, headers = headers)
    return text_for_callback

# Функция отключения всех в Call центре
def offcallcenter(message, bot):
    today = datetime.datetime.today()
    todaytime = today.strftime("%H:%M:%S")
    print(todaytime, "[", message.chat.first_name, message.chat.last_name, "] нажал на кнопку [Выключить Call-центр]")
    for element in numbermanagers:
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
        #subprocess.Popen([sys.executable ,"C:/Users/Reserved2/Documents/PycharmProjects/BotGless2/Синхронизация файлов GlessGroup и настройка Call-центра.bat"])
        # subprocess.call("C:/Users/Reserved2/Documents/PycharmProjects/uploadfilesonserverglessgroup/main.py", shell=True)
        #exec(open("C:/Users/Reserved2/Documents/PycharmProjects/BotGless2/Синхронизация файлов GlessGroup и настройка Call-центра.bat").read())
        #os.system('start Синхронизация файлов GlessGroup и настройка Call-центра.bat')
        #open('Синхронизация файлов GlessGroup и настройка Call-центра.bat')

        subprocess.Popen('Синхронизация файлов GlessGroup и настройка Call-центра.bat')
        text = "Перезапуск программы завершён"
        bot.send_message(message.chat.id, text=text)
    except Exception as e:
        text = "Перезапуск не удался(\nКод ошибки[" + str(e) + "]"
        print(text)
        bot.send_message(message.chat.id, text=text)

