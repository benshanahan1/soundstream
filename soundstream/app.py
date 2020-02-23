from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
from soundstream.audio import AudioWire  # noqa: E402
from soundstream.utils import info  # noqa: E402


app = Flask(__name__)
app.config['SECRET_KEY'] = 'superdupersecret123'
socketio = SocketIO(app)


@socketio.on('connect')
def connect():
    info('client connected')


@socketio.on('start stream')
def start_stream():
    pass


@socketio.on('disconnect')
def disconnect():
    info('client disconnected')


@app.route('/')
def index():
    return render_template('index.html')


def start_server():
    PROTOCOL = 'http'
    HOST = 'localhost'
    PORT = 3000

    # info('Available input devices:')
    # info(sd.query_devices())

    audio_wire = AudioWire(socketio)
    audio_wire.start()
    print('Started audio wire thread.')

    print(f'Serving web server on {PROTOCOL}://{HOST}:{PORT}/')
    socketio.run(app, host=HOST, port=PORT, use_reloader=False)

    print('Stopping audio wire thread.')
    audio_wire.stop()


if __name__ == '__main__':
    start_server()
