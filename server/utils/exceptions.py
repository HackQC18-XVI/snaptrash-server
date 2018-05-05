from flask import jsonify


class HTTPError(Exception):

    def __init__(self, status_code, message=None, payload=None):
        super().__init__(self)
        self.message = message
        self.payload = payload
        self.status_code = status_code

    def to_dict(self):
        ret = dict(self.payload or ())
        ret['message'] = self.message
        return ret
