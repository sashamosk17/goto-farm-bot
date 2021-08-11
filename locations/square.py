import random
from random import randint
from content.questions import questions
import time


def event(user, bot, helpers):
    print("Event in square")


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Тут проходит викторина',
                                          'Кто-то предлагает купить.. грядки? За 10 000 золотых он продаёт 10 грядок...',
                                          'Вернуться на ферму'])
    bot.send_message(user['id'], "Вы на площади. Тут довольно людно. Слышно, как поёт Ростислав.",
                     reply_markup=keyboard)


def process_message(message, user, bot, helpers):
    if message.text == "Вернуться на ферму":
        helpers.change_location(user, "farm", bot, helpers)
        return
    if 'current_question' in user:
        if user['current_question']['correct'] == message.text:
            bot.send_message(user['id'], "Верно! Вам начислено 30 монет!")
            user['balance'] += 30
            bot.send_message(user['id'], "Ваш баланс составляет {} монет".format(user['balance']))
            helpers.change_location(user, "square", bot, helpers)
        else:
            bot.send_message(user['id'], "Нет")
            helpers.change_location(user, "square", bot, helpers)
        del user['current_question']
    else:
        if "Тут проходит викторина" in message.text:
            question = random.choice(questions)
            keyboard = helpers.generate_keyboard(question["answers"])
            bot.send_message(user['id'], question['text'], reply_markup=keyboard)
            user['current_question'] = question
        if "Кто-то предлагает купить.. грядки? За 10 000 золотых он продаёт 10 грядок..." in message.text:
            if user['balance'] >= 10000:
                user['width'] += 1
                user['balance'] -= 10000
                bot.send_message(user['id'], "Ура! Вы купили 10 грядок для овощей и цветов!!1")
                helpers.change_location(user, "square", bot, helpers)
            else:
                bot.send_message(user['id'], "Не хватает деняк")
