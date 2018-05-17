answers = {'привет': 'И тебе привет!', 'как дела': 'Лучше всех',
           'пока': 'Увидимся!', 'хорошо': 'Вот и славно!'}
stop_words = ['хорошо', 'пока']


def get_answer(question):
    return answers.get(question.lower(), 'Я могу продолжать это вечно...')


def ask_user():
    while True:
        user_say = input('Как дела?\n').lower()
        answer = get_answer(user_say)
        print(answer)

        if user_say in stop_words:
            break


ask_user()
