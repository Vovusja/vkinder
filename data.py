import sqlalchemy
from sqlalchemy import desc

from VKinder.db.database import VKusers, Found_person, session


class User_data:

    def __init__(self):
        self.uid = None
        self.name = None
        self.age = None
        self.sex = None
        self.city = None
        self.relation = None

        self.search_age_from = None
        self.search_age_to = None
        self.search_sex = None
        self.search_city = None
        self.search_relation = None

        self.data_user_dict = {}
        self.quant_query = 10
        self.step = 0
        self.city_count = None
        self.city_input_list = []

    def create_data_dict(self):
        self.data_user_dict[self.uid] = {}

        self.data_user_dict[self.uid]['name'] = self.name
        self.data_user_dict[self.uid]['age'] = self.age
        self.data_user_dict[self.uid]['sex'] = self.sex
        self.data_user_dict[self.uid]['city'] = self.city
        self.data_user_dict[self.uid]['relation'] = self.relation

        self.data_user_dict[self.uid]['name'] = self.name
        self.data_user_dict[self.uid]['age'] = self.age
        self.data_user_dict[self.uid]['sex'] = self.sex
        self.data_user_dict[self.uid]['city'] = self.city
        self.data_user_dict[self.uid]['relation'] = self.relation


class Found_data:

    def __init__(self):
        self.person_id = None
        self.name = None
        self.user_id = None
        self.person_date = None
        self.person_photo_id = None
        self.person_status = None
        self.is_shown = None
        self.raiting_ph = None


class Session:

    def __init__(self):
        self.db_session = session()

    def add_user(self, user):
        self.new_user = VKusers(user_id=user.uid,
                                user_name=user.name,
                                search_age_from=user.search_age_from,
                                search_age_to=user.search_age_to,
                                search_sex=user.search_sex,
                                search_city=user.search_city,
                                search_relation=user.search_relation,
                                )
        try:
            self.db_session.add(self.new_user)
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
        finally:
            self.db_session.close()

    def add_found_info(self, data):
        self.new_data = Found_person(
            person_id=data.person_id,
            user_id=data.user_id,
            person_name=data.name,
            person_date=data.person_date,
            person_photo_id=data.person_photo_id,
            person_status=data.person_status,
            is_shown=data.is_shown,
            raiting_ph=data.raiting_ph,
        )
        try:
            self.db_session.add(self.new_data)
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
        finally:
            self.db_session.close()

    def upd_found(self, p_id):
        self.query = self.db_session.query(Found_person).filter(Found_person.person_id == p_id).one()
        self.query.is_shown = True

        self.db_session.add(self.query)
        self.db_session.commit()
        self.db_session.close()

    def dlt_user_and_found(self):
        self.query_found = self.db_session.query(Found_person).filter(Found_person.user_id == user_data.uid).delete(synchronize_session='fetch')
        self.query_user = self.db_session.query(VKusers).filter(VKusers.user_id == user_data.uid).one()
        self.db_session.delete(self.query_user)
        self.db_session.commit()
        self.db_session.close()

    def get_user(self):
        query_user = self.db_session.query(VKusers).filter(VKusers.user_id == user_data.uid).all()
        return query_user


    def get_found(self):
        count = self.db_session.query(Found_person).filter(Found_person.user_id == user_data.uid, Found_person.is_shown == False).count()
        if count > 0:
            query_found = self.db_session.query(Found_person).filter(Found_person.user_id == user_data.uid, Found_person.is_shown == False).order_by(desc(Found_person.raiting_ph)).first()
            print(query_found.person_id, query_found.person_name, query_found.person_date, query_found.raiting_ph, )
            found_data.person_id = query_found.person_id
            found_data.name = query_found.person_name
            found_data.person_date = query_found.person_date
            found_data.person_photo_id = query_found.person_photo_id
            found_data.person_status = query_found.person_status
            self.upd_found(query_found.person_id)
        else:
            user_data.quant_query += 10
        return count

s = Session()

user_data = User_data()
found_data = Found_data()
