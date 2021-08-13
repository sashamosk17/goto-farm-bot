from datetime import datetime, timezone, timedelta


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(
        ['На огород', 'В сад', 'К животным', 'Пойти в магазин', 'Пойти на площадь', 'Посмотреть баланс',
         'Склад'])  # ДОПИЛИТЬ ЖИВОТНЫХ
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи в огороде, собирать цветы в саду, "
                     "и разводить скот в загонах для последущей продажи в магазине. "
                     "Собирайте урожай вовремя, иначе он сгниет, и вы потеряете деньги! "
                     "Также не забывайте кормить скот, иначе животные умрут голодной смертью!",
                     reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=0.0833)))
    hour = current_time.hour


def process_message(message, user, bot, helpers, users):
    if message.text == "На огород":
        helpers.change_location(user, "garden", bot, helpers)
        return
    if message.text == "В сад":
        helpers.change_location(user, "flowers", bot, helpers)
        return
    if message.text == "К животным":
        helpers.change_location(user, "animals", bot, helpers)
        return
    if message.text == "Пойти в магазин":
        helpers.change_location(user, "shop", bot, helpers)
        return
    if message.text == "Пойти на площадь":
        helpers.change_location(user, "square", bot, helpers)
        return
    if message.text == "Посмотреть баланс":
        bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user['balance']))
    if message.text == "Склад":
        storage_template = '''
У вас: 
🥕 морковок {} 
🥔 картошек {} 
🍆 баклажанов {}
🫑 болгарских перцев {} 
🌶 острых перцев {}
🍄 грибов {}
🌻 подсолнухов {}
🌷 тюльпанов {}
☘ клевера {}
🌹 роз {}
🌵 кактуса{}
🥚 яиц {}
✨ пыльцы {}
🥛 молока {}
🦙 мотков шерсти {}
        '''
        bot.send_message(user['id'],
                         storage_template.format(user["carrot"], user["potato"], user["eggplant"],
                                                 user["pepper"], user["pepper_hot"], user["mushrooms"],
                                                 user["sunflower"], user["tulip"], user["clover"],
                                                 user["rose"], user["cactus"], user["egg"],
                                                 user["spark"], user["milk"], user["wool"]))


def event(user, bot, helpers):
    print("Event in farm")
