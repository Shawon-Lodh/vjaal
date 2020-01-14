import string
import random
import pprint

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
    s = set()
    with open(filepath, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                line = line.translate(line.maketrans('', '', bd_punctuation))
                words = line.split() 
                for word in words:
                    s.add(word)
    return list(s)

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

def vejal(word):
    vw = []
    for char_list in char_set_list:
        vw.append(word_vejal(word, char_list))
    return [w for w in vw if w != None]

def gen_vejal(wordlist):
    d = {}
    for word in wordlist:
        d[word] = vejal(word)
    return d

def main():
    w = get_words('data.txt')
    d = gen_vejal(w)
    pprint.pprint(d)

if __name__ == "__main__":
    main()