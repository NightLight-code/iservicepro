from telebot import custom_filters

from siteservice.models import NewPhone, MacBook
from tgbot.bot.bot import bot, text_user_admin
from tgbot.bot import keyboard as kb
from telebot.handler_backends import StatesGroup, State

from tgbot.bot.message import *
from tgbot.bot.users_controller import check_user_block
from tgbot.models import Profile
from telebot import StateMemoryStorage

state_storage = StateMemoryStorage()

# Создай хранилище нарушителей. Для примера буду использовать обычный сет.
banned_users = set()


class Dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    price = State()  # с этого момента достаточно создавать экземпляры класса State
    end = State()


def all_callback_query(call):
    try:
        if call.data == 'sale_new_iphone':
            bot.send_message(call.message.chat.id, text="iPhone 📱", reply_markup=kb.inline_kb_chose_new_model_iphone)
        elif call.data == 'sale_new_macbook':
            bot.send_message(call.message.chat.id, text="MacBook 💻", reply_markup=kb.inline_mac_menu)
        elif call.data == 'sale_iphone14':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone=f'14').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14plus':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone=f'14 plus').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14pro':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone=f'14 pro').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone14promax':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone=f'14 pro max').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone=f'13').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, text=f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13pro':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='13 pro').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13promax':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='13 pro max').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone13mini':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='13 mini').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12promax':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='12 pro max').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12pro':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='12 pro').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone12':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='12').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, '⬇️ Отлично! Отправляю прайс ⬇️')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_12mini':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='12 mini').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)

                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_se2':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='SE (2-го поколения)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11pro':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='11 pro').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11promax':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='11 Pro Max').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)

        elif call.data == 'sale_iphone_11':
            try:
                model = NewPhone.objects.filter(model_phone__name_phone='11').exclude(status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'iPhone {item}')
            except NewPhone.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_air13_22':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Air 13 (mid 2022)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro13_22':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Pro 13(mid 2022)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_air13_20':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Air 13(mid 2020)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro13_20':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Pro 13(mid 2020)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro14_21':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Pro 14(mid 2021)').exclude(
                    status='not_available')
                if not model:
                    bot.send_message(call.message.chat.id, 'Увы! Пока в наличии нет ☹️', reply_markup=kb.markup_menu)
                else:
                    bot.send_message(call.message.chat.id, 'Отлично! Отправляю прайс')
                    for item in model:
                        bot.send_message(call.message.chat.id, f'{item}')
            except MacBook.DoesNotExist as s:
                print(s)
        elif call.data == 'macbook_pro16_21':
            try:
                model = MacBook.objects.filter(model__macbook_name_mac='MacBook Pro 16(mid 2021)').exclude(
                    status='not_available')
                if not model:
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


def text_user(message):
    chat_id = message.chat.id
    user_text = message.text.lower()
    try:
        if check_user_block(chat_id):
            bot.send_message(chat_id, text=MESSAGE_FROM_BLOCK_USER)
        elif user_text in USER_BUY:
            bot.send_message(chat_id, text="Прайc на Apple", reply_markup=kb.inline_kb_sale_menu)
        elif user_text in USER_TEXT_REPAIR:
            bot.send_message(chat_id,
                             text='Я так понимаю вас интересует ремонт, мы работаем над этим')
        elif user_text in USER_SALE:
            bot.send_message(chat_id,
                             text='Я так понимаю вы хотите что-то продать, мы работаем над этим')
        elif user_text in USER_OTHER:
            bot.send_message(chat_id,
                             text='Если не нашли то, что вам нужно вы можете написать:\n @leaderisaev')
        elif user_text in ADMIN:
            text_user_admin(message)

        elif user_text == 'рассылка':
            notification(message)

        elif user_text == 'назад':
            bot.send_message(chat_id, text='ок', reply_markup=kb.markup_menu)

    except Exception as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m


def notification(message):
    bot.set_state(message.from_user.id, Dialog.spam, message.chat.id)
    bot.send_message(message.chat.id, 'Напиши текст рассылки')


@bot.message_handler(state=Dialog.spam)
def name_get(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=kb.markup_menu)
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.set_state(message.from_user.id, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
            data_user['admin_text'] = message.text
            print(data_user)
            # print(message.text)
        user_id = Profile.objects.in_bulk()
        for us_id in user_id:
            chat_id = user_id[us_id].external_id
            bot.send_message(user_id[chat_id], message.text)


@bot.message_handler(user_id=banned_users)
async def handle_banned(message):
    print(f"{message.from_user.full_name} пишет, но мы ему не ответим!")
    return True


def handle_ban_command(message):
    # проверяем, что ID передан правильно
    try:
        abuser_id = int(message.get_args())
    except (ValueError, TypeError):
        return message.reply("Укажи ID пользователя.")
    banned_users.add(abuser_id)
    message.reply(f"Пользователь {abuser_id} заблокирован.")


@bot.message_handler(content_types=['text'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "Welcome to bot. what's your name?")
    bot.register_next_step_handler(sent_msg, name_handler)  # Next message will call the name_handler function


def name_handler(pm):
    name = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"Your name is {name}. how old are you?")
    bot.register_next_step_handler(sent_msg, age_handler, name)  # Next message will call the age_handler function


def age_handler(pm, name):
    age = pm.text
    bot.send_message(pm.chat.id, f"Your name is {name}, and your age is {age}.")


bot.add_custom_filter(custom_filters.StateFilter(bot))
