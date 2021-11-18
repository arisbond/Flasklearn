import pymysql


class UseDatabase:
    def __init__(self, dbconfig: dict) -> None:
        self.config = dbconfig

    def __enter__(self) -> 'cursor':
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
