from tgbot.models import Profile, Message


def check_user_block(chat_id):
    """ Проверка пользователя, не заблокирован ли"""
    check_user = Profile.objects.filter(external_id=chat_id, block_user='block')
    if check_user:
        return True
    else:
        return False


def check_user_from_admin(chat_id):
    """Функция для проверки доступа пользователя к Админ панелю"""
    check_admin_user = Profile.objects.filter(external_id=chat_id, admin_or_not='admin')
    if check_admin_user:
        return True
    else:
        return False

# def add_user_in_db():
#     profile, _ = Profile.objects.get_or_create(external_id=chat_id,
#                                                defaults={'name': message.from_user.first_name,
#                                                          'admin_or_not': 'no_admin'})
#     user_id = Message(profile=profile)
#     user_id.save()
