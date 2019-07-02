
import sqlite3, logging, random, time
logger = logging.getLogger(__name__)

from View import MessageSource

class Database:
    # Using sqlite for simplicity, even though it doesn't store my dict in a convenient matter.
    def __init__(self):
        self.create_db()
    
    def create_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Levels (
            user TEXT PRIMARY KEY,
            code TEXT,
            weight REAL
        )
        """
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")
        sql = """
        CREATE TABLE IF NOT EXISTS LevelClear (
            time INTEGER
        )
        """
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")
        sql = """
        CREATE TABLE IF NOT EXISTS LevelCurrent (
            user TEXT,
            code TEXT
        )
        """
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")

        clear_t = self.get_clear_time()
        if len(clear_t) == 0:
            self.set_clear_time()

    def execute(self, sql, values=None, fetch=False):
        with sqlite3.connect("Levels.db") as conn:
            cur = conn.cursor()
            if values is None:
                cur.execute(sql)
            else:
                cur.execute(sql, values)
            conn.commit()
            if fetch:
                return cur.fetchall()

    def add_level(self, user, code, weight):
        if self.execute("SELECT SUM(user) FROM LevelCurrent WHERE user == ?", values=(user,), fetch=True)[0][0] != None:
            return MessageSource.ADD_LEVEL_ERROR

        warning = self.execute("SELECT SUM(user) FROM Levels WHERE user == ?", values=(user,), fetch=True)[0][0] != None
        self.execute("INSERT OR REPLACE INTO Levels VALUES(?, ?, ?)", values=(user, code, weight))
        return MessageSource.ADD_LEVEL_WARNING if warning else MessageSource.ADD_LEVEL_SUCCESS

    def set_new_current(self, user, code):
        # Remove the winner from the Levels database
        self.execute("DELETE FROM Levels WHERE user == ?;", (user,))
        # Clear the current database
        self.execute("DELETE FROM LevelCurrent;")
        # Set the new current
        self.execute("INSERT INTO LevelCurrent VALUES(?, ?);", values=(user, code,))

    def get_current_level(self):
        return self.execute("SELECT user, code FROM LevelCurrent;", fetch=True)

    def get_levels(self):
        return self.execute("SELECT user, code FROM Levels;", fetch=True)
    
    def get_levels_weight(self):
        return self.execute("SELECT * FROM Levels;", fetch=True)

    def get_clear_time(self):
        return self.execute("SELECT time FROM LevelClear;", fetch=True)

    def clear(self):
        # Deletes all items
        self.execute("DELETE FROM Levels;")
        self.execute("DELETE FROM LevelCurrent;")
        self.execute("DELETE FROM LevelClear;")
        self.set_clear_time()

    def set_clear_time(self):
        self.execute("INSERT INTO LevelClear VALUES(?);", values=(round(time.time()),))
