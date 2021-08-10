from datetime import datetime, timezone, timedelta
from threading import Thread
import time


def event(user, bot, helpers):
    print("Event in garden")


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей. Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


def select_ovosh(message, user, bot, helpers):
    product = user["height"] * user["width"]
    if message.text == '🥕':
        user["what_plant"] = "🥕"
        bot.send_message(user['id'], ('[🥕]' * user['width'] + "\n") * user['height'])
        user["carrot"] = product
        user["balance"] = user["balance"] - (0 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🥔" and user['balance'] >= 100 * product:
        user["what_plant"] = "🥔"
        bot.send_message(user['id'], ('[🥔]' * user['width'] + "\n") * user['height'])
        user["potato"] = product
        user["balance"] = user["balance"] - (100 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🍆" and user['balance'] >= 500 * product:
        user["what_plant"] = "🍆"
        bot.send_message(user['id'], ('[🍆]' * user['width'] + "\n") * user['height'])
        user["eggplant"] = product
        user["balance"] = user["balance"] - (500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🫑" and user['balance'] >= 1000 * product:
        user["what_plant"] = "🫑"
        bot.send_message(user['id'], ('[🫑]' * user['width'] + "\n") * user['height'])
        user["pepper"] = product
        user["balance"] = user["balance"] - (1000 * user["height"] * user["width"])
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🌶" and user['balance'] >= 1500 * product:
        user["what_plant"] = "🌶"
        bot.send_message(user['id'], ('[🌶]' * user['width'] + "\n") * user['height'])
        user["pepper_hot"] = product
        user["balance"] = user["balance"] - (1500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🍄" and user['balance'] >= 1700 * product:
        user["what_plant"] = "🍄"
        bot.send_message(user['id'], ('[🍄]' * user['width'] + "\n") * user['height'])
        user["mushrooms"] = product
        user["balance"] = user["balance"] - (1700 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    else:
        bot.send_message(user['id'], "Не хватает деняк")
    user["field_condition"] = 1
    print(user["field_condition"])
    bot.send_message(message.chat.id, "Вы вернулись в меню. Напишите команду")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))


def animate(message_id, chat_id, bot, user):
    time.sleep(0.5)

    for i in range(1,11):
        bot.edit_message_text("[ ]\n" * i + user["what_plant"]+"\n" * (11 - i), chat_id, message_id)
        time.sleep(0.5)
    bot.send_message(user['id'], "Ваше поле пустое")


def start(message, user, bot):
    message = bot.send_message(message.chat.id, ("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    print(("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    t = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    t.start()


def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"],
                     ["[", "]"]]
    if message.text == '/plant':
        bot.send_message(user['id'], "Выберите овощ", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda x: select_ovosh(x, user, bot, helpers))
    if message.text == '/gather':
        print(user["field_condition"])
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            bot.send_message(user['id'], "Собираем овощи")
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]))
            start(message, user, bot)
            user["field_condition"] = 0

    if message.text == "/field":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
