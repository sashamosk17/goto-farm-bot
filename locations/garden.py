from datetime import datetime, timezone, timedelta



def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей. Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour

def select_ovosh(message, user, bot, helpers):
    if message.text == '🥕':
        user["what_plant"] = "🥕"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🥕".join(x), user["field"]))))
    elif message.text == "🥔" and user['balance'] >= 100 * user["height"] * user["width"]:
        user["what_plant"] = "🥔"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🥔".join(x), user["field"]))))
    elif message.text == "🍆" and user['balance'] >= 500 * user["height"] * user["width"]:
        user["what_plant"] = "🍆"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🍆".join(x), user["field"]))))
    elif message.text == "🫑" and user['balance'] >= 1000 * user["height"] * user["width"]:
        user["what_plant"] = "🫑"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🫑".join(x), user["field"]))))
    elif message.text == "🌶" and user['balance'] >= 1500 * user["height"] * user["width"]:
        user["what_plant"] = "🌶"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🌶".join(x), user["field"]))))
    elif message.text == "🍄" and user['balance'] >= 1700 * user["height"] * user["width"]:
        user["what_plant"] = "🍄"
        for j in range(user["width"]):
            bot.send_message(user['id'], ('\n'.join(map(lambda x: "🍄".join(x), user["field"]))))
    user["field_condition"] = 1
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
