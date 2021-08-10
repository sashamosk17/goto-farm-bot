import random
from random import randint
from content.questions import questions
import time

def event(user, bot, helpers):
    print("Event in square")

def welcome(user, bot, helpers):
    bot.send_message(user['id'], "Вы на площади. Тут довольно людно. Слышно, как поёт Ростислав.")

def beds(message, user, bot):
    if message.text == 'Кто-то предлагает купить... грядки?':
        user['width'] += 1


def process_message(message, user, bot, helpers):
    beds(message, user, bot)
    keyboard = helpers.generate_keyboard(['Тут проходит викторина', 'Кто-то предлагает купить... грядки?'])
    bot.send_message(user['id'], 'Вы всё ещё на дееврейской площади.', reply_markup=keyboard)

    if 'current_question' in user:
        if user['current_question']['correct'] == message.text:
            bot.send_message(user['id'], "Верно! Вам начислено 300 монет!")
            user['balance'] += 300
        else:
            bot.send_message(user['id'], "Нет")
        del user['current_question']
    else:
        if "/question" in message.text:
            question = random.choice(questions)
            keyboard = helpers.generate_keyboard(question["answers"])
            bot.send_message(user['id'], question['text'], reply_markup=keyboard)
            user['current_question'] = question