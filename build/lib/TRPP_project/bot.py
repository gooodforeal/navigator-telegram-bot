import telebot
from auth_data import TOKEN
from texts import *
from keybords import *
from db import DataBase
from parse import parse
import os


def run_bot(TOKEN):
    '''
    Executes telegram bot

    :param TOKEN: token of telegram bot
    :type TOKEN: str
    :return 0: Zero
    :rtype: int
    '''
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])  # Реакция на команду /start
    def start(message):
        bot.send_message(message.chat.id, msg_greed, parse_mode="html", reply_markup=main_markup)

    @bot.message_handler(content_types=["text"])  # Обработчик текстовых сообщений
    def main_menu(message):
        if message.text == 'Построить маршрут':
            msg = bot.send_message(message.chat.id, ms_route, parse_mode="html")
            bot.register_next_step_handler(msg, build_route)
        elif message.text == 'История':
            db = DataBase()
            lst = db.get_notes_by_user(message.chat.id)
            for line in lst:
                bot.send_message(message.chat.id, line, reply_markup=main_markup)
        else:
            bot.send_message(message.chat.id, text="Неизвестная команда")

    def build_route(message):
        bot.send_message(message.chat.id, "Идет обработка запроса...", parse_mode="html")
        a, b = message.text.split("\n")
        res_dct = parse(a, b)
        mes = f'''
        Расстояние: {res_dct["dist"]}
Время в пути: {res_dct["time"]}
        '''
        bot.send_photo(message.chat.id, photo=open(res_dct["screen"], "rb"), caption=mes, reply_markup=main_markup)
        os.remove(res_dct["screen"])
        user = message.chat.id
        place_from = a
        place_to = b
        db = DataBase()
        db.add_note(user, place_from, place_to)
        msg = bot.send_message(message.chat.id, "Ваш результат готов!", parse_mode="html", reply_markup=main_markup)
        bot.register_next_step_handler(msg, main_menu)

    bot.polling(none_stop=True)
    return 0


if __name__ == "__main__":
    run_bot(TOKEN)
