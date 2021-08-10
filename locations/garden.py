from datetime import datetime, timezone, timedelta
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
    if message.text in list(helpers.vegetables.keys()):
            if helpers.vegetables[message.text][1] * product <= user['balance']:
                user["what_plant"] = message.text
                bot.send_message(user['id'], ('[{}]'.format(message.text) * user['width'] + "\n") * user['height'])
                user[helpers.vegetables[message.text][0]] = product
                user["balance"] -= (helpers.vegetables[message.text][1] * product)
                bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]))
                user["field_condition"] = 1
            else:
                bot.send_message(user['id'], "У вас недосаточно деняк")
    '''
    if message.text == '🥕':
        user["what_plant"] = "🥕"
        bot.send_message(user['id'],  ('[🥕]' * user['width'] + "\n") * user['height'])
        user["carrot"] = product
        user["balance"] = user["balance"] - (0 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🥔" and user['balance'] >= 100 * product:
        user["what_plant"] = "🥔"
        bot.send_message(user['id'],  ('[🥔]' * user['width'] + "\n") * user['height'])
        user["potato"] = product
        user["balance"] = user["balance"] - (100 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🍆" and user['balance'] >= 500 * product:
        user["what_plant"] = "🍆"
        bot.send_message(user['id'],  ('[🍆]' * user['width'] + "\n") * user['height'])
        user["eggplant"] = product
        user["balance"] = user["balance"] - (500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🫑" and user['balance'] >= 1000 * product:
        user["what_plant"] = "🫑"
        bot.send_message(user['id'],  ('[🫑]' * user['width'] + "\n") * user['height'])
        user["pepper"] = product
        user["balance"] = user["balance"] - (1000 * user["height"] * user["width"])
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🌶" and user['balance'] >= 1500 * product:
        user["what_plant"] = "🌶"
        bot.send_message(user['id'],  ('[🌶]' * user['width'] + "\n") * user['height'])
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
    '''
    bot.send_message(message.chat.id, "Вы вернулись в меню. Напишите команду")
    bot.register_next_step_handler(message, lambda x:process_message(x,user,bot,helpers))

def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field_condition"] = 0
    user["field"] = [["[","]"], ["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"]]
    if message.text == '/plant':
        bot.send_message(user['id'], "Выберите овощ", reply_markup= keyboard)
        bot.register_next_step_handler(message, lambda x:select_ovosh(x, user, bot, helpers))
    if message.text == '/gather':
        bot.send_message(user['id'], "Собираем овощи")
        bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]))
        user["field_condition"] = 0
    if message.text == "/field":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
