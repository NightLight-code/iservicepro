from django.core.management.base import BaseCommand
import telebot
from telebot import StateMemoryStorage  # Нужно для работы Proxy
from django.conf import settings
import re
from telebot import custom_filters
from telebot.handler_backends import StatesGroup, State
from siteservice.models import Phone, NewiPhone, AllColors, Memory, Region, MacBook
from tgbot.bot import keyboard as kb
import environ
from tgbot.models import Profile, Message

env = environ.Env()
environ.Env.read_env()
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(settings.TOKEN, state_storage=state_storage)  # Передаём токен из файла setting.py
# apihelper.proxy = {'http': settings.proxy}  # Передаём Proxy из файла config.py
# Initialise environment variables

print('Start BOT')

user_repear = ['ремонт', 'починить', 'отремонтировать', 'почистить', 'замена', 'заменить']
user_buy = ['покупка', 'купить', 'покупать']
user_sale = ['продать', 'продажа', 'продаю', 'продавать']
user_other = ['другое']
admin = env('admin_commands')


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    price = State()  # с этого момента достаточно создавать экземпляры класса State
    end = State()


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
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    send_mess = f'Приветсвую Вас {user_name}!' \
                "\nДанный бот создан с целью сэкономить Свое и ваше время на телефонные разговоры.\n" \
                "\n" \
                "Узнать стоимость ремонта.\n" \
                "Узнать стоимость новых и б\у телефонов.\n" \
                "Оставить заявку на ремонт, чтобы Мы связались с вами\n" \
                "\n" \
                "\n" \
                "Если все же вы не нашли то, что вам нужно! Пишите\n" \
                "\n" \
                "@leaderisaev \n"
    try:

        # Добавляем пользователя после запуска бота
        profile, _ = Profile.objects.get_or_create(external_id=chat_id, defaults={'name': message.from_user.first_name})
        user_id = Message(profile=profile)
        user_id.save()
        # print('Логин добавлен')
        bot.send_message(message.chat.id, send_mess, reply_markup=kb.markup_menu)

    except Exception as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m


def update_price(message):
    bot.set_state(message.from_user.id, MyStates.price, message.chat.id)
    bot.send_message(message.chat.id, 'Напишите прайс')


@bot.message_handler(state=MyStates.price)
def name_get(message):
    bot.set_state(message.from_user.id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price'] = message.text
        write_data(data['price'])
        # print(data['price'])
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, 'Отправлено', reply_markup=kb.markup_menu)
    # msg = ("Все верно?:\n<b>"
    #        f"{data['price']}\n</b>")
    # bot.send_message(message.chat.id, msg, parse_mode="html")


def write_data(data, filename='price.txt'):
    with open(filename, "w+") as f:
        f.write(f'{data}\n')
        f.close()
    create_price()


def if_error(message):
    bot.send_message(message.chat.id, 'Что-то пошло не так', reply_markup=kb.markup_menu)


def create_price(count=3000):
    with open('price.txt', 'r+') as s:
        file = s.readlines()
        for line in file:
            t = re.sub('[.,-]', ' ', line)
            phone_data = t.split()
            try:
                if len(phone_data) >= 7:
                    model = ' '.join(phone_data[:3])
                    memory = phone_data[3]
                    color = phone_data[4]
                    region = phone_data[5][-2:]
                    price = int(phone_data[6]) + count
                    add_data_in_db(model, memory, color, region, price)
                elif len(phone_data) == 6:
                    model = ' '.join(phone_data[:2])
                    memory = phone_data[2]
                    color = phone_data[3]
                    price = int(phone_data[5]) + count
                    region = phone_data[4][-2:]
                    add_data_in_db(model, memory, color, region, price)
                elif len(phone_data) == 5:
                    model = ' '.join(phone_data[:1])
                    memory = phone_data[1]
                    color = phone_data[2]
                    price = int(phone_data[4]) + count
                    region = phone_data[3][-2:]
                    add_data_in_db(model, memory, color, region, price)
            except ValueError as v:
                print(v)


def add_data_in_db(model, memory, color, region, price):
    try:
        p, _ = Phone.objects.get_or_create(name=model)
        m, _ = Memory.objects.get_or_create(memory=memory)
        c, _ = AllColors.objects.get_or_create(colors=color)
        r, _ = Region.objects.get_or_create(regions=region)
        data, _ = NewiPhone.objects.filter(model_phone=p, memory_phone=m, colors_phone=c, region_phone=r,
                                           price_phone=price)
        if data.exists():
            print(f'Уже есть в БД {data}')
        else:
            print(f'Нету данных')
            new = NewiPhone(model_phone=p, memory_phone=m, colors_phone=c, region_phone=r, price_phone=price)
            new.save()

    except Phone.DoesNotExist as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == 'sale_new_iphone':
            bot.send_message(call.message.chat.id, text="iPhone 📱", reply_markup=kb.inline_kb_chose_new_model_iphone)
        elif call.data == 'sale_new_macbook':
            bot.send_message(call.message.chat.id, text="MacBook 💻", reply_markup=kb.inline_mac_menu)
            # callback_mac_query(call.data, call.message)
        elif call.data == 'sale_iphone14':
            try:
                model = NewiPhone.objects.filter(model_phone__name=f'14')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14plus':
            try:
                model = NewiPhone.objects.filter(model_phone__name=f'14 plus')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14pro':
            try:
                model = NewiPhone.objects.filter(model_phone__name=f'14 pro')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14promax':
            try:
                model = NewiPhone.objects.filter(model_phone__name=f'14 pro max')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13':
            try:
                model = NewiPhone.objects.filter(model_phone__name=f'13')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13pro':
            try:
                model = NewiPhone.objects.filter(model_phone__name='13 pro')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13promax':
            try:
                model = NewiPhone.objects.filter(model_phone__name='13 pro max')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13mini':
            try:
                model = NewiPhone.objects.filter(model_phone__name='13 mini')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12promax':
            try:
                model = NewiPhone.objects.filter(model_phone__name='12 pro max')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12pro':
            try:
                model = NewiPhone.objects.filter(model_phone__name='12 pro')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone12':
            try:
                model = NewiPhone.objects.filter(model_phone__name='12')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12mini':
            try:
                model = NewiPhone.objects.filter(model_phone__name='12 mini')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)

                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_se2':
            try:
                model = NewiPhone.objects.filter(model_phone__name='SE (2-го поколения)')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)

                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11pro':
            try:
                model = NewiPhone.objects.filter(model_phone__name='11 pro')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11promax':
            try:
                model = NewiPhone.objects.filter(model_phone__name='11 Pro Max')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11':
            try:
                model = NewiPhone.objects.filter(model_phone__name='11')
                status = NewiPhone.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewiPhone.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_air13_22':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Air 13 (mid 2022)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro13_22':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Pro 13(mid 2022)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_air13_20':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Air 13(mid 2020)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro13_20':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Pro 13(mid 2020)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro14_21':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Pro 14(mid 2021)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro16_21':
            try:
                model = MacBook.objects.filter(model__macbook_name='MacBook Pro 16(mid 2021)')
                status = MacBook.objects.filter(status='n')
                if not model or status:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        else:
            bot.send_message(call.message.chat.id, 'Мы работаем над этим 🤧')
    except Exception as e:
        bot.send_message(call.message.chat.id, 'Упс 🤧 что-то не работает ⚙️')
        print(e)


def callback_mac_query(data, message):
    ...
    # chat_id = message.chat.id
    # user_message, _ = Profile.objects.get_or_create(external_id=chat_id, defaults={'message': data})
    # user_id = Message(profile=user_message)
    # print(user_id)
    # bot.send_message(data.message.chat.id, text="MacBook", reply_markup=kb.inline_mac_menu)


class SearchInDb:
    def __init__(self, data):
        self.data = data


# Тут улавливает тексты пользователей
@bot.message_handler(content_types=['text'])
def text_user(message):
    chat_id = message.chat.id
    text_user = message.text.lower()
    if text_user in admin and chat_id == 113129447:
        update_price(message)
    elif text_user in user_buy:
        bot.send_message(chat_id, text="Прайc на Apple", reply_markup=kb.inline_kb_sale_menu)
    elif text_user in user_repear:
        bot.send_message(chat_id,
                         text='Я так понимаю вас интересует ремонт, мы работаем над этим')
    elif text_user in user_sale:
        bot.send_message(chat_id,
                         text='Я так понимаю вы хотите что-то продать, мы работаем над этим')
    elif text_user in user_other:
        bot.send_message(chat_id,
                         text='Если не нашли то, что вам нужно вы можете написать:\n @leaderisaev')
    else:
        bot.send_message(chat_id,
                         text='А вот это мне не знакомо, пожалуй запомню ☺️', reply_markup=kb.markup_menu)
        if not message.chat.id == 113129447:
            try:
                user_name, _ = Profile.objects.get_or_create(external_id=chat_id,
                                                             defaults={'name': message.from_user.first_name})
                user_message = Message(profile=user_name, text=text_user)
                user_message.save()
            except Exception as m:
                error_message = f'Произошла ошибка: {m}'
                print(error_message)
                raise m


def main():
    try:
        start = bot.polling(none_stop=True, timeout=123, interval=1)
    except Exception as e:
        print(f'Error {e}')
    return start


bot.add_custom_filter(custom_filters.StateFilter(bot))


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        try:
            bot.polling(none_stop=True, timeout=123, interval=1)
        except Exception as e:
            print(f'Error {e}')


if __name__ == '__main__':
    main()
# __gt для сравнений если больше
# __ls если меньше
# __gte больше или равно
# exclude не равно
# __isnull true or false
# obj, created = NewiPhone.objects.update_or_create(
#                             model_phone__phone_name=model,
#                             memory_phone__memory=memory,
#                             colors_phone__colors=color,
#                             region_phone__regions=region,
#                             price_phone=price)
# obj = NewiPhone(**created)
# data = NewiPhone(data=obj)
# data.save()
# data = {'model_phone': model,
#         'memory_phone': memory,
#         'colors_phone' : color,
#         'region_phone' : region,
#         'price_phone' : price}

# elif len(phone_data) == 5:
#     model = ' '.join(phone_data[:1])
#     memory = phone_data[1]
#     color = phone_data[2]
#     price = int(phone_data[4])
#     region = phone_data[3][-2:]
#     print(model, memory, color, price, region)

# лучше bulk_create - множественоое создание. но это не критично
# Data.object.create(
#     model=model,
#     memory=memory,
#     color=color,
#     price=price,
#     # тут смайлики, создай dict в котором ключи со смайликами будут ассоцироваться с корректным названием страны
#     region=region,
# )


# def send_info(message, data):
#     user_name = message.from_user.first_name
#     chat_id = message.chat.id
#     bot.send_message(message.chat.id, f"{data}\n</b>", parse_mode="html",reply_markup=kb.btn_add_price)

# NewiPhone.objects.update_or_create(
#     memory_phone=Memory.objects.create(memory=memory),
#     colors_phone=AllColors.objects.create(colors=color),
#     region_phone=Region.objects.create(regions=region),
#     model_phone=Phone.objects.create(phone_name=model),
#     price_phone=price)
# elif call.data == 'sale_iphone_xs':
#     try:
#         model = Phone.objects.filter(model_phone__name='XS')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'iPhone_xsmax':
#     try:
#         model = Phone.objects.filter(model_phone__name='XS Max')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_xr':
#     try:
#         model = Phone.objects.filter(model_phone__name='XR')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_x':
#     try:
#         model = Phone.objects.filter(model_phone__name='X')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_8':
#     try:
#         model = Phone.objects.filter(model_phone__name='8')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_8plus':
#     try:
#         model = Phone.objects.filter(model_phone__name='8 plus')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_7':
#     try:
#         model = Phone.objects.filter(model_phone__name='7')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_7plus':
#     try:
#         model = Phone.objects.filter(model_phone__name='7 plus')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
#
# elif call.data == 'sale_iphone_se1':
#     try:
#         model = NewiPhone.objects.filter(model_phone__name='SE (1-го поколения)')
#         status = Phone.objects.filter(status='n')
#         if not model or status:
#             bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет')
#         else:
#             bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
#             for item in model:
#                 bot.send_message(call.message.chat.id, f'iPhone {item}')
#     except Phone.DoesNotExist as s:
#         print(s)
