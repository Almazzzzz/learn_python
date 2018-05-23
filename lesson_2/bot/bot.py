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

DICT = {'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
        'шесть': 6, 'семь': 7, 'восемь': 7, 'девять': 9, 'десять': 10,
        'умножить': '*', 'разделить': '/', 'плюс': '+', 'минус': '-',
        'и': '.', 'на': ''}

CALCULATION_DATA = {
    'number': lambda arg_string, args:
        get_numbers_calculation_data(arg_string),
    'text': lambda arg_string, args: get_text_calculation_data(args)
}


def main():
    my_bot = Updater(config.bot_api_key, request_kwargs=PROXY)

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', get_constellation, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', word_count, pass_args=True))
    dp.add_handler(CommandHandler('calc', numbers_calculator, pass_args=True))
    dp.add_handler(CommandHandler('text_calc',
                                  text_calculator,
                                  pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    my_bot.start_polling()
    my_bot.idle()


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


def numbers_calculator(bot, update, args):
    if args:
        arg_string = ''.join(args)
        p = re.compile(r'^((0|(0\.\d+)|((0\.)|([1-9]\d*\.)\d+)|([1-9]\d*))'
                       r'[\+\-\*\/])+((0|(0\.\d+)|((0\.)|([1-9]\d*\.)\d+)|'
                       r'([1-9]\d*))\=)$')
        text = calculator_body(p, args, arg_string, 'number')
        print(text)
    else:
        print(args)
        text = 'Вы ввели пустую строку'

    update.message.reply_text(text)


def text_calculator(bot, update, args):
    if args:
        args[:] = [x.lower() for x in args]
        arg_string = ' '.join(args)
        p = re.compile(r'^[а-я]+(\sи\s[а-я]+)?(\s[а-я]+(\sна)?\s[а-я]+'
                       r'(\sи\s[а-я]+)?)+')
        text = calculator_body(p, args, arg_string, 'text')
        print(text)
    else:
        print(args)
        text = 'Вы ввели пустую строку'

    update.message.reply_text(text)


def calculator_body(p, args, arg_string, calc_type):
    if re.fullmatch(p, arg_string):
        digits_list, operations_list = get_calculation_data(calc_type,
                                                            arg_string,
                                                            args)
        if not digits_list or not operations_list:
            print(arg_string, digits_list, operations_list)
            return 'Строка не соответствует формату ввода'
        try:
            text = calculate(digits_list, operations_list)
        except ZeroDivisionError:
            text = 'На ноль делить нельзя'
    else:
        print(args)
        text = 'Строка не соответствует формату ввода'

    return text


def get_calculation_data(calc_type, arg_string, args):
    return CALCULATION_DATA[calc_type](arg_string, args)


def get_numbers_calculation_data(arg_string):
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


def get_text_calculation_data(args):
    digits_list, operations_list = [], []
    for a in args:
        arg = DICT.get(a, None)
        if arg is not None:
            if isinstance(arg, int) or arg == '.':
                digits_list.append(arg)
            elif isinstance(arg, str):
                operations_list.append(arg)
        else:
            return [], []

    operations_list = list(filter(None, operations_list))
    digits_list[:] = [str(x) for x in digits_list]

    while '.' in digits_list:
        i = digits_list.index('.')
        string = ''.join(digits_list[i - 1:i + 2])
        print(string)
        digits_list[i - 1:i + 2] = [string, '', '']
    digits_list = list(filter(None, digits_list))
    digits_list[:] = [to_digits(x) for x in digits_list]

    return digits_list, operations_list


def calc(action, x, y):
    return OPERATIONS[action](x, y)


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


main()
