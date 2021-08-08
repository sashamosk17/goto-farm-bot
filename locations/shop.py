import bank
from helpers import generate_keyboard

def welcome(user, bot):
    pass

def process_message(message, user, bot):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном", "Дверь. Ведёт в подвал. Наверное..."]
    keyboard = generate_keyboard(buttons)

    if message == "Полочка 'Всё для животных'":
        pass
    if message == "Полочка 'Всё для растений'":
        pass
    if message == "В углу стоит подозрительный гном":
        bot.send_message(user['id'], "Он предлагает мне мешочек с...")
        buttons = ["1000 монет в обмен на 50 готублей", "3000 монет в обмен на 120 готублей","5000 монет в обмен на 200 готублей","15000 монет в обмен на 500 готублей", "Назад"]
        keyboard = generate_keyboard(buttons)
        #bank.ask_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, 'Пользователь обменивает готубли на внутреигровую валюту игры"Весёлая ферма: Возрождение"')
        #bank.verify_transaction(НОМЕРСЧЕТАПОКУПАТЕЛЯ, КОДПОДТВЕРЖДЕНИЯ)
        #send_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, "ОПИСАНИЕ ПЕРЕВОДА")
    if message == "Дверь. Ведёт в подвал. Наверное...":
        bot.send_message(user, "Я попал в казино")







