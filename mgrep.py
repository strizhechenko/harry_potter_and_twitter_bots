# coding: utf-8
import sys
from re import match, UNICODE
from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()


BLACKLIST_WORDS = [u'какой', u'такой', u'этот', u'тот',
                   u'каждый', u'такие', u'это', u'эта', u'их', u'все']
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
