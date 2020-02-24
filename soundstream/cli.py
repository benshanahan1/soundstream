from argparse import ArgumentParser
from soundstream.utils import int_or_str
from soundstream.config import APP_DESCRIPTION, DEFAULT_HOST, DEFAULT_PORT


def parse_args():
    parser = ArgumentParser(description=APP_DESCRIPTION)
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
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='show verbose debug output')
    return parser.parse_args()
