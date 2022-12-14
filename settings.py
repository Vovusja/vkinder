# Data Base
DATABASE = 'postgresql'
DRIVER = 'psycopg2'
PORT = 5432
HOST = 'localhost'
NAME = "vkinder"
OWNER = 'netology_bd'
PASSWORD = ''


# VK_api Tokens
GROUP_TOKEN = ''
USER_TOKEN = ''
# APP_ID = 0


def get_token(GROUP_TOKEN, USER_TOKEN):
    if GROUP_TOKEN == '':
        GROUP_TOKEN = input("Введите токен сообщества ВК: ")
    if USER_TOKEN == '':
        USER_TOKEN = input("Введите токен пользователя (Access token): ")
    return {'group_token': GROUP_TOKEN, 'user_token': USER_TOKEN}


token = get_token(GROUP_TOKEN, USER_TOKEN)
group_token = token['group_token']
user_token = token['user_token']
