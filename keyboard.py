import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from VKinder.db.data import user_data
from VKinder.settings import group_token


vk_session = vk_api.VkApi(token=group_token)
vk = vk_session.get_api()

def start(user_id: int, message):
    start_keyboard = VkKeyboard(one_time=False)

    start_keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=start_keyboard.get_keyboard(),
        message=message
    )

def choose_a_search_method(user_id: int, message):
    choose_method = VkKeyboard(one_time=False)

    choose_method.add_button('Общий', color=VkKeyboardColor.NEGATIVE)
    choose_method.add_button('Авто', color=VkKeyboardColor.POSITIVE)
    choose_method.add_button('По параметрам', color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=choose_method.get_keyboard(),
        message=message
    )

def next_(user_id: int):
    next_keyboard = VkKeyboard(one_time=False)
    next_keyboard.add_button('Дальше', color=VkKeyboardColor.POSITIVE)
    next_keyboard.add_button('Изменить параметры поиска', color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=next_keyboard.get_keyboard(),
        message="________________________________________"
    )

def choose_sex(user_id: int):
    choose_sex_keyboard = VkKeyboard(one_time=True)

    choose_sex_keyboard.add_button('М', color=VkKeyboardColor.PRIMARY)
    choose_sex_keyboard.add_button('Ж', color=VkKeyboardColor.POSITIVE)
    choose_sex_keyboard.add_button('Любой', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=choose_sex_keyboard.get_keyboard(),
        message='Выберите пол человека для поиска:'
    )

def choose_age_from(user_id: int):
    age = user_data.age
    recommend_from = [age - 3, age - 2, age - 1, age, age + 1, age + 2]

    choose_age_keyboard = VkKeyboard(one_time=True)

    choose_age_keyboard.add_button(recommend_from[0], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_from[1], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_from[2], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_line()
    choose_age_keyboard.add_button(recommend_from[3], color=VkKeyboardColor.POSITIVE)
    choose_age_keyboard.add_button(recommend_from[4], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_from[5], color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=choose_age_keyboard.get_keyboard(),
        message='Введите минимальный возраст для поиска либо выберите из предложенных вариантов:'
    )

def choose_age_to(user_id: int):
    age = user_data.age
    recommend_to = [age - 2, age - 1, age, age + 1, age + 2, age + 3]

    choose_age_keyboard = VkKeyboard(one_time=True)

    choose_age_keyboard.add_button(recommend_to[0], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_to[1], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_to[2], color=VkKeyboardColor.POSITIVE)
    choose_age_keyboard.add_line()
    choose_age_keyboard.add_button(recommend_to[3], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_to[4], color=VkKeyboardColor.PRIMARY)
    choose_age_keyboard.add_button(recommend_to[5], color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=choose_age_keyboard.get_keyboard(),
        message='Введите максимальный возраст для поиска либо выберите из предложенных вариантов:'
    )

def choose_city(user_id: int):
    recommend_city = user_data.city
    choose_city_keyboard = VkKeyboard(one_time=True)

    if user_data.city_count is None or user_data.city_count == 0:
        choose_city_keyboard.add_button(recommend_city, color=VkKeyboardColor.POSITIVE)

        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=choose_city_keyboard.get_keyboard(),
            message='Введите город для поиска либо кликните на Ваш город:'
        )
    else:
        for en, city in enumerate(user_data.city_input_list, start=1):
            if len(city) > 39:
                city = city[:39]
            choose_city_keyboard.add_button(city, color=VkKeyboardColor.PRIMARY)
            if en % 3 == 0:
                choose_city_keyboard.add_line()
        choose_city_keyboard.add_button("Мой город", color=VkKeyboardColor.POSITIVE)

        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=choose_city_keyboard.get_keyboard(),
            message='можете выбрать из предложенных:'
        )

def choose_status(user_id: int):
    choose_status_keyboard = VkKeyboard(one_time=True)

    choose_status_keyboard.add_button("В активном поиске", color=VkKeyboardColor.POSITIVE)
    choose_status_keyboard.add_button("Холост(не замужем)", color=VkKeyboardColor.POSITIVE)
    choose_status_keyboard.add_button("Всё сложно", color=VkKeyboardColor.PRIMARY)
    choose_status_keyboard.add_line()
    choose_status_keyboard.add_button("Встречается", color=VkKeyboardColor.PRIMARY)
    choose_status_keyboard.add_button("Влюблен(-а)", color=VkKeyboardColor.NEGATIVE)
    choose_status_keyboard.add_button("Женат(замужем)", color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=choose_status_keyboard.get_keyboard(),
        message='Выберите семейное положение:'
    )

def confirm(user_id: int):
    confirm_keyboard = VkKeyboard(one_time=True)
    sex_list = ["Любой", "Женский", "Мужской"]

    confirm_keyboard.add_button('Подтверждаю!', color=VkKeyboardColor.POSITIVE)
    confirm_keyboard.add_button('Изменить данные', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=confirm_keyboard.get_keyboard(),
        message='Подтвердите выбранные параметры:'
                f'\nПол: {sex_list[user_data.search_sex]}'
                f'\nВозраст: {user_data.search_age_from} - {user_data.search_age_to}'
                f'\nГород: {user_data.search_city}'
                f'\nСтатус: {user_data.search_relation}'
    )

