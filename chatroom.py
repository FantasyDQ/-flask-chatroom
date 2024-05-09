import random
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = []
nicknames = []

# 从文件读取昵称列表
with open('nickName.txt', 'r', encoding='utf-8') as file:
    nicknames = [line.strip() for line in file.readlines()]

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('send_message')
def handle_message(data):
    username = data.get('username')
    message = data['message']

    # 如果未提供昵称，随机选择一个预定义昵称
    if not username:
        username = random.choice(nicknames)

    if message:
        new_message = {'username': username, 'message': message}
        messages.append(new_message)
        emit('receive_message', new_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
