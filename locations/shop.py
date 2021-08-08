import bank
from helpers import generate_keyboard

def welcome(user, bot):
    bot.send_message(user['id'], "Привет! Это местный магазин. Здесь ты можешь купить животных или семена для растений, а также продать овощи или цветы со склада")

def send_menu(chat_id, bot):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном",
               "Дверь. Ведёт в подвал. Наверное..."]
    keyboard = generate_keyboard(buttons)
    bot.send_message(chat_id, "Чего хотите?", reply_markup=keyboard)

def process_message(message, user, bot):
    send_menu(user['id'], bot)

    if message == "Полочка 'Всё для животных'":
        pass
    if message == "Полочка 'Всё для растений'":
        pass
    if message == "В углу стоит подозрительный гном":
        bot.send_message(user['id'], "Он предлагает мне мешочек с...")
        buttons = ["1000 монет в обмен на 50 готублей", "3000 монет в обмен на 120 готублей","5000 монет в обмен на 200 готублей","15000 монет в обмен на 400 готублей", "Назад"]
        keyboard = generate_keyboard(buttons)
        #bank.ask_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, 'Пользователь обменивает готубли на внутреигровую валюту игры"Весёлая ферма: Возрождение"')
        #bank.verify_transaction(НОМЕРСЧЕТАПОКУПАТЕЛЯ, КОДПОДТВЕРЖДЕНИЯ)
        #send_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, "ОПИСАНИЕ ПЕРЕВОДА")
    if message == "Дверь. Ведёт в подвал. Наверное...":
        bot.send_message(user, "Я попал в казино")







