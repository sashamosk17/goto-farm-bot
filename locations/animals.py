from datetime import datetime, timezone, timedelta


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Вы в амбаре. У вас есть загоны, в которые можно разместить 5 животных. Покупать дополнительные"
                     " загоны можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы посадить животных в загоны введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour

def process_message(message, user, bot, helpers):
    buttons = ["🐓", "🐂", "🐄", "🐑"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field_animal"] = 0
    if message.text == "🐓" and user['balance'] >= 0 * user["height"]* user["width"]:
        user["what_animal"] = "🐓"
    elif message.text == "🐂" and user['balance'] >= 100 * user["height"]* user["width"]:
        user["what_animal"] = "🐂"
    elif message.text == "🐄" and user['balance'] >= 500 * user["height"] * user["width"]:
        user["what_animal"] = "🐄"
    elif message.text == "🐑" and user['balance'] >= 1000 * user["height"] * user["width"]:
        user["what_animal"] = "🐑"
    if message.text == '/feed':
        bot.send_message(user['id'], "Вы покормили животных")
    if message.text == '/gather':
        bot.send_message(user['id'], "Вы собрали ресурсы с животных(??)")
        for i in range(user["height"]):
            for j in range(user["width"]):
                bot.send_message(user['id'], "Вы получили ", user["height"] * user["width"], user["what_animal"])
        user["field_animal"] = 0
    if message.text == "/field_animal":
        if user["field_animal"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_animal"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
