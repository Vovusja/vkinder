from datetime import datetime
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from VKinder import management as mg
from VKinder.db.data import user_data
from VKinder.settings import group_token, user_token


class VKbot:

    def __init__(self):
        self.token = group_token
        self.user_token = user_token
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_session = vk_api.VkApi(token=self.user_token)
        self.vk_app = self.vk_session.get_api()

    def write_to_chat(self, id_to_send, message, photo):
        self.vk.method('messages.send', {
            'chat_id': id_to_send,
            'message': message,
            'attachment': f'photo{photo}',
            'random_id': randrange(10 ** 9),
        })

    def write_msg(self, id_to_send, message, photo):
        self.vk.method('messages.send', {
            'user_id': id_to_send,
            'message': message,
            'attachment': f'photo{photo}',
            'random_id': randrange(10 ** 9)})

    def listen_chat(self):

        try:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    print(event.user_id, event.text)
                    user_info = self.vk_app.users.get(user_ids=event.user_id, fields=['bdate', 'city', 'sex', 'relation'])
                    user_data.uid = user_info[0]['id']
                    user_data.name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
                    year = datetime.date(datetime.today()).year
                    user_data.age = year - int(user_info[0]['bdate'][-4:])
                    user_data.sex = user_info[0]['sex']
                    user_data.city = user_info[0]['city']['title']
                    user_data.relation = user_info[0]['relation']
                    user_data.create_data_dict()
                    select_data = mg.Selection(event.user_id)

                    if event.to_me:
                        user = self.vk.method("users.get", {"user_ids": event.user_id})
                        if event.from_chat:
                            self.write_to_chat(event.chat_id, f"{user[0]['first_name']}, я ответил Вам в личном сообщении.", None)
                        request = select_data.request(event.text, user[0]['first_name'], user_data.uid)
                        answer = request[0]
                        photo = request[1]
                        if answer is not None and answer != '':
                            print(answer)
                            self.write_msg(event.user_id, answer, photo)

        except:
            print('Не удалось отправить ответ пользователю')
            self.listen_chat()

    def search_people(self, uid):
        select_data = mg.Selection(uid)

        user_search = self.vk_app.users.search(count=user_data.quant_query,
                                                    hometown=user_data.search_city,
                                                    sex=user_data.search_sex,
                                                    status=user_data.search_relation,
                                                    age_from=user_data.search_age_from,
                                                    age_to=user_data.search_age_to,
                                                    is_closed=False,
                                                    fields=["is_closed", "bdate", "status", "photo_max_orig",
                                                            "photo_id"])

        for user_dict in user_search['items']:
            if not user_dict["is_closed"]:
                print(user_dict["id"], "- Добавлен в бд")
                likes = 0
                comments = 0
                try:
                    photo = user_dict['photo_id']
                    likes = self.vk_app.likes.getList(
                        type='photo',
                        owner_id=user_dict['id'],
                        item_id=photo[-9:],
                    )['count']
                    try:
                        comments = self.vk_app.photos.getComments(
                            owner_id=user_dict['id'],
                            photo_id=photo[-9:],
                        )['count']
                    except:
                        comments = 0
                except:
                    photo = "фото отсутствует"
                rating_photo = likes + comments
                select_data.save_found_data(user_dict, rating_photo, photo)
            else:
                print(user_dict["id"], "- страница закрыта")
        user_info = select_data.select_people()
        if user_info == ['Нет подходящих вариантов, попробуйте изменить параметры поиска', None]:
            user_info = self.search_people(uid)
            user_data.quant_query += 10

        return user_info

    def get_city_list(self, name_city):
        city_data = self.vk_app.database.getCities(country_id=1, q=name_city, need_all=1, count=15)
        user_data.city_count = city_data["count"]
        user_data.city_input_list = [i['title'] for i in city_data["items"]]



bot = VKbot()

if __name__ == '__main__':
    bot.listen_chat()


