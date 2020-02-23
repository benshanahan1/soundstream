from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
import sounddevice as sd  # noqa: E402
from soundstream.audio import AudioWire  # noqa: E402
from soundstream.utils import info  # noqa: E402
from argparse import ArgumentParser  # noqa: E402


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3000
DESCRIPTION = 'Websocket server for near real-time audio visualization.'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'superdupersecret123'
socketio = SocketIO(app)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


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


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--host',
                        default=DEFAULT_HOST,
                        help='web server hostname')
    parser.add_argument('--port', default=DEFAULT_PORT, help='web server port')
    parser.add_argument('-d', '--device',
                        type=int_or_str,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-l', '--list-devices',
                        action='store_true',
                        default=False,
                        help='show list of audio devices and exit')
    return parser.parse_args()


def start_server():
    args = parse_args()

    if args.list_devices:
        print('Audio input devices:')
        print(sd.query_devices())
        exit(0)

    audio_wire = AudioWire(socketio, device=args.device)
    audio_wire.start()

    print(f'Serving web server on http://{args.host}:{args.port}/')
    try:
        socketio.run(app, host=args.host, port=args.port, use_reloader=False)
    except KeyboardInterrupt:
        audio_wire.stop()
    finally:
        print('Goodbye.')


if __name__ == '__main__':
    start_server()
