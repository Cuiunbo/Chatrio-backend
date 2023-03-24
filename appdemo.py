from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import Mysql
from models import User

app = Flask(__name__)
CORS(app)


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # print(username)
    mysql = Mysql()
    sql = "select * from users where email = '" + username + "'"
    # print(sql)
    a = mysql.fetch_one_db(sql)
    # print(a)
    if a is not None:
        r = User(a)
        if r.password == password:
            return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401


@app.route('/api/signup', methods=['POST'])
def signup():
    flag = False
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    mysql = Mysql()
    sql1 = "select * from users where email = '" + email + "'"
    sql2 = "select * from users where user_name = '" + username + "'"
    r1 = mysql.fetch_one_db(sql1)
    r2 = mysql.fetch_one_db(sql2)

    print(r1)
    print(r2)
    if r1 is not None or r2 is not None:
        return jsonify({'success': False, 'message': 'Name or email has been occupied!'}), 401
    sql3 = "insert into chatrio.users (user_name, password, email) values ('" + username + "','" + password + "','" + email + "')"
    print(sql3)
    r3 = mysql.exe_db(sql3)
    print(r3)
    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run()
