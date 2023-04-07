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


@app.route('/api/addContact', methods=['POST'])
def addContact():
    data = request.json
    print(data)
    userid = data['username']
    isGroup = data['content']['isGroup']
    id = data['content']['id']
    print(isGroup)
    print(id)
    mysql = Mysql()
    if isGroup == '1':
        sql = 'select room_id from rooms where room_id = ' + id
        r = mysql.fetch_one_db(sql)
        if r is None:
            return jsonify({'success': False, 'message': 'Group does not exist!'}), 401
        sql = 'select room_id from room_user where user_id = ' + userid + ' and room_id = ' + id
        r = mysql.fetch_one_db(sql)
        if r is not None:
            return jsonify({'success': False, 'message': 'You are already in this group!'}), 401
        sql = "insert into room_user (user_id, room_id) values(" + userid + ', ' + id + ')'
        print(sql)
        mysql.exe_db(sql)
        sql = 'update rooms set num_members=num_members+1 where room_id = ' + id
        mysql.exe_db(sql)
        return jsonify({'success': True, 'message': 'Success!'}), 200
    sql = 'select user_id from users where user_id = ' + id
    r = mysql.fetch_one_db(sql)
    if r is None:
        return jsonify({'success': False, 'message': 'User does not exist!'}), 401
    sql = 'select room_id from rooms where num_members=2 and room_id in (select room_id from room_user where user_id = ' + userid + ' or user_id = ' + id + ' group by room_id having count(*)=2)'
    print(sql)
    r = mysql.fetch_one_db(sql)
    print(r)
    if r is not None:
        return jsonify({'success': False, 'message': 'Friend exists!'}), 401
    print(sql)
    sql = 'insert into room_user values (' + userid + ',@id,0), (' + id + ',@id,0)'
    sql1 = 'select @@identity'
    mysql.exe_db('insert into rooms values ()')
    mysql.exe_db('set @id = @@identity')
    r = mysql.fetch_one_db(sql1)
    print(r)
    mysql.exe_db(sql)
    return jsonify({'success': True, 'message': 'Success!', 'room_id': r[0]}), 200


@app.route('/api/createGroup', methods=['POST'])
def createGroup():
    data = request.json
    user1 = data['username']
    user2 = data['content']['id1']
    user3 = data['content']['id2']
    name = data['content']['name']
    print(user1, user2, user3, name)
    if user3 != user1 and user2 != user1 and user2 != user3:
        mysql = Mysql()
        sql = 'insert into rooms values (null, ' + name + "'3')"
        mysql.exe_db(sql)
        sql = 'select @@identity'
        mysql.exe_db('set @id = @@identity')
        sql = 'insert into room_user values (' + user1 + ',@id,1),(' + user2 + ',@id,0),(' + user3 + ',@id,0)'
        mysql.exe_db(sql)
        # sql = 'update rooms set num_members=num_members+1 where room_id = @id'
        # mysql.exe_db(sql)

        return jsonify({'success': True, 'message': 'Success!'}), 200
    return jsonify({'success': False, 'message': 'No!'}), 401


# 消息发送
@socketio.on('message')
def handle_message(msg):
    print(f'Received message: {msg}')
    mysql = Mysql()

    sql = "insert into messages (content, user_id, room_id, time) values ('" + msg['content']['content'] + "'," + str(
        msg['userId']) + "," + str(msg['roomId']) + ",now())"
    print(sql)
    a = mysql.exe_db(sql)
    print(a)
    send(msg, broadcast=True)


# 获取聊天室列表
@socketio.on('get_room_list')
def handle_get_room_list(user_id):
    print('--------------------get_room_list---------------------')
    mysql = Mysql()
    sql = "select room_id, room_name,num_members from rooms where room_id=any(select room_id from room_user where user_id = " + user_id + ")"
    print(sql)
    a = mysql.fetch_all_db(sql)
    print(a)
    # 存成字典
    result = {}
    for i in a:
        roomid = i[0]
        num_members = i[2]
        roomname = ''
        if num_members == 2:
            # sql 通过 room_user表获取另一个人的id
            sql = "select user_id from room_user where room_id = " + str(roomid) + " and user_id != " + str(user_id)
            print(sql)
            b = mysql.fetch_one_db(sql)
            # 容错处理
            if b is None:
                continue
            print(b)
            # 通过id获取另一个人的名字
            sql = "select user_name from users where user_id = " + str(b[0])
            print(sql)
            c = mysql.fetch_one_db(sql)
            print(c)
            if c is None:
                continue
            roomname = c[0]
        else:
            # roomname 就是 room_name
            roomname = i[1]
        result[roomid] = {'room_name': roomname, 'num_members': num_members}
    print(result)
    emit('room_list', result)
    print('--------------------get_room_list---------------------')


# 获取聊天室历史消息
@socketio.on('get_all_history')
def handle_get_all_history(room_id):
    print('--------------------get_all_history---------------------')
    print(room_id)
    mysql = Mysql()

    for i in room_id:
        print(i)
        result = {
            'history': [],
        }
        try:
            sql = "select content, user_id, time from messages where room_id = " + str(i)
            print(sql)
            a = mysql.fetch_all_db(sql)
            print(a)
            for j in a:
                sql = "select user_name from users where user_id = " + str(j[1])
                b = mysql.fetch_one_db(sql)
                print(b)
                datatime = j[2].strftime("%Y/%m/%d %H:%M:%S")
                result['history'].append({'time': datatime, 'content': j[0], 'sender': b[0]})
            print(result)
            emit('room_history', {'result': result, 'room_id': i})
        except Exception as e:
            print(f"An error occurred while querying messages for room {i}: {str(e)}")
    emit('get_end', {'result': 'end'})
    print('--------------------get_all_history---------------------')


# 加入聊天室


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    # app.run()
