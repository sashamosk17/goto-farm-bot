from telebot import types

def welcome(user, bot):
    pass

def process_message(message, user, bot):
    # bot.send_message(user['id'], "Вы в магазине")
    keyboard = types.InlineKeyboardMarkup()
    animalButton = types.InlineKeyboardButton(text="Полочка 'Всё для животных'", callback_data="animalButton")
    plantsButton = types.InlineKeyboardButton(text="Полочка 'Всё для растений'", callback_data="plantsButton")
    strangeTipButton = types.InlineKeyboardButton(text="В углу стоит подозрительный гном",
                                                  callback_data="strangeTipButton")
    strangeDoorButton = types.InlineKeyboardButton(text="Дверь. Ведёт в подвал. Наверное...",
                                                   callback_data="strangeDoorButton")
    keyboard.add(animalButton)
    keyboard.add(plantsButton)
    keyboard.add(strangeTipButton)
    keyboard.add(strangeDoorButton)
