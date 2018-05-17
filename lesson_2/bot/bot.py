import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import logging

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def main():
    mybot = Updater(config.bot_api_key, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', get_constellation, pass_args=True))
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


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


main()
