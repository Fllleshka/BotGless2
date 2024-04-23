from projectfiles.functionsforallusers import *
from projectfiles.functionsforadmin import *

# Токен для связи с ботом
bot = telebot.TeleBot(botkey)

# Командa start
@bot.message_handler(commands = ['start', 'Вернуться в начало'])
def start(message):
    # Создаём кнопочки и "плитку"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Кнопки для клиентов
    btn1 = types.KeyboardButton("⏰Режим работы⏰")
    btn2 = types.KeyboardButton("🖥Наши социальные сети🖥")
    btn3 = types.KeyboardButton("📝Записаться📝")
    btn5 = types.KeyboardButton("📲Ссылки с отзывами📲")
    btn10 = types.KeyboardButton("📱Ссылка с TG и отзывами📱")
    # Кнопки для администратора
    btn4 = types.KeyboardButton("☎Отредактировать call-центр☎")
    btn6 = types.KeyboardButton("Выяснить id пользователя")
    btn7 = types.KeyboardButton("Выключить Call-центр")
    btn8 = types.KeyboardButton("Перезапуск скрипта")
    btn9 = types.KeyboardButton("Сохранить файл в папку")
    # Общие кнопки

    # Определяем тип аккаунта
    id = message.chat.id
    match id:
        # Аккаунта администратора
        case userid.id_6080:
            markup.add(btn1, btn2, btn3, btn4, btn5, btn10, btn7, btn8, btn9)
        # Аккаунт программиста
        case userid.id_fleysner:
            markup.add(btn5, btn4, btn7, btn8)
        # Аккаунты менеджеров
        case userid.id_beregovoy | userid.id_konovalov | userid.id_zagravskiy | userid.id_peshkov:
            markup.add(btn1, btn2, btn5, btn4, btn9)
        # Аккаунт технического специалиста
        case userid.id_pushkar:
            markup.add(btn3, btn5, btn4, btn7, btn8)
        # Аккаунт клиента
        case _:
            markup.add(btn1, btn2, btn3, btn5, btn6)

    # Отравляем первое приветственное сообщение
    textmessage = "Привет, {0.first_name}!\nЯ бот автотехцента ⚙GlessGroup⚙\nЧем я могу вам помочь?"
    bot.send_message(message.chat.id,
                     text = textmessage.format(message.from_user),
                     reply_markup=markup)

# Команды по кнопкам в чате
@bot.message_handler(content_types= ['text'])
def textmessage(message):
    match(message.text):
        # Кнопки для клиентов
        case "⏰Режим работы⏰":
            timeworking(message, bot)
        case "🖥Наши социальные сети🖥":
            socialntworks(message, bot)
        case "📝Записаться📝":
            #pass
            serviserecord(message, bot)
        case "📱Ссылка с TG и отзывами📱":
            channellinkandreviews(message, bot)
        case "📲Ссылки с отзывами📲":
            reviews(message, bot)
        case "Выяснить id пользователя":
            youid(message, bot)
        # Кнопки для администратора
        case "☎Отредактировать call-центр☎":
            changecallcener(message, bot)
        case "Выключить Call-центр":
            offcallcenter(message, bot)
        case "Перезапуск скрипта":
            reloadscriptuploadfilesonserverglessgroup(message, bot)
        # Кнопки для менеджеров
        case "Сохранить файл в папку":
            savefileinfolder(message, bot)
        case _:
            senderrormessage(message, bot)

# Функция сохраниения фаилов в папки менеджеров
def savefileinfolder(message, bot):
    match message.chat.id:
        case userid.id_konovalov:
            bot.send_message(message.chat.id, "Готов к приёму файлов", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, savefileinfolder2, bot, class_pathmanagers.konovalov)
        case userid.id_zagravskiy:
            bot.send_message(message.chat.id, "Готов к приёму файлов", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, savefileinfolder2, bot, class_pathmanagers.zagravskiy)
        case userid.id_beregovoy:
            bot.send_message(message.chat.id, "Готов к приёму файлов", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, savefileinfolder2, bot, class_pathmanagers.beregovoy)
        case _:
            text = "Вы не имеете доступа к данной функции"
            print(text)
            bot.send_message(message.chat.id, text)

# Класс времён
class times:
    today = datetime.datetime.today()
    timetoScan = today.strftime("%H:%M")

while True:
    try:
        # Запустили постоянный опрос бота Telegram
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)