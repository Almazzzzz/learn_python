answers = { 'привет': 'И тебе привет!', 'как дела': 'Лучше всех', 'пока': 'Увидимся' }

def get_answer(question):
    return answers.get(question.lower(), 'не понял...')

def dialog():
    while True:
        question = input('Чо как? ')
        answer = get_answer(question)
        print(answer)
        if question == 'пока':
            break

dialog()
