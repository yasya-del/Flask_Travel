import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Airport(SqlAlchemyBase, UserMixin):
    __tablename__ = 'airports'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
