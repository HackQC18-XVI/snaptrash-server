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

## Usage

`/predict` (Get best match in trash categories from a picture):

```sh
HOST='localhost:5000'
FILE='banana.jpeg'
curl -F file=@$FILE $HOST/predict
```

`/categories/{wordnet_id}` (Get best match in trash categories from a WordNet synset ID):

```sh
HOST='localhost:5000'
SYNSET='banana.n.02'
curl $HOST/categories/$SYNSET
```
