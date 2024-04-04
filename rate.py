import os

import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telebot import types

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


# добавление Handler, обрабатывающего команду start, создание меню
@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Respond to a /start message."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("USD/RUB курс")
    btn2 = types.KeyboardButton("EUR/RUB курс")
    btn3 = types.KeyboardButton("CNY/RUB курс")
    btn4 = types.KeyboardButton("Я устал, отправь цитату из аниме")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}!".format(message.from_user),
        reply_markup=markup,
    )


# добавление Handler, который парсит данные о наиболее актуальном курсе USD, EUR, CNY или показывает цитату из аниме по API
@bot.message_handler(content_types=["text"])
def get_fx_rate(message):
    # парсим данные с сайта ЦБ
    url = "https://www.cbr.ru/"
    page = requests.get(url)
    # Текст html страницы
    soup = BeautifulSoup(page.text, "html.parser")
    # находим дату, на которую будут показываться курсы
    all_data = soup.findAll("div", class_="col-md-2 col-xs-7 _right")
    latest_date = all_data[1].text
    # данные по всем валютам:
    all_data_currencies = soup.findAll("div", class_="main-indicator_rate")

    if message.text == "CNY/RUB курс":
        # данные по CNY
        usd_all = all_data_currencies[0]
        # находим наиболее актуальный курс USD
        fx_usd = usd_all.findAll("div", class_="col-md-2 col-xs-9 _right mono-num")
        fx_usd_latest = fx_usd[0].text
        fx_usd_latest = fx_usd_latest.split("₽")[0].strip() + " ₽"
        bot.send_message(
            message.chat.id, text=f"На {latest_date} курс CNY равен {fx_usd_latest}"
        )

    elif message.text == "USD/RUB курс":
        usd_all = all_data_currencies[1]
        # находим наиболее актуальный курс EUR
        fx_usd = usd_all.findAll("div", class_="col-md-2 col-xs-9 _right mono-num")
        fx_usd_latest = fx_usd[0].text
        fx_usd_latest = fx_usd_latest.split("₽")[0].strip() + " ₽"
        bot.send_message(
            message.chat.id, text=f"На {latest_date} курс USD равен {fx_usd_latest}"
        )

    elif message.text == "EUR/RUB курс":
        usd_all = all_data_currencies[2]
        # находим наиболее актуальный курс CNY
        fx_usd = usd_all.findAll("div", class_="col-md-2 col-xs-9 _right mono-num")
        fx_usd_latest = fx_usd[0].text
        fx_usd_latest = fx_usd_latest.split("₽")[0].strip() + " ₽"
        bot.send_message(
            message.chat.id, text=f"На {latest_date} курс EUR равен {fx_usd_latest}"
        )

    elif message.text == "Я устал, отправь цитату из аниме":
        path_link = "https://animechan.vercel.app/api/random"
        response = requests.get(path_link)

        if response.status_code == 200:
            quote = response.json()
            anime_name = quote["anime"]
            anime_quote = quote["quote"]
            bot.send_message(
                message.chat.id, text=f'"{anime_quote}" - цитата из аниме {anime_name}'
            )
        else:
            bot.send_message(message.chat.id, "Извините, наблюдаются проблемы с АPI")


bot.polling(none_stop=True)
