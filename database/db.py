import psycopg2

from config import DB_CONFIG


class Database:

    def __init__(self):
        self.connection = None

    def connect(self):

        if self.connection is None:

            self.connection = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                database=DB_CONFIG["database"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"]
            )

        return self.connection

    def cursor(self):
        return self.connect().cursor()

    def execute(self, sql, params=None):

        cur = self.cursor()
        cur.execute(sql, params)
        return cur

    def commit(self):

        if self.connection:
            self.connection.commit()

    def rollback(self):

        if self.connection:
            self.connection.rollback()

    def close(self):

        if self.connection:
            self.connection.close()
            self.connection = None


db = Database()