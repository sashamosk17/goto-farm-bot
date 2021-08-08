from datetime import datetime, timezone, timedelta


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей. Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


bed = 1
height = 10
width = bed


def process_message(message, user, bot, helpers):
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field"] = 0

    what_plant = "🥕"

    if message.text == "🥔" and user['balance'] >= 100 * height * width:
        what_plant = "🥔"
    elif message.text == "🍆" and user['balance'] >= 500 * height * width:
        what_plant = "🍆"
    elif message.text == "🫑" and user['balance'] >= 1000 * height * width:
        what_plant = "🫑"
    elif message.text == "🌶" and user['balance'] >= 1500 * height * width:
        what_plant = "🌶"
    elif message.text == "🍄" and user['balance'] >= 1700 * height * width:
        what_plant = "🍄"
    elif message.text == '/plant':
        bot.send_message(user['id'], "Выберите овощ")
        for i in range(height):
            for j in range(width):
                bot.send_message(user['id'], "[", what_plant, "]")
        user["field"] = 1


#
# @bot.message_handler(commands=["plant"])
# def plants(user, bot):
#     bot.send_message(user['id'], "Выберите овощ")
#     for i in range(height):
#         for i in range(width):
#             bot.send_message(user['id'], "[", what_plant, "]")
#     users[user.id]["field"] = 1
#
#
# @bot.message_handler(commands=["gather"])
# def plants(user, bot):
#     bot.send_message(user['id'], "Вы получили", height * width, what_plant, sep=" ")
#     users[user.id]["field"] = 0
#
#
# @bot.message_handler(commands=["field"])
# def field(user, bot):
#     if users[user.id]["field"] == 0:
#         bot.send_message(user['id'], "Ваше поле пустое")
#     else:
#         pass
