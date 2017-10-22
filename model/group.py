from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, func
from sqlalchemy.orm.exc import NoResultFound

# from conn import engine

from telegram import Chat as TGChat
from telegram import Update as TGUpdate

from datetime import datetime
from pytz import timezone

from .base import Base, Session
#Base = declarative_base(bind=engine)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String)
    telegramid = Column(Integer)
    lang = Column(String, default="en_US")
    link = Column(String)
    info = Column(String)
    rules = Column(String)
    welcome = Column(String)
    timeadded = Column(DateTime)

    def __repr__(self):
        return "<Group(Title: {}, Telegramid: {}>".format(self.name, self.telegramid)

    @staticmethod
    def from_tg_chat_object(chat: TGChat):
        session = Session()

        if chat.id > 0:
            return False

        try:
            g = session.query(Group).filter(Group.telegramid == chat.id).one()
            g.name = chat.title
            g.username = chat.username
        except NoResultFound:
            g = Group(name=chat.title, username=chat.username, telegramid=chat.id,
                      timeadded=datetime.now(timezone('Asia/Hong_Kong')))
            session.add(g)

        session.commit()
        session.expunge_all()
        return g

    @staticmethod
    def from_tg_update(update: TGUpdate):
        session = Session()

        chat = update.effective_chat
        g = Group.from_tg_user_object(chat)

        session.expunge_all()
        return g

    @staticmethod
    def from_chat_id(chat_id: int):
        session = Session()
        try:
            g = session.query(Group).filter(Group.telegramid == chat_id).one()
            session.expunge_all()
            return g
        except:
            return False

    @property
    def title(self):
        return self.name

    @property
    def markdown_title(self):
        text = self.name
        if self.username:
            text = "[{}](http://t.me/{})".format(self.name, self.username)
        return text

    @staticmethod
    def count():
        session = Session()
        count = session.query(func.count(Group.groupid)).scalar()
        return count

    def setlink(self, link):
        session = Session()
        self.link = link
        session.add(self)
        session.commit()

    def setinfo(self, info):
        session = Session()
        self.info = info
        session.add(self)
        session.commit()

    def setrules(self, rules):
        session = Session()
        self.rules = rules
        session.add(self)
        session.commit()

    def setwelcome(self, welcome):
        session = Session()
        self.welcome = welcome
        session.add(self)
        session.commit()
