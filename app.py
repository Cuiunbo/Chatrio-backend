from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    # 获取前端发送过来的用户名和密码
    username = request.json.get('username')
    password = request.json.get('password')

    # 连接数据库
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='mydatabase'
    )

    # 执行 SQL 查询
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 判断是否登录成功
    if user:
        # 如果登录成功，返回登录成功的信息
        return jsonify({'message': '登录成功'})
    else:
        # 如果登录失败，返回登录失败的信息
        return jsonify({'message': '用户名或密码错误'})