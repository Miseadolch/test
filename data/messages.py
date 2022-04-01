import sqlalchemy
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('chats', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('chats.id')),
    sqlalchemy.Column('messages', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('messages.id'))
)


class Messages(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
