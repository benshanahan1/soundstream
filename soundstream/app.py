from flask import Flask
from flask_socketio import SocketIO
from sounddevice import query_devices
from soundstream.audio.audio_wire import AudioWire
from soundstream.cli import parse_args
from soundstream.logger import init_logger


socketio = SocketIO()


def create_app():
    """ Create Flask app. """
    app = Flask(__name__,
                static_url_path='/static',
                static_folder='web/static',
                template_folder='web/templates')
    from soundstream.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    socketio.init_app(app)
    return app


def run_server(app):
    # Parse command line arguments.
    args = parse_args()
    if args.list_devices:
        print('Audio input devices:')
        print(query_devices())
        exit(0)

    # Initialize logger.
    init_logger(args.verbose)

    # Start AudioWire interface to read from sound input device.
    audio_wire = AudioWire(socketio, device=args.device)
    audio_wire.start()

    # Start Flask server.
    print(f'Server started on http://{args.host}:{args.port}/')
    try:
        socketio.run(app, host=args.host, port=args.port, use_reloader=False)
    except KeyboardInterrupt:
        audio_wire.stop()
    finally:
        print('Goodbye.')
