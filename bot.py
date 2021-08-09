from config import TOKEN
from telebot import TeleBot
import helpers

bot = TeleBot(TOKEN)
users = {}


@bot.message_handler(content_types='text')
def process(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        #Тут расширяем словарь
        users[user_id]["height"] = 10
        users[user_id]["width"] = 1
        users[user_id]["field"] = 0
        users[user_id]['balance'] = 100000
        users[user_id]['id'] = user_id
        users[user_id]['carrot'] = 0
        users[user_id]['potato'] = 0
        users[user_id]['pepper'] = 0
        users[user_id]['pepper_hot'] = 0
        users[user_id]['mushrooms'] = 0
        users[user_id]['eggplant'] = 0
        bot.send_message(user_id, "Привет, " + str(message.from_user.username) + "! Укажи название фермы.")
        bot.send_message(user_id, "Привет, {}! Укажи название фермы.".format(str(message.from_user.username)))
        return
    
    user = users[user_id]

    if "farm_name" not in user:
        user['farm_name'] = message.text
        user['location'] = 'farm'
        bot.send_message(user_id, "История")
        helpers.change_location(user, "farm", bot, helpers)
    elif "/balance" == message.text:
        bot.send_message(user_id, "Ваш баланс составляет {} монет".format(user['balance']))
    elif "/goto" in message.text:
        cmd, location = message.text.split(" ")

        if location not in list(helpers.location_managers.keys()):
            bot.send_message(user['id'], "Нет такой локации")
        else:
            helpers.change_location(user, location, bot, helpers)
    else:
        location = user['location']
        manager = helpers.location_managers[location]
        manager.process_message(message, user, bot, helpers)

    if message.text == "/storage":
        bot.send_message(user['id'], "У вас морковок {} ".format(user["carrot"]))
        bot.send_message(user['id'], "У вас картошек {} ".format(user["potato"]))
        bot.send_message(user['id'], "У вас баклажанов {} ".format(user["eggplant"]))
        bot.send_message(user['id'], "У вас болгарских перцев {} ".format(user["pepper"]))
        bot.send_message(user['id'], "У вас острых перцев {} ".format(user["pepper_hot"]))
        bot.send_message(user['id'], "У вас грибов {} ".format(user["mushrooms"]))

bot.polling(none_stop=True)