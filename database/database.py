import sqlite3
from config.config import config as Config

DATABASE_NAME = Config.get('database', 'name')


class Database:
    """
    Class for creating and modifying a SQLite3 database.

    Attributes:
        connection: Connection to the database
        cursor: Cursor that is attached to the connection
    """

    def __init__(self):
        """
        The constructor for Database class.
        """
        self.startConnection()

# Miscellaneous
    def startConnection(self, database=f"{DATABASE_NAME}.db"):
        """
        A function to create a connection to database
        """

        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        """
        A function to close the connection
        """

        self.connection.close()

    def executeScript(self, script):
        """
        A function to execute multiple SQL queries in one go.

        Parameters:
            script (str): query to be executed
        """

        self.cursor.executescript(script)
        self.connection.commit()

    def execute(self, query):
        """
        A function to execute  SQL query.

        Parameters:
            script (str): query to be executed
        """

        self.cursor.execute(query)
        self.connection.commit()

    def fetchall(self, query):
        """
        A function to fetch all results from a query.

        Parameters:
            script (str): query to be executed

         Returns:
            array: array of all elements that fit the querry
        """
        self.cursor.execute(query)
        return (self.cursor.fetchall())
