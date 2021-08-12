from datetime import datetime, timezone, timedelta
import time
from content import goods
from threading import Thread


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Посадить цветы', 'Собрать цветы', 'Проверить поле',
                                          "Удобрить почву", 'Вернуться на ферму'])
    bot.send_message(user['id'],
                     "Вы в саду 🌼. У вас есть грядки ({}), на которых вы можете выращивать цветы. "
                     "Покупать дополнительные грядки можно в магазине.".format(user['height'] * user['width']),
                     reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


def event(user, bot, helpers):
    print("Event in flowers")


def select_flower(message, user, bot, helpers):
    buttons = ['Вернуться на ферму', 'Назад']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Назад":
        helpers.change_location(user, 'flowers', bot, helpers)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
    product = user["height"] * user["width"]
    if message.text in list(goods.flowers.keys()):
        if goods.flowers[message.text][1] * product <= user['balance']:
            user["what_flower"] = message.text
            user["plantf_time"] = time.time()
            user[goods.flowers[message.text][0]] = product
            user["balance"] -= (goods.flowers[message.text][1] * product)
            bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]),
                             reply_markup=keyboard)
            user["flowers_condition"] = 1
            user["growf_time"] = goods.flowers[message.text][2]
            if user['f_buster']:
                user['growf_time'] *= 0.8
                user['f_buster'] = False
            print(user["flowers_condition"])
            msg = bot.send_message(user['id'], ('[.]' * user['width'] + "\n") * user['height'])
            flowers_animation = Thread(target=animate_of_grow, args=(msg.message_id, user, bot))
            flowers_animation.start()
            helpers.change_location(user, "flowers", bot, helpers)
        else:
            bot.send_message(user['id'], "У вас недосаточно деняк")
    elif user["flowers_condition"] == 1:
        bot.send_message(user['id'], "Ваше поле засажено",
                         reply_markup=keyboard)
    else:
        bot.send_message(user['id'], "У вас недосаточно деняк", reply_markup=keyboard)
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))


def animate(message_id, chat_id, bot, user):
    time.sleep(0.5)
    for i in range(1, 11):
        bot.edit_message_text("[ ]\n" * i + ("[" + user["what_flower"] + "] " + "\n") * (11 - i), chat_id, message_id)
    time.sleep(0.5)

def animate_of_grow(message_id, user, bot):
    time.sleep(user['grow_time'])
    bot.edit_message_text(text=('[{}]'.format(user['what_flower']) * user['width'] + "\n") * user['height'],
                          message_id=message_id, chat_id=user['id'])


def start(message, user, bot):
    message = bot.send_message(message.chat.id, ("[", user["what_flower"] * user['width'] + "]\n") * user['height'])
    print(("[", user["what_flower"] * user['width'] + "]\n") * user['height'])
    t = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    t.start()


def process_message(message, user, bot, helpers, users):
    print(message)
    buttons = ["🌻", "🌷", "☘", "🌹", "🌵", 'Назад']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    if message.text == "Назад":
        helpers.change_location(user, 'flowers', bot, helpers)
    user["flowers"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"]]
    if message.text == "Удобрить почву":
        if not user['f_buster']:
            if user['buster_willingness']:
                if user['flowers_condition'] == 1:
                    bot.send_message(user['id'], "Удобрение нужно сыпать на незасеянную почву")
                    return
                else:
                    user['f_buster'] = True
                    user['buster_willingness'] = False
                    bot.send_message(user['id'], "Теперь поле удобрено")
            else:
                bot.send_message(user['id'], "У вас нет удобрний")
                return
        else:
            bot.send_message(user['id'], "Ваше поля уже удобрено")
            return
    if message.text == 'Посадить цветы':
        bot.send_message(user['id'], "Выберите цвэток", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda x: select_flower(x, user, bot, helpers))
    if message.text == 'Собрать цветы':
        if (time.time() > user["plantf_time"] + user["growf_time"] + 60 * 60):
            bot.send_message(user['id'], "Цветы сгнили :(")
            user["flowers_condition"] = 0
            return
        if (time.time() - user["plantf_time"] < user["growf_time"]):
            get_time(message, user, bot, keyboard)
            # bot.send_message(user['id'], "цветы не созрели. Осталось {} минут".format(int(user["plantf_time"]+user["growf_time"] - time.time())//60),  reply_markup=keyboard)
        if user["flowers_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        elif (time.time() - user["plantf_time"] > user["growf_time"]):
            bot.send_message(user['id'], "Собираем цветы")
            start(message, user, bot)
            bot.send_message(user['id'],
                             "Вы получили {} {}".format(user["height"] * user["width"], user["what_flower"]),
                             reply_markup=keyboard)
            user["flowers_condition"] = 0
    if message.text == "Проверить поле":
        if user["flowers_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
            helpers.change_location(user, "flowers", bot, helpers)
        else:
            get_time(message, user, bot, keyboard)
            helpers.change_location(user, "flowers", bot, helpers)


def get_time(message, user, bot, keyboard):
    needed_time = user["plantf_time"] + user["growf_time"] - time.time()
    minutes = int((user["plantf_time"] + user["growf_time"] - time.time()) / 60)
    seconds = int(needed_time - minutes * 60)
    x = seconds % 10
    if x == 0 or 5 <= x <= 9 or 11 <= seconds % 100 <= 14:
        bot.send_message(user['id'], "Цветы не расцвели. Осталось {} минут, {} секунд".format(minutes, seconds),
                         reply_markup=keyboard)
    elif x == 1:
        bot.send_message(user['id'], "Цветы не расцвели. Осталось {} минут, {} секунда".format(minutes, seconds),
                         reply_markup=keyboard)
    else:
        bot.send_message(user['id'], "Цветы не расцвели. Осталось {} минут, {} секунды".format(minutes, seconds),
                         reply_markup=keyboard)
