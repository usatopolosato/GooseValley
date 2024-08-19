import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    test = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("blocks.id"))

    block = orm.relationship('Block')
