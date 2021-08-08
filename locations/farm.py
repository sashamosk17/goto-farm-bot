from bot import bot
from datetime import datetime, timezone, timedelta
from bot import location_manages
from bot import users


def welcome(user, bot):
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи а огороде, собирать цветы в саду, и разводить скот в загонах для последущей продажи в магазине(/goto shop). Внимание! Собирайте вовремя урожай, иначе он сгниет, и вы потеряете готубли.\n"
                     "огород - /goto garden \n"
                     "cад - /goto flowers \n"
                     "загон - /goto paddock \n")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour
@bot.message_handler(content_types='text')
def process(message):
    user_id = message.chat.id
    user = users[user_id]
    if "/goto" in message.text:
        cmd, location = message.text.split(" ")
        if location not in [location_manages.keys()]:
            bot.send_message(user['id'], "Нет такой локации")
        else:
            # bot.send_message(user['id'], "Теперь вы в {}".format(location))
            user['location'] = location
            manager = location_manages[location]
            manager.welcome(user, bot)
    else:
        location = user['location']
        manager = location_manages[location]
        manager.process_message(message, user, bot)


def process_message(message, user, bot):
    pass


