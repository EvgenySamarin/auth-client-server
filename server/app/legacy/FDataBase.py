# Класс может работать некорректно в виду передачи flask.globals.g
# следует рассмотреть возможность отказа от проброса этого параметра в класс
# класс оставлен в качестве примера работы с SQLite средствами Python

import sqlite3

from server.app.utils import print_debug


class FDataBase:
    def __init__(self, application, global_context):
        """
        Flask database helper class to work with SQLite database directly by cursor.
        To class work correctly you must specify the SQLite database config param app.config['DATABASE']

        Must be invoked into @app.before_request function

        :param application: the flask application
        :param global_context: flask.globals.g variable which representatives the global context dictionary
        """
        self.__db = self.get_db()
        self.__cur = self.__db.cursor()
        self.__app = application
        self.__g = global_context

    def connect_db(self):
        """
        Obtain database connection
        """
        print_debug(application=self.__app, message="get connection")
        connection = sqlite3.connect(self.__app.config['DATABASE'])
        connection.row_factory = sqlite3.Row
        return connection

    def close_db(self, error):
        """
        Close database connection if it does exist, when request was complete or terminate
        Must be invoked into @app.teardown_appcontext function
        """
        if hasattr(self.__g, 'link_db'):
            self.__g.link_db.close()
            if error:
                print_debug(application=self.__app, message=f"close database with error {error}")
            else:
                print_debug(application=self.__app, message="close database")

    def create_db(self, sql_scratch):
        """
        Create database from sql scratch

        :param sql_scratch: the SQL script file for database creation. For example: file "sq_db.sql"
        """
        db = self.connect_db()
        with self.__app.open_resource(sql_scratch, mode='r') as file:
            db.cursor().execute(file.read())
        db.commit()
        db.close()

    def get_db(self):
        """
        Obtain the database connection linked by request global context

        :returns: database connection
        """
        if not hasattr(self.__g, 'link_db'):
            self.__g.link_db = self.connect_db()
        return self.__g.link_db

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
