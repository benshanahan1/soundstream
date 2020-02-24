import logging
from logging import getLogger, StreamHandler, Formatter
from soundstream.config import APP_NAME


logger = getLogger(APP_NAME)


def get_formatter():
    msg_fmt_str = '[%(asctime)s] [%(levelname)s] %(message)s'
    date_fmt_str = '%m-%d-%Y %H:%M:%S'
    return Formatter(fmt=msg_fmt_str, datefmt=date_fmt_str)


def create_stream_handler():
    handler = StreamHandler()
    handler.setFormatter(get_formatter())
    return handler


def init_logger(verbose):
    logger = getLogger(APP_NAME)
    logger.addHandler(create_stream_handler())
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
