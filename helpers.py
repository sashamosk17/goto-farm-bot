from telebot import types
from locations import farm, square, shop, garden, flowers, animals

location_managers = {
    "farm": farm,
    "square": square,
    "shop": shop,
    "garden": garden,
    "flowers": flowers,
    "animals": animals
}

vegetables = {
    "🥕": ['carrot', 0],
    "🥔": ['potato', 300],
    "🍆": ['eggplant', 500],
    "🫑": ['pepper', 700],
    "🌶": ['hot_pepper', 1000],
    "🍄": ['mushrooms', 1500]
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
