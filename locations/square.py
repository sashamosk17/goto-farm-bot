import random
from content.questions import questions


def event(user, bot, helpers):
    print("Event in square")


def welcome(user, bot, helpers):
    keyboard = helpers.generate_keyboard(['Тут проходит викторина',
                                          'Кто-то предлагает купить.. грядки? За 10 000 золотых он продаёт 10 грядок...',
                                          'Топ игроков (по деньгхам)',
                                          'Вернуться на ферму'])
    bot.send_message(user['id'], "Вы на дееврейской площади. Тут довольно людно. Слышно, как поёт Ростислав.",
                     reply_markup=keyboard)


def process_message(message, user, bot, helpers, users):
    if message.text == 'Топ игроков (по деньгхам)':
        n = 1
        if len(list(users.keys())) >= n:
            top_of_users = []
            real_top_of_users = {}
            for i in range(0, len(list(users.keys()))):
                print(top_of_users)
                top_of_users.append(users[list(users.keys())[i]]['balance'])
                print(top_of_users)
                top_of_users.sort()
                top_of_users.reverse()
                top_of_users = top_of_users
                print(top_of_users)
                for j in range(0, len(top_of_users)):
                    for k in range(0, len(list(users.keys()))):
                        if top_of_users[j] == users[list(users.keys())[k]]['balance']:
                            real_top_of_users[users[list(users.keys())[k]]['farm_name']] = top_of_users[j]
                            print(list(real_top_of_users.keys())[k])
                            print(real_top_of_users[list(real_top_of_users.keys())[k]])
                            bot.send_message(user['id'], str(k+1) + " место: " + str(list(real_top_of_users.keys())[k]) + " " + str(real_top_of_users[list(real_top_of_users.keys())[k]]))
        else:
            bot.send_message(user['id'], "В нашу игру ещё почти никто не играет🙁")

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
                helpers.change_location(user, "square", bot, helpers)
