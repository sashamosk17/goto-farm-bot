from datetime import datetime, timezone, timedelta
import time
from threading import Thread
from content import goods


def event(user, bot, helpers):
    print("Event in garden")


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Посадить овощи', 'Собрать урожай', 'Проверить грядки', 'Вернуться на ферму'])
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей."
                     " Покупать дополнительные грядки можно в магазине.", reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour
def select_ovosh(message, user, bot, helpers):
    buttons = [ 'Вернуться на ферму', 'Склад продуктов']
    keyboard = helpers.generate_keyboard(buttons)
    product = user["height"] * user["width"]
    if message.text in list(goods.vegetables.keys()):
        if goods.vegetables[message.text][1] * product <= user['balance']:
            user["what_plant"] = message.text
            bot.send_message(user['id'], ('[{}]'.format(message.text) * user['width'] + "\n") * user['height'])
            user["plant_time"] = time.time()
            print(user["plant_time"])
            user[goods.vegetables[message.text][0]] = product
            user["balance"] -= (goods.vegetables[message.text][1] * product)
            bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user["balance"]), reply_markup=keyboard)
            user["field_condition"] = 1
            user['grow_time'] = goods.vegetables[message.text][2]
            print(message.id, user['id'])
            '''
            a = Thread(target=animate_of_grow, args=(message.id, bot, user))
            a.start()
            '''
            print(user["field_condition"])
            print(user["what_plant"])
        else:
            bot.send_message(user['id'], "У вас недосаточно деняк")
    else:
        bot.send_message(user['id'], "Эт не оващ")
    bot.register_next_step_handler(message, lambda x: process_message(x, user, bot, helpers))

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

def animate(message_id, chat_id, bot, user):
    time.sleep(0.5)
    for i in range(1, 11):
        bot.edit_message_text("[ ]\n" * i + ("[" + user["what_plant"] + "] " + "\n") * (11 - i), chat_id, message_id)
    time.sleep(0.5)
    '''
    for i in range(1,12):
        #bot.edit_message_text("[ ]\n" * i + ("[" + user["what_plant"] + "] "+"\n") * (11 - i), chat_id, message_id)
        message = bot.send_message(message.chat.id, ("[", user["what_plant"] * user['width'] + "]\n") * user['height'])
        time.sleep(0.5)
    bot.send_message(user['id'], "Ваше поле пустое")
    '''

def start(message, user, bot):
    message = bot.send_message(message.chat.id, ("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    print(("[",user["what_plant"] * user['width'] +"]\n") * user['height'])
    t = Thread(target=animate, args=(message.id, message.chat.id, bot, user))
    t.start()
def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄",'Вернуться на ферму', 'Склад продуктов']
    keyboard = helpers.generate_keyboard(buttons)
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    user["field"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"],
                     ["[", "]"]]
    if message.text == "Склад продуктов":
        bot.send_message(user, "У вас {} морковок\n"
                               "У вас {} картошек\n"
                               "У вас {} баклажанов\n"
                               "У вас {} перчев\n"
                               "У вас {} горячих перцев\n"
                               "У вас {} хрибов\n".format(user["carrot"], user["potato"], user["eggplant"], user["pepper"],
                                                 user["pepper_hot"], user["mushrooms"]))

    if message.text == 'Посадить овощи':
        bot.send_message(user['id'], "Выберите овощ", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda x: select_ovosh(x, user, bot, helpers))
    if message.text == 'Собрать урожай':
        if (time.time() > user["plant_time"] + user["grow_time"] + 60*60):
            bot.send_message(user['id'], "Овоши сгнили")
            return
        if (time.time() - user["plant_time"] < user["grow_time"]):
            bot.send_message(user['id'], "Овоши не созрели. Осталось {} минут".format(int(user["plant_time"]+user["grow_time"] - time.time())//60),  reply_markup=keyboard)
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        elif (time.time()- user["plant_time"] > user["grow_time"] ):
            bot.send_message(user['id'], "Собираем овощи")
            start(message, user, bot)
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]), reply_markup=keyboard)
            user["field_condition"] = 0
    if message.text == "Проверить грядки":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно",)
'''
def process_message(message, user, bot, helpers):
    print(message)
    buttons = ["🥕", "🥔", "🍆", "🫑", "🌶", "🍄"]
    keyboard = helpers.generate_keyboard(buttons)
    user["field_condition"] = 0
    user["field"] = [["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"], ["[", "]"],
                     ["[", "]"]]
    if message.text == '/plant':
        bot.send_message(user['id'], "Выберите овощ", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda x: select_ovosh(x, user, bot, helpers))

    if message.text == '/gather':
        print(user["field_condition"])
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            bot.send_message(user['id'], "Собираем овощи")
            start(message, user, bot)
            bot.send_message(user['id'], "Вы получили {} {}".format(user["height"] * user["width"], user["what_plant"]))
            user["field_condition"] = 0

    if message.text == "/field":
        if user["field_condition"] == 0:
            bot.send_message(user['id'], "Ваше поле пустое")
        else:
            if user["field_condition"] == 1:
                bot.send_message(user['id'], "Ваше поле засеяно")
'''
