from bot import bot
from datetime import datetime, timezone, timedelta

def welcome(user, bot):
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи а огороде, собирать цветы в саду, и разводить скот в загонах для последущей продажи в магазине(/goto shop). Внимание! Собирайте вовремя урожай, иначе он сгниет, и вы потеряете готубли.\n"
                     "огород - /goto garden \n"
                     "cад - /goto flowers \n"
                     "загон - /goto paddock \n")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour
def process_message(message, user, bot):
    pass


