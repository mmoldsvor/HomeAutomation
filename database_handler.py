import MySQLdb


class DatabaseHandler:
    def __init__(self, host, user, password, db_name):
        self.db = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name)
        self.cursor = self.db.cursor()

    def add_device(self, device_type, *args):
        pass
