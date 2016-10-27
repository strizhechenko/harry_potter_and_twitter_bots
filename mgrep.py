# coding: utf-8
import sys
from re import match, UNICODE
from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()


BLACKLIST_WORDS = [u'какой', u'какая', u'какое', u'какие',
                   u'такой', u'такая', u'такое', u'такие',
                   u'каждый', u'каждая', u'каждые', u'каждое',
                   u'который', u'которая', u'которые', u'которое',
                   u'этот', u'эта', u'это', u'эти',
                   u'весь', u'вся', u'всё', u'всю',
                   u'тот', u'та', u'то', u'те',
                   u'мой', u'моя', u'моё', u'мои',
                   u'твой', u'твоя', u'твоё', u'твои',
                   u'её', u'его', u'их']
BLACKLIST_COMBOS = [
    [u'доброе', u'утро']
]


def choose_suitable_form(parsed, grammem):
    for word in parsed:
        if grammem in word.tag and u'nomn' in word.tag:
            return word.word.capitalize()


def is_blacklisted(words):
    return words in BLACKLIST_COMBOS or any(word in BLACKLIST_WORDS for word in words)


def validate(words):
    if not all(match(u'^[а-я]+$', word, flags=UNICODE) for word in words):
        return
    if is_blacklisted(words):
        return
    if not all(len(word) > 1 for word in words):
        return
    parsed = (
        choose_suitable_form(morpher.parse(words[0]), u'ADJF'),
        choose_suitable_form(morpher.parse(words[1]), u'NOUN'),
    )
    return all(parsed) and parsed


def process_line(line):
    words = line.lower().split()
    combos = [words[i:i + 2] for i in range(len(words) - 1)]
    for i in combos:
        try:
            result = validate(i)
            if result:
                return u" ".join(result)
        except:
            pass

if __name__ == '__main__':
    process_line(unicode(" ".join(sys.argv[1:]), 'utf-8'))
