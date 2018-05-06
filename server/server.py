import os
import tempfile

from flask import Flask
from flask import jsonify
from flask import request
from tf import TFNodeLookup

from utils.exceptions import HTTPError

from synset import get_trash_category_payload
from utils.geo_locator import GeoLocator


FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg')

app = Flask(__name__)
geojson_locator = GeoLocator(cities=['montreal'])


def allowed_file(filename):
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


@app.route("/ping")
def ping():
    return "pong"


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')

    if file and allowed_file(file.filename):
        tf_object = TFNodeLookup()
        tf_pred = tf_object.run_inference_on_image(file.read())
    else:
        raise HTTPError(400,
                        f"'file' form data is required of type {SUPPORTED_EXTENSIONS}")

    # obtain the best classification match
    wordnet_id = max(tf_pred, key=lambda x:x['score']).get('wordnet_id')

    payload = get_trash_category_payload(wordnet_id)
    return jsonify(payload)


@app.route('/categories/<wordnet_id>', methods=['GET'])
def get_category(wordnet_id):
    payload = get_trash_category_payload(wordnet_id)
    return jsonify(payload)


@app.route('/drop-info/<drop_type>', methods=['GET'])
def drop_info(drop_type):
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    payload = get_drop_info(drop_type, latitude, longitude)
    return jsonify(payload)


@app.route('/pickup-info/<pickup_type>', methods=['GET'])
def pickup_info(pickup_type):
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    payload = get_pickup_info(pickup_type, latitude, longitude)
    return jsonify(payload)


def get_drop_info(drop_type, latitude, longitude):
    return {}


def get_pickup_info(pickup_type, latitude, longitude):
    geojson_feature = geojson_locator.get_feature('montreal',
                                                  'pickup',
                                                  pickup_type,
                                                  latitude,
                                                  longitude)
    return geojson_feature


# Handler for error class
@app.errorhandler(HTTPError)
def handle_http_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5005)
