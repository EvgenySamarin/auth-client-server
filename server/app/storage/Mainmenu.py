from sqlalchemy import Column, TEXT, INTEGER

from .base import database


class Mainmenu(database.Model):
    """ Mainmenu storage class to save data into SQLAlchemy's table the same name """
    __tablename__ = "mainmenu"

    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT(50), unique=True)
    url = Column(TEXT(50), nullable=True)

    def __str__(self):
        return f"<mainmenu {self.id}>"


def fill_mainmenu():
    database.session.add(Mainmenu(title="Main", url="/index"))
    database.session.add(Mainmenu(title="Sign-In", url="/auth"))
    database.session.add(Mainmenu(title="About", url="/about"))
    database.session.add(Mainmenu(title="Auth-logs", url="/logs"))
    database.session.add(Mainmenu(title="Sign-out", url="/signout"))
    database.session.commit()


def get_menu(is_login: bool) -> list:
    if is_login:
        return Mainmenu.query.all()
    else:
        return Mainmenu.query.filter(Mainmenu.url != "/signout").all()