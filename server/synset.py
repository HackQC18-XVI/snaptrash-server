import enum
import json
import operator

from nltk.corpus import wordnet

wordnet.ensure_loaded()


with open('server/datasets/trash_categories.json') as trash_categories_file:
    TRASH_CATEGORIES = json.load(trash_categories_file)

SYNSET_CHOICES = [wordnet.synset(cat['synset']) for cat in TRASH_CATEGORIES]


class PartOfSpeech(enum.auto):
    """Codes for the various part-of-speech classes
    """
    NOUN = 'n'


def get_trash_category_payload(synset):
    if isinstance(synset, int):
        synset = get_synset_by_number(synset)
    else:
        synset = get_synset_by_name(synset)
    best_match, _score = get_best_match(synset)

    return [cat for cat in TRASH_CATEGORIES if cat['synset'] == best_match.name()][0]


def get_synset_by_number(number):
    return wordnet.synset_from_pos_and_offset(PartOfSpeech.NOUN, number)


def get_synset_by_name(name):
    return wordnet.synset(name)


def get_best_match(synset):
    return get_similarities(synset)[0]


def get_similarities(target_synset):
    similarities = {synset: target_synset.wup_similarity(synset) for synset in SYNSET_CHOICES}
    sorted_similarities = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_similarities


if __name__ == '__main__':
    import sys
    print(get_trash_category_payload(sys.argv[1]))
