import os
import tempfile

from flask import Flask
from flask import jsonify
from flask import request

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)

app = Flask(__name__)


SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg')


def allowed_file(filename):
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


@app.route("/ping")
def ping():
    return "pong"


@app.route('/photo', methods=['POST'])
def upload():
    file = request.files['file']

    if file and allowed_file(file.filename):
        # get classification from Sultan's classifier

        return results


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5005)
