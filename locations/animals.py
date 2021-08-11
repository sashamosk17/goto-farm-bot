from datetime import datetime, timezone, timedelta
import time


def event(user, bot, helpers):
    print("Event in animals")


def background_events(users, bot, helpers):
    while True:
        for location in helpers.location_managers.values():
            for user in users:
                location.event(user, bot, helpers)
        time.sleep(60)


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Привести животных', 'Собрать ресурсы', 'Покормить животных', 'Прогнать животных', 'Вернуться на ферму'])
    bot.send_message(user['id'],
                     "Вы в амбаре. У вас есть загоны, в которые можно разместить 5 животных. Покупать дополнительные"
                     " загоны можно в магазине.", reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


def process_message(message, user, bot, helpers):
    buttons = ["🐓", "🐂", "🐄", "🐑", 'Вернуться на ферму']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    user["field_animal"] = 0



    if message.text == 'Покормить животных':
        bot.send_message(user['id'], "Вы покормили животных")
        #ДОПИСАТЬ ОБНОВЛЕНИЕ ВРЕМЕНИ
    if message.text == 'Собрать ресурсы':
        bot.send_message(user['id'], "Вы собрали ресурсы с животных(??)")
        for i in range(user["height"]):
            for j in range(user["width"]):
                bot.send_message(user['id'], "Вы получили ", user["height"] * user["width"], user["what_animal"])
       # user["field_animal"] = 0 ИЛИ ДОПИСАТЬ ОБНОВЛЕНИЕ ВРЕМЕНИ
    if message.text == "Проверить загоны":
        if user["field_animal"] == 0:
            bot.send_message(user['id'], "Ваши загоны пусты")
        else:
            if user["field_animal"] == 1:
                bot.send_message(user['id'], "В ваших загонах есть животные")
