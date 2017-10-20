from sqlalchemy import Column, Integer, String, DateTime, BigInteger, func
from sqlalchemy.orm.exc import NoResultFound

#  import engine

from telegram import User as TGUser
from telegram import Update as TGUpdate

from datetime import datetime
from pytz import timezone

from .base import Base, Session
#Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'user'

    id =  Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    telegramid = Column(Integer)
    ban = Column(Integer, default=0)
    kick = Column(Integer, default=0)
    lang = Column(String, default="en_US")
    timeadded = Column(DateTime)

    def __repr__(self):
        return "<User(Name: {}, Telegramid: {}>".format(self.first_name, self.telegramid)

    @staticmethod
    def from_tg_user_object(user: TGUser):
        session = Session()

        try:
            u = session.query(User).filter(User.telegramid == user.id).one()
            u.first_name = user.first_name
            u.last_name = user.last_name
            u.username = user.username
        except NoResultFound:
            u = User(first_name=user.first_name, last_name=user.last_name, telegramid=user.id, username=user.username,
                     timeadded=datetime.now(timezone('Asia/Hong_Kong')))
            session.add(u)

        session.commit()
        session.expunge_all()
        return u

    @staticmethod
    def from_tg_update(update: TGUpdate):
        session = Session()

        user = update.effective_user
        u = User.from_tg_user_object(user)

        if update.message.reply_to_message:
            User.from_tg_user_object(update.message.reply_to_message.from_user)

        session.expunge_all()
        return u

    @staticmethod
    def from_user_id(user_id: int):
        session = Session()
        try:
            u = session.query(User).filter(User.telegramid == user_id).one()
            session.expunge_all()
            return u
        except:
            return False

    @property
    def full_name(self):
        full = self.first_name
        if self.last_name:
            full += " {}".format(self.last_name)
        return full

    @property
    def markdown_first(self):
        text = self.first_name
        if self.username:
            text = "[{}](http://t.me/{})".format(self.first_name, self.username)
        return text

    @property
    def markdown_full(self):
        text = self.full_name
        if self.username:
            text = "[{}](http://t.me/{})".format(self.full_name, self.username)
        return text

    def add_ban(self, num: int):
        session = Session()

        self.ban += num

        session.commit()
        return self

    def add_kick(self, num: int):
        session = Session()

        self.kick += num

        session.commit()
        return self

    @staticmethod
    def count():
        session = Session()
        count = session.query(func.count(User.userid)).scalar()
        return count
