from datetime import datetime, timezone, timedelta
import time
from content import goods


def event(user, bot, users):
    if users[user]['animal_feed_time'] != False:
        if users[user]['animal_feed_time'] - 5 * 60 < time.time():
            if users[user]['animal_feed_time'] < time.time():
                users[user][users[user]['animal']] = 0
                users[user]['animal'] = False
                users[user]['animal_feed_time'] = False
                users[user]['animal_farming_timer'] = False
                bot.send_message(user, "Ваши живтные умерли от голода.")
            else:
                time_min = int(users[user]['animal_feed_time'] - time.time()) // 60
                time_sec = int(users[user]['animal_feed_time'] - time.time()) - time_min * 60
                msg = "Ваши животные умрут через {} минут, {} секунд".format(time_min, time_sec)
                users[user]['check'] = bot.send_message(users[user]['id'], msg)
    if users[user]['animal_farming_time'] != False:
        if users[user]['animal_farming_time'] < time.time():
            if users[user]['animal'] == 'chicken':
                users[user]['egg'] += users[user][users[user]['animal']] * users[user]['magic_grib']
                users[user]['animal_farming_timer'] = time.time() + 10*60
            elif users[user]['animal'] == 'cow':
                users[user]['milk'] += users[user][users[user]['animal']] * users[user]['magic_grib']
                users[user]['animal_farming_timer'] = time.time() + 30*60
            elif users[user]['animal'] == 'butterfly':
                users[user]['spark'] += users[user][users[user]['animal']] * users[user]['magic_grib']
                users[user]['animal_farming_timer'] = time.time() + 20*60
            elif users[user]['animal'] == 'sheep':
                users[user]['wool'] += users[user][users[user]['animal']] * users[user]['magic_grib']
                users[user]['animal_farming_timer'] = time.time() + 60*60



def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(
        ['Проверить загоны', 'Покормить животных', 'Прогнать животных', 'Вернуться на ферму'])
    bot.send_message(user['id'],
                     "Вы в амбаре 🐴. У вас есть загоны, в которые можно разместить {} животных. Покупать дополнительные"
                     " загоны можно в магазине.".format(user['paddock']),
                     reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour

'''
def process_message(message, user, bot, helpers, users):
    buttons = ["🐓", "🐂", "🐄", "🐑", 'Вернуться на ферму']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    user["field_animal"] = 0
    if message.text == "🐓":
        user["what_product"] = "🥚"
    if message.text == "🦋":
        user["what_product"] = "✨"
    if message.text == "🐄":
        user["what_product"] = "🥛"
    if message.text == "🐑":
        user["what_product"] = "🦙"
    if message.text == 'Покормить животных 🥕':
        user["carrot"] -= user[goods.animals[message.text][2]]
        user["feed_time"] = time.time()
        bot.send_message(user['id'], "Вы покормили животных")
        #ДОПИСАТЬ ОБНОВЛЕНИЕ ВРЕМЕНИ
    if (user["feed_time"] + user[goods.animals[message.text][3]])< time.time() + 60*60:
        bot.send_message(user['id'], "Животные умерли😭")
        user["animal_condition"] = 0

    if message.text == 'Собрать ресурсы 🥛':
        bot.send_message(user['id'], "Вы собрали ресурсы с животных(??)")
        bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_product"]), reply_markup=keyboard)
        user[goods.products['what_product'][0]] += user['paddock']
       # user["field_animal"] = 0 ИЛИ ДОПИСАТЬ ОБНОВЛЕНИЕ ВРЕМЕНИ
    if message.text == "Проверить загоны 🥅":
        if user["field_animal"] == 0:
            bot.send_message(user['id'], "Ваши загоны пусты")
        else:
            if user["field_animal"] == 1:
                bot.send_message(user['id'], "В ваших загонах есть животные")
'''
def process_message(message, user, bot, helpers, users):
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    if message.text == 'Покормить животных':
        if user['animal'] == 'chicken':
            if user['sunflower'] < user['chicken'] * 10:
                user['sunflower'] -= user['chicken'] * 10
                bot.send_message(user['id'], "Вы успешно покормили куриц, потраив {} подсолнухов".format(user['chicken'] * 10))
                user['animal_feed_time'] = time.time() + goods.animals_2[user['animal'][1]]
                return
            else:
                bot.send_message(user['id'], "Мне не хватает ещё {} подсолнухов".format(user['chicken'] * 10 - user['sunflower']))
                return
        if user['animal'] == 'butterfly':
            if user['tulip'] < user['butterfly'] * 10:
                user['tulip'] -= user['butterfly'] * 10
                bot.send_message(user['id'], "Вы успешно покормили бабочек, потраив {} тюльпанов".format(user['butterfly'] * 10))
                user['animal_feed_time'] = time.time() + goods.animals_2[user['animal'][1]]
                return
            else:
                bot.send_message(user['id'], "Мне не хватает ещё {} тюльпанов".format(user['butterfly'] * 10 - user['tulip']))
                return
        if user['animal'] == 'cow':
            if user['carrot'] < user['cow'] * 10:
                user['carrot'] -= user['cow'] * 10
                bot.send_message(user['id'], "Вы успешно покормили коров, потраив {} морковок".format(user['cow'] * 10))
                user['animal_feed_time'] = time.time() + goods.animals_2[user['animal'][1]]
                return
            else:
                bot.send_message(user['id'], "Мне не хватает ещё {} морковок".format(user['cow'] * 10 - user['carrot']))
                return
        if user['animal'] == 'sheep':
            if user['clover'] < user['sheep'] * 10:
                user['clover'] -= user['sheep'] * 10
                bot.send_message(user['id'], "Вы успешно покормили овец, потраив {} клеверов".format(user['sheep'] * 10))
                user['animal_feed_time'] = time.time() + goods.animals_2[user['animal'][1]]
                return
            else:
                bot.send_message(user['id'], "Мне не хватает ещё {} клеверов".format(user['sheep'] * 10 - user['clover']))
                return
        if user['animal'] == False:
            bot.send_message(user['id'], "У вас нет животных")
        #ДОПИСАТЬ ОБНОВЛЕНИЕ ВРЕМЕНИ
    if message.text == "Проверить загоны":
        if user["animal"] == False:
            bot.send_message(user['id'], "Ваши загоны пусты")
        else:
            time_min = int(user['animal_feed_timer'] - time.time()) // 60
            time_sec = int(user['animal_feed_timer'] - time.time()) - time_min * 60
            time_feed_min = int(user['animal_farming_timer'] - time.time()) // 60
            time_feed_sec = int(user['animal_farming_timer'] - time.time()) - time_feed_min * 60
            msg = "В ваших загонах сидят {} {}. Они дадут ресурсы через {} минут, {} секунд. Их надо будет покормть через {} минут {} секунд".format(user[user['animal']], goods.ru_animals[user['animal']], time_min, time_sec, time_feed_min, time_feed_sec)
            bot.send_message(user['id'], msg)
    if message.text == 'Прогнать животных':
        user[user['animal']] = 0
        user['animal'] = False
        user['animal_farming_timer'] = False
        user['animal_farming_timer'] = False

