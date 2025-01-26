import json
import time
from json import JSONDecoder
import threading
from datetime import datetime

import telebot
import os
import requests
from dotenv import load_dotenv

from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

users = []

BotToken = os.getenv("TOKEN")
bot = telebot.TeleBot(BotToken)
 
@bot.message_handler(commands=['start'])
def welcome(message):
    global users

    if message.chat.id not in users:
        users.append(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать текущую стоимость")

    markup.add(item1)

    init_thread_loop()
    bot.send_message(message.chat.id, f"Вы подписаны на уведомления об изменении стоимости туров на о. Хайнань в отели \n\nSSAW \n\nPALM BEACH".format(message.from_user, bot.get_me()), parse_mode = 'html',  reply_markup=markup)



@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text == "Узнать текущую стоимость":
        bot.send_message(message.chat.id, 'Загружаем...'.format(message.from_user, bot.get_me()), parse_mode = 'html')

        text = gen_msg()

        bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')



def check_price():
    body = '{"departure":"6","destination":["106"],"adults":"2","children":[],"date":{"from":"13.02.2025","till":"15.02.2025"},"nights":{"from":"7","till":"14"},"stars":[1,2,3,4,5],"hotels":[],"resorts":[],"subResorts":[],"mealType":1,"hotelStatus":false,"minCost":0,"maxCost":99999999,"sourceCurrency":"RUB","offerCurrency":"RUB","source":"search_online_page","cid":1,"page":1,"hotels_count":0,"results_count":0,"firstCoastline":false,"debug":0}'
    response = requests.post('https://search.bankturov.ru/api/v3/search', data=body)
    response = json.loads(response.text)
    hotels = []
    list = response['data']['rows'][:100]
    for obj in list:
        if 'SSAW' in obj['residenses']['hotel_name'] or 'PALM BEACH' in obj['residenses']['hotel_name']:
            hotels.append(obj)

    prices = []
    for obj in hotels:
        val = f"{obj['residenses']['hotel_name']} - {obj['costValues']['RUB']['rounded']}"
        # val = { "name": obj['residenses']['hotel_name'], "price": obj['costValues']['RUB']['rounded'] }
        prices.append(val)

    return prices


def gen_msg():
    prices = check_price()
    text = ''

    for line in prices:
        text = text + line + '\n\n'

    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M")

    return f"❗Обновление от {formatted_datetime} ❗ \n\n {text}."

def timer_loop(interval):
    while True:
        text = gen_msg()

        for usr_id in users:
            bot.send_message(usr_id, text, parse_mode='html')

        time.sleep(interval)

def init_thread_loop():
    interval = 14400  # Интервал в секундах
    thread = threading.Thread(target=timer_loop, args=(interval,))
    thread.daemon = True  # Поток завершится, если основная программа завершится
    thread.start()

# RUN
while True:
    try:
        bot.infinity_polling()
    except:
        continue