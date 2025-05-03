import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Plan(SqlAlchemyBase, UserMixin):
    __tablename__ = 'planns'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cities = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)