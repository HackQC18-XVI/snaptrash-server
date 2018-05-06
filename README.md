# SnapTrash Server

:ghost::put_litter_in_its_place: Use image recognition to know where to dispose of anything.

The API is a [Flask](http://flask.pocoo.org) application.

Images are classified by a [TensorFlow](https://www.tensorflow.org/) model trained over the [ImageNet](http://www.image-net.org/) database.

We use [WordNet](https://wordnet.princeton.edu/) to map the recognition labels with trash disposal categories from [Données Québec](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte).

## Technologies
SnapTrash uses modern tools
* [Docker](https://www.docker.com/) #containers
* [Flask](http://flask.pocoo.org) #server app
* [TensorFlow](https://www.tensorflow.org/) #image classification
* [ImageNet](https://wordnet.princeton.edu/) #recognition mapping
* [Données Québec](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte) #datasets

## Setup

```sh
python3 -m venv snaptrash.venv
source snaptrash.venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw')"
```

## Docker Setup
```sh
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Make any requests at:
http://localhost:5005
```

## Run

```sh
source snaptrash.venv/bin/activate
cd server/
FLASK_APP='server.py'
flask run --host=0.0.0.0
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

* Montréal (for pickup)
* Québec
* Sherbrooke

## Usage

#### Image prediction
Get best match in trash categories from a picture

`/predict`:

```sh
HOST='localhost:5000'
FILE='banana.jpeg'
curl -F file=@$FILE $HOST/predict
```

#### Trash Categories
Get best match in trash categories from a WordNet synset ID.

`/categories/{wordnet_id}`:

```sh
HOST='localhost:5000'
SYNSET='banana.n.02'
curl $HOST/categories/$SYNSET
```

#### Trash Pickup Information
Get information regarding waste pickup based on location.
You should be in Montreal to obtain the correct **pickup** information (we use only the Montréal dataset for now) in the form of a **GeoLocation Feature**.

`/pickup-info/<pickup_type>?latitude=<latitude_coordinate>&longitude=<long_coordinate>`:

```sh
HOST='localhost:5000'
curl $HOST/pickup-info/compost?longitude=-73.56229610000003&latitude=45.4946761
```

#### Trash Drop-off Information
When you have dangerous trash, you would probably need to throw it out at a specific dropoff location. This endpoint gets that information for you in the form of a **GeoLocation Feature**.

`/drop-info/dangerux?latitude=46.8921&longitude=-71.195`

```sh
HOST='localhost:5000'
curl $HOST/drop-info/dangerux?latitude=46.8921&longitude=-71.195
```
