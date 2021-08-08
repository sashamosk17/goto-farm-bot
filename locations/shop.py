from telebot import types


def process_message(message, user, bot):
    bot.send_message(user['id'], "Вы в магазине")
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Полочка 'Всё для животных'", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Полочка 'Всё для растений'", callback_data="button2")
    keyboard.add(button1)
    keyboard.add(button2)