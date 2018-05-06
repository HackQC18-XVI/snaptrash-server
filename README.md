# SnapTrash Server

:ghost::put_litter_in_its_place: Use image recognition to know where to dispose of anything.

The API is a [Flask](http://flask.pocoo.org) application.

Images are classified by a [TensorFlow](https://www.tensorflow.org/) model trained over the [ImageNet](http://www.image-net.org/) database.

We use [WordNet](https://wordnet.princeton.edu/) to map the recognition labels with trash disposal categories from [Données Québec](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte).

## Technologies
SnapTrash uses modern tools
* [Docker](https://www.docker.com/) # containers
* [Flask](http://flask.pocoo.org) # server app
* [nltk](https://pypi.org/project/nltk/) # natural language processing
* [TensorFlow](https://www.tensorflow.org/) # image classification
* [ImageNet](https://wordnet.princeton.edu/) # recognition mapping
* [Shapely](https://pypi.org/project/Shapely/) # analysis of geometric objects in the cartesian plane
* [GeoPy](https://pypi.org/project/geopy/) # geocoding services
* [NumPy](https://pypi.org/project/numpy/) # array-processing package
* [Données Québec](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte) # datasets

## Setup and Server Serving Options
### Run via Docker
If you don't want to start the server on your localhost directly, you can use our prepared `Dockerfile`, which serves the Flask app at port 5005 (make sure this port is exposed on your VM, etc):

```sh
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Make any requests at:
http://localhost:5005
```

### Run Locally
If you want to install the flask server and the other dependencies and requirements on your local machine, you can do so this way as well:

```sh
python3 -m venv snaptrash.venv
source snaptrash.venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw')"
cd server/
FLASK_APP='server.py'
flask run --host=0.0.0.0 --port=5005
```

## Supported Pickup Types
We use the Laval dataset to categorize the various types of trash that should be classified. The types we classify images into are as follows:

* materiaux
* compost
* recyclage
* ordures
* dangereux

## Supported Cities
We use the datasets from the following cities to help people know where to go to pickup/dropoff their trash:

* Montréal (for pickup information **only**)
* Québec (for dropoff locations **only**)
* Sherbrooke (for dropoff locations **only**)

## Usage

#### Image prediction
Get best match in trash categories from a picture

`/predict`:

```sh
HOST='localhost:5005'
FILE='banana.jpeg'
curl -F file=@$FILE $HOST/predict
```

#### Trash Categories
Get best match in trash categories from a WordNet synset ID.

`/categories/{wordnet_id}`:

```sh
HOST='localhost:5005'
SYNSET='banana.n.02'
curl $HOST/categories/$SYNSET
```

#### Trash Pickup Information
Get information regarding waste pickup based on location.
You should be in Montreal to obtain the correct **pickup** information (we use only the Montréal dataset for now) in the form of a **GeoLocation Feature**.

`/pickup-info/<pickup_type>?latitude=<latitude_coordinate>&longitude=<long_coordinate>`:

```sh
HOST='localhost:5005'
curl $HOST/pickup-info/compost?longitude=-73.56229610000003&latitude=45.4946761
```

#### Trash Drop-off Information
When you have dangerous trash, you would probably need to throw it out at a specific dropoff location. This endpoint gets that information for you in the form of a **GeoLocation Feature**.

`/drop-info/dangerux?latitude=46.8921&longitude=-71.195`

```sh
HOST='localhost:5005'
curl $HOST/drop-info/dangerux?latitude=46.8921&longitude=-71.195
```

## Datasets Used
We used the following datasets from their respective cities:

### City of Montréal
* [Secteurs Info-collectes](https://www.donneesquebec.ca/recherche/fr/dataset/vmtl-info-collectes)
### Québec
* [Lieux Publics](https://www.donneesquebec.ca/recherche/fr/dataset/vque_14)
### Sherbrooke
* [Écocentres](https://www.donneesquebec.ca/recherche/fr/dataset/ecocentres-liste-et-horaires)
### Laval
* [Matières Résiduelles Acceptées Par Collecte](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte)
