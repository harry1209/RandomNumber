import eventlet
eventlet.monkey_patch()

from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None

def randomNumber():
    while True:
        sleep(0.5)
        num = randint(0,100)
        socketio.emit('random', {'num': num}, namespace='/test')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=randomNumber)
        thread.daemon = True
        thread.start()
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
