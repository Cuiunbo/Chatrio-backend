import pymysql

config_root = {'user': 'root',
               'password': 'Aa123456',
               'port': 3306,
               'host': '47.94.222.108',
               'db': 'chatrio'}


class Mysql:

    def __init__(self):
        self.connection = pymysql.connect(host=config_root['host'],
                                          port=config_root['port'],
                                          user=config_root['user'],
                                          password=config_root['password'],
                                          db=config_root['db'])

        # self.connection = pymysql.connect(host=config['host'],
        #                                  port=config['port'],
        #                                  user=config['user'],
        #                                  password=config['password'],
        #                                  db=config['db'])

    def fetch_one_db(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    def fetch_all_db(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def exe_db(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
