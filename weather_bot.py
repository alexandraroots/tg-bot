import json
import os

import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
open_weather_api_key = os.getenv("WEATHER_TOKEN")


@bot.message_handler(commands=["start"])
def start_message(message):
    # пишет стартовое сообщение с именем пользователя
    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.username}! \n\nЯ - погодный бот! \nВведи название города, для которого хочешь узнать погоду  \n",
    )


@bot.message_handler(content_types=["text"])
def get_weather(message):
    # ответ на запрос о погоде
    city = message.text.strip().lower()
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_key}&units=metric"
    )
    if res.status_code == 200:
        data = json.loads(res.text)

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        bot.reply_to(
            message,
            text=f"Сейчас в {city} {weather_description}, \nТемпература воздуха {temp}°С, ощущается как {feels_like}°С.\
                         \nСкорость ветра {wind}м/с.\
                         \nВлажность воздуха составляет {humidity}%.\
                         \nДавление {pressure} мм.рт.ст",
        )
    else:
        bot.send_message(message.chat.id, "Город не найден \U00002620")


bot.polling()
