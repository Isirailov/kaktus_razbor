import json
from os.path import exists

import telebot
from telebot import types

from parsing import main, today


token = '5870199630:AAEE5EmWgI3Z4tCBZeHCB3ZPKqOTuVIMWzY'

bot = telebot.TeleBot(token)

def get_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    with open(f'new_{today}s.json') as file:
        for number, news in enumerate(json.load(file)):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=news['title'],
                    callback_data=str(number)

                )
            )
    return keyboard



@bot.message_handler(commands=['start'])
def start_bot(message: types.Message):
    if not exists(f'new_{today}s.json'):
        main()
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Новости на сегодня: ', reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda callback: True)
def send_news_detail(callback: types.CallbackQuery):

    with open(f'new_{today}s.json') as file:
        news = json.load(file)[int(callback.data)]
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Ссылка', news['news_link']) 
        keyboard.add(button1)
        text = f"{news['title']}\n\n{news['description']}\n{news['news_link']}"
        bot.send_message(callback.message.chat.id, text=text, reply_markup=keyboard)   
       

bot.polling()


# TODO: поправить создание файла
# TODO: При нажатии на кнопку "Quit" бот должен отправить сообщения "До свидания"