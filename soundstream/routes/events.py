from soundstream.app import socketio
from soundstream.logger import logger


@socketio.on('connect')
def connect():
    logger.info('client connected')


@socketio.on('disconnect')
def disconnect():
    logger.info('client disconnected')


@socketio.on('start stream')
def start_stream():
    logger.info('client requested data stream start')
