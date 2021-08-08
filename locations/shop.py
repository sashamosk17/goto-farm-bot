from telebot import types
from bot import bot
from helpers import generate_keyboard

def welcome(user, bot):
    pass

def process_message(message, user):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном", "Дверь. Ведёт в подвал. Наверное..."]
    keyboard = generate_keyboard(buttons)

    if message.text == "Полочка 'Всё для животных'":
        pass





