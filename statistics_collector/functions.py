from nltk import pos_tag, download, word_tokenize

VERB_TAGS = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
NOUN_TAGS = ('NN', 'NNS', 'NNP', 'NNPS')


def flat_list(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_special_function(function):
    return function.startswith('__') and function.endswith('__')


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_')]


def get_verbs(words):
    try:
        classification = pos_tag(word_tokenize(' '.join(words)))
    except LookupError:
        download('averaged_perceptron_tagger')
        download('punkt')
        classification = pos_tag(word_tokenize(' '.join(words)))
    return [tag[0] for tag in classification if tag[1] in VERB_TAGS]


def get_nouns(words):
    try:
        classification = pos_tag(word_tokenize(' '.join(words)))
    except LookupError:
        download('averaged_perceptron_tagger')
        download('punkt')
        classification = pos_tag(word_tokenize(' '.join(words)))
    return [tag[0] for tag in classification if tag[1] in NOUN_TAGS]
