import telebot

class LeftMenu:
    def __init__(self, bot):
        self.bot = bot

    def initmenu(self):
        self.bot.set_my_commands([
            telebot.types.BotCommand('/start', 'Главное меню')
        ])