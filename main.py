from projectfiles.functionsforallusers import *
from projectfiles.functionsforadmin import *
from projectfiles.transportscompanys import *


# Токен для связи с ботом
bot = telebot.TeleBot(class_bot.botkey)

# Командa start
@bot.message_handler(commands = ['start', 'Вернуться в начало'])
def start(message):

    # Кнопки
    class buttons:
        btn1 = types.KeyboardButton("⏰Режим работы⏰")
        btn2 = types.KeyboardButton("🖥Наши социальные сети🖥")
        btn3 = types.KeyboardButton("📝Записаться📝")
        btn5 = types.KeyboardButton("📲Ссылки с отзывами📲")
        btn4 = types.KeyboardButton("☎Отредактировать call-центр☎")
        btn6 = types.KeyboardButton("Выяснить id пользователя")
        btn7 = types.KeyboardButton("Выключить Call-центр")
        btn8 = types.KeyboardButton("Перезапуск скрипта")
        btn9 = types.KeyboardButton("Сохранить файл в папку")
        btn10 = types.KeyboardButton("Подписки на ТК")

    # Создание плитки
    class createmarkup:

        # Обьявление переменных
        def __init__(self, message):
            # Определяем тип аккаунта
            self.id = message.chat.id
            # Создаём "плитку"
            self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Создание плитки
        def create(self):
            match self.id:
                # Аккаунты администраторов
                case users.id_administrator | users.id_pushkar | users.id_sekachev:
                    self.markup.add(buttons.btn1, buttons.btn2, buttons.btn5, buttons.btn4, buttons.btn3)
                    self.markup.add(buttons.btn7, buttons.btn8, buttons.btn10, buttons.btn9)
                # Аккаунты менеджеров
                case users.id_peshkov | users.id_zagravskiy | users.id_konovalov | users.id_beregovoy:
                    self.markup.add(buttons.btn1, buttons.btn2, buttons.btn5)
                    self.markup.add(buttons.btn4, buttons.btn7)
                    self.markup.add(buttons.btn9)
                # Аккаунты кладовщиков
                case users.id_ivanov | users.id_kireev:
                    self.markup.add(buttons.btn8, buttons.btn10)
                    self.markup.add(buttons.btn9)
                # Аккаунт технического специалиста
                case users.id_fleysner:
                    self.markup.add(buttons.btn1, buttons.btn2, buttons.btn3)
                    self.markup.add(buttons.btn4, buttons.btn5, buttons.btn6)
                    self.markup.add(buttons.btn7, buttons.btn8, buttons.btn9)
                    self.markup.add(buttons.btn10)
                # Аккаунт клиента
                case _:
                    self.markup.add(buttons.btn1, buttons.btn2, buttons.btn5)
                    self.markup.add(buttons.btn3)
            return self.markup

    markupclass = createmarkup(message)
    markup = markupclass.create()

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
            print(f"{userid.id_6080}\t{type(userid.id_6080)}")
            print(f"{users.administrator['id']}\t{type(users.administrator['id'])}")
            func_not_ready(message, bot)
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
        # Кнопки для кладовщиков
        case "Подписки на ТК":
            subscribetotransportcompany(message, bot)
        # Кнопки для менеджеров
        case "Сохранить файл в папку":
            savefileinfolder2(message, bot)
        case _:
            senderrormessage(message, bot)

# Функция отправки сообщения, что функция пока не реализована
def func_not_ready(message, bot):
    textmessage = "Уважаемый, {0.first_name}!\nЯ бот автотехцента ⚙GlessGroup⚙\nПока эта функция ещё не рализована.\nКак только появится такая возможность, мы всё поправим."
    bot.send_message(message.chat.id, text=textmessage.format(message.from_user))
    start(message)

# Запуск функции опроса данных по ТК
x = class_tk(bot)
t0 = Thread(target=x.startprocessing)
t0.start()

while True:
    try:
        # Запустили постоянный опрос бота Telegram
        bot.polling(none_stop=True, interval=0)

    except Exception as e:
        print(e)
        time.sleep(15)

