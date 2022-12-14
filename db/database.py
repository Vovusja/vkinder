import sqlalchemy as sql
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from VKinder.settings import DATABASE, DRIVER, OWNER, PASSWORD, PORT, NAME, HOST

engine = sql.create_engine(f"{DATABASE}+{DRIVER}://{OWNER}:{PASSWORD}@{HOST}:{PORT}/{NAME}", echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


class VKusers(Base):
    __tablename__ = 'vkusers'
    user_id = sql.Column(sql.Integer, primary_key=True)
    user_name = sql.Column(sql.String, nullable=False)
    search_age_from = sql.Column(sql.Integer, default=18)
    search_age_to = sql.Column(sql.Integer, default=50)
    search_sex = sql.Column(sql.Integer, default=50)
    search_city = sql.Column(sql.String, default=None)
    search_relation = sql.Column(sql.Integer, default=6)
    user_found = relationship('Found_person', back_populates='user')


class Found_person(Base):
    __tablename__ = 'found_person'

    person_id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('vkusers.user_id'), nullable=False)
    person_name = sql.Column(sql.String, nullable=False)
    person_date = sql.Column(sql.Date)
    person_photo_id = sql.Column(sql.String, nullable=False)
    person_status = sql.Column(sql.String)
    is_shown = sql.Column(sql.Boolean, default=False)
    raiting_ph = sql.Column(sql.Integer, default=0)
    user = relationship(VKusers, back_populates='user_found')



Base.metadata.create_all(engine)
