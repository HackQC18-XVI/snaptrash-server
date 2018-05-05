import os
import tempfile

from flask import Flask
from flask import jsonify
from flask import request
from tf import TFNodeLookup


app = Flask(__name__)

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg')


def allowed_file(filename):
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)

@app.route("/ping")
def ping():
    return "pong"


@app.route('/predict', methods=['POST'])
def upload():
    file = request.files['file']
    results = []

    if file and allowed_file(file.filename):
    	tf_object = TFNodeLookup()
    	pred = tf_object.run_inference_on_image(file.read())
    return jsonify(pred)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5005)
