from datetime import datetime, timezone, timedelta
import time
from threading import Thread
from content import goods


def event(user, bot, helpers):
    print("Event in garden")
    '''
    if (time.time() > user["plant_time"] + user["grow_time"] + 60 * 50):
        bot.send_message(user['id'], "Овощи сгниют через 10 минут")
    '''

def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(
        ['Посадить овощи', 'Собрать урожай', 'Проверить грядки', "Удобрить почву", 'Вернуться на ферму'])
    bot.send_message(user['id'],
                     "Вы на огороде 🌽. У вас есть грядки ({}), на которых вы можете выращивать овощи."
                     " Покупать дополнительные грядки можно на площади.".format(user['height'] * user['width']),
                     reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour


def select_ovosh(message, user, bot, helpers, users):
    buttons = ['Вернуться на ферму', 'Назад']
    keyboard = helpers.generate_keyboard(buttons)
    product = user["height"] * user["width"]
    if message.text == "Назад":
        helpers.change_location(user, 'garden', bot, helpers)
        return
    if message.text in list(goods.vegetables.keys()):
        if user["field_condition"] == 0:
            if goods.vegetables[message.text][1] * product <= user['balance']:
                user["what_plant"] = message.text
                bot.send_message(user['id'], ('[{}]'.format(message.text) * user['width'] + "\n") * user['height'])
                user["plant_time"] = time.time()
                user[goods.vegetables[message.text][0]] = product
                user["balance"] -= (goods.vegetables[message.text][1] * product)
                bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]),
                                 reply_markup=keyboard)
                user["field_condition"] = 1
                user['grow_time'] = goods.vegetables[message.text][2]
                if user['buster']:
                    user['grow_time'] *= 0.8
                    user['buster'] = False

                a = Thread(target=animate_of_grow, args=(message.id, bot, user))
                a.start()

            else:
                bot.send_message(user['id'], "У вас недосаточно деняк")
    else:
        bot.send_message(user['id'], "Эт не оващ")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers, users))


def animate_of_grow(message_id, user, bot):
    time.sleep(user['grow_time'])
    bot.edit_message_text(text=('[{}]'.format(user['what_plant']) * user['width'] + "\n") * user['height'],
                          message_id=message_id, chat_id=user['id'])



def start_grow(message, user, bot):
    message = bot.send_message(message.chat.id, ("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    print(("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    a = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    a.start_grow()



def animate(message_id, chat_id, bot, user):
    time.sleep(1)
    for i in range(1, 11):
        bot.edit_message_text("[ ]\n" * i + ("[" + user["what_plant"] + "] " + "\n") * (user['width'] + 1 - i)* user["height"], chat_id, message_id)
    time.sleep(1)


def start(message, user, bot):
    message = bot.send_message(message.chat.id, ("[", user["what_plant"] * user['width'] + "]\n") * user['height'])
    t = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    t.start()


def process_message(message, user, bot, helpers, users):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄", 'Назад']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    if message.text == "Назад":
        helpers.change_location(user, 'garden', bot, helpers)
    user["field"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"],
                     ["[", "]"]]
    if message.text == "Удобрить почву":
        if not user['buster']:
            if user['buster_willingness']:
                if user['field_condition'] == 1:
                    bot.send_message(user['id'], "Удобрение нужно сыпать на незасеянную почву")
                    return
                else:
                    user['buster'] = True
                    user['buster_willingness'] = False
                    bot.send_message(user['id'], "Теперь грядки удобрены")
            else:
                bot.send_message(user['id'], "У вас нет удобрний")
                return
        else:
            bot.send_message(user['id'], "Ваши грядки уже удобрены")
            return
    if message.text == "Склад продуктов":
        bot.send_message(user, "У вас {} морковок\n"
                               "У вас {} картошек\n"
                               "У вас {} баклажанов\n"
                               "У вас {} перчев\n"
                               "У вас {} горячих перцев\n"
                               "У вас {} хрибов\n".format(user["carrot"], user["potato"], user["eggplant"],
                                                          user["pepper"],
                                                          user["pepper_hot"], user["mushrooms"]))

    if message.text == 'Посадить овощи':
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Выберите овощ", reply_markup=keyboard)
            bot.register_next_step_handler(message, lambda x: select_ovosh(x, user, bot, helpers, users))
        else:
            bot.send_message(user['id'], "Ваши грядки уже засеяны")
    if message.text == 'Собрать урожай':
        if (time.time() > user["plant_time"] + (user["grow_time"]/2) and time.time()< user["plant_time"] + user["grow_time"]):
            bot.send_message(user['id'], "Овощи растут")
            bot.send_message(user['id'], ('[🌱]'.format(message.text) * user['width'] + "\n") * user['height'])
        if (time.time() > user["plant_time"] + user["grow_time"] + 60 * 60):
            bot.send_message(user['id'], "Овощи сгнили")
            bot.send_message(user['id'], ('[💩]'.format(message.text) * user['width'] + "\n") * user['height'])
            return
        if (time.time() - user["plant_time"] < user["grow_time"]):
            get_time(message, user, bot, keyboard)
            bot.send_message(user['id'], ('[.]'.format(message.text) * user['width'] + "\n") * user['height'])
            # bot.send_message(user['id'], "Овощи не созрели. Осталось {} минут".format(int(user["plant_time"]+user["grow_time"] - time.time())//60),  reply_markup=keyboard)
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваши грядки пусты")
        elif (time.time() - user["plant_time"] > user["grow_time"]):
            bot.send_message(user['id'], "Собираем овошчи")
            start(message, user, bot)
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]))
            user["field_condition"] = 0
    if message.text == "Проверить грядки":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваши грядки пусты")
        else:
            if user["field_condition"] == 1:
                get_time(message, user, bot, keyboard)


def get_time(message, user, bot, keyboard):
    needed_time = user["plant_time"] + user["grow_time"] - time.time()
    minutes = int((user["plant_time"] + user["grow_time"] - time.time()) / 60)
    seconds = int(needed_time - minutes * 60)
    x = seconds % 10
    if x == 0 or 5 <= x <= 9 or 11 <= seconds % 100 <= 14:
        bot.send_message(user['id'], "Овощи не созрели. Осталось {} минут, {} секунд".format(minutes, seconds))
    elif x == 1:
        bot.send_message(user['id'], "Овощи не созрели. Осталось {} минут, {} секунда".format(minutes, seconds))
    else:
        bot.send_message(user['id'], "Овощи не созрели. Осталось {} минут, {} секунды".format(minutes, seconds))

'''
def animate_of_grow(message_id,chat_id,user,bot):
    time.sleep(1)
    #bot.edit_message_text(text='[.]\n' * 10, chat_id=user['id'], message_id=message_id)
    #bot.edit_message_text('.\n' * 10, user['id'], message_id)
    time.sleep(user['grow_time'])
    for i in range(10):
        bot.edit_message_text(text='[' + user['what_plant'] + '\n', chat_id=user['id'], message_id=message_id)
    del user['grow_time']
def start_grow(message, user, bot):
    message = bot.send_message(message.chat.id, ("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    print(("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    a = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    a.start_grow()
'''