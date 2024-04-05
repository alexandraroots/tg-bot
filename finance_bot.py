import os

import gspread
import telebot
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Настройка клиента Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "test-bot-419309-fff86c642dd6.json", scope
)
client = gspread.authorize(creds)
sheet = client.open("economics").sheet1


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    # Создание кастомной клавиатуры для команд
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    expense_btn = types.KeyboardButton("Добавить расход")
    income_btn = types.KeyboardButton("Добавить доход")
    report_btn = types.KeyboardButton("Показать отчет")
    markup.add(expense_btn, income_btn, report_btn)
    bot.send_message(
        message.chat.id,
        "Привет! Я помогу тебе отслеживать финансы. Выбери действие на клавиатуре.",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text in ["Добавить расход", "Добавить доход"]
)
def handle_transaction(message):
    command = "/expense" if message.text == "Добавить расход" else "/income"
    msg = bot.send_message(
        message.chat.id,
        f"Введите сумму и описание для {command[1:]} через запятую (например, 500, обед).",
    )
    bot.register_next_step_handler(msg, process_transaction_step, command=command)


def process_transaction_step(message, command):
    try:
        amount, description = message.text.split(", ")
        user_id = message.from_user.id
        row = [user_id, command.strip("/"), amount.strip(), description.strip()]
        sheet.append_row(row)
        bot.send_message(message.chat.id, "Транзакция добавлена!")
    except Exception as e:
        bot.reply_to(
            message, 'Ошибка. Пожалуйста, введите данные в формате "сумма, описание".'
        )


@bot.message_handler(func=lambda message: message.text == "Показать отчет")
def report(message):
    transactions = sheet.get_all_records()
    user_transactions = [
        t for t in transactions if str(t["ID"]) == str(message.from_user.id)
    ]
    if not user_transactions:
        bot.send_message(message.chat.id, "Транзакций не найдено.")
        return
    report_msg = "Отчет за все время:\n"
    for transaction in user_transactions:
        report_msg += f"{transaction['command']}: {transaction['amount']} на {transaction['description']}\n"
    bot.send_message(message.chat.id, report_msg)


bot.infinity_polling()
