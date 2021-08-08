from bot import bot
from helpers import generate_keyboard
from datetime import datetime, timezone, timedelta


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей. Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour



def process_message(message, user, bot, helpers):
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field"] = 0
    if message.text == "🥕" and user['balance'] >= 0 * user["height"]* user["width"]:
        user["what_plant"]= "🥕"
    elif message.text == "🥔" and user['balance'] >= 100 * user["height"]* user["width"]:
        user["what_plant"] = "🥔"
    elif message.text == "🍆" and user['balance'] >= 500 * user["height"] * user["width"]:
        user["what_plant"] = "🍆"
    elif message.text == "🫑" and user['balance'] >= 1000 * user["height"] * user["width"]:
        user["what_plant"] = "🫑"
    elif message.text == "🌶" and user['balance'] >= 1500 * user["height"] * user["width"]:
        user["what_plant"] = "🌶"
    elif message.text == "🍄" and user['balance'] >= 1700 * user["height"] * user["width"]:
        user["what_plant"] = "🍄"
    elif message.text == '/plant':
        bot.send_message(user['id'], "Выберите овощ")
        for i in range(user["height"]):
            for j in range(user["width"]):
                bot.send_message(user['id'], "[", user["what_plant"], "]")
        user["field"] = 1
    elif message.text == '/gather':
        bot.send_message(user['id'], "Собираем овощи")
        for i in range(user["height"]):
            for j in range(user["width"]):
                bot.send_message(user['id'], "Вы получили ", user["height"] * user["width"], user["what_plant"])
        user["field"] = 0

@bot.message_handler(commands=["field"])
def field(user, bot):
    if user["field"] == 0:
        bot.send_message(user['id'], "Ваше поле пустое")
    else:
        if user["field"] == 1:
            bot.send_message(user['id'], "Ваше поле засеяно")