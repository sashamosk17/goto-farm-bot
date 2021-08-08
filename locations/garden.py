from bot import bot
from helpers import generate_keyboard
from bot import users[user.id]
from datetime import datetime, timezone, timedelta
def welcome(user, bot):
    bot.send_message(user['id'],
                     "Вы на огороде. У вас есть грядка на которой вы можете выращивать 10 овощей. Покупать дополнительные грядки можно в магазине.\n"
                     "/goto shop \n"
                     "Чтобы засадить грядки введите /plant")
    current_time = datetime.now(timezone(timedelta(hours=3)))
    hour = current_time.hour
users[user.id]["field"] = 0
bed = 1
height = 10
width = bed
what_plant = "🥕"
def process_message(message, user):
    buttons = ["🥕", "🥔", "🍆", "🫑","🌶","🍄"]
    keyboard = generate_keyboard(buttons)

    if message.text == "🥔" and user['balance'] >= 100*height*width :
        what_plant = "🥔"
    elif message.text == "🍆" and user['balance'] >= 500*height*width:
        what_plant = "🍆"
    elif message.text == "🫑" and user['balance'] >= 1000 * height * width:
        what_plant = "🫑"
    elif message.text == "🌶" and user['balance'] >= 1500 * height * width:
        what_plant = "🌶"
    elif message.text == "🍄" and user['balance'] >= 1700 * height * width:
        what_plant = "🍄"
@bot.message_handler(commands=["plant"])
def plants(user,bot):
    bot.send_message(user['id'],"Выберите овощ")
    for i in range(height):
        for i in range(width):
            bot.send_message(user['id'],"[",what_plant,"]")
    users[user.id]["field"] = 1
@bot.message_handler(commands=["gather"])
def plants(user,bot):
    bot.send_message(user['id'],"Вы получили",height*width,what_plant,sep = " ")
    users[user.id]["field"]= 0

@bot.message_handler(commands=["field"])
def field():
    if users[user.id]["field"] == 0:
        bot.send_message(user['id'], "Ваше поле пустое")
    else:
        pass