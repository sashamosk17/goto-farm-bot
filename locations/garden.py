from datetime import datetime, timezone, timedelta
import time
from threading import Thread
from telebot import types
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
    if message.text in list(helpers.vegetables.keys()):
        if helpers.vegetables[message.text][1] * product <= user['balance']:

            user["what_plant"] = message.text
            bot.send_message(user['id'], ('[{}]'.format(message.text) * user['width'] + "\n") * user['height'])
            user[helpers.vegetables[message.text][0]] = product
            user["balance"] -= (helpers.vegetables[message.text][1] * product)
            bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]))
            user["field_condition"] = 1
            print(user["field_condition"])
        else:
            bot.send_message(user['id'], "У вас недосаточно деняк")

    bot.send_message(message.chat.id, "Вы вернулись в меню. Напишите команду.")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))



def animate(message_id, chat_id, bot, user):
    time.sleep(0.5)

    for i in range(1,12):
        bot.edit_message_text("[ ]\n" * i + ("[" + user["what_plant"] + "] "+"\n") * (11 - i), chat_id, message_id)
        time.sleep(0.5)
    bot.send_message(user['id'], "Ваше поле пустое")


def start(message, user, bot):
    message = bot.send_message(message.chat.id, ("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    print(("[",user["what_flower"] * user['width'] +"]\n") * user['height'])
    t = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    t.start()


def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    keyboard = types.InlineKeyboardMarkup()
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
            start(message, user, bot)
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]))
            user["field_condition"] = 0

    if message.text == "/field":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
