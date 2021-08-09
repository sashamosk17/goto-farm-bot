import bank

def welcome(user, bot, helpers):
    bot.send_message(user['id'], "Привет! Это местный магазин. Здесь ты можешь купить животных или семена для растений, а также продать овощи или цветы со склада")

def send_menu(chat_id, bot, helpers):
    buttons = ["Полочка 'Всё для животных'", "Полочка 'Всё для растений'", "В углу стоит подозрительный гном",
               "Дверь. Ведёт в подвал. Наверное..."]
    keyboard = helpers.generate_keyboard(buttons)
    bot.send_message(chat_id, "Вы вошли в магазин", reply_markup=keyboard)

def exchange(message, user, bot):
    if "{} монет в обмен на {} готублей".format() == message:
        bot.send_message(user['id'], 'Введите "/donate "НОМЕР_СЧЁТА"" без внутренних каывчек')
        user['gived_money'] = int(message.split()[2])
        user['wanted_money'] = int(message.split()[0])
    if "/donate" in message:
        user['nomer_shota'] = message.split(' ')[1]
        donate_text = "Пользователь поукпает внутреигровую (Весёлая ферма:Возрождение) валюту за {} готублей".format(str(user['wanted_money']))
        bank.ask_money(user['nomer_shota'], user['gived_money'], "test", )
        bot.send_message(user['id'], 'Введите "/verify_donate "КОД_ПОДТВЕРЖДЕНИЯ"" без внутренних кавычек')
    if "/verify_donate" in message:
        print(user['balance'])
        bank.verify_transaction(user['nomer_shota'], message.split[1])
        user['balance'] += user['wanted_money']
        print(user['balance'])

def process_message(message, user, bot, helpers):
    send_menu(user['id'], bot, helpers)
    exchange(message, user, bot)
    if message == "Полочка 'Всё для животных'":
        pass
    if message == "Полочка 'Всё для растений'":
        pass
    if message == "В углу стоит подозрительный гном":
        buttons = ["1000 монет в обмен на 50 готублей", "3000 монет в обмен на 120 готублей","5000 монет в обмен на 199 готублей","15000 монет в обмен на 400 готублей", "Назад"]
        keyboard = helpers.generate_keyboard(buttons)
        bot.send_message(user['id'], "Он предлагает мне мешочек с...", reply_markup=keyboard)
        #bank.ask_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, 'Пользователь обменивает готубли на внутреигровую валюту игры"Весёлая ферма: Возрождение"')
        #bank.verify_transaction(НОМЕРСЧЕТАПОКУПАТЕЛЯ, КОДПОДТВЕРЖДЕНИЯ)
        #send_money(НОМЕР СЧЕТА ПОКУПАТЕЛЯ, СУММА, "ОПИСАНИЕ ПЕРЕВОДА")
    if message == "Дверь. Ведёт в подвал. Наверное...":
        bot.send_message(user, "Я попал в казино")