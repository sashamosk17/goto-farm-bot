import random
from random import randint
from content.questions import questions


def welcome(user, bot, helpers):
    bot.send_message(user['id'], "Вы на площади")


def process_message(message, user, bot, helpers):
    #    bot.send_message(user['id'], "Вы на площади")

    if 'current_question' in user:
        if user['current_question']['correct'] == message.text:
            bot.send_message(user['id'], "Верно! Вам начислено 300 монет!")
            user['balance'] += 300
        else:
            bot.send_message(user['id'], "Нет")
        del user['current_question']
    else:
        if "/anek" in message.text:
            bot.send_message(user['id'], get_anek())
        if "/question" in message.text:
            question = random.choice(questions)
            keyboard = helpers.generate_keyboard(question["answers"])
            bot.send_message(user['id'], question['text'], reply_markup=keyboard)
            user['current_question'] = question


def get_anek():
    anek = {
        1: "Залез сын на меня как на лошадку и говорит — поехали. Я ему объясняю надо говорить Но!, чтобы лошадка поехала, и Тпруу, чтобы остановилась. Он говорит Но! и я начинаю изображать скачку. 1,2-5 минут, начинаю уставать. Говорю ему: Скажи тпруу!. Он отвечает: — Зачем? Мне ещё долго ехать.",
        2: "Умная, воспитанная, интеллигентная, вроде даже добрая! Но, блин, как сажусь с ребенком за уроки, как будто два срока отмотала.",
        3: "Я видел, как друг со своей женой ссорился: она беснуется, орёт, машет руками... Илюха спокойно достал телефон и стал снимать. Через некоторое время Лиза это увидела и — мол, чё за фигня? А он, красавчик: Это когда я дождливым вечером буду сидеть один и думать, почему я с тобой развёлся, а потом включу видео и такой: а, не, всё правильно! Ни разу не видел, чтоб женщины так быстро успокаивались.",
        4: "Не удивлюсь, если в доме начальника ГИБДД Москвы найдут Янтарную комнату.",
        5: "Странная у меня работа. Спрашивают как с умного, платят как дебилу.",
        7: "Пуля, попавшая в школьного учителя, вышла и зашла как положено.",
        8: "",

    }
    a = randint(1, 15)
    return anek[a]
