import sqlite3
from classes.config import config as Config

DATABASE_NAME = Config.get('database', 'name')

class Database:
    
    def __init__(self) -> None:
        self.connection = sqlite3.connect(f"{DATABASE_NAME}.db")
        self.cursor = self.connection.cursor()

# Miscellaneous
    def close(self):
        self.connection.close()

    def executeScript(self, script):
        self.cursor.executescript(script)
        self.connection.commit()
    
    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetchall(self, query):
        self.cursor.execute(query)
        return (self.cursor.fetchall())
