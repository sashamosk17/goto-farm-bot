from telebot import types
from locations import farm,square,shop,garden,flowers,animals

location_managers = {
    "farm": farm,
    "square": square,
    "shop": shop,
    "garden": garden,
    "flowers": flowers,
    "animals": animals
}


def generate_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for button in buttons:
        keyboard.add(types.KeyboardButton(text=button))

    return keyboard


def change_location(user, location, bot, helpers):
    user['location'] = location
    manager = location_managers[location]
    manager.welcome(user, bot, helpers)
