from telebot import types

def generate_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for button in buttons:
        keyboard.add(types.KeyboardButton(text=button))

    return keyboard



