import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class City(SqlAlchemyBase, UserMixin):
    __tablename__ = 'russian_cities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tourism = sqlalchemy.Column(sqlalchemy.String, nullable=True)
