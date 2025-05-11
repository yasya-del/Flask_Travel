import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class City(SqlAlchemyBase, UserMixin):
    __tablename__ = 'cities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tourism = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)