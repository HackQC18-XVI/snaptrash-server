# SnapTrash Server

:ghost::put_litter_in_its_place: Use image recognition to know where to dispose of anything.

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
