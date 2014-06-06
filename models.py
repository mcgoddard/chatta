from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(128), unique=False)
    active_until = Column(DateTime, unique=False, default=(datetime.datetime.now))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String(144), unique=False)
    created_at = Column(DateTime, unique=False, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('messages', lazy='dynamic'))

    def __init__(self, text, user):
        self.text = text
        self.user = user

    def __repr__(self):
        return '<Message %r>' % (self.text)