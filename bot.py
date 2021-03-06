import json
import time
from config import TOKEN
from telebot import TeleBot
from threading import Thread
import helpers

bot = TeleBot(TOKEN)

try:
    with open('storage.json', 'r') as file:
        users = json.load(file)
except:
    users = {}



def background_events(users, bot, helpers):
    while True:
        for location in helpers.location_managers.values():
            for user in users:
                location.event(user, bot, users)
        time.sleep(30)



@bot.message_handler(content_types='text')
def process(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        # Тут расширяем словарь
        users[user_id]["plant_time"] = 0
        users[user_id]["what_plant"] = 0
        users[user_id]["plantf_time"] = 0
        users[user_id]["growf_time"] = 0
        users[user_id]["what_flowers"] = 0
        users[user_id]["height"] = 10
        users[user_id]["width"] = 1
        users[user_id]["flowers_condition"] = 0
        users[user_id]["field_condition"] = 0
        users[user_id]["animal_condition"] = 0
        users[user_id]['balance'] = 100000
        users[user_id]['id'] = user_id

        users[user_id]['carrot'] = 0
        users[user_id]['potato'] = 0
        users[user_id]['pepper'] = 0
        users[user_id]['pepper_hot'] = 0
        users[user_id]['mushrooms'] = 0
        users[user_id]['sunflower'] = 0

        users[user_id]['tulip'] = 0
        users[user_id]['shamrock'] = 0
        users[user_id]['rose'] = 0
        users[user_id]['clover'] = 0
        users[user_id]['cactus'] = 0
        users[user_id]['eggplant'] = 0

        users[user_id]['paddock'] = 0
        users[user_id]['chicken'] = 0
        users[user_id]['butterfly'] = 0
        users[user_id]['cow'] = 0
        users[user_id]['sheep'] = 0
        users[user_id]['egg'] = 0
        users[user_id]['spark'] = 0
        users[user_id]['milk'] = 0
        users[user_id]['wool'] = 0
        users[user_id]['buster_willingness'] = False
        users[user_id]['buster'] = False
        users[user_id]['f_buster'] = False

        users[user_id]['animal'] = False
        users[user_id]['animal_feed_time'] = False
        users[user_id]['animal_farming_time'] = False
        users[user_id]['magic_grib'] = 1
        bot.send_message(user_id, "Привет, " + str(message.from_user.username) + "! Укажи название фермы.")

        with open('storage.json', 'w') as file:
            json.dump(users, file)

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
        manager.process_message(message, user, bot, helpers, users)

    with open('storage.json', 'w') as file:
        json.dump(users, file)


background_thread = Thread(target=background_events, args=(users, bot, helpers))
background_thread.start()

bot.polling(none_stop=True)
