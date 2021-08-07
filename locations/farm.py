from bot import bot


def process_message(message, user, bot):
    bot.send_message(user['id'],
                     "Вы на ферме! Здесь можно выращивать овощи а огороде, собирать цветы в саду, и разводить скот в загонах для последущей продажи в магазине(/goto shop). Внимание! Собирайте вовремя урожай, иначе он сгниет, и вы потеряете готубли./n"
                     "огород - /garden /n"
                     "cад - /flowers /n"
                     "загон - /paddock /n")


@bot.message_handler(commands=["garden"])
def repeat_all_messages(message):
    pass
@bot.message_handler(commands=["flowers"])
def repeat_all_messages(message):
    pass
@bot.message_handler(commands=["paddock"])
def repeat_all_messages(message):
    pass
