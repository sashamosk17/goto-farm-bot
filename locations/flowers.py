from datetime import datetime, timezone, timedelta
import time


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Посадить цветы', 'Собрать урожай', 'Проверить грядки', 'Вернуться на ферму', 'Склад продуктов'])
    bot.send_message(user['id'],
                     "Вы в саду. У вас есть грядки, на которых вы можете выращивать 10 цветов. "
                     "Покупать дополнительные грядки можно в магазине.", reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


def event(user, bot, helpers):
    print("Event in flowers")


def select_flower(message, user, bot, helpers, goods):
    product = user["height"] * user["width"]
    if message.text in list(goods.flowers.keys()):
        if goods.flowers[message.text][1] * product <= user['balance']:
            user["what_flower"] = message.text
            bot.send_message(user['id'], ('[{}]'.format(message.text) * user['width'] + "\n") * user['height'])
            user[goods.flowers[message.text][0]] = product
            user["balance"] -= (goods.flowers[message.text][1] * product)
            bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]))
            user["flowers_condition"] = 1
            print(user["flowers_condition"])
            helpers.change_location(user, "flowers", bot, helpers)
        else:
            bot.send_message(user['id'], "У вас недосаточно деняк")

    bot.send_message(message.chat.id, "Вы вернулись в меню. Напишите команду.")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))

    '''
    if message.text == '🌻':
        user["what_flower"] = "🌻"
        bot.send_message(user['id'], ('[🌻]' * user['width'] + "\n") * user['height'])
        user["carrot"] = product
        user["balance"] = user["balance"] - (0 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
        user["field_condition_flower"] = 1
    elif message.text == "🌷" and user['balance'] >= 100 * product:
        user["what_flower"] = "🌷"
        bot.send_message(user['id'], ('[🌷]' * user['width'] + "\n") * user['height'])
        user["potato"] = product
        user["balance"] = user["balance"] - (100 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
        user["field_condition_flower"] = 1
    elif message.text == "☘" and user['balance'] >= 500 * product:
        user["what_flower"] = "☘"
        bot.send_message(user['id'], ('[☘]' * user['width'] + "\n") * user['height'])
        user["eggplant"] = product
        user["balance"] = user["balance"] - (500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
        user["field_condition_flower"] = 1
    elif message.text == "🌹" and user['balance'] >= 1000 * product:
        user["what_flower"] = "🌹"
        bot.send_message(user['id'], ('[🌹]' * user['width'] + "\n") * user['height'])
        user["pepper"] = product
        user["balance"] = user["balance"] - (1000 * user["height"] * user["width"])
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
        user["field_condition_flower"] = 1
    elif message.text == "🌵" and user['balance'] >= 1500 * product:
        user["what_flower"] = "🌵"
        bot.send_message(user['id'], ('[🌵]' * user['width'] + "\n") * user['height'])
        user["pepper_hot"] = product
        user["balance"] = user["balance"] - (1500 * product)
        bot.send_message(user['id'], "Ваш баланс {}".format(user["balance"]))
        user["field_condition_flower"] = 1
    else:
        bot.send_message(user['id'], "Не хватает деняк")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))


'''  # Это, наверное, можно удалить, но пока оставлю для back up'a




def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🌻", "🌷", "☘", "🌹", "🌵", 'Вернуться на ферму', 'Склад продуктов']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    user["flowers"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"]]
    if message.text == "Склад продуктов":
        bot.send_message(user, "У вас {} подсолнухов\n"
                               "У вас {} тюльпанов\n"
                               "У вас {} клеверов\n"
                               "У вас {} роз\n"
                               "У вас {} kekтусов\n".format(user["sunflower"], user["tulip"], user["clover"], user["rose"],user["cactus"]))
    if message.text == 'Посадить цветы':
        bot.send_message(user['id'], "Выберите цветок", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda x: select_flower(x, user, bot, helpers))
    if message.text == 'Собрать урожай':
        if user["flowers_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
            helpers.change_location(user, "flowers", bot, helpers)
        else:
            bot.send_message(user['id'], "Собираем цветы")
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_flower"]))
            user["flowers_condition"] = 0
            helpers.change_location(user, "flowers", bot, helpers)
    if message.text == "Проверить грядки":
        if user["flowers_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
            helpers.change_location(user, "flowers", bot, helpers)
        else:
            bot.send_message(user['id'], "Ваше поле засеяно")
            helpers.change_location(user, "flowers", bot, helpers)
