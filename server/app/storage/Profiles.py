from sqlalchemy import Column, TEXT, INTEGER, ForeignKey

from .base import database


class Profiles(database.Model):
    """ Profile storage class to save data into SQLAlchemy's table the same name """
    __tablename__ = "profiles"

    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT(50), nullable=True)
    old = Column(INTEGER)
    city = Column(TEXT(100))

    user_id = Column(INTEGER, ForeignKey('users.id'))

    def __str__(self):
        return f"<profiles {self.id}>"


