import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iservicepro.settings")
import django

django.setup()

from tgbot.bot.bot_handler import *
from tgbot.bot.message import *
import telebot
from telebot import StateMemoryStorage  # Нужно для работы Proxy
from iservicepro import settings
from tgbot.bot import keyboard as kb
from users_controller import *
from tgbot.models import Profile, Message
import time

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(settings.TOKEN, state_storage=state_storage)

print('Start BOT')


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


# Тут работаем с командой start
@bot.message_handler(commands=['start'])
def welcome_start(message):
    """Функция на отклик старт"""
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    hello_message = f'Приветсвую Вас {user_name}!' \
                    f'\n' \
                    f'Выберите из пункта меню'
    try:
        """Проверяем не заблокирован ли пользователь"""
        if check_user_block(chat_id):
            bot.send_message(message.chat.id, text=MESSAGE_FROM_BLOCK_USER)
        else:
            """Добавляем пользователя после запуска бота если его не было в БД"""
            profile, _ = Profile.objects.get_or_create(external_id=chat_id,
                                                       defaults={'name': message.from_user.first_name,
                                                                 'admin_or_not': 'no_admin'})
            user_id = Message(profile=profile)
            user_id.save()
            bot.send_message(message.chat.id, hello_message, reply_markup=kb.markup_menu)

    except Exception as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m


@bot.message_handler(content_types=['text'])
def user_text_all(message):
    """Передаем весь текст от пользователя"""
    # if check_user_from_admin():
    text_user(message)


def text_user_admin(message):
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    try:
        if check_user_from_admin(chat_id):
            bot.send_message(chat_id, text=f'Приветствую Вас {user_name}!', reply_markup=kb.ad)
        else:
            bot.send_message(chat_id, text="Увы у вас нет доступа к Админ-Панели",
                             reply_markup=kb.markup_menu)
    except Exception as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """все callback query для инлайн кнопок"""
    all_callback_query(call)


def user_menu(message):
    chat_id = message.chat.id
    user_text = message.text.lower()
    if user_text == 'Рассылка':
        notification()


def main():
    while True:
        try:
            bot.polling(none_stop=True)
            # send_time_namaz()
        except Exception as e:
            # time.sleep(3)
            print(e)


if __name__ == '__main__':
    main()
