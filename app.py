from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO
from json import dumps
import pyaudio
from audio import AudioWire




app = Flask(__name__)
app.config['SECRET_KEY'] = 'superdupersecret123'
socketio = SocketIO(app)


@socketio.on('connect')
def connect():
    print('client connected')


@socketio.on('start stream')
def start_stream():
    pass


@socketio.on('disconnect')
def disconnect():
    print('client disconnected')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    PROTOCOL = 'http'
    HOST = 'localhost'
    PORT = 3000

    audio_wire = AudioWire(socketio)
    audio_wire.start()
    print('Started audio wire thread.')

    print(f'Serving web server on {PROTOCOL}://{HOST}:{PORT}/')
    socketio.run(app, host=HOST, port=PORT, use_reloader=False)

    print('Stopping audio wire thread.')
    audio_wire.stop()
