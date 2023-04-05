from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, decode_token
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import Mysql
from models import User

app = Flask(__name__)
CORS(app)  # 跨域
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['JWT_SECRET_KEY'] = 'mysecretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins='*')  # 允许所有源


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
            token = str(r.user_id)  # Replace this with a more secure token, such as JWT
            # token = create_access_token(identity=r.user_id)
            # print(token)
            # response = jsonify({'success': True, 'token': token})
            # print(response.json)
            # print(response.json.get('token'))
            return jsonify(
                {'success': True, 'token': token, 'username': r.user_name, 'email': r.email, 'userid': r.user_id}), 200
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


# 消息发送
@socketio.on('message')
def handle_message(msg):
    print(f'Received message: {msg}')

    send(msg, broadcast=True)


# 获取聊天室列表
@socketio.on('get_room_list')
def handle_get_room_list(user_id):
    mysql = Mysql()
    sql = "select room_id, room_name,num_members from rooms where room_id=any(select room_id from room_user where user_id = " + user_id + ")"
    a = mysql.fetch_all_db(sql)
    print(a)
    emit('room_list', a)


# @socketio.on('fetch_chat_rooms')
# def handle_fetch_chat_rooms(data):
#     user_id = data['userId']

#     # Fetch chat rooms for the given user_id
#     # You might need to adjust the following line according to your database
#     chat_rooms = get_chat_rooms(user_id)

#     # Emit an event with the chat rooms
#     emit('chat_rooms', chat_rooms)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    # app.run()
