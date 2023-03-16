from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    # 获取前端POST过来的数据
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print(username)
    if username == 'test@126.com' and password == '123':
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run()