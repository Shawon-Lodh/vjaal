import string
import random
import json

from util.file_processor import fileToDict


BD_PUNCTUATION = string.punctuation + '।’॥‘'
EXP_LIST = {'্য': '{jfola}', '্র': '{rfola}'}
BASE_CHAR_SET_LIST = [
        ['শ', 'ষ', 'স'],
        ['ই', 'ঈ'],
        ['ণ', 'ন'],
        ['জ', 'য'],
        ['ড়', 'র'],
        ['ি', 'ী'],
        ['ু', 'ূ'],
        ['ো', '']
    ]


def get_char_set(bcs, word):
    ncs = []
    for cs in bcs:
        for c in cs:
            if c in word:
                ncs.append(cs)
                break
    return ncs


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


def do_corruption(word, char_set):
    exploded_word = list(word)
    locations = [i for i, ch in enumerate(exploded_word) if ch in char_set]
    for index in locations:
        r = char_set[:]
        r.remove(exploded_word[index])
        exploded_word[index] = random.choice(r)
    imploded_word = ''.join(exploded_word)
    return imploded_word if imploded_word != word else None


def synthetic_word_corruption(word, csl):
    wl = [do_corruption(word, char_set) for char_set in csl]
    return [w for w in wl if w is not None]


def corrupt_word(word, csl, ww):
    corrupted_words = []
    corrupted_words.extend(synthetic_word_corruption(word, csl))
    x = ww.get(word, None)
    z = [x] if x else []
    corrupted_words.extend(z)
    # TODO: wiki wrong words list will be added here
    return corrupted_words


def preprocessor(word):
    for k, v in EXP_LIST.items():
        word = word.replace(k, v)
    return word


def postprocessor(words):
    r = []
    for w in words:
        for k, v in EXP_LIST.items():
            w = w.replace(v, k)
        r.append(w)
    return r


def main():
    wd = get_words('data/top_10k_sorted.txt')
    wrong_words = load_wrong_words('data/wrong_word.txt')
    d = {}
    for word in wd:
        char_set_list = get_char_set(BASE_CHAR_SET_LIST, word)
        d[word] = postprocessor(corrupt_word(preprocessor(word), char_set_list, wrong_words))
    j = json.dumps(d, indent=4, ensure_ascii=False)
    print(j)


if __name__ == "__main__":
    main()
