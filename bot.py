from config import TOKEN
from telebot import TeleBot
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
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        # Тут расширяем словарь
        users[user_id]['id'] = user_id
        users[user_id]['balance'] = 0
        bot.send_message(user_id, "Привет, {}! Укажи название фермы.".format(str(message.from_user.username)))
        return

    user = users[user_id]

    if "farm_name" not in user:
        user['farm_name'] = message.text
        user['location'] = 'farm'
        bot.send_message(user_id, "История")
    elif "/goto" in message.text:
        cmd, location = message.text.split(" ")
        print(location_manages.keys())
        print(list(location_manages.keys()))
        if location not in list(location_manages.keys()):
            bot.send_message(user['id'], "Нет такой локации")
        else:
            #bot.send_message(user['id'], "hi")
            #bot.send_message(user['id'], "Теперь вы в {}".format(location))
            user['location'] = location
            manager = location_manages[location]
            manager.process_message(message.text, user, bot)
    else:
        location = user['location']
        manager = location_manages[location]
        manager.process_message(message, user, bot)


bot.polling(none_stop=True)
