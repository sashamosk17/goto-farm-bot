import bank
from content.prices import price_list
import time


def event(user, bot, helpers):
    pass


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Привет! Это местный магазин. Здесь ты можешь купить животных или семена для растений, "
                     "а также продать овощи или цветы со склада")
    send_menu(user['id'], bot, helpers)


def send_menu(chat_id, bot, helpers):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном",
               "Дверь. Ведёт в подвал. Наверное...", "Вернуться на ферму"]
    keyboard = helpers.generate_keyboard(buttons)
    bot.send_message(chat_id, "Вы вошли в магазин", reply_markup=keyboard)


def exchange(message, user, bot):
    for (money, price) in price_list.items():
        if "{} монет в обмен на {} готублей".format(money, price) == message.text:
            answer = bank.ask_money(user['id'], price, "test")

            if not answer:
                bot.send_message(user['id'], 'Ошибка взаимодействия с банком')
            elif answer['state'] == 'error':
                bot.send_message(user['id'], 'Банк вернул ошибку: {}'.format(answer['error']))
            else:
                msg = bot.send_message(user['id'], 'Пришлите код подтверждения:')
                user['transaction_id'] = answer['transaction_id']
                user['asked_money'] = money


def verify_transaction(message, user, bot, helpers):
    try:
        code = int(message.text)
        answer = bank.verify_transaction(user['transaction_id'], code)

        if not answer:
            bot.send_message(user['id'], 'Ошибка взаимодействия с банком')
        elif answer['state'] == 'error':
            bot.send_message(user['id'], 'Банк вернул ошибку: {}'.format(answer['error']))
        else:
            msg = bot.send_message(user['id'], 'Счет пополнен')
            del user['transaction_id']
            user['balance'] += user['asked_money']
    except:
        bot.send_message(user['id'], "Код подтверждения должен быть числом")


def animals(message, user, helpers, bot):
    if message.text == "Тут продаются палки. Сделаю-ка из них загоны (3000 монет)":
        if user['balance'] >= 3000:
            user['balance'] -= 3000
            user['paddock'] += 1
        else:
            bot.send_message(user['id'], "У меня нет столько деняжек")


def plants(message, user, helpers, bot):
    if message.text == "Купить удобрение (1000 монет)":
        if user['balance'] >= 1000:
            user['balance'] -= 1000
            user['plant_buster_willingness'] = True
        else:
            bot.send_message(user['id'], "У меня нет столько деньег")


def process_message(message, user, bot, helpers):
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, 'farm', bot, helpers)
    if message.text == "Назад":
        helpers.change_location(user, 'shop', bot, helpers)
    animals(message, user, helpers, bot)
    plants(message, user, helpers, bot)
    if 'transaction_id' in user:
        verify_transaction(message, user, bot, helpers)
    exchange(message, user, bot)
    if message.text == "Полочка 'Всё для животных'":
        buttons = ["Тут продаются палки. Сделаю-ка из них загоны (1000 монет)", "Назад"]
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Тут всё для животных", reply_markup=keyboard)
    if message.text == "Полочка 'Всё для растений'":
        buttons = ["Купить удобрение (1000 монет)", "Назад"]
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Тут всё для растений", reply_markup=keyboard)
    if message.text == "В углу стоит подозрительный гном":
        buttons = ["1000 монет в обмен на 50 готублей", "3000 монет в обмен на 100 готублей",
                   "7000 монет в обмен на 200 готублей", "18000 монет в обмен на 500 готублей", "Назад"]
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Он предлагает мне мешочек с...", reply_markup=keyboard)
    if "монет в обмен" in message.text:
        exchange(message, user, bot)
    if message.text == "Дверь. Ведёт в подвал. Наверное...":
        bot.send_message(user['id'], "Я попал в казино")
