import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import logging
import re

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

OPERATIONS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}

OPERATORS = ['*', '/', '+', '-']


def main():
    mybot = Updater(config.bot_api_key, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', get_constellation, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', word_count, pass_args=True))
    dp.add_handler(CommandHandler('calc', calculator, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def get_constellation(bot, update, args):
    if args:
        try:
            planet_name = args[0].capitalize()
            planet = getattr(ephem, planet_name)()
            planet.compute()
            constellation = ephem.constellation(planet)
            text = f'{planet_name} сейчас находится ' \
                   f'в созвездии {constellation[-1]}'
        except AttributeError:
            text = 'Такой планеты не существует'
    else:
        text = 'Не указано название планеты'

    print(args)
    update.message.reply_text(text)


def word_count(bot, update, args):
    if args:
        arg = ' '.join(args)
        p = re.compile(r'(^["\'][\w\s"\']+["\']$)')
        if re.search(p, arg):
            args[:] = [x for x in args if not x == '"']
            text = f'Количество слов: {len(args)}'
        else:
            text = 'Строка не соответствует формату ввода'
    else:
        text = 'Вы ввели пустую строку'

    print(args)
    update.message.reply_text(text)


def calculator(bot, update, args):
    if args:
        arg_string = ''.join(args)
        p = re.compile(r'^((0|(0\.\d+)|((0\.)|([1-9]\d*\.)\d+)|([1-9]\d*))'
                       r'[\+\-\*\/])+((0|(0\.\d+)|((0\.)|([1-9]\d*\.)\d+)|'
                       r'([1-9]\d*))\=)$')
        if re.fullmatch(p, arg_string):
            digits_list, operations_list = get_calculation_data(arg_string)
            print(arg_string, digits_list, operations_list)
            try:
                text = calculate(digits_list, operations_list)
            except ZeroDivisionError:
                text = 'На ноль делить нельзя'
        else:
            print(args)
            text = 'Строка не соответствует формату ввода'
    else:
        print(args)
        text = 'Вы ввели пустую строку'

    update.message.reply_text(text)


def get_calculation_data(arg_string):
    digit_split_pattern = re.compile(r'[\+\-\*\/\=]')
    digits_list = re.split(digit_split_pattern, arg_string)
    digits_list = list(filter(None, digits_list))
    digits_list[:] = [to_digits(x) for x in digits_list]
    operations_list = [x for x in arg_string if x in OPERATORS]

    return digits_list, operations_list


def to_digits(string):
    return float(string) if '.' in string else int(string)


def calculate(digits_list, operations_list):
    while operations_list:
        for operator in operations_list:
            i = operations_list.index(operator)
            if operator in ['*', '/']:
                break

        second_number = digits_list.pop(i+1)
        first_number = digits_list.pop(i)
        operation = operations_list.pop(i)
        middle_result = calc(operation, first_number, second_number)
        digits_list.insert(i, middle_result)
        print(middle_result, digits_list, operations_list, first_number,
              operation, second_number)

    return digits_list[0]


def calc(action, x, y):
    return OPERATIONS[action](x, y)


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


main()
