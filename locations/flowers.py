from datetime import datetime, timezone, timedelta
import time

def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы в саду. У вас есть грядки, на которых вы можете выращивать 10 цветов. "
                     "Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour

def event(user, bot, helpers):
    print("Event in flowers")

def select_flower(message, user, bot, helpers):
    product = user["height"] * user["width"]
    if message.text == '🌻':
        user["what_flower"] = "🌻"
        bot.send_message(user['id'], ('[🌻]' * user['width'] + "\n") * user['height'])
        user["carrot"] = product
        user["balance"] = user["balance"] - (0 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🌷" and user['balance'] >= 100 * product:
        user["what_flower"] = "🌷"
        bot.send_message(user['id'], ('[🌷]' * user['width'] + "\n") * user['height'])
        user["potato"] = product
        user["balance"] = user["balance"] - (100 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "☘" and user['balance'] >= 500 * product:
        user["what_flower"] = "☘"
        bot.send_message(user['id'], ('[☘]' * user['width'] + "\n") * user['height'])
        user["eggplant"] = product
        user["balance"] = user["balance"] - (500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🍀" and user['balance'] >= 1000 * product:
        user["what_flower"] = "🍀"
        bot.send_message(user['id'], ('[🍀]' * user['width'] + "\n") * user['height'])
        user["pepper"] = product
        user["balance"] = user["balance"] - (1000 * user["height"] * user["width"])
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    elif message.text == "🌵" and user['balance'] >= 1500 * product:
        user["what_flower"] = "🌵"
        bot.send_message(user['id'], ('[🌵]' * user['width'] + "\n") * user['height'])
        user["pepper_hot"] = product
        user["balance"] = user["balance"] - (1500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
    else:
        bot.send_message(user['id'], "Не хватает деняк")
    user["field_condition_flower"] = 1
    bot.send_message(message.chat.id, "Вы вернулись в меню. Напишите команду")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))

def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🌻", "🌷", "☘", "🍀", "🌵"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field_condition_flower"] = 0
    user["field"] = [["[","]"], ["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"],["[","]"]]
    if message.text == '/plant':
        bot.send_message(user['id'], "Выберите цветок", reply_markup= keyboard)
        bot.register_next_step_handler(message, lambda x: select_flower(x, user, bot, helpers))
    if message.text == '/gather':
        bot.send_message(user['id'], "Собираем цветы")
        bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_flower"]))
        user["field_condition_flower"] = 0
    if message.text == "/field":
        if user["field_condition_flower"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition_flower"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
