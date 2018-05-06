# SnapTrash Server

:ghost::put_litter_in_its_place: Use image recognition to know where to dispose of anything.

The API is a [Flask](http://flask.pocoo.org) application.

Images are classified by a [TensorFlow](https://www.tensorflow.org/) model trained over the [ImageNet](http://www.image-net.org/) database.

We use [WordNet](https://wordnet.princeton.edu/) to map the recognition labels with trash disposal categories from [Données Québec](https://www.donneesquebec.ca/recherche/fr/dataset/matieres-residuelles-acceptees-par-collecte).

## Setup

```sh
python3 -m venv snaptrash.venv
source snaptrash.venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet')"
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
