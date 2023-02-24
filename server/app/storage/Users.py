from datetime import datetime
from sqlalchemy import Column, VARCHAR, DATETIME, TEXT, INTEGER

from .base import database


class Users(database.Model):
    """ User storage class to save data into SQLAlchemy's table the same name """
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True)
    login = Column(VARCHAR(32), unique=True)
    email = Column(TEXT(50), unique=True)
    psw = Column(TEXT(500), nullable=True)
    date = Column(DATETIME, default=datetime.utcnow)

    def __str__(self):
        return f"<users {self.id}, {self.email}, {self.psw}, {self.date}>"
