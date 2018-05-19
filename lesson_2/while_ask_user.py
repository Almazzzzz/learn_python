def ask_user():
    while True:
        user_say = input('Как дела?\n')
        if user_say.lower() == 'хорошо':
            print('Вот и славно!')
            break
        else:
            print('Я могу продолжать это вечно...')


ask_user()
