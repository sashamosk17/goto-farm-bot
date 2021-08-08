from datetime import datetime, timezone, timedelta

def welcome(user, bot):
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи в огороде, собирать цветы в саду, и разводить скот в загонах для последущей продажи в магазине(/goto shop).Собирайте урожай вовремя, иначе он сгниет, и вы потеряете деньги! Также не забывайте кормить скот, иначе животные умрут голодной смертью! \n"
                     "На огород - /goto garden \n"
                     "В сад - /goto flowers \n"
                     "К животным - /goto animals \n")
    current_time = datetime.now(timezone(timedelta(hours=0.0833)))
    hour = current_time.hour
def process_message(message, user, bot):
    pass


