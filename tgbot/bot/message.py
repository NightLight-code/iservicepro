import environ

env = environ.Env()
environ.Env.read_env()


MESSAGE_FROM_BLOCK_USER = 'Вас заблокировали, если ошибочно, то обратитесь @leaderisaev'

USER_TEXT_REPAIR = ['ремонт', 'починить', 'отремонтировать', 'почистить', 'замена', 'заменить']
USER_BUY = ['покупка', 'купить', 'покупать']
USER_SALE = ['продать', 'продажа', 'продаю', 'продавать']
USER_OTHER = ['другое']
ADMIN = env('admin_commands')
UPDATE_CON = env('update_command')