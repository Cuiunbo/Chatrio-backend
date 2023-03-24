import datetime
from utils import Mysql

config = {'user': 'root',
          'password': 'Aa123456',
          'port': 3306,
          'host': '47.94.222.108',
          'db': 'chatrio'}


def query(id):
    mysql = Mysql(config)
    r = mysql.fetch_one_db("select * from users where user_id = "+id)
    return r


class User:
    user_id = int
    user_name = str
    password = str
    email = str

    def __init__(self, t):
        self.user_id = t[0]
        self.user_name = t[1]
        self.password = t[2]
        self.email = t[3]


class Room:
    room_id = 0
    room_name = str
    num_members = 0

    def __init__(self, t):
        self.room_id = t[0]
        self.room_name = t[1]
        self.num_members = t[2]


class Message:
    message_id = int
    room_id = int
    is_text = bool
    content = str
    time = datetime.datetime
    user_id = int
    is_recalled = bool

    def __init__(self, t):
        self.message_id = t[0]
        self.room_id = t[1]
        self.is_text = t[2]
        self.content = t[3]
        self.time = t[4]
        self.user_id = t[5]
        self.is_recalled = t[6]
