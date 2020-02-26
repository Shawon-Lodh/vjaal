from collections import OrderedDict
import json
import functools


def fileToJson(file_source, file_destination):
    '''
    example:
    @fileToJson('data/wrong_word.txt', 'data/wrong_word_d.json')
    def file_processor1(*args, **kwargs):
        sl = args[0].strip().split()
        return sl[0], sl[2]
    '''
    def decorator_fileToJson(func):
        @functools.wraps(func)
        def wrapper_fileToJson(*args, **kwargs):
            words = OrderedDict()
            with open(file_source, 'r') as fp:
                for line in fp:
                    k, v = func(line)
                    words[k] = v
            json_d = json.dumps(words, indent=4, ensure_ascii=False)
            with open(file_destination, 'w', encoding='utf8') as fp:
                fp.write(json_d)
        return wrapper_fileToJson
    return decorator_fileToJson


def fileToDict(file_source):
    def decorator_fileToDict(func):
        @functools.wraps(func)
        def wrapper_fileToDict(*args, **kwargs):
            word_dict = {}
            with open(file_source, 'r') as fp:
                for line in fp:
                    k, v = func(line)
                    word_dict[k] = v
            return word_dict
        return wrapper_fileToDict
    return decorator_fileToDict
