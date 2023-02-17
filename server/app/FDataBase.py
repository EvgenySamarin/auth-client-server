import sqlite3
from utils import print_debug


class FDataBase:
    def __init__(self, database, application):
        self.__db = database
        self.__cur = database.cursor()
        self.__app = application

    def get_menu(self, is_user_login: bool):
        sql = '''SELECT * FROM mainmenu  WHERE url <> "/signout"'''
        if is_user_login:
            sql = '''SELECT * FROM mainmenu WHERE url <> "/auth"'''

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print_debug(application=self.__app, message=res)
            if res:
                return res
        except sqlite3.Error as error:
            print_debug(application=self.__app, message=f"Database fetch error: {error}")
        return []

    def add_auth_log(self, login, password):
        """
        Logging an authentication attempt
        """
        try:
            self.__cur.execute("INSERT INTO logs VALUES(NULL, ?, ?)", (login, password))
            self.__db.commit()
            print_debug(application=self.__app, message="log data added to database")
        except sqlite3.Error as error:
            print_debug(application=self.__app, message=f"Database add error: {error}")
            return False
        return True

    def get_logs(self):
        """
        Get all auth logs
        """
        sql = '''SELECT * FROM logs'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print_debug(application=self.__app, message=res)
            if res:
                return res
        except sqlite3.Error as error:
            print_debug(application=self.__app, message=f"Database fetch error: {error}")
        return []
