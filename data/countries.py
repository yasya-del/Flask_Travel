import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Country(SqlAlchemyBase, UserMixin):
    __tablename__ = 'countries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cities = sqlalchemy.Column(sqlalchemy.String, nullable=True)