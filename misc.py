import numpy as np
from json import dumps, JSONEncoder
from datetime import datetime, date


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
