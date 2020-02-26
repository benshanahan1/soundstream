import os
import numpy as np
from json import dumps, JSONEncoder
from datetime import datetime, date


def get_list_of_visualizations(app):
    return os.listdir(os.getcwd() + '/soundstream/web/static/viz')


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


class BetterJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, np.int64):
            return int(obj)
        else:
            try:
                return JSONEncoder.default(self, obj)
            except Exception:
                return str(obj)


def better_dumps(d):
    return dumps(d, cls=BetterJSONEncoder)
