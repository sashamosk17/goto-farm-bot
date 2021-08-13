import bank
from content.prices import price_list
import time
from content import goods


def event(user, bot, helpers):
    pass


def welcome(user, bot, helpers):
    bot.send_message(user['id'],
                     "Привет! Это местный магазин. Здесь ты можешь купить животных или семена для растений, "
                     "а также продать овощи или цветы со склада")
    send_menu(user['id'], bot, helpers)


def send_menu(chat_id, bot, helpers):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном",
               "Дверь. Ведёт в подвал. Наверное...", "Продажа", "Вернуться на ферму"]
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
    if message.text == "Кажется, Степан готов расширить загон за скромную сумму 🪚... (3000 монет)":
        if all([user['chicken'], user['butterfly'], user['cow'], user['sheep']]) == 0:
            if user['balance'] >= 3000:
                user['balance'] -= 3000
                user['paddock'] += 1
                bot.send_message(user['id'], "Конгратс! Вы купили 1 загон для животных!")
                user['location'] = 'shop'
            else:
                bot.send_message(user['id'], "У меня нет столько денек")
                user['location'] = 'shop'
        else:
            bot.send_message(user['id'], "Сначала надо опустошить загоны")
    elif message.text == "Купить животинку":
        buttons = list(goods.animals.keys())
        buttons.append("Назад")
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Вы хотите купить...", reply_markup=keyboard)
    elif message.text in list(goods.animals.keys()):
        if user[goods.animals[message.text][0]] < user['paddock']:
            wanted_animals = goods.animals.copy()
            del wanted_animals[message.text]
            wanted_animals = list(wanted_animals.values())
            for i in range(0, len(wanted_animals)):
                wanted_animals[i] = user[wanted_animals[i][0]]
            if any(wanted_animals) > 0:
                bot.send_message(user['id'], "Ваши загоны заполнены другими животными")
            else:
                user[goods.animals[message.text][0]] += 1
                user['animal'] = goods.animals[message.text][0]
                if user[user['animal']] == 1:
                    user['animal_feed_time'] = goods.animals[message.text][2] + time.time()
                    user['animal_farming_time'] = goods.animals[message.text][3] + time.time()
                bot.send_message(user['id'], "Животина успешно куплена")
        else:
            bot.send_message(user['id'], "У вас не хватает загонов")
    elif message.text == "Купить чайный гриб (30000). Увеличивает плодоносность животных в два раза":
        if user['balance'] >= 30000:
            user['magic_grib'] = 2
        else:
            bot.send_message(user['id'], "Нет монет")



def plants(message, user, helpers, bot):
    if message.text == "Купить удобрение (1000 монет)":
        if user['balance'] >= 1000:
            user['balance'] -= 1000
            if user['buster_willingness']:
                bot.send_message(user['id'], "Я купил кучу удобрений! Но она оказалась настолько большой, "
                                             "что её увидел Михаил. Ваши удобрения были съедены, *все*.")
                user['buster_willingness'] = False
            else:
                bot.send_message(user['id'], "Я купил кучу удобрений! Но пока что она небольшая.")
                user['buster_willingness'] = True
            user['location'] = 'shop'
        else:
            bot.send_message(user['id'], "У меня нет столько деньег")
            user['location'] = 'shop'


def process_message(message, user, bot, helpers, users):
    if message.text == "Продажа":
        buttons = list(goods.types_of_goods.keys())
        buttons.append("Назад")
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Вы хотите продать...", reply_markup=keyboard)
    if message.text in list(goods.types_of_goods.keys()):
        buttons = list(goods.types_of_goods[message.text].keys())
        buttons.append("Назад")
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Вы хотите продать...", reply_markup=keyboard)
    if message.text in list(goods.sell_price.keys()):
        if user[goods.sell_price[message.text][0]] > 0:
            user[goods.sell_price[message.text][0]] = 0
            user['balance'] += goods.sell_price[message.text][1]
        else:
            bot.send_message(user['id'], "А продавать-то и нечего")
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
        buttons = ["Кажется, Степан готов расширить загон за скромную сумму 🪚... (3000 монет)", "Купить животинку",
                   "Купить чайный гриб (30000). Увеличивает плодоносность животных в два раза", "Назад"]
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
        bot.send_message(user['id'], "Я попал в казино 🃏🎰🎱 💸 ✅✅✅(@The_Venetian_Casino_bot)")
        user['location'] = 'shop'

