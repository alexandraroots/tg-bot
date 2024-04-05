import telebot
from telebot import types

from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

QUIZ = [
    {
        "question": "Какой тип данных в Python представляет собой изменяемый список?",
        "options": ["tuple", "dict", "list", "set"],
        "answer": "list",
    },
    {
        "question": "Какая функция используется для вывода данных на экран?",
        "options": ["input", "print", "type", "return"],
        "answer": "print",
    },
    {
        "question": "С помощью какого ключевого слова можно определить функцию в Python?",
        "options": ["def", "function", "lambda", "method"],
        "answer": "def",
    },
    {
        "question": "Какое ключевое слово используется для создания цикла, который выполняется, пока условие истинно?",
        "options": ["for", "while", "loop", "during"],
        "answer": "while",
    },
    {
        "question": "Как называется метод, который добавляет элемент в конец списка?",
        "options": ["push", "append", "insert", "add"],
        "answer": "append",
    },
    {
        "question": "Какой оператор используется для возврата значения из функции?",
        "options": ["return", "yield", "break", "continue"],
        "answer": "return",
    },
    {
        "question": "Какое ключевое слово используется для обработки исключений?",
        "options": ["except", "try", "error", "catch"],
        "answer": "try",
    },
    {
        "question": "Каким методом можно заменить часть строки новым значением?",
        "options": ["substitute", "replace", "change", "swap"],
        "answer": "replace",
    },
    {
        "question": "Какое ключевое слово используется для объявления анонимной функции?",
        "options": ["func", "lambda", "anonymous", "def"],
        "answer": "lambda",
    },
    {
        "question": "Какой метод используется для преобразования строки в нижний регистр?",
        "options": ["downcase", "tolower", "lower", "small"],
        "answer": "lower",
    },
    {
        "question": "Как в Python создать словарь?",
        "options": ["list()", "dict()", "set()", "tuple()"],
        "answer": "dict()",
    },
    {
        "question": "Какой метод позволяет удалить и возвратить последний элемент списка?",
        "options": ["remove", "pop", "delete", "cut"],
        "answer": "pop",
    },
    {
        "question": "Какое ключевое слово используется для создания нового класса?",
        "options": ["class", "struct", "object", "new"],
        "answer": "class",
    },
    {
        "question": "Как в Python проверить, является ли переменная числом?",
        "options": ["isnumeric()", "isdigit()", "isnumber()", "isint()"],
        "answer": "isdigit()",
    },
    {
        "question": "Какой модуль содержит математические функции?",
        "options": ["math", "cmath", "algorithm", "numbers"],
        "answer": "math",
    },
]


user_state = {}


def generate_markup(question):
    markup = types.InlineKeyboardMarkup()
    for option in question["options"]:
        button = types.InlineKeyboardButton(text=option, callback_data=option)
        markup.add(button)
    return markup


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Я викторина Python. Напишите 'викторина' для начала игры."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if message.text.lower() == "викторина":
        user_state[user_id] = 0
        question = get_quiz_question(user_id)
        if question:
            markup = generate_markup(question)
            bot.send_message(message.chat.id, question["question"], reply_markup=markup)
        else:
            bot.reply_to(message, "Извините, викторина закончилась.")
    else:
        bot.reply_to(message, "Напишите 'викторина' для начала игры.")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    question = get_quiz_question(user_id)
    if not question:
        bot.answer_callback_query(call.id, "Викторина закончилась.")
        return

    if call.data == question["answer"]:
        bot.answer_callback_query(call.id, "Верно!")
        user_state[user_id] += 1
        question = get_quiz_question(user_id)
        if question:
            markup = generate_markup(question)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=question["question"],
                reply_markup=markup,
            )
        else:
            bot.send_message(
                call.message.chat.id, "Поздравляю! Вы ответили на все вопросы."
            )
    else:
        bot.answer_callback_query(call.id, "Неверно. Попробуйте еще раз.")


def get_quiz_question(user_id):
    question_index = user_state.get(user_id, 0)
    if question_index < len(QUIZ):
        return QUIZ[question_index]
    else:
        return None


if __name__ == "__main__":
    bot.polling()
