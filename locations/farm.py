from datetime import datetime, timezone, timedelta

def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['На огород', 'В сад', 'К животным', 'Пойти в магазин', 'Пойти на площадь'])
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи в огороде, собирать цветы в саду, "
                     "и разводить скот в загонах для последущей продажи в магазине(/goto shop). "
                     "Собирайте урожай вовремя, иначе он сгниет, и вы потеряете деньги!"
                     "Также не забывайте кормить скот, иначе животные умрут голодной смертью!",
                     reply_markup=keyboard)
    current_time = datetime.now(timezone(timedelta(hours=0.0833)))
    hour = current_time.hour


def process_message(message, user, bot, helpers):
    if message.text == "На огород":
        helpers.change_location(user, "garden", bot, helpers)
