from config import TOKEN
from telebot import TeleBot
from telebot import types
from locations import farm, shop, square

bot = TeleBot(TOKEN)

users = {}

location_manages = {
    "farm": farm,
    "square": square,
    "shop": shop
}

@bot.message_handler(content_types='text')
def process(message):
    message.chat.id
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        #Тут расширяем словарь
        users[user_id]['id'] = user_id
        bot.send_message(user_id, "Привет, " + str(message.from_user.username) + "! Укажи название фермы.")
        return
    
    user = users[user_id]
    
    if "farm_name" not in user:
        user['farm_name'] = message.text
        user['location'] = 'farm'
        bot.send_message(user_id, "Тут будет история про ферму от дедушки.")
    elif "/goto" in message.text:
        cmd, location = message.text.split(" ")

        if location not in ["farm", "shop", "square"]:
            bot.send_message(user['id'], "Нет такой локации")
        else:
            bot.send_message(user['id'], "Теперь вы в {}".format(location))
            user['location'] = location
            #for i in user['buttons']:
            #    types.ReplyKeyboardRemove(i)

    else:
        location = user['location']
        manager = location_manages[location]
        manager.process_message(message, user, bot)

bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass
    '''
    if call.message:
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "Вы нажали на первую кнопку.")
        if call.data == "button2":
            bot.send_message(call.message.chat.id, "Вы нажали на вторую кнопку.")
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "Вы нажали на первую кнопку.")
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "Вы нажали на первую кнопку.")
    '''
bot.polling(none_stop=True)