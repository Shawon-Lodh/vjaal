import string
import random
import pprint
import json
from util.file_processor import fileToDict


bd_punctuation = string.punctuation + '।’॥‘'
char_set_list = [
        ['শ', 'ষ', 'স'],
        ['ই', 'ঈ'],
        ['ণ', 'ন'],
        ['জ', 'য'],
        ['ড়', 'র'],
        ['ি','ী'],
        ['ু','ূ']
    ]


def get_words(filepath):
    @fileToDict(filepath)
    def load_10k(*args, **kwargs):
        sl = args[0].strip().split()
        return sl[0], None
    d = load_10k()
    return d.keys()


def load_wrong_words(filepath):
    @fileToDict(filepath)
    def load_wrong_words(*args, **kwargs):
        sl = args[0].strip().split()
        return sl[0], sl[2]
    return load_wrong_words()


def word_vejal(word, ch_list):
    lword = list(word)
    # find all location of sh
    locations = [i for i, letter in enumerate(lword) if letter in ch_list]
    # pick a randon char fron sh list
    for index in locations:
        rest = ch_list[:]
        rest.remove(lword[index])
        lword[index] = random.choice(rest)
    m = ''.join(lword)
    return m if m != word else None


def synthetic_word_corruption(word):
    vw = []
    for char_list in char_set_list:
        vw.append(word_vejal(word, char_list))
    return [w for w in vw if w != None]


def vejal(word):
    manual_wrong_words = load_wrong_words('data/wrong_word.txt')
    corrupted_words = []
    corrupted_words = corrupted_words + synthetic_word_corruption(word)
    x = manual_wrong_words.get(word, None)
    z = [x] if x else []
    corrupted_words = corrupted_words + z
    # TODO: wiki wrong words list will be added here
    return corrupted_words


def gen_vejal(word_list):
    d = {}
    for word in word_list:
        d[word] = vejal(word)
    return d


def main():
    wd = get_words('data/top_10k_sorted.txt')
    wd = gen_vejal(wd)
    pprint.pprint(wd)

if __name__ == "__main__":
    main()