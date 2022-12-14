from VKinder.main import bot
from VKinder.db.data import user_data, s, found_data
from VKinder import keyboard


class Selection:

    def __init__(self, my_id):
        self.my_id = my_id
        self.data_dict = user_data.data_user_dict[my_id]
        self.reverse_sex = [0, 2, 1]

    def search_data_main(self):
        user_data.uid = self.my_id
        user_data.name = self.data_dict['name']
        s.add_user(user_data)

    def search_data_auto(self):
        user_data.uid = self.my_id
        user_data.name = self.data_dict['name']
        user_data.search_city = self.data_dict['city']
        user_data.search_sex = self.reverse_sex[self.data_dict['sex']]
        user_data.search_status = self.data_dict['relation']
        user_data.search_age_from = self.data_dict['age'] - 2
        user_data.search_age_to = self.data_dict['age'] + 2
        s.add_user(user_data)

    def select_people(self):
        get_f = s.get_found()
        if get_f == 0:
            return ['Нет подходящих вариантов, попробуйте изменить параметры поиска', None]
        found_people_info = [f"{found_data.name} " \
                             f"\n{found_data.person_date}" \
                             f"\nhttps://vk.com/id{found_data.person_id}" \
                             f"\n{found_data.person_status}",
                             found_data.person_photo_id]
        return found_people_info

    def save_found_data(self, user_dict, rating_photo, photo):
        found_data.name = f"{user_dict['first_name']} {user_dict['last_name']}"
        found_data.user_id = self.my_id
        found_data.person_id = user_dict['id']
        try:
            if len(user_dict['bdate'].split('.')) == 3:
                found_data.person_date = user_dict['bdate']
        except:
            pass
        found_data.person_photo_id = photo
        found_data.person_status = user_dict['status']
        found_data.raiting_ph = rating_photo
        s.add_found_info(found_data)

    def request(self, request, user_name, uid):
        if user_data.step == 0:
            if request.lower() in ["привет", "приветствую", "хэллоу", "хай", "hello", "hi", "дароф", ]:
                keyboard.start(uid, f"Здравствуйте, {user_name}, коль не шутите")
                return ["Для начала поиска человека жмите \"Начать\"", None]
            elif request.lower() in ["начать", "start", ]:
                user_data.step = 1
                keyboard.choose_a_search_method(uid, 'Выберите вариант поиска: ')
                return ['Общий - поиск людей без параметров, '
                        '\nАвто - программа автоматически задаст параметры поиска по Вашей анкете, '
                        '\nПо параметрам - ввести параметры поиска самостоятельно',
                        None]
            elif request.lower() in ["пока", "досвидния", "до свидния", "bye", "goodbye", "good bye", ]:
                user_data.step = 0
                return [f"до скорой встречи, {user_name}", None]
            else:
                keyboard.start(uid, 'Я понял это намек, я все ловлю на лету, но не понятно, что конкретно Вы имели ввиду... ')
                return [
                    "Для начала поиска человека жмите \"Начать\"",
                    None]
        elif user_data.step == 1:
            if request.lower() in ["общий", "main", ]:
                user_data.step = 3
                bot.write_msg(uid, "Ну поехали... \n немного терпения... я уже подбираю для Вас подходящих людей ",
                              None)
                self.search_data_main()
                keyboard.next_(uid)
                return bot.search_people(uid)

            elif request.lower() in ["авто", "auto", ]:
                user_data.step = 3
                bot.write_msg(uid, "Ну поехали... \n немного терпения... я уже подбираю для Вас подходящих людей ",
                              None)
                self.search_data_auto()
                keyboard.next_(uid)
                return bot.search_people(uid)

            elif request.lower() in ["по параметрам", "by parameters", ]:
                user_data.step = 2
                keyboard.choose_sex(uid)
                return [None, None]

            elif request.lower() in ["начать", "start", ]:
                return [f"{user_name}, уже начали...", None]
            elif request.lower() in ["привет", "приветствую", "хэллоу", "хай", "hello", "hi", "дароф", ]:
                return [f"Здоровались уже. {user_name}, алё, проснитесь", None]

            elif request.lower() in ["пока", "досвидния", "до свидния", "bye", "goodbye", "good bye", ]:
                user_data.step = 0
                return [f"до скорой встречи, {user_name}", None]
            else:
                keyboard.choose_a_search_method(uid,
                                       'Я понял это намек, я все ловлю на лету, но не понятно, что конкретно Вы имели ввиду... ')
                return [
                    "Выберите вариант поиска",
                    None]

        elif user_data.step == 2:
            if request.lower() in ["м", "муж", "2", ]:
                user_data.step = 21
                user_data.search_sex = 2
                keyboard.choose_age_from(uid)
                return [None, None]
            elif request.lower() in ["ж", "жен", "1", ]:
                user_data.step = 21
                user_data.search_sex = 1
                keyboard.choose_age_from(uid)
                return [None, None]
            elif request.lower() in ["любой", "не важно", "0", ]:
                user_data.step = 21
                user_data.search_sex = 0
                keyboard.choose_age_from(uid)
                return [None, None]
            else:
                bot.write_msg(uid, "Не верный ввод, попробуйте еще раз", None)
                keyboard.choose_sex(uid)
                return [None, None]

        elif user_data.step == 21:
            try:
                request = int(request)
                user_data.step = 22
                user_data.search_age_from = request
                keyboard.choose_age_to(uid)
            except:
                bot.write_msg(uid, "Не верный ввод, попробуйте еще раз", None)
                keyboard.choose_age_from(uid)
            finally:
                return [None, None]


        elif user_data.step == 22:
            try:
                request = int(request)
                user_data.search_age_to = request
                keyboard.choose_city(uid)
                user_data.step = 23
            except:
                print(int(request))
                bot.write_msg(uid, "Не верный ввод, попробуйте еще раз", None)
                keyboard.choose_age_to(uid)
            finally:
                return [None, None]

        elif user_data.step == 23:
            bot.get_city_list(request)
            request = request.capitalize()
            if user_data.city_count == 0:
                if request == "Мой город":
                    user_data.step = 24
                    user_data.search_city = user_data.city
                    keyboard.choose_status(uid)
                else:
                    bot.write_msg(uid, "Не верный ввод, попробуйте еще раз", None)
                    keyboard.choose_city(uid)
                return [None, None]
            elif user_data.city_count == 1:
                user_data.step = 24
                user_data.search_city = request
                keyboard.choose_status(uid)
                return [None, None]
            else:
                print(user_data.search_city, '=?', request)
                if user_data.search_city == request:
                    user_data.search_city = user_data.city_input_list[0]
                    keyboard.choose_status(uid)
                    user_data.step = 24
                elif request == user_data.city or request == "Мой город":
                    user_data.step = 24
                    user_data.search_city = user_data.city
                    keyboard.choose_status(uid)
                else:
                    bot.write_msg(uid,
                                  "Не очень понятно. Уточните, пожалуйста, название города.",
                                  None)
                    user_data.search_city = request
                    keyboard.choose_city(uid)
                return [None, None]

        elif user_data.step == 24:
            status_dict = {'не женат (не замужем)': 1, 'холост(не замужем)': 1, 'холост': 1, 'не замужем': 1,
                           'встречается': 2, 'помолвлен(-а)': 3, 'помолвлен': 3, 'помолвлена': 3,
                           'женат(замужем)': 4, 'женат': 4, 'замужем': 4,'в браке': 4, 'всё сложно': 5,
                           'в активном поиске': 6, 'в поиске': 6, 'влюблен(-а)': 7, 'влюблен': 7, 'влюблена': 7,
                           'в гражданском браке': 8}
            if request.lower() in status_dict.keys():
                user_data.search_relation = status_dict[request.lower()]
                bot.write_msg(uid, f"Вы выбрали статус, {status_dict[request.lower()]}", None)
                keyboard.confirm(uid)
                user_data.step = 25
                return [None, None]

            else:
                bot.write_msg(uid, "Не верный ввод, попробуйте еще раз", None)
                keyboard.choose_status(uid)
                return [None, None]

        elif user_data.step == 25:
            if request.lower() in ['confirm', "подтверждаю", "подтверждаю!", "да", "ок", "подтверждение",
                                     "согласен", "ok", "yes", "y"]:
                user_data.step = 3
                bot.write_msg(uid, "Ну поехали... \n немного терпения... я уже подбираю для Вас подходящих людей ", None)
                self.search_data_main()
                keyboard.next_(uid)
                return bot.search_people(uid)

            elif request.lower() in ['change', "изменить данные", "изменить параметры", "нет", "изменить",
                                     "назад", "ok", "no", "n"]:
                bot.write_msg(uid, "Начнем заново", None)
                keyboard.choose_sex(uid)
                user_data.step = 2
                return [None, None]
            else:
                bot.write_msg(uid, "Вы не подтвердили выбор параметров", None)
                user_data.step = 25
                keyboard.confirm(uid)
                return [None, None]

        elif user_data.step == 3:
            if request.lower() in ["дальше", "далее", "продолжить", "следующий", "следующая", "next", ]:
                keyboard.next_(uid)
                sp = self.select_people()
                if sp == ['Нет подходящих вариантов, попробуйте изменить параметры поиска', None]:
                    bot.write_msg(uid, "пожалуйста, подождите... ", None)
                    return bot.search_people(uid)
                return sp

            elif request.lower() in ["изменить параметры поиска", "изменить параметры", "другие параметры параметры",
                                     "сначала", ]:
                user_data.step = 1
                s.dlt_user_and_found()
                user_data.quant_query = 10
                keyboard.choose_a_search_method(uid, 'Выберите вариант поиска: ')
                return ['Общий - поиск людей без параметров, '
                        '\nАвто - программа автоматически задаст параметры поиска по Вашей анкете, '
                        '\nПо параметрам - ввести параметры поиска самостоятельно',
                        None]

            elif request.lower() in ["начать", "start", ]:
                return [f"{user_name}, уже начали...", None]
            elif request.lower() in ["привет", "приветствую", "хэллоу", "хай", "hello", "hi", "дароф", ]:
                return [f"Здоровее видали", None]
            elif request.lower() in ["пока", "досвидния", "до свидния", "bye", "goodbye", "good bye", ]:
                user_data.step = 0
                return [f"до скорой встречи, {user_name}", None]
            else:
                return ['Я понял это намек, я все ловлю на лету, но не понятно, что конкретно Вы имели ввиду... ', None]

